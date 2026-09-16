/**
 * JMSHOP - Script de la Página Dedicada al Catálogo (catalogo.html)
 * Tema Obsidian Cyberpunk Minimalista & Consumo Dinámico de API REST FastAPI.
 */

document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

    // State Variables
    let activeType = 'all';
    let activeCategory = 'all';
    let activeBrand = 'all';
    let maxPrice = 5000000;
    let searchQuery = '';
    let sortBy = 'featured';

    // DOM Elements
    const grid = document.getElementById('catalog-full-grid');
    const emptyState = document.getElementById('catalog-empty-state');
    const resultCount = document.getElementById('catalog-result-count');
    const searchInput = document.getElementById('catalog-search-input');
    const sortSelect = document.getElementById('catalog-sort-select');
    const priceRangeInput = document.getElementById('price-range');
    const priceRangeLabel = document.getElementById('price-range-label');

    // Sidebar Filter Controls
    const typeRadios = document.querySelectorAll('input[name="filter-type"]');
    const categoryBtns = document.querySelectorAll('.cat-filter-btn');
    const brandBtns = document.querySelectorAll('.brand-filter-btn');
    const resetFiltersBtn = document.getElementById('reset-filters-btn');

    let currentProductsList = [];

    // Inferir marca comercial a partir del título para el filtro por marca
    function detectBrand(title) {
        const t = title.toLowerCase();
        if (t.includes('nvidia') || t.includes('geforce') || t.includes('rtx')) return 'nvidia';
        if (t.includes('intel') || t.includes('i7') || t.includes('i9') || t.includes('i5')) return 'intel';
        if (t.includes('amd') || t.includes('ryzen') || t.includes('radeon')) return 'amd';
        if (t.includes('asus') || t.includes('rog') || t.includes('strix')) return 'asus';
        if (t.includes('corsair')) return 'corsair';
        if (t.includes('logitech')) return 'logitech';
        if (t.includes('samsung')) return 'samsung';
        if (t.includes('kingston')) return 'kingston';
        if (t.includes('lenovo')) return 'lenovo';
        if (t.includes('hyperx')) return 'hyperx';
        if (t.includes('nzxt')) return 'nzxt';
        if (t.includes('keychron')) return 'keychron';
        if (t.includes('microsoft') || t.includes('windows')) return 'microsoft';
        return 'other';
    }

    function formatPrice(value) {
        if (typeof value === 'number') {
            return '$' + value.toLocaleString('es-AR', { maximumFractionDigits: 0 });
        }
        return value;
    }

    // Obtener productos desde la API REST de FastAPI
    async function fetchCatalogFromAPI() {
        try {
            // Traer todos los productos del catálogo (hasta 100)
            const response = await fetch(`${API_BASE_URL}/products?limit=100`);
            if (!response.ok) {
                throw new Error(`HTTP error ${response.status}`);
            }
            const data = await response.json();

            return data.map(item => ({
                id: item.id,
                title: item.title,
                category: item.category,
                type: item.type,
                brand: detectBrand(item.title),
                price: formatPrice(item.price),
                numericPrice: item.price,
                badge: item.badge || (item.type === 'servicio' ? 'Servicio Taller' : 'Producto Hardware'),
                image: item.image,
                shortDesc: item.short_desc,
                fullDesc: item.full_desc,
                specs: item.specs || []
            }));
        } catch (err) {
            console.warn('Backend offline o inaccesible en catalogo.js. Usando fallback.', err);
            return [];
        }
    }

    async function renderCatalog() {
        if (!grid) return;

        if (currentProductsList.length === 0) {
            currentProductsList = await fetchCatalogFromAPI();
        }

        grid.innerHTML = '';

        let filtered = currentProductsList.filter(item => {
            const matchesType = (activeType === 'all') || (item.type === activeType);
            const matchesCategory = (activeCategory === 'all') || (item.category === activeCategory);
            
            // Lógica de coincidencia de marca
            let matchesBrand = (activeBrand === 'all');
            if (activeBrand === 'nvidia' && (item.brand === 'nvidia')) matchesBrand = true;
            if (activeBrand === 'intel' && (item.brand === 'intel')) matchesBrand = true;
            if (activeBrand === 'amd' && (item.brand === 'amd')) matchesBrand = true;
            if (activeBrand === 'asus' && (item.brand === 'asus')) matchesBrand = true;
            if (activeBrand === 'corsair' && (item.brand === 'corsair')) matchesBrand = true;

            const matchesPrice = item.numericPrice <= maxPrice;
            const matchesSearch = item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                                  item.shortDesc.toLowerCase().includes(searchQuery.toLowerCase());

            return matchesType && matchesCategory && matchesBrand && matchesPrice && matchesSearch;
        });

        // Ordenamiento
        if (sortBy === 'price-low') {
            filtered.sort((a, b) => a.numericPrice - b.numericPrice);
        } else if (sortBy === 'price-high') {
            filtered.sort((a, b) => b.numericPrice - a.numericPrice);
        }

        if (resultCount) {
            resultCount.textContent = `${filtered.length} Ítem(s) encontrados`;
        }

        if (filtered.length === 0) {
            if (emptyState) emptyState.classList.remove('hidden');
            return;
        } else {
            if (emptyState) emptyState.classList.add('hidden');
        }

        filtered.forEach(item => {
            const isService = item.type === 'servicio';
            const categoryBadge = isService ? 'bg-pink-500/20 text-pink-400 border-pink-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30';
            const categoryLabel = isService ? 'Servicio Taller' : 'Producto Hardware';

            const card = document.createElement('article');
            card.className = `group bg-slate-900/90 rounded-2xl border border-slate-800 hover:border-rose-500/50 overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 hover:-translate-y-1.5 flex flex-col justify-between animate-fade-in`;

            card.innerHTML = `
                <div>
                    <!-- Imagen de la tarjeta limpia -->
                    <div class="overflow-hidden aspect-video bg-slate-950">
                        <img src="${item.image}" alt="${item.title}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy">
                    </div>

                    <!-- Cuerpo de la tarjeta -->
                    <div class="p-5">
                        <h3 class="text-base font-bold text-slate-100 group-hover:text-rose-400 transition-colors line-clamp-2 mb-2 font-tech-title">
                            ${item.title}
                        </h3>
                        <p class="text-slate-400 text-xs line-clamp-2 mb-4 leading-relaxed">
                            ${item.shortDesc}
                        </p>
                    </div>
                </div>

                <!-- Footer de la tarjeta -->
                <div class="px-5 pb-5 pt-3 border-t border-slate-800/60 flex items-center justify-between mt-auto">
                    <div>
                        <span class="text-[10px] text-slate-500 block">Precio Estimado</span>
                        <span class="text-lg font-black text-rose-500 font-mono">${item.price}</span>
                    </div>

                    <div class="flex gap-2">
                        <button class="view-detail-btn p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-xs transition-all border border-slate-700" data-id="${item.id}" aria-label="Ver detalles">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                        </button>
                        <button class="add-to-cart-btn px-3.5 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs transition-all shadow-md hover:shadow-rose-600/30 flex items-center gap-1.5" data-id="${item.id}">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z"/></svg>
                            Agregar
                        </button>
                    </div>
                </div>
            `;

            grid.appendChild(card);
        });

        // Event listeners de Carrito y Detalles
        grid.querySelectorAll('.add-to-cart-btn').forEach(btn => {
            btn.onclick = (e) => {
                const id = parseInt(e.currentTarget.getAttribute('data-id'));
                const item = currentProductsList.find(c => c.id === id);
                if (item && window.JMSHOP_Cart) {
                    window.JMSHOP_Cart.addItem(item);
                }
            };
        });

        grid.querySelectorAll('.view-detail-btn').forEach(btn => {
            btn.onclick = (e) => {
                const id = parseInt(e.currentTarget.getAttribute('data-id'));
                openModal(id);
            };
        });
    }

    // Modal de Detalle
    const modal = document.getElementById('detail-modal');
    const modalCloseBtn = document.getElementById('modal-close');

    function openModal(id) {
        const item = currentProductsList.find(i => i.id === id);
        if (!item || !modal) return;

        const titleEl = document.getElementById('modal-title');
        const badgeEl = document.getElementById('modal-badge');
        const imgEl = document.getElementById('modal-image');
        const priceEl = document.getElementById('modal-price');
        const descEl = document.getElementById('modal-full-desc');
        const specsList = document.getElementById('modal-specs');

        if (titleEl) titleEl.textContent = item.title;
        if (badgeEl) badgeEl.textContent = item.badge;
        if (imgEl) imgEl.src = item.image;
        if (priceEl) priceEl.textContent = item.price;
        if (descEl) descEl.textContent = item.fullDesc;

        if (specsList) {
            specsList.innerHTML = '';
            (item.specs || []).forEach(spec => {
                const li = document.createElement('li');
                li.className = 'flex items-center gap-2 text-slate-300 text-sm';
                li.innerHTML = `
                    <svg class="w-4 h-4 text-emerald-400 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
                    <span>${spec}</span>
                `;
                specsList.appendChild(li);
            });
        }

        const actionBtn = document.getElementById('modal-action-btn');
        if (actionBtn) {
            actionBtn.onclick = () => {
                closeModal();
                if (window.JMSHOP_Cart) {
                    window.JMSHOP_Cart.addItem(item);
                }
            };
        }

        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    function closeModal() {
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    }

    if (modalCloseBtn) modalCloseBtn.onclick = closeModal;

    // Listeners de los Filtros de la Barra Lateral
    typeRadios.forEach(r => {
        r.addEventListener('change', (e) => {
            activeType = e.target.value;
            renderCatalog();
        });
    });

    categoryBtns.forEach(b => {
        b.addEventListener('click', () => {
            categoryBtns.forEach(btn => {
                btn.classList.remove('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');
                btn.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
            });

            b.classList.remove('bg-slate-900', 'text-slate-400', 'border-slate-800');
            b.classList.add('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');

            activeCategory = b.getAttribute('data-category');
            renderCatalog();
        });
    });

    brandBtns.forEach(b => {
        b.addEventListener('click', () => {
            brandBtns.forEach(btn => btn.classList.remove('border-rose-500', 'text-rose-400'));
            b.classList.add('border-rose-500', 'text-rose-400');
            activeBrand = b.getAttribute('data-brand');
            renderCatalog();
        });
    });

    if (priceRangeInput) {
        priceRangeInput.addEventListener('input', (e) => {
            maxPrice = parseInt(e.target.value);
            if (priceRangeLabel) {
                priceRangeLabel.textContent = '$' + maxPrice.toLocaleString('es-AR');
            }
            renderCatalog();
        });
    }

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            searchQuery = e.target.value.trim();
            renderCatalog();
        });
    }

    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            sortBy = e.target.value;
            renderCatalog();
        });
    }

    if (resetFiltersBtn) {
        resetFiltersBtn.onclick = () => {
            activeType = 'all';
            activeCategory = 'all';
            activeBrand = 'all';
            maxPrice = 5000000;
            searchQuery = '';
            sortBy = 'featured';
            currentProductsList = []; // Forzar re-busqueda si estaba vacio

            if (searchInput) searchInput.value = '';
            if (priceRangeInput) priceRangeInput.value = 5000000;
            if (priceRangeLabel) priceRangeLabel.textContent = '$5.000.000';

            typeRadios.forEach(r => r.checked = (r.value === 'all'));

            categoryBtns.forEach((b, idx) => {
                if (idx === 0) {
                    b.classList.add('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');
                } else {
                    b.classList.remove('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');
                    b.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
                }
            });

            brandBtns.forEach((b, idx) => {
                if (idx === 0) b.classList.add('border-rose-500', 'text-rose-400');
                else b.classList.remove('border-rose-500', 'text-rose-400');
            });

            renderCatalog();
        };
    }

    renderCatalog();
});
