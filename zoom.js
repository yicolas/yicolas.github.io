// ZOOM LOGIC: modifies body font-size
const zoomStep = 1.2; // 20% step
const zoomMin = 6;    // px
const zoomMax = 32;   // px

const body = document.body;

function getFontSize() {
    return parseFloat(window.getComputedStyle(body).fontSize);
}

// Zoom In Button
const zoomInBtn = document.getElementById('zoom-in-btn');
if (zoomInBtn) {
    zoomInBtn.addEventListener('click', function() {
        let currentFontSize = getFontSize();
        let newFontSize = currentFontSize * zoomStep;
        if (newFontSize > zoomMax) newFontSize = zoomMax;
        body.style.fontSize = newFontSize + 'px';
    });
}

// Zoom Out Button
const zoomOutBtn = document.getElementById('zoom-out-btn');
if (zoomOutBtn) {
    zoomOutBtn.addEventListener('click', function() {
        let currentFontSize = getFontSize();
        let newFontSize = currentFontSize / zoomStep;
        if (newFontSize < zoomMin) newFontSize = zoomMin;
        body.style.fontSize = newFontSize + 'px';
    });
}
