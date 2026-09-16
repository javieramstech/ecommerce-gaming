/**
 * JMSHOP - Módulo de Carrito Drawer Lateral & Pasarela de Pago
 * Mantiene el estado global del carrito persistido en localStorage.
 */

window.JMSHOP_Cart = (function() {
    let cart = [];

    function init() {
        const saved = localStorage.getItem('jmshop_cart_v2');
        if (saved) {
            try {
                cart = JSON.parse(saved);
            } catch (e) {
                cart = [];
            }
        }
        updateBadgeCount();
    }

    function save() {
        localStorage.setItem('jmshop_cart_v2', JSON.stringify(cart));
        updateBadgeCount();
        renderCartDrawer();
    }

    function updateBadgeCount() {
        const count = cart.reduce((sum, item) => sum + item.quantity, 0);
        const badges = document.querySelectorAll('.cart-badge-count');
        badges.forEach(b => {
            b.textContent = count;
            b.classList.toggle('hidden', count === 0);
        });
    }

    function addItem(product) {
        const existing = cart.find(i => i.id === product.id);
        if (existing) {
            existing.quantity += 1;
        } else {
            cart.push({
                id: product.id,
                title: product.title,
                price: product.price,
                numericPrice: product.numericPrice || parsePrice(product.price),
                image: product.image,
                type: product.type,
                quantity: 1
            });
        }
        save();
        showNotification(`"${product.title}" agregado al carrito`);
        openDrawer();
    }

    function parsePrice(priceStr) {
        if (typeof priceStr === 'number') return priceStr;
        return parseInt(priceStr.replace(/[^0-9]/g, '')) || 0;
    }

    function removeItem(id) {
        cart = cart.filter(i => i.id !== id);
        save();
    }

    function updateQuantity(id, change) {
        const item = cart.find(i => i.id === id);
        if (item) {
            item.quantity += change;
            if (item.quantity <= 0) {
                removeItem(id);
            } else {
                save();
            }
        }
    }

    function clearCart() {
        cart = [];
        save();
    }

    function getCartItems() {
        return cart;
    }

    function getTotals() {
        const subtotal = cart.reduce((sum, item) => sum + (item.numericPrice * item.quantity), 0);
        const tax = Math.round(subtotal * 0.21); // IVA 21%
        const total = subtotal; // Precio final con IVA incluido
        return { subtotal, tax, total };
    }

    function formatCurrency(amount) {
        return '$' + amount.toLocaleString('es-AR');
    }

    // Notifications
    function showNotification(msg) {
        let toast = document.getElementById('global-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'global-toast';
            toast.className = 'fixed bottom-6 right-6 z-50 bg-emerald-500 text-slate-950 font-bold px-5 py-3 rounded-2xl shadow-2xl border border-emerald-300 flex items-center gap-3 animate-slide-up pointer-events-none';
            document.body.appendChild(toast);
        }
        toast.innerHTML = `
            <svg class="w-5 h-5 text-slate-950 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
            <span>${msg}</span>
        `;
        toast.style.display = 'flex';
        setTimeout(() => {
            toast.style.display = 'none';
        }, 3000);
    }

    // Drawer Management
    function openDrawer() {
        const drawer = document.getElementById('cart-drawer');
        if (drawer) {
            drawer.classList.remove('hidden');
            renderCartDrawer();
        }
    }

    function closeDrawer() {
        const drawer = document.getElementById('cart-drawer');
        if (drawer) {
            drawer.classList.add('hidden');
        }
    }

    function renderCartDrawer() {
        const itemsContainer = document.getElementById('cart-drawer-items');
        const emptyView = document.getElementById('cart-drawer-empty');
        const footerView = document.getElementById('cart-drawer-footer');
        const subtotalEl = document.getElementById('cart-subtotal-price');

        if (!itemsContainer) return;

        itemsContainer.innerHTML = '';

        if (cart.length === 0) {
            emptyView.classList.remove('hidden');
            footerView.classList.add('hidden');
            return;
        }

        emptyView.classList.add('hidden');
        footerView.classList.remove('hidden');

        cart.forEach(item => {
            const div = document.createElement('div');
            div.className = 'flex items-center gap-4 bg-slate-900/80 p-3.5 rounded-2xl border border-slate-800/80';
            div.innerHTML = `
                <img src="${item.image}" alt="${item.title}" class="w-16 h-16 rounded-xl object-cover shrink-0 bg-slate-950" />
                <div class="flex-grow min-w-0">
                    <h4 class="text-sm font-bold text-slate-100 truncate">${item.title}</h4>
                    <span class="text-xs font-extrabold text-rose-500 font-mono block mt-0.5">${formatCurrency(item.numericPrice)}</span>
                    <div class="flex items-center gap-2 mt-2">
                        <button class="cart-qty-btn-minus w-6 h-6 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold flex items-center justify-center text-xs" data-id="${item.id}">-</button>
                        <span class="text-xs font-bold text-white px-2">${item.quantity}</span>
                        <button class="cart-qty-btn-plus w-6 h-6 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold flex items-center justify-center text-xs" data-id="${item.id}">+</button>
                    </div>
                </div>
                <button class="cart-remove-btn p-2 text-slate-500 hover:text-rose-400 transition-colors" data-id="${item.id}" aria-label="Eliminar ítem">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
            `;
            itemsContainer.appendChild(div);
        });

        const totals = getTotals();
        if (subtotalEl) {
            subtotalEl.textContent = formatCurrency(totals.total);
        }

        // Attach event handlers
        itemsContainer.querySelectorAll('.cart-qty-btn-minus').forEach(b => {
            b.onclick = () => updateQuantity(parseInt(b.getAttribute('data-id')), -1);
        });
        itemsContainer.querySelectorAll('.cart-qty-btn-plus').forEach(b => {
            b.onclick = () => updateQuantity(parseInt(b.getAttribute('data-id')), 1);
        });
        itemsContainer.querySelectorAll('.cart-remove-btn').forEach(b => {
            b.onclick = () => removeItem(parseInt(b.getAttribute('data-id')));
        });
    }

    // Checkout Modal Setup
    function openCheckoutModal() {
        closeDrawer();
        const modal = document.getElementById('checkout-modal');
        const summaryContainer = document.getElementById('checkout-order-summary');
        const totalEl = document.getElementById('checkout-total-price');

        if (!modal) return;

        // Render summary items
        summaryContainer.innerHTML = '';
        cart.forEach(item => {
            const div = document.createElement('div');
            div.className = 'flex justify-between text-xs text-slate-300 py-1 border-b border-slate-800/40';
            div.innerHTML = `
                <span class="truncate max-w-[200px]">${item.quantity}x ${item.title}</span>
                <span class="font-bold text-rose-500 font-mono">${formatCurrency(item.numericPrice * item.quantity)}</span>
            `;
            summaryContainer.appendChild(div);
        });

        const totals = getTotals();
        totalEl.textContent = formatCurrency(totals.total);

        // Reset forms & views
        document.getElementById('checkout-form-view').classList.remove('hidden');
        document.getElementById('checkout-success-view').classList.add('hidden');

        modal.classList.remove('hidden');
        modal.classList.add('flex');
    }

    function closeCheckoutModal() {
        const modal = document.getElementById('checkout-modal');
        if (modal) {
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }
    }

    function initEvents() {
        init();

        // Cart Drawer Open Buttons
        document.querySelectorAll('.open-cart-btn').forEach(b => {
            b.onclick = openDrawer;
        });

        const drawerCloseBtn = document.getElementById('cart-drawer-close');
        if (drawerCloseBtn) drawerCloseBtn.onclick = closeDrawer;

        const clearCartBtn = document.getElementById('cart-clear-btn');
        if (clearCartBtn) clearCartBtn.onclick = clearCart;

        const checkoutBtn = document.getElementById('cart-checkout-btn');
        if (checkoutBtn) checkoutBtn.onclick = openCheckoutModal;

        const whatsappCheckoutBtn = document.getElementById('cart-whatsapp-btn');
        if (whatsappCheckoutBtn) {
            whatsappCheckoutBtn.onclick = () => {
                const totals = getTotals();
                let msg = "Hola JMSHOP! Quisiera realizar el siguiente pedido desde la web:\n\n";
                cart.forEach(i => {
                    msg += `- ${i.quantity}x ${i.title} (${formatCurrency(i.numericPrice * i.quantity)})\n`;
                });
                msg += `\n*Total a Pagar:* ${formatCurrency(totals.total)}`;
                
                const url = `https://wa.me/5493580000000?text=${encodeURIComponent(msg)}`;
                window.open(url, '_blank');
            };
        }

        // Checkout Modal Events
        const checkoutCloseBtn = document.getElementById('checkout-close-btn');
        if (checkoutCloseBtn) checkoutCloseBtn.onclick = closeCheckoutModal;

        const checkoutForm = document.getElementById('checkout-payment-form');
        if (checkoutForm) {
            checkoutForm.onsubmit = (e) => {
                e.preventDefault();
                // Process payment simulation
                const orderNum = 'JMS-' + Math.floor(100000 + Math.random() * 900000);
                document.getElementById('checkout-order-number').textContent = orderNum;

                document.getElementById('checkout-form-view').classList.add('hidden');
                document.getElementById('checkout-success-view').classList.remove('hidden');

                clearCart();
            };
        }

        const checkoutFinishBtn = document.getElementById('checkout-finish-btn');
        if (checkoutFinishBtn) checkoutFinishBtn.onclick = closeCheckoutModal;
    }

    return {
        initEvents,
        addItem,
        removeItem,
        updateQuantity,
        clearCart,
        getCartItems,
        getTotals,
        formatCurrency,
        openDrawer,
        closeDrawer
    };
})();

document.addEventListener('DOMContentLoaded', () => {
    window.JMSHOP_Cart.initEvents();
});
