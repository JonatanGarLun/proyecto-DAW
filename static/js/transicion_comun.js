document.addEventListener("DOMContentLoaded", () => {
    const overlay = document.getElementById("fade-overlay");
    if (!overlay) return;

    overlay.style.opacity = '1';
    overlay.style.pointerEvents = 'auto';
    setTimeout(() => {
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.pointerEvents = 'none';
        }, 400);
    }, 50);

    const enlaces = document.querySelectorAll("a[href]");
    enlaces.forEach(link => {
        link.addEventListener("click", (e) => {
            const href = link.getAttribute("href");
            if (!href || href === "#") return;

            e.preventDefault();
            overlay.style.opacity = '1';
            overlay.style.pointerEvents = 'auto';
            setTimeout(() => {
                window.location.href = href;
            }, 500);
        });
    });
});

window.addEventListener("pageshow", () => {
    const overlay = document.getElementById("fade-overlay");
    if (!overlay) return;
    overlay.style.opacity = '1';
    overlay.style.pointerEvents = 'auto';
    setTimeout(() => {
        overlay.style.opacity = '0';
        setTimeout(() => {
            overlay.style.pointerEvents = 'none';
        }, 400);
    }, 50);
});