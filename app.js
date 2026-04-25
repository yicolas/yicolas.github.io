// ==========================================
// Nicolas Anderson - Personal Website
// Main Application JavaScript
// ==========================================

// Page content templates
const pages = {
    home: `
        <div class="content-header">
            <div class="content-title">Welcome</div>
            <div class="content-welcome">
                I am a geologist pursuing a PhD at Caltech, using field observation, paleomagnetism, 
                geochemistry, geochronology and petrology to better understand true polar wander events, 
                meteorite impacts, and sedimentation rates.
            </div>
        </div>
        <div class="blank-state">
            <div class="blank-icon">◇</div>
            <div class="blank-text">Select a page to explore</div>
        </div>
    `,

    cv: `
        <div class="page-header">
            <div>
                <div class="page-title">Curriculum Vitae</div>
                <div class="page-subtitle">Education, experience, and publications</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="cv-section">
            <div class="section-title">Education</div>
            <div class="cv-item">
                <div class="cv-item-title">California Institute of Technology</div>
                <div class="cv-item-meta">PhD Geology · 2023 – 2028 (expected)</div>
            </div>
            <div class="cv-item">
                <div class="cv-item-title">University of California, Berkeley</div>
                <div class="cv-item-meta">BS Earth & Planetary Science · 2020 – 2023 · GPA 3.8</div>
                <div class="cv-item-desc">High Honors, Cum Laude. Honors Thesis: Paleomagnetism & Geochronology of Mesoproterozoic Diabase Sills from Death Valley, California.</div>
            </div>
            <div class="cv-item">
                <div class="cv-item-title">City College of San Francisco</div>
                <div class="cv-item-meta">2016 – 2022</div>
            </div>
        </div>
        
        <div class="cv-section">
            <div class="section-title">Teaching Experience</div>
            <div class="cv-item">
                <div class="cv-item-title">Teaching Assistant — Ge 136: Regional Field Geology</div>
                <div class="cv-item-meta">California Institute of Technology · 2024 – 2025</div>
                <div class="cv-item-desc">Designed and led multi-day camping field trips for Earth Science students across the Southwestern United States.</div>
            </div>
            <div class="cv-item">
                <div class="cv-item-title">Co-instructor — Advanced Field Course</div>
                <div class="cv-item-meta">Nanyang Technical University, Singapore · 2023</div>
                <div class="cv-item-desc">Taught 20 geology students on a 3-week field campaign in eastern California covering structural mapping, glacial geomorphology, and topographic surveying.</div>
            </div>
        </div>
        
        <div class="cv-section">
            <div class="section-title">Work Experience</div>
            <div class="cv-item">
                <div class="cv-item-title">Research Assistant — Earth Surface Dynamics Laboratory</div>
                <div class="cv-item-meta">Caltech (Mike Lamb Lab) · 2023</div>
                <div class="cv-item-desc">Design, fabricate and test clay and sediment flocculating devices for SURF and WAVE undergraduate fellows.</div>
            </div>
            <div class="cv-item">
                <div class="cv-item-title">Exploration Geologist</div>
                <div class="cv-item-meta">Brimstone Energy · 2022 – 2023</div>
                <div class="cv-item-desc">Used geoscientific datasets to identify exploration targets for carbon neutral Portland cement substrates.</div>
            </div>
            <div class="cv-item">
                <div class="cv-item-title">Undergraduate Research Assistant</div>
                <div class="cv-item-meta">Swanson-Hysell Lab, UC Berkeley · 2020 – 2023</div>
                <div class="cv-item-desc">Paleomagnetic sample preparation and measurement on SQUID DC2. Mineral separation, zircon picking and mounting. SEM and XRD analysis.</div>
            </div>
        </div>
        
        <div class="cv-section">
            <div class="section-title">Publications</div>
            <div class="cv-item">
                <div class="cv-item-desc">
                    Zhang, Y., <strong>Anderson, N.S.</strong>, Mohr, M.T., et al. (2024). Paleomagnetic Records From Pulsed Magmatism in the Southwestern Laurentia Large Igneous Province and Cardenas Basalt Support Rapid Late Mesoproterozoic Plate Motion. <em>JGR: Solid Earth</em>. <a href="https://doi.org/10.1029/2024JB029036" target="_blank">doi:10.1029/2024JB029036</a>
                </div>
            </div>
            <div class="cv-item">
                <div class="cv-item-desc">
                    Mohr, M.T., Schmitz, M.D., Swanson-Hysell, N.L., et al. (2024). High-Precision U-Pb geochronology links magmatism in the SW Laurentia Large Igneous Province and Midcontinent Rift. <em>Geology</em>. <a href="https://doi.org/10.1130/G51786.1" target="_blank">doi:10.1130/G51786.1</a>
                </div>
            </div>
        </div>
        
        <div class="cv-section">
            <div class="section-title">Funding & Awards</div>
            <div class="cv-item">
                <div class="cv-item-desc">
                    Ian Campbell Award for Excellence in Field Geology (2025) · 
                    NSF GRFP (2024) · 
                    GSA Shoemaker Impact Cratering Award (2023) · 
                    Caltech GPS Internal Grant (2023) · 
                    Caltech Provost Diversity Fellowship (2021) · 
                    SURF Fellowship (2021) · 
                    Charles H. Ramsden Scholarship (2021)
                </div>
            </div>
        </div>
        
        <div class="cv-tags">
            <span class="cv-tag">Paleomagnetism</span>
            <span class="cv-tag">Geochronology</span>
            <span class="cv-tag">Field geology</span>
            <span class="cv-tag">Geochemistry</span>
            <span class="cv-tag">XRF</span>
            <span class="cv-tag">Python</span>
        </div>
    `,

    thesis: `
        <div class="page-header">
            <div>
                <div class="page-title">GSA 2022 Honors Thesis</div>
                <div class="page-subtitle">Paleomagnetism & Geochronology of Mesoproterozoic Diabase Sills</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="pdf-container">
            <iframe src="SWLLIP-GSA-Anderson-github.pdf"></iframe>
        </div>
    `,

    pyrockmag: `
        <div class="page-header">
            <div>
                <div class="page-title">pyRockmag</div>
                <div class="page-subtitle">Rock magnetic analysis suite</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="iframe-header">
            <div></div>
            <div class="iframe-actions">
                <a href="pyrockmag_6.html" target="_blank" class="res-btn">Open in new tab ↗</a>
            </div>
        </div>
        
        <div class="iframe-container">
            <iframe src="pyrockmag_6.html"></iframe>
        </div>
    `,

    flume: `
        <div class="page-header">
            <div>
                <div class="page-title">Half-channel flume erosion model</div>
                <div class="page-subtitle">Interactive erosion simulation</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="iframe-header">
            <div></div>
            <div class="iframe-actions">
                <a href="flume_model_17.html" target="_blank" class="res-btn">Open in new tab ↗</a>
            </div>
        </div>
        
        <div class="iframe-container">
            <iframe src="flume_model_17.html"></iframe>
        </div>
    `,

    mill: `
        <div class="page-header">
            <div>
                <div class="page-title">Sediment mill</div>
                <div class="page-subtitle">High-resolution particle imaging system</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="two-col-grid">
            <div>
                <div class="featured-img" onclick="openLightbox(0)">
                    <img id="mill-featured" src="IMG_0819.JPG" alt="Sediment mill">
                    <span class="zoom-hint">Click to zoom</span>
                </div>
                <div class="thumb-row">
                    <div class="thumb active" onclick="setMillImage(0)"><img src="IMG_0819.JPG" alt=""></div>
                    <div class="thumb" onclick="setMillImage(1)"><img src="IMG_0822.JPG" alt=""></div>
                    <div class="thumb" onclick="setMillImage(2)"><img src="IMG_0823.JPG" alt=""></div>
                    <div class="thumb" onclick="setMillImage(3)"><img src="IMG_9366.JPG" alt=""></div>
                    <div class="thumb" onclick="setMillImage(4)"><img src="IMG_9553.JPG" alt=""></div>
                    <div class="thumb" onclick="setMillImage(5)"><img src="IMG_9569.JPG" alt=""></div>
                </div>
            </div>
            <div>
                <div class="specs-panel">
                    <div class="specs-title">Specifications</div>
                    <div class="spec-row"><span class="spec-label">Camera</span><span class="spec-value">Nikon D750</span></div>
                    <div class="spec-row"><span class="spec-label">Magnification</span><span class="spec-value">5x – 40x</span></div>
                    <div class="spec-row"><span class="spec-label">Particle range</span><span class="spec-value">10µm – 2mm</span></div>
                    <div class="spec-row"><span class="spec-label">Resolution</span><span class="spec-value">6016 × 4016 px</span></div>
                    <div class="spec-row"><span class="spec-label">Lens design</span><span class="spec-value">Ted Kinsman (RIT)</span></div>
                </div>
                
                <div class="desc-section">
                    <div class="desc-title">About this system</div>
                    <div class="desc-text">
                        Custom-built optical system for imaging fine sediment particles and flocs. 
                        Combines precision optics with standard DSLR photography for high-resolution 
                        particle characterization in the Earth Surface Dynamics Lab at Caltech.
                    </div>
                </div>
                
                <div class="resources">
                    <a href="lens_build.pdf" target="_blank" class="res-btn">Parts list (PDF)</a>
                    <a href="https://youtu.be/ue3mB6ektW8" target="_blank" class="res-btn">Video tutorial ↗</a>
                </div>
            </div>
        </div>
    `,

    press: `
        <div class="page-header">
            <div>
                <div class="page-title">Sediment pellet press</div>
                <div class="page-subtitle">Portable XRF sample preparation</div>
            </div>
            <a class="back-link" data-page="home">← Back</a>
        </div>
        
        <div class="two-col-grid">
            <div>
                <div class="model-viewer-container">
                    <model-viewer 
                        id="press-model"
                        src="caulk_pill_press_v5.stl" 
                        alt="Pellet press 3D model"
                        camera-controls
                        auto-rotate
                        shadow-intensity="1"
                        style="width: 100%; height: 100%; background: transparent;">
                    </model-viewer>
                    <div class="model-hint">Drag to rotate · Scroll to zoom</div>
                </div>
                
                <div class="download-card">
                    <div class="dl-info">
                        <div class="dl-title">Download STL file</div>
                        <div class="dl-meta">caulk_pill_press_v5.stl · 3D printable</div>
                    </div>
                    <a href="caulk_pill_press_v5.stl" download class="dl-btn">Download ↓</a>
                </div>
            </div>
            <div>
                <div class="steps-section">
                    <div class="steps-title">Assembly (5 parts)</div>
                    <div class="step-row active">
                        <div class="step-num">1</div>
                        <div class="step-text"><strong>Base cylinder</strong> — circular relief connects to sediment chamber</div>
                    </div>
                    <div class="step-row">
                        <div class="step-num">2</div>
                        <div class="step-text"><strong>Sediment cylinder</strong> — holds the sample material</div>
                    </div>
                    <div class="step-row">
                        <div class="step-num">3</div>
                        <div class="step-text"><strong>Compression dowel</strong> — presses sediment into pellet</div>
                    </div>
                    <div class="step-row">
                        <div class="step-num">4</div>
                        <div class="step-text"><strong>Dowel topper</strong> — interface for hand or caulk gun</div>
                    </div>
                    <div class="step-row">
                        <div class="step-num">5</div>
                        <div class="step-text"><strong>Caulk gun</strong> — optional, for consistent pressure</div>
                    </div>
                </div>
                
                <div class="specs-mini">
                    <div class="spec-chip">
                        <div class="spec-chip-label">Material</div>
                        <div class="spec-chip-value">PLA / PETG</div>
                    </div>
                    <div class="spec-chip">
                        <div class="spec-chip-label">Print time</div>
                        <div class="spec-chip-value">~3 hours</div>
                    </div>
                    <div class="spec-chip">
                        <div class="spec-chip-label">Pellet size</div>
                        <div class="spec-chip-value">25mm dia.</div>
                    </div>
                    <div class="spec-chip">
                        <div class="spec-chip-label">Weight</div>
                        <div class="spec-chip-value">~45g</div>
                    </div>
                </div>
                
                <div class="desc-section">
                    <div class="desc-title">Overview</div>
                    <div class="desc-text">
                        Portable pellet press for pXRF measurements of fresh clays and fine sands. 
                        Cheap, reproducible, lightweight and durable design that works with a standard 
                        caulk gun or by hand. Extrudes and drains water as pellets are pressed.
                    </div>
                </div>
            </div>
        </div>
    `
};

// Mill images for gallery
const millImages = [
    'IMG_0819.JPG',
    'IMG_0822.JPG', 
    'IMG_0823.JPG',
    'IMG_9366.JPG',
    'IMG_9553.JPG',
    'IMG_9569.JPG',
    'IMG_9584.JPG',
    'IMG_9600.JPG',
    'IMG_9816.JPG'
];

let currentImageIndex = 0;

// Load page content
function loadPage(pageName) {
    const contentPanel = document.getElementById('content-panel');
    contentPanel.innerHTML = pages[pageName] || pages.home;
    
    // Update active nav link
    document.querySelectorAll('.nav-link[data-page]').forEach(link => {
        link.classList.remove('active');
        if (link.dataset.page === pageName) {
            link.classList.add('active');
        }
    });
    
    // Scroll to top
    contentPanel.scrollTop = 0;
    
    // Update URL hash
    window.location.hash = pageName === 'home' ? '' : pageName;
    
    // Re-bind back links
    document.querySelectorAll('.back-link[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            loadPage(link.dataset.page);
        });
    });
}

// Mill image gallery
function setMillImage(index) {
    currentImageIndex = index;
    const featured = document.getElementById('mill-featured');
    if (featured) {
        featured.src = millImages[index];
    }
    
    // Update active thumb
    document.querySelectorAll('.thumb').forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
}

// Lightbox
function openLightbox(index) {
    currentImageIndex = index;
    const lightbox = document.getElementById('lightbox');
    const img = document.getElementById('lightbox-img');
    img.src = millImages[index];
    lightbox.classList.add('active');
}

function closeLightbox() {
    document.getElementById('lightbox').classList.remove('active');
}

function nextImage() {
    currentImageIndex = (currentImageIndex + 1) % millImages.length;
    document.getElementById('lightbox-img').src = millImages[currentImageIndex];
}

function prevImage() {
    currentImageIndex = (currentImageIndex - 1 + millImages.length) % millImages.length;
    document.getElementById('lightbox-img').src = millImages[currentImageIndex];
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set up nav links
    document.querySelectorAll('.nav-link[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            loadPage(link.dataset.page);
        });
    });
    
    // Load initial page from hash or default to home
    const hash = window.location.hash.slice(1);
    loadPage(hash || 'home');
    
    // Handle hash changes
    window.addEventListener('hashchange', () => {
        const hash = window.location.hash.slice(1);
        loadPage(hash || 'home');
    });
    
    // Lightbox keyboard navigation
    document.addEventListener('keydown', (e) => {
        const lightbox = document.getElementById('lightbox');
        if (lightbox.classList.contains('active')) {
            if (e.key === 'Escape') closeLightbox();
            if (e.key === 'ArrowRight') nextImage();
            if (e.key === 'ArrowLeft') prevImage();
        }
    });
    
    // Close lightbox on background click
    document.getElementById('lightbox').addEventListener('click', (e) => {
        if (e.target.id === 'lightbox') closeLightbox();
    });
});
