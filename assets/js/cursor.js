/* JMSHOP - Cursor Glow Sutil & Parallax 3D para Hero */
document.addEventListener('DOMContentLoaded', () => {
    // 1. Crear el elemento para el Cursor Glow Sutil
    const cursorGlow = document.createElement('div');
    cursorGlow.id = 'cyber-cursor-glow';
    document.body.appendChild(cursorGlow);

    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let cursorX = mouseX;
    let cursorY = mouseY;

    // Actualización de posición mediante rAF para 60fps sin lag
    document.addEventListener('mousemove', (e) => {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });

    function animateCursor() {
        // Suavizado lerp (0.15)
        cursorX += (mouseX - cursorX) * 0.15;
        cursorY += (mouseY - cursorY) * 0.15;

        cursorGlow.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;
        requestAnimationFrame(animateCursor);
    }
    animateCursor();

    // Reacción al pasar sobre elementos interactivos (Hover Glow Expansion)
    const interactiveSelectors = 'a, button, input, select, textarea, .interactive-card, [role="button"]';
    document.body.addEventListener('mouseover', (e) => {
        if (e.target.closest(interactiveSelectors)) {
            cursorGlow.classList.add('active');
        }
    });
    document.body.addEventListener('mouseout', (e) => {
        if (e.target.closest(interactiveSelectors)) {
            cursorGlow.classList.remove('active');
        }
    });

    // 2. Parallax 3D Interactivo para la Tarjeta de Hardware del Hero
    const heroCard = document.getElementById('hero-hardware-card');
    const heroSection = document.getElementById('hero-section');

    if (heroCard && heroSection) {
        heroSection.addEventListener('mousemove', (e) => {
            const rect = heroSection.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;

            const rotateX = ((e.clientY - centerY) / rect.height) * -12; // Max 12deg
            const rotateY = ((e.clientX - centerX) / rect.width) * 12;

            heroCard.style.transform = `perspective(1000px) rotateX(${rotateX.toFixed(2)}deg) rotateY(${rotateY.toFixed(2)}deg) translateZ(10px)`;
        });

        heroSection.addEventListener('mouseleave', () => {
            heroCard.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)`;
        });
    }
});
