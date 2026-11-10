#!/usr/bin/env python3
"""Field Photo Extractor — pull full-resolution photos out of field-app data.

Sources (auto-detected from the path you pass):
  Notability  .nbn package folder or .note export   -> originals/ + with_annotations/ (your ink redrawn at photo resolution)
  Freeform    --freeform "Board Name" [--freeform-pdf export.pdf]
              -> originals/ (+ JPEG copies of HEIC) + images from attached PDFs
                 + with_annotations/ when given a PDF exported from Freeform (File > Export as PDF)
  FieldMove   .fm project folder, or a CSV export folder containing image.csv
              -> originals/ named by locality/time with GPS written into EXIF, photos.csv index
  Gaia GPS    .geojson / .gpx / .kmz export
              -> photos embedded in KMZ; full-size downloads for photo URLs in GeoJSON; photos.csv index

Usage:  python3 field_photo_extract.py SOURCE [SOURCE ...] -o OUTDIR
        python3 field_photo_extract.py --freeform "Peru Notebook Freeform" -o OUTDIR
Needs: Pillow, numpy; pycairo (Notability ink); pillow-heif (HEIC); pymupdf (Freeform PDF annotations).
Originals are always copied byte-for-byte; nothing in the source is modified.
"""
import argparse, csv, io, json, math, os, plistlib, re, shutil, sqlite3, struct, sys, tempfile, zipfile, urllib.request
from datetime import datetime, timezone

try:
    import pillow_heif; pillow_heif.register_heif_opener(); HEIF = True
except Exception:
    HEIF = False
from PIL import Image, ImageOps

IMG_EXT = {'.jpg', '.jpeg', '.png', '.heic', '.heif', '.tif', '.tiff', '.gif', '.webp'}

def log(*a): print(*a, flush=True)
def safe(s): return re.sub(r'[^\w\-. ]+', '_', str(s)).strip()[:80] or 'untitled'
def ensure(*p): d = os.path.join(*p); os.makedirs(d, exist_ok=True); return d

def heic_to_jpeg(src, dst):
    if not HEIF: return False
    im = Image.open(src); exif = im.info.get('exif')
    im.convert('RGB').save(dst, quality=95, subsampling=0, **({'exif': exif} if exif else {}))
    return True

def write_index(out, rows):
    if not rows: return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(os.path.join(out, 'photos.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, keys); w.writeheader(); w.writerows(rows)

def add_gps(path, lat, lon, alt=None, when=None):
    """Write GPS (and capture time) into a JPEG copy, losslessly when piexif exists, else by re-saving at q100."""
    def rat(x): x = abs(x); d = int(x); m = int((x - d) * 60); s = round(((x - d) * 60 - m) * 60 * 10000)
    def dms(x): x=abs(x); d=int(x); m=int((x-d)*60); s=((x-d)*60-m)*60; return ((d,1),(m,1),(int(round(s*10000)),10000))
    try:
        import piexif
        ex = piexif.load(path)
        ex['GPS'] = {piexif.GPSIFD.GPSLatitudeRef: b'N' if lat >= 0 else b'S', piexif.GPSIFD.GPSLatitude: dms(lat),
                     piexif.GPSIFD.GPSLongitudeRef: b'E' if lon >= 0 else b'W', piexif.GPSIFD.GPSLongitude: dms(lon)}
        if alt is not None:
            ex['GPS'][piexif.GPSIFD.GPSAltitudeRef] = 0 if alt >= 0 else 1
            ex['GPS'][piexif.GPSIFD.GPSAltitude] = (int(abs(alt) * 100), 100)
        if when: ex['Exif'][piexif.ExifIFD.DateTimeOriginal] = when.strftime('%Y:%m:%d %H:%M:%S').encode()
        piexif.insert(piexif.dump(ex), path); return True
    except ImportError:
        return False

# ---------------------------------------------------------------- Notability
def notability(src, out):
    import numpy as np, cairo
    tmp = None
    if os.path.isfile(src) and zipfile.is_zipfile(src):           # .note export
        tmp = tempfile.mkdtemp(); zipfile.ZipFile(src).extractall(tmp)
        roots = [r for r, d, f in os.walk(tmp) if 'Session.plist' in f]; src = roots[0]
    p = plistlib.load(open(os.path.join(src, 'Session.plist'), 'rb')); O = p['$objects']
    R = lambda x: O[x.data] if isinstance(x, plistlib.UID) else x
    def B(x): x = R(x); return x['NS.bytes'] if isinstance(x, dict) else x
    num = lambda s: [float(v) for v in re.findall(r'-?[\d.]+(?:[eE][-+]?\d+)?', s)]
    ovs = [o for o in O if isinstance(o, dict) and 'curvespoints' in o]
    ov = max(ovs, key=lambda o: R(o['numcurves'])) if ovs else None
    if ov is not None and R(ov['numcurves']):
        npts = np.frombuffer(B(ov['curvesnumpoints']), '<i4'); pts = np.frombuffer(B(ov['curvespoints']), '<f4').reshape(-1, 2).astype(float)
        wid = np.frombuffer(B(ov['curveswidth']), '<f4'); col = np.frombuffer(B(ov['curvescolors']), 'u1').reshape(-1, 4)
        fw = np.frombuffer(B(ov['curvesfractionalwidths']), '<f4')
        starts = np.concatenate([[0], np.cumsum(npts)[:-1]]); fst = np.concatenate([[0], np.cumsum((npts - 1) // 3 + 1)[:-1]])
        bb = np.array([[*pts[s:s+n].min(0), *pts[s:s+n].max(0)] for s, n in zip(starts, npts)])
    else:
        npts = []; bb = np.zeros((0, 4))
    od, ad = ensure(out, 'originals'), ensure(out, 'with_annotations')
    for f in sorted(os.listdir(os.path.join(src, 'Images'))):
        shutil.copy2(os.path.join(src, 'Images', f), od)
    rows = []; inked = 0
    for o in O:
        if not (isinstance(o, dict) and 'figure' in o): continue
        fig = R(o['figure']); snap = R(R(fig['FigureBackgroundObjectKey'])['kImageObjectSnapshotKey'])
        rel = R(snap['relativePath']); ox, oy = num(R(o['documentOrigin'])); dw, dh = num(R(o['unscaledContentSize']))
        cx, cy, cw, chh = num(R(fig['FigureCropRectKey'])); a = float(o['rotationDegrees'])
        stem = os.path.splitext(os.path.basename(rel))[0].replace(' ', '_')
        if stem == 'Image_': stem = 'Image_0'
        pil = ImageOps.exif_transpose(Image.open(os.path.join(src, rel))).convert('RGB')
        pil = pil.crop((round(cx), round(cy), round(cx + cw), round(cy + chh)))
        W, H = pil.size; s = W / dw
        ca, sa = abs(math.cos(a)), abs(math.sin(a)); OW, OH = int(round(W*ca + H*sa)), int(round(W*sa + H*ca))
        surf = cairo.ImageSurface(cairo.FORMAT_RGB24, OW, OH); c = cairo.Context(surf)
        cxd, cyd = ox + dw/2, oy + dh/2
        c.translate(OW/2, OH/2); c.save(); c.rotate(a); c.translate(-W/2, -H/2)
        bgra = np.array(pil.convert('RGBA'))[:, :, [2, 1, 0, 3]].copy()
        c.set_source_surface(cairo.ImageSurface.create_for_data(memoryview(bgra), cairo.FORMAT_ARGB32, W, H, W*4), 0, 0)
        c.get_source().set_filter(cairo.FILTER_BEST); c.paint(); c.restore()
        c.save(); c.rotate(a); c.rectangle(-W/2, -H/2, W, H); c.restore(); c.clip()
        c.scale(s, s); c.translate(-cxd, -cyd)
        rr = math.hypot(dw, dh) / 2
        sel = np.where((bb[:, 2] >= cxd-rr) & (bb[:, 0] <= cxd+rr) & (bb[:, 3] >= cyd-rr) & (bb[:, 1] <= cyd+rr))[0]
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
        for i in sel:
            P = pts[starts[i]:starts[i]+npts[i]]; r, g, b, al = col[i] / 255; F = fw[fst[i]:fst[i] + (npts[i]-1)//3 + 1]
            hl = al < 1
            if hl: c.push_group()
            c.set_source_rgba(r, g, b, 1)
            if npts[i] < 4:
                c.arc(P[0, 0], P[0, 1], wid[i]/2, 0, 2*math.pi); c.fill()
            elif hl or np.ptp(F) < 0.05:
                c.set_line_width(wid[i] * (F.mean() if len(F) else 1)); c.move_to(*P[0])
                for j in range(1, len(P)-2, 3): c.curve_to(*P[j], *P[j+1], *P[j+2])
                c.stroke()
            else:
                for j in range(0, len(P)-3, 3):
                    c.set_line_width(wid[i] * (F[j//3] + F[j//3+1]) / 2)
                    c.move_to(*P[j]); c.curve_to(*P[j+1], *P[j+2], *P[j+3]); c.stroke()
            if hl:
                c.pop_group_to_source(); c.set_operator(cairo.OPERATOR_MULTIPLY); c.paint_with_alpha(al); c.set_operator(cairo.OPERATOR_OVER)
        arr = np.ndarray((OH, OW, 4), np.uint8, surf.get_data())[:, :, [2, 1, 0]].copy()
        srcext = os.path.splitext(rel)[1].lower(); outname = stem + ('.png' if srcext == '.png' else '.jpg')
        if srcext == '.png': Image.fromarray(arr).save(os.path.join(ad, outname))
        else: Image.fromarray(arr).save(os.path.join(ad, outname), quality=95, subsampling=0)
        diff = np.abs(np.asarray(Image.fromarray(arr).resize((200, 200)), int) - np.asarray(
            pil.rotate(math.degrees(-a), expand=True).resize((200, 200)), int)).max(2) > 60
        has = bool(diff.mean() > 0.002) if a == 0 else None; inked += bool(has)
        rows.append(dict(file=os.path.basename(rel), annotated=outname, width=OW, height=OH, has_ink=has,
                         doc_x=round(ox, 1), doc_y=round(oy, 1), rotated_deg=round(math.degrees(a))))
    write_index(out, sorted(rows, key=lambda r: r['doc_y']))
    placed = {r['file'] for r in rows}; unused = [f for f in os.listdir(od) if f not in placed]
    log(f'Notability: {len(os.listdir(od))} originals, {len(rows)} annotated renders ({inked} with ink)'
        + (f'; not on any page: {", ".join(unused)}' if unused else ''))
    if tmp: shutil.rmtree(tmp, ignore_errors=True)

# ---------------------------------------------------------------- Freeform
FF_GROUP = os.path.expanduser('~/Library/Group Containers/group.com.apple.freeform/Boards')

def freeform(board, out, boards_dir=None, pdf=None):
    bd = boards_dir or FF_GROUP
    tmpdb = os.path.join(tempfile.mkdtemp(), 'b.db')
    for ext in ('', '-wal', '-shm'):
        if os.path.exists(os.path.join(bd, 'boards.db' + ext)): shutil.copy(os.path.join(bd, 'boards.db' + ext), tmpdb + ext)
    c = sqlite3.connect(tmpdb)
    match = [(bid, d) for bid, d in c.execute('select board_identifier, data from boards where tombstoned=0') if d and board.encode() in d]
    if not match: sys.exit(f'Freeform board "{board}" not found in {bd}')
    exact = [m for m in match if re.search(rb'\x12.' + re.escape(board.encode()) + rb'\x12', m[1])]
    bid = (exact or match)[0][0]
    rows = c.execute("""select r.referrer_asset_name, hex(r.asset_uuid), a.extension from asset_references r
                        left join assets a on a.asset_uuid=r.asset_uuid where r.board_identifier=?""", (bid,)).fetchall()
    od, jd, pd = ensure(out, 'originals'), ensure(out, 'originals_jpeg_from_heic'), ensure(out, 'from_attached_pdfs')
    idx = []; k = 0
    for name, h, e in rows:
        u = f'{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}'; src = os.path.join(bd, 'Assets', f'{u}.{e}' if e else u)
        if not os.path.exists(src): continue
        if name == 'image':
            k += 1; dst = os.path.join(od, f'Freeform_{k:02d}.{e}'); shutil.copy2(src, dst)
            size = Image.open(src).size if (e != 'heic' or HEIF) else ('?', '?')
            if e in ('heic', 'heif'): heic_to_jpeg(src, os.path.join(jd, f'Freeform_{k:02d}.jpg'))
            idx.append(dict(file=os.path.basename(dst), asset=u, width=size[0], height=size[1]))
        elif name == 'file' and e == 'pdf':
            import subprocess
            sub = ensure(pd, u[:8]); shutil.copy2(src, os.path.join(pd, u[:8] + '.pdf'))
            subprocess.run(['pdfimages', '-all', '-p', src, os.path.join(sub, 'img')], check=False)
    write_index(out, idx)
    log(f'Freeform "{board}": {k} photos/images, {len(os.listdir(pd)) // 2} attached PDFs mined')
    if pdf: freeform_pdf_annotated(pdf, out)
    elif k: log('  For versions with your drawing on top: Freeform > File > Export as PDF, then rerun with --freeform-pdf')

def freeform_pdf_annotated(pdf, out):
    """Render each photo's region of a Freeform PDF export at the photo's own native resolution (ink included)."""
    import pymupdf
    ad = ensure(out, 'with_annotations'); doc = pymupdf.open(pdf); n = 0
    for page in doc:
        for info in page.get_image_info(xrefs=True):
            x0, y0, x1, y1 = info['bbox']; w = x1 - x0
            if w < 30 or (y1 - y0) < 30: continue
            zoom = min(info['width'] / w, 12)
            clip = pymupdf.Rect(info['bbox']) & page.rect
            pix = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip, alpha=False)
            n += 1; pix.save(os.path.join(ad, f'Freeform_page{page.number+1}_{n:02d}.jpg'), jpg_quality=95)
    log(f'Freeform PDF: {n} photo regions rendered with ink at native resolution')

# ---------------------------------------------------------------- FieldMove
def _pb(b):
    def vi(i):
        r = s = 0
        while True:
            x = b[i]; i += 1; r |= (x & 0x7f) << s; s += 7
            if x < 0x80: return r, i
    i = 0; o = {}
    while i < len(b):
        k, i = vi(i); f, t = k >> 3, k & 7
        if t == 0: v, i = vi(i)
        elif t == 1: v = struct.unpack('<d', b[i:i+8])[0]; i += 8
        elif t == 5: v = struct.unpack('<f', b[i:i+4])[0]; i += 4
        elif t == 2: n, i = vi(i); v = b[i:i+n]; i += n
        else: raise ValueError
        o.setdefault(f, v)
    return o

def find_photo(name, roots):
    for root in roots:
        for r, d, fs in os.walk(root):
            if name in fs: return os.path.join(r, name)

def fieldmove(src, out, search_roots):
    od = ensure(out, 'originals'); rows = []; missing = []
    if os.path.exists(os.path.join(src, 'main.db')):                     # project folder (.fm)
        tmp = os.path.join(tempfile.mkdtemp(), 'fm.db'); shutil.copy(os.path.join(src, 'main.db'), tmp)
        c = sqlite3.connect(tmp)
        locs = {}
        for lid, m in c.execute('select localityId, message from localities'):
            try: q = _pb(m)
            except Exception: q = {}
            dec = lambda v: v.decode('utf-8', 'ignore').strip() if isinstance(v, bytes) else ''
            locs[lid] = (dec(q.get(3)) or lid[:8], dec(q.get(4)))
        recs = []
        for did, lid, m in c.execute('select dataId, localityId, message from data'):
            try: p = _pb(m)
            except Exception: continue
            name = p.get(21)
            if not isinstance(name, bytes): continue
            g = _pb(p[6]) if isinstance(p.get(6), bytes) else {}
            L = locs.get(lid, (lid[:8], ''))
            recs.append(dict(image=name.decode(), locality=L[0], latitude=g.get(1), longitude=g.get(2),
                             altitude=g.get(3), heading=p.get(8), time=datetime.fromtimestamp(p[12], timezone.utc) if 12 in p else None, notes=L[1]))
        roots = [os.path.join(src, 'images')] + search_roots
    else:                                                                   # CSV export folder
        f = [x for x in os.listdir(src) if re.match(r'image( \d+)?\.csv$', x)]
        if not f: return log(f'FieldMove: no image.csv in {src}')
        recs = []
        for r in csv.DictReader(open(os.path.join(src, f[0]), newline=''), skipinitialspace=True):
            t = None
            try: t = datetime.strptime(r.get('timedate', '').strip(), '%a %b %d %H:%M:%S %Y')
            except Exception: pass
            recs.append(dict(image=r['image name'].strip(), locality=r.get('localityName', '').strip(), latitude=float(r['latitude']),
                             longitude=float(r['longitude']), altitude=float(r['altitude']), heading=float(r['heading']), time=t, notes=r.get('notes', '').strip()))
        roots = [src] + search_roots
    for r in recs:
        p = find_photo(r['image'], roots)
        if not p: missing.append(r['image']); r['saved_as'] = 'MISSING'; rows.append(r); continue
        stamp = r['time'].strftime('%Y%m%d-%H%M%S') if r['time'] else ''
        base = safe(f"{r['locality']}_{stamp}_{os.path.splitext(r['image'])[0]}" + (f"_{r['notes'][:40]}" if r['notes'] else ''))
        dst = os.path.join(od, base + os.path.splitext(p)[1].lower()); shutil.copy2(p, dst)
        if r['latitude'] is not None and dst.endswith(('.jpg', '.jpeg')): r['gps_in_exif'] = add_gps(dst, r['latitude'], r['longitude'], r['altitude'], r['time'])
        r['saved_as'] = os.path.basename(dst); r['pixels'] = 'x'.join(map(str, Image.open(dst).size)); rows.append(r)
    write_index(out, rows)
    log(f'FieldMove {os.path.basename(src)}: {len(rows) - len(missing)} photos saved' + (f', {len(missing)} referenced but not found: {", ".join(missing)}' if missing else ''))

# ---------------------------------------------------------------- Gaia GPS
def gaia(src, out):
    od = ensure(out, 'originals'); rows = []; ext = src.lower().rsplit('.', 1)[-1]
    if ext in ('kmz', 'zip'):
        z = zipfile.ZipFile(src)
        for n in z.namelist():
            if os.path.splitext(n)[1].lower() in IMG_EXT and not n.startswith(('assets/', 'files/icons')):
                data = z.read(n)
                if len(data) < 20000: continue                              # map icons
                dst = os.path.join(od, safe(n.replace('/', '_'))); open(dst, 'wb').write(data)
                rows.append(dict(file=os.path.basename(dst), source=n, pixels='x'.join(map(str, Image.open(dst).size))))
    elif ext in ('geojson', 'json'):
        g = json.load(open(src))
        for f in g.get('features', []):
            pr = f.get('properties', {})
            for k, ph in enumerate(pr.get('photos') or []):
                url = None
                if isinstance(ph, dict):
                    cands = {kk: v for kk, v in ph.items() if isinstance(v, str) and v.startswith('http')}
                    url = next((v for kk, v in cands.items() if re.search('full|orig|large', kk)), next(iter(cands.values()), None))
                elif isinstance(ph, str) and ph.startswith('http'): url = ph
                row = dict(waypoint=pr.get('title'), latitude=pr.get('latitude'), longitude=pr.get('longitude'), url=url)
                if url:
                    dst = os.path.join(od, safe(f"{pr.get('title','wpt')}_{k+1}") + '.jpg')
                    try:
                        urllib.request.urlretrieve(url, dst); row['file'] = os.path.basename(dst)
                        if pr.get('latitude') is not None: add_gps(dst, pr['latitude'], pr['longitude'], pr.get('elevation'))
                    except Exception as e: row['file'] = f'DOWNLOAD FAILED: {e}'
                rows.append(row)
        if not rows: log(f'Gaia {os.path.basename(src)}: {len(g.get("features", []))} features, but no photos attached in this export. '
                         'Export the folder from gaiagps.com as KMZ with photos, or add photos to the waypoints first.')
    elif ext == 'gpx':
        txt = open(src, encoding='utf-8', errors='ignore').read()
        for url in sorted(set(re.findall(r'https?://[^"<\s]+\.(?:jpe?g|png|heic)', txt, re.I))):
            dst = os.path.join(od, safe(url.rsplit('/', 1)[-1]))
            try: urllib.request.urlretrieve(url, dst); rows.append(dict(file=os.path.basename(dst), url=url))
            except Exception as e: rows.append(dict(file=f'DOWNLOAD FAILED: {e}', url=url))
        if not rows: log(f'Gaia {os.path.basename(src)}: GPX has no photo links (GPX never embeds photos).')
    write_index(out, rows)
    if rows: log(f'Gaia {os.path.basename(src)}: {sum(1 for r in rows if str(r.get("file","")).startswith("DOWNLOAD") is False)} photos')

# ---------------------------------------------------------------- dispatch
def detect(path):
    if path.rstrip('/').endswith('.nbn') or os.path.exists(os.path.join(path, 'Session.plist')): return 'notability'
    if path.lower().endswith('.note'): return 'notability'
    if os.path.isdir(path) and (path.rstrip('/').endswith('.fm') or os.path.exists(os.path.join(path, 'main.db'))): return 'fieldmove'
    if os.path.isdir(path) and any(re.match(r'image( \d+)?\.csv$', x) for x in os.listdir(path)): return 'fieldmove'
    if path.lower().endswith(('.geojson', '.gpx', '.kmz')): return 'gaia'
    return None

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('sources', nargs='*'); ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--freeform', help='Freeform board name'); ap.add_argument('--freeform-pdf', help='PDF exported from that board')
    ap.add_argument('--freeform-dir', help='Freeform Boards folder (default: the Mac group container)')
    ap.add_argument('--search', action='append', default=[], help='extra folders to look in for FieldMove photos')
    a = ap.parse_args()
    if a.freeform: freeform(a.freeform, ensure(a.out, safe(a.freeform)), a.freeform_dir, a.freeform_pdf)
    for s in a.sources:
        kind = detect(s)
        if not kind: log(f'Skipped (unrecognised): {s}'); continue
        dest = ensure(a.out, safe(os.path.basename(s.rstrip('/'))))
        {'notability': lambda: notability(s, dest), 'fieldmove': lambda: fieldmove(s, dest, a.search + [os.path.dirname(s.rstrip('/'))]),
         'gaia': lambda: gaia(s, dest)}[kind]()

if __name__ == '__main__':
    main()
