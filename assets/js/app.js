/**
 * JMSHOP - Script Principal de la Página de Inicio (index.html)
 * Tema Obsidian Cyberpunk Minimalista
 */

document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // 1. BASE DE DATOS DE OFERTAS FLASH & PROMOS
    // ==========================================
    const flashDeals = [
        {
            id: 101,
            title: "Placa de Video NVIDIA RTX 4070 Super 12GB OC Edition",
            category: "hardware",
            type: "producto",
            price: "$789.990",
            oldPrice: "$920.000",
            discount: "-14% OFF",
            badge: "Oferta Flash",
            image: "https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=600&q=80",
            shortDesc: "Rendimiento extremo 1440p / 4K con Ada Lovelace, DLSS 3.5 y Ray Tracing de 3a Generación.",
            fullDesc: "La NVIDIA GeForce RTX 4070 Super entrega la potencia definitiva para juegos de eSports y títulos AAA en alta velocidad de cuadros por segundo.",
            specs: ["Memoria: 12GB GDDR6X", "Bus: 192-bit", "Recomendado: Fuente 650W+", "Garantía: 24 Meses"]
        },
        {
            id: 102,
            title: "Notebook Gamer ASUS ROG Strix G16 i9 16GB RTX 4060",
            category: "notebooks",
            type: "producto",
            price: "$1.890.000",
            oldPrice: "$2.150.000",
            discount: "-12% OFF",
            badge: "Lanzamiento",
            image: "https://images.unsplash.com/photo-1603302576837-37561b2e2302?auto=format&fit=crop&w=600&q=80",
            shortDesc: "Pantalla ROG Nebula 165Hz QHD+, procesador Intel Core i9 de 13a Gen y almacenamiento SSD NVMe Gen 4.",
            fullDesc: "Laptop de alta gama diseñada para eSports profesionales. Cuenta con teclado RGB por tecla y sistema de enfriamiento metal líquido ROG.",
            specs: ["Pantalla: 16 QHD+ 165Hz", "RAM: 16GB DDR5 4800MHz", "SSD: 1TB NVMe PCIe 4.0", "GPU: RTX 4060 8GB"]
        },
        {
            id: 103,
            title: "Servicio Técnico: Armado Profesional de PC Gamer & Cable Management",
            category: "servicios",
            type: "servicio",
            price: "$35.000",
            oldPrice: "$45.000",
            discount: "-22% OFF",
            badge: "Servicio Top",
            image: "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=600&q=80",
            shortDesc: "Montaje limpio de componentes, gestión oculta de cables, actualización de BIOS y prueba de estrés por 2 horas.",
            fullDesc: "Servicio especializado de ensamble garantizado. Incluye instalación optimizada de sistema operativo y reporte térmico.",
            specs: ["Entrega: 24 a 48 hs", "Prueba de Estrés Incluida", "Actualización de BIOS", "Garantía: 6 Meses"]
        },
        {
            id: 104,
            title: "Licencia Digital Microsoft Windows 11 Pro Vitalicia",
            category: "software",
            type: "producto",
            price: "$24.990",
            oldPrice: "$39.990",
            discount: "-37% OFF",
            badge: "Digital Express",
            image: "https://images.unsplash.com/photo-1629654297299-c8506221ca97?auto=format&fit=crop&w=600&q=80",
            shortDesc: "Clave de activación digital oficial para 1 PC. Activación inmediata vía correo electrónico.",
            fullDesc: "Licencia original Windows 11 Pro Retail vitalicia. Acceso completo a BitLocker, Hyper-V y actualizaciones oficiales.",
            specs: ["Tipo: Clave Retail Vitalicia", "Envío Digital Inmediato", "Arquitectura: 64-bit", "Soporte Microsoft"]
        }
    ];

    // ==========================================
    // 2. TEMPORIZADOR REGRESIVO (FLASH COUNTDOWN)
    // ==========================================
    function initCountdown() {
        let hours = 14;
        let minutes = 32;
        let seconds = 45;

        const timerH = document.getElementById('timer-hours');
        const timerM = document.getElementById('timer-minutes');
        const timerS = document.getElementById('timer-seconds');

        if (!timerH) return;

        setInterval(() => {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
                if (minutes < 0) {
                    minutes = 59;
                    hours--;
                    if (hours < 0) {
                        hours = 23;
                    }
                }
            }

            timerH.textContent = String(hours).padStart(2, '0');
            timerM.textContent = String(minutes).padStart(2, '0');
            timerS.textContent = String(seconds).padStart(2, '0');
        }, 1000);
    }

    initCountdown();

    // ==========================================
    // 3. RENDERIZADO DE OFERTAS FLASH PREVIEW
    // ==========================================
    function renderFlashDeals() {
        const container = document.getElementById('flash-deals-container');
        if (!container) return;

        container.innerHTML = '';

        flashDeals.forEach(deal => {
            const isService = deal.type === 'servicio';
            const categoryBadge = isService ? 'bg-pink-500/20 text-pink-400 border-pink-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30';
            const categoryLabel = isService ? 'Servicio Taller' : 'Producto Hardware';

            const card = document.createElement('article');
            card.className = `group bg-slate-900/90 rounded-2xl border border-slate-800 hover:border-rose-500/50 overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1.5 flex flex-col justify-between animate-fade-in`;

            card.innerHTML = `
                <div>
                    <!-- Imagen limpia -->
                    <div class="overflow-hidden aspect-video bg-slate-950">
                        <img src="${deal.image}" alt="${deal.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy">
                    </div>

                    <!-- Info -->
                    <div class="p-5">
                        <h3 class="text-base font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-2 mb-2 font-tech-title">
                            ${deal.title}
                        </h3>
                        <p class="text-slate-400 text-xs line-clamp-2 mb-4 leading-relaxed">
                            ${deal.shortDesc}
                        </p>
                    </div>
                </div>

                <!-- Footer de tarjeta -->
                <div class="px-5 pb-5 pt-3 border-t border-slate-800/60 flex items-center justify-between mt-auto">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="text-[10px] text-slate-500 line-through block">${deal.oldPrice}</span>
                            <span class="text-[10px] font-black px-1.5 py-0.5 rounded bg-rose-600/20 text-rose-400 border border-rose-500/30">${deal.discount}</span>
                        </div>
                        <span class="text-lg font-black text-rose-500 font-mono">${deal.price}</span>
                    </div>

                    <div class="flex gap-2">
                        <button class="add-to-cart-btn p-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition-all shadow-lg shadow-rose-600/30 active:scale-95 flex items-center justify-center glow-crimson" data-id="${deal.id}" aria-label="Agregar al carrito">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                        </button>
                    </div>
                </div>
            `;

            container.appendChild(card);
        });

        // Attach event listeners for Add to Cart
        container.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.onclick = (e) => {
                const id = parseInt(e.currentTarget.getAttribute('data-id'));
                const deal = flashDeals.find(d => d.id === id);
                if (deal && window.JMSHOP_Cart) {
                    window.JMSHOP_Cart.addItem(deal);
                }
            };
        });
    }

    renderFlashDeals();

    // ==========================================
    // 4. MODO OSCURO / CLARO & MENÚ MÓVIL
    // ==========================================
    const themeToggleBtn = document.getElementById('theme-toggle');
    const themeIconDark = document.getElementById('theme-icon-dark');
    const themeIconLight = document.getElementById('theme-icon-light');

    function initTheme() {
        const savedTheme = localStorage.getItem('jmshop_theme');
        if (savedTheme === 'light') {
            document.documentElement.classList.remove('dark');
            if (themeIconDark) themeIconDark.classList.remove('hidden');
            if (themeIconLight) themeIconLight.classList.add('hidden');
        } else {
            document.documentElement.classList.add('dark');
            if (themeIconDark) themeIconDark.classList.add('hidden');
            if (themeIconLight) themeIconLight.classList.remove('hidden');
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.onclick = () => {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('jmshop_theme', isDark ? 'dark' : 'light');
            if (themeIconDark) themeIconDark.classList.toggle('hidden', isDark);
            if (themeIconLight) themeIconLight.classList.toggle('hidden', !isDark);
        };
    }

    initTheme();

    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.onclick = () => mobileMenu.classList.toggle('hidden');
    }
});
