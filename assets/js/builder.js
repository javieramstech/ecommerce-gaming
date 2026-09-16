/**
 * JMSHOP - Script de la Herramienta 'Arma tu PC' (builder.html)
 * Validador de compatibilidad, calculador de Watts y precio total en vivo.
 */

document.addEventListener('DOMContentLoaded', () => {
    // ==========================================
    // 1. BASE DE DATOS DE COMPONENTES DEL BUILDER
    // ==========================================
    let builderData = {
        cpus: [
            { id: 'cpu-1', title: 'Intel Core i5-13400F (10 Cores / Socket LGA1700)', platform: 'intel', socket: 'LGA1700', price: 245000, watts: 65, image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=400&q=80' },
            { id: 'cpu-2', title: 'Intel Core i7-14700K (20 Cores / Socket LGA1700)', platform: 'intel', socket: 'LGA1700', price: 519000, watts: 125, image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=400&q=80' },
            { id: 'cpu-3', title: 'AMD Ryzen 5 7600 (6 Cores / Socket AM5)', platform: 'amd', socket: 'AM5', price: 289000, watts: 65, image: 'https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=400&q=80' },
            { id: 'cpu-4', title: 'AMD Ryzen 7 7800X3D (8 Cores 3D V-Cache / Socket AM5)', platform: 'amd', socket: 'AM5', price: 649000, watts: 120, image: 'https://images.unsplash.com/photo-1555680202-c86f0e12f086?auto=format&fit=crop&w=400&q=80' }
        ],
        mbs: [
            { id: 'mb-1', title: 'Motherboard ASUS Prime B760M-A (Intel Socket LGA1700 / DDR5)', platform: 'intel', socket: 'LGA1700', ramType: 'DDR5', price: 185000, watts: 25, image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80' },
            { id: 'mb-2', title: 'Motherboard ROG Strix Z790-F Gaming (Intel Socket LGA1700 / DDR5)', platform: 'intel', socket: 'LGA1700', ramType: 'DDR5', price: 420000, watts: 35, image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80' },
            { id: 'mb-3', title: 'Motherboard ASUS TUF Gaming B650-PLUS (AMD Socket AM5 / DDR5)', platform: 'amd', socket: 'AM5', ramType: 'DDR5', price: 235000, watts: 25, image: 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=400&q=80' }
        ],
        rams: [
            { id: 'ram-1', title: 'Memoria RAM Corsair Vengeance 16GB (1x16GB) DDR5 5600MHz', ramType: 'DDR5', price: 89000, watts: 5, image: 'https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=400&q=80' },
            { id: 'ram-2', title: 'Memoria RAM Corsair Vengeance RGB 32GB (2x16GB) DDR5 6000MHz', ramType: 'DDR5', price: 185000, watts: 10, image: 'https://images.unsplash.com/photo-1562976540-1502c2145186?auto=format&fit=crop&w=400&q=80' }
        ],
        gpus: [
            { id: 'gpu-1', title: 'NVIDIA GeForce RTX 4060 8GB GDDR6', price: 459000, watts: 115, image: 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=400&q=80' },
            { id: 'gpu-2', title: 'NVIDIA GeForce RTX 4070 Super 12GB GDDR6X', price: 789990, watts: 220, image: 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=400&q=80' },
            { id: 'gpu-3', title: 'AMD Radeon RX 7800 XT 16GB GDDR6', price: 699000, watts: 263, image: 'https://images.unsplash.com/photo-1587202372775-e229f172b9d7?auto=format&fit=crop&w=400&q=80' }
        ],
        ssds: [
            { id: 'ssd-1', title: 'SSD Kingston NV2 1TB NVMe M.2 PCIe 4.0 (3500MB/s)', price: 79000, watts: 5, image: 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=400&q=80' },
            { id: 'ssd-2', title: 'SSD Samsung 990 PRO 2TB NVMe M.2 PCIe 4.0 (7450MB/s)', price: 219000, watts: 8, image: 'https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?auto=format&fit=crop&w=400&q=80' }
        ],
        psus: [
            { id: 'psu-1', title: 'Fuente Corsair CV650 650W 80 Plus Bronze', capacity: 650, price: 95000, watts: 0, image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=400&q=80' },
            { id: 'psu-2', title: 'Fuente Corsair RM850x 850W 80 Plus Gold Full Modular', capacity: 850, price: 189000, watts: 0, image: 'https://images.unsplash.com/photo-1591799264318-7e6ef8ddb7ea?auto=format&fit=crop&w=400&q=80' }
        ],
        cases: [
            { id: 'case-1', title: 'Gabinete Corsair 4000D Airflow Tempered Glass', price: 119000, watts: 0, image: 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=400&q=80' },
            { id: 'case-2', title: 'Gabinete ASUS TUF Gaming GT501 RGB', price: 195000, watts: 0, image: 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=400&q=80' }
        ]
    };

    async function loadBuilderDataFromAPI() {
        try {
            const host = window.location.hostname;
            const apiUrl = (host === 'localhost' || host === '127.0.0.1' || window.location.protocol === 'file:')
                ? 'http://127.0.0.1:8000/api/v1/products?limit=100'
                : (window.location.origin.includes('vercel.app') ? '/api/v1/products?limit=100' : 'https://backend-zolab1.vercel.app/api/v1/products?limit=100');
            const res = await fetch(apiUrl);
            if (!res.ok) return;
            const items = await res.json();
            if (!Array.isArray(items) || items.length === 0) return;

            const cpus = [], mbs = [], rams = [], gpus = [], ssds = [], psus = [], cases = [];

            items.forEach(item => {
                const title = item.title;
                const tLower = title.toLowerCase();
                const specs = item.specs || [];
                const specsStr = (Array.isArray(specs) ? specs.join(' ') : String(specs)).toLowerCase();

                const isAmd = tLower.includes('amd') || tLower.includes('ryzen') || tLower.includes('radeon');
                const isAM5 = specsStr.includes('am5') || tLower.includes('am5');
                const isLGA1700 = specsStr.includes('lga1700') || tLower.includes('lga1700');

                if (tLower.includes('procesador')) {
                    cpus.push({
                        id: `cpu-api-${item.id}`,
                        title: title,
                        platform: isAmd ? 'amd' : 'intel',
                        socket: isAM5 ? 'AM5' : (isLGA1700 ? 'LGA1700' : (isAmd ? 'AM5' : 'LGA1700')),
                        price: item.price,
                        watts: tLower.includes('i9') || tLower.includes('7800x3d') ? 120 : (tLower.includes('i7') ? 125 : 65),
                        image: item.image
                    });
                } else if (tLower.includes('motherboard') || tLower.includes('placa madre')) {
                    mbs.push({
                        id: `mb-api-${item.id}`,
                        title: title,
                        platform: isAmd ? 'amd' : 'intel',
                        socket: isAM5 ? 'AM5' : (isLGA1700 ? 'LGA1700' : (isAmd ? 'AM5' : 'LGA1700')),
                        ramType: specsStr.includes('ddr4') ? 'DDR4' : 'DDR5',
                        price: item.price,
                        watts: 25,
                        image: item.image
                    });
                } else if (tLower.includes('memoria ram')) {
                    rams.push({
                        id: `ram-api-${item.id}`,
                        title: title,
                        ramType: specsStr.includes('ddr4') ? 'DDR4' : 'DDR5',
                        price: item.price,
                        watts: specsStr.includes('32gb') ? 10 : 5,
                        image: item.image
                    });
                } else if (tLower.includes('placa de video')) {
                    let watts = 200;
                    if (tLower.includes('4080')) watts = 320;
                    if (tLower.includes('4070')) watts = 220;
                    if (tLower.includes('7900')) watts = 300;
                    gpus.push({
                        id: `gpu-api-${item.id}`,
                        title: title,
                        price: item.price,
                        watts: watts,
                        image: item.image
                    });
                } else if (tLower.includes('ssd') || tLower.includes('nvme')) {
                    ssds.push({
                        id: `ssd-api-${item.id}`,
                        title: title,
                        price: item.price,
                        watts: 6,
                        image: item.image
                    });
                } else if (tLower.includes('fuente')) {
                    let cap = 750;
                    if (tLower.includes('1000w') || tLower.includes('1000')) cap = 1000;
                    if (tLower.includes('850w')) cap = 850;
                    if (tLower.includes('650w')) cap = 650;
                    psus.push({
                        id: `psu-api-${item.id}`,
                        title: title,
                        capacity: cap,
                        price: item.price,
                        watts: 0,
                        image: item.image
                    });
                } else if (tLower.includes('gabinete')) {
                    cases.push({
                        id: `case-api-${item.id}`,
                        title: title,
                        price: item.price,
                        watts: 0,
                        image: item.image
                    });
                }
            });

            if (cpus.length > 0) builderData.cpus = cpus;
            if (mbs.length > 0) builderData.mbs = mbs;
            if (rams.length > 0) builderData.rams = rams;
            if (gpus.length > 0) builderData.gpus = gpus;
            if (ssds.length > 0) builderData.ssds = ssds;
            if (psus.length > 0) builderData.psus = psus;
            if (cases.length > 0) builderData.cases = cases;
        } catch (err) {
            console.warn('API no disponible para el Builder. Usando fallback estático.', err);
        }
    }

    // State
    const buildState = {
        platform: 'all', // 'intel', 'amd', 'all'
        selectedCPU: null,
        selectedMB: null,
        selectedRAM: null,
        selectedGPU: null,
        selectedSSD: null,
        selectedPSU: null,
        selectedCase: null,
        includeAssembly: true
    };

    const assemblyPrice = 35000;

    // DOM Elements
    const stepCPU = document.getElementById('step-cpu-list');
    const stepMB = document.getElementById('step-mb-list');
    const stepRAM = document.getElementById('step-ram-list');
    const stepGPU = document.getElementById('step-gpu-list');
    const stepSSD = document.getElementById('step-ssd-list');
    const stepPSU = document.getElementById('step-psu-list');
    const stepCase = document.getElementById('step-case-list');
    const checkAssembly = document.getElementById('check-assembly-service');

    // Summary Elements
    const summaryList = document.getElementById('builder-summary-list');
    const totalWattsEl = document.getElementById('builder-total-watts');
    const psuCapacityEl = document.getElementById('builder-psu-capacity');
    const totalPriceEl = document.getElementById('builder-total-price');
    const btnAddToCart = document.getElementById('btn-add-builder-to-cart');
    const btnWhatsApp = document.getElementById('btn-builder-whatsapp');

    function formatMoney(num) {
        return '$' + num.toLocaleString('es-AR');
    }

    function renderComponentStep(container, list, selectedObj, onSelectKey) {
        if (!container) return;
        container.innerHTML = '';

        list.forEach(item => {
            const isSelected = selectedObj && selectedObj.id === item.id;
            const borderClass = isSelected ? 'border-rose-500 bg-rose-500/10' : 'border-slate-800 bg-slate-900/80 hover:border-slate-700';

            const card = document.createElement('div');
            card.className = `p-4 rounded-2xl border ${borderClass} cursor-pointer transition-all flex items-center justify-between gap-4`;
            card.innerHTML = `
                <div class="flex items-center gap-3 min-w-0">
                    <img src="${item.image}" alt="${item.title}" class="w-12 h-12 rounded-xl object-cover shrink-0 bg-slate-950" />
                    <div class="min-w-0">
                        <h4 class="text-xs font-bold text-white truncate">${item.title}</h4>
                        <span class="text-xs text-slate-400 font-medium">${item.watts > 0 ? item.watts + 'W Consumo' : ''}</span>
                    </div>
                </div>
                <div class="text-right shrink-0">
                    <span class="text-sm font-black text-rose-500 font-mono block">${formatMoney(item.price)}</span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${isSelected ? 'bg-rose-600 text-white' : 'bg-slate-800 text-slate-400'}">
                        ${isSelected ? 'Seleccionado' : 'Elegir'}
                    </span>
                </div>
            `;

            card.onclick = () => {
                if (isSelected) {
                    buildState[onSelectKey] = null;
                } else {
                    buildState[onSelectKey] = item;
                    // If CPU changed, check MB compatibility
                    if (onSelectKey === 'selectedCPU') {
                        if (buildState.selectedMB && buildState.selectedMB.socket !== item.socket) {
                            buildState.selectedMB = null;
                        }
                    }
                }
                updateAll();
            };

            container.appendChild(card);
        });
    }

    function updateAll() {
        // Filter CPUs by platform
        const filteredCPUs = builderData.cpus.filter(c => buildState.platform === 'all' || c.platform === buildState.platform);
        renderComponentStep(stepCPU, filteredCPUs, buildState.selectedCPU, 'selectedCPU');

        // Filter MBs by Socket of CPU if selected
        const filteredMBs = builderData.mbs.filter(m => {
            const matchesPlatform = buildState.platform === 'all' || m.platform === buildState.platform;
            const matchesSocket = !buildState.selectedCPU || m.socket === buildState.selectedCPU.socket;
            return matchesPlatform && matchesSocket;
        });
        renderComponentStep(stepMB, filteredMBs, buildState.selectedMB, 'selectedMB');

        renderComponentStep(stepRAM, builderData.rams, buildState.selectedRAM, 'selectedRAM');
        renderComponentStep(stepGPU, builderData.gpus, buildState.selectedGPU, 'selectedGPU');
        renderComponentStep(stepSSD, builderData.ssds, buildState.selectedSSD, 'selectedSSD');
        renderComponentStep(stepPSU, builderData.psus, buildState.selectedPSU, 'selectedPSU');
        renderComponentStep(stepCase, builderData.cases, buildState.selectedCase, 'selectedCase');

        renderSummary();
    }

    function renderSummary() {
        if (!summaryList) return;
        summaryList.innerHTML = '';

        const selectedItems = [
            { label: 'Procesador', item: buildState.selectedCPU },
            { label: 'Motherboard', item: buildState.selectedMB },
            { label: 'Memoria RAM', item: buildState.selectedRAM },
            { label: 'Placa de Video', item: buildState.selectedGPU },
            { label: 'Almacenamiento', item: buildState.selectedSSD },
            { label: 'Fuente', item: buildState.selectedPSU },
            { label: 'Gabinete', item: buildState.selectedCase },
        ];

        let totalPrice = 0;
        let totalWatts = 0;

        selectedItems.forEach(entry => {
            if (entry.item) {
                totalPrice += entry.item.price;
                totalWatts += entry.item.watts || 0;

                const div = document.createElement('div');
                div.className = 'flex justify-between items-center text-xs text-slate-300 py-1.5 border-b border-slate-800/60';
                div.innerHTML = `
                    <span class="truncate max-w-[190px]"><strong class="text-slate-400">${entry.label}:</strong> ${entry.item.title}</span>
                    <span class="font-bold text-rose-500 font-mono">${formatMoney(entry.item.price)}</span>
                `;
                summaryList.appendChild(div);
            }
        });

        if (checkAssembly && checkAssembly.checked) {
            totalPrice += assemblyPrice;
            const div = document.createElement('div');
            div.className = 'flex justify-between items-center text-xs text-slate-300 py-1.5 border-b border-slate-800/60';
            div.innerHTML = `
                <span><strong class="text-slate-400">Servicio:</strong> Armado & Testeo 2h</span>
                <span class="font-bold text-pink-400 font-mono">${formatMoney(assemblyPrice)}</span>
            `;
            summaryList.appendChild(div);
        }

        if (totalWattsEl) totalWattsEl.textContent = totalWatts + 'W';
        
        const psuCap = buildState.selectedPSU ? buildState.selectedPSU.capacity : 0;
        if (psuCapacityEl) psuCapacityEl.textContent = psuCap > 0 ? psuCap + 'W' : 'No elegida';

        if (totalPriceEl) totalPriceEl.textContent = formatMoney(totalPrice);
    }

    // Platform Selector (Intel / AMD / Todos)
    document.querySelectorAll('.platform-btn').forEach(b => {
        b.onclick = () => {
            document.querySelectorAll('.platform-btn').forEach(btn => {
                btn.classList.remove('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');
                btn.classList.add('bg-slate-900', 'text-slate-400', 'border-slate-800');
            });
            b.classList.remove('bg-slate-900', 'text-slate-400', 'border-slate-800');
            b.classList.add('bg-rose-500/20', 'text-rose-400', 'border-rose-500/30');

            buildState.platform = b.getAttribute('data-platform');
            updateAll();
        };
    });

    if (checkAssembly) {
        checkAssembly.onchange = renderSummary;
    }

    // Add Complete Build to Cart
    if (btnAddToCart) {
        btnAddToCart.onclick = () => {
            const items = [
                buildState.selectedCPU, buildState.selectedMB, buildState.selectedRAM,
                buildState.selectedGPU, buildState.selectedSSD, buildState.selectedPSU, buildState.selectedCase
            ].filter(Boolean);

            if (items.length === 0) {
                alert('Por favor selecciona al menos un componente para tu PC.');
                return;
            }

            if (window.JMSHOP_Cart) {
                items.forEach(item => {
                    window.JMSHOP_Cart.addItem({
                        id: item.id,
                        title: item.title,
                        price: formatMoney(item.price),
                        numericPrice: item.price,
                        image: item.image,
                        type: 'producto'
                    });
                });

                if (checkAssembly && checkAssembly.checked) {
                    window.JMSHOP_Cart.addItem({
                        id: 'service-armado-custom',
                        title: 'Servicio de Armado & Testeo de PC Custom',
                        price: formatMoney(assemblyPrice),
                        numericPrice: assemblyPrice,
                        image: 'https://images.unsplash.com/photo-1587202372634-32705e3bf49c?auto=format&fit=crop&w=400&q=80',
                        type: 'servicio'
                    });
                }
            }
        };
    }

    // WhatsApp Builder Quote
    if (btnWhatsApp) {
        btnWhatsApp.onclick = () => {
            const items = [
                buildState.selectedCPU, buildState.selectedMB, buildState.selectedRAM,
                buildState.selectedGPU, buildState.selectedSSD, buildState.selectedPSU, buildState.selectedCase
            ].filter(Boolean);

            if (items.length === 0) {
                alert('Por favor selecciona al menos un componente para armar la cotización.');
                return;
            }

            let msg = "Hola JMSHOP! Quisiera cotizar el siguiente armado de PC a medida:\n\n";
            items.forEach(i => {
                msg += `- ${i.title}: ${formatMoney(i.price)}\n`;
            });

            if (checkAssembly && checkAssembly.checked) {
                msg += `- Servicio de Armado & Testeo: ${formatMoney(assemblyPrice)}\n`;
            }

            let total = items.reduce((s, i) => s + i.price, 0) + (checkAssembly.checked ? assemblyPrice : 0);
            msg += `\n*Presupuesto Total Estimado:* ${formatMoney(total)}`;

            window.open(`https://wa.me/5493580000000?text=${encodeURIComponent(msg)}`, '_blank');
        };
    }

    async function initBuilder() {
        await loadBuilderDataFromAPI();
        updateAll();
    }
    initBuilder();
});
