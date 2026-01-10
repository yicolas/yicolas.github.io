// Digital Clock Functionality
function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    // Update desktop clock
    const desktopClock = document.getElementById('desktop-clock');
    if (desktopClock) {
        desktopClock.textContent = timeString;
    }
    
    // Update mobile clock
    const mobileClock = document.getElementById('mobile-clock');
    if (mobileClock) {
        mobileClock.textContent = timeString;
    }
}

// Update clock immediately and then every second
updateClock();
setInterval(updateClock, 1000);
