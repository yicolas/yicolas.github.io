# Nicolas Anderson - Personal Website

A modern, responsive geology portfolio website featuring a side-panel layout with project showcase.

## 📁 Files Included

### HTML Pages
- `index.html` - Home page with project listings
- `cv.html` - Full curriculum vitae
- `thesis.html` - GSA 2022 Honors Thesis
- `sediment-mill.html` - Sediment Mill project
- `sediment-press.html` - Sediment Pellet Press project
- `stuff.html` - Geologic Maps & Field Work

### CSS
- `style.css` - Complete styling for all pages

### JavaScript
- `clock.js` - Digital clock functionality
- `zoom.js` - Zoom in/out functionality

## 🎨 Design Features

### Layout
- **Desktop**: Side panel (right) with profile/bio, main content area (left) with projects
- **Mobile**: Responsive stack layout with mobile header/footer
- **Modern Grid System**: CSS Grid for flexible, responsive layouts

### Key Features
1. **Fixed Right Panel** (desktop) - Profile, contact info, and bio
2. **Project Grid** - Clean project cards with images and descriptions
3. **Digital Clock** - Live updating 24-hour clock
4. **Zoom Controls** - Adjustable font size for accessibility
5. **Responsive Design** - Works on desktop, tablet, and mobile

## 📝 Setup Instructions

### 1. Upload to GitHub

Upload all files to your GitHub repository. Your file structure should look like:

```
your-repo/
├── index.html
├── cv.html
├── thesis.html
├── sediment-mill.html
├── sediment-press.html
├── stuff.html
├── style.css
├── clock.js
├── zoom.js
├── geo_compass.png
├── pill_press.png
├── caulk_gun.png
├── IMG_0819.JPG
├── IMG_0822.JPG
├── IMG_0823.JPG
├── IMG_9366.JPG
├── IMG_9553.JPG
├── IMG_9569.JPG
├── IMG_9584.JPG
├── IMG_9600.JPG
├── IMG_9816.JPG
├── kim_floc_outline_labels.svg
├── SWLLIP-GSA-Anderson-github.pdf
├── maps.pdf
├── lens_build.pdf
└── caulk_pill_press_v5.stl
```

### 2. Enable GitHub Pages

1. Go to your repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select your main/master branch
4. Click "Save"
5. Your site will be published at: `https://yourusername.github.io/repository-name/`

### 3. Required Assets

Make sure these image/file assets are in your repository:

**Images:**
- `geo_compass.png` - Your geological compass image (for home page)
- `pill_press.png` - Sediment press image
- `caulk_gun.png` - Caulk gun assembly image
- `IMG_0819.JPG` through `IMG_9816.JPG` - Sediment mill photos
- `kim_floc_outline_labels.svg` - Floc outline diagram
- `map_preview.png` - (Optional) Preview image for maps page

**PDFs:**
- `SWLLIP-GSA-Anderson-github.pdf` - Your thesis PDF
- `maps.pdf` - Your geologic maps PDF
- `lens_build.pdf` - Parts list and assembly guide

**Downloads:**
- `caulk_pill_press_v5.stl` - 3D printable file

## 🎯 Customization

### Changing Colors
The design uses a clean black and white aesthetic. To customize colors, edit `style.css`:

```css
/* Main text color */
color: #222;

/* Muted text */
color: rgba(0, 0, 0, 0.4);

/* Borders */
border-color: rgba(0, 0, 0, 0.15);
```

### Adjusting Layout Widths
The right panel width can be adjusted in `style.css`:

```css
.right-panel {
    width: 30%;  /* Change this percentage */
    max-width: 400px;  /* Change max width */
}
```

### Adding/Removing Projects
Edit the `<article class="project-item">` sections in `index.html`:

```html
<article class="project-item">
    <div class="project-image">
        <a href="your-project.html">
            <img src="your-image.png" alt="Your Project">
        </a>
    </div>
    <div class="project-info">
        <h3>005—YOUR PROJECT NAME</h3>
        <div class="project-subtitle">PROJECT TYPE</div>
        <p class="project-description">
            Your project description here...
        </p>
        <a href="your-project.html" class="read-more">Read more…</a>
    </div>
    <div class="project-icon">
        ⌘
    </div>
</article>
```

## 📱 Responsive Breakpoints

- **Desktop**: > 1024px (side panel visible)
- **Tablet**: 768px - 1024px (mobile layout)
- **Mobile**: < 768px (full mobile layout)

## 🔧 Browser Compatibility

Tested and working in:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📄 Content Notes

All content has been migrated from your original website including:
- Full CV with all experience, publications, awards
- Project descriptions and details
- Contact information
- External links (GitHub, Google Scholar)

## 🐛 Troubleshooting

### Images not showing?
- Check file names match exactly (case-sensitive on Linux/Mac)
- Verify images are in the same directory as HTML files
- Check browser console for 404 errors

### PDFs not loading?
- Ensure PDF files are uploaded to repository
- Some browsers block PDFs in iframes - test in multiple browsers
- PDF file names are case-sensitive

### Layout issues on mobile?
- Clear browser cache
- Check that viewport meta tag is present in HTML
- Test responsive design using browser dev tools

## 📞 Support

For issues or questions, you can:
1. Check browser console for errors
2. Verify all files are uploaded correctly
3. Test in different browsers

## ✨ Credits

Design inspired by modern portfolio layouts with a focus on clean typography and readability. Built with standard HTML5, CSS3, and vanilla JavaScript for maximum compatibility and performance.
