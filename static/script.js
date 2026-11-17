/* ==========================================================
   SmartServe - JavaScript Logic
   - LocalStorage shopping cart
   - Automatic bill calculation
   - Modal management (Add/Edit item, Edit customer)
   - Category dropdowns with custom type support
   - Category filtering on menu
   ========================================================== */

// Key used to store cart items in browser LocalStorage
const CART_STORAGE_KEY = "smartserve_cart";

// Load cart items from LocalStorage (or return empty array)
function getCart() {
    const data = localStorage.getItem(CART_STORAGE_KEY);
    return data ? JSON.parse(data) : [];
}

// Save cart items to LocalStorage and update navbar badge
function saveCart(cart) {
    localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(cart));
    updateCartBadge();
}

// Update the cart count badge shown in the top navigation
function updateCartBadge() {
    const badge = document.getElementById("cartCountBadge");
    if (!badge) return;

    const cart = getCart();
    const totalCount = cart.reduce((sum, item) => sum + item.qty, 0);
    badge.innerText = totalCount;
    badge.style.display = totalCount > 0 ? "inline-block" : "none";
}

// Toggle custom category input when "+ Add New Category / Type" is selected in dropdown
function toggleCustomCategory(prefix) {
    const select = document.getElementById(`${prefix}_category_select`);
    const group = document.getElementById(`${prefix}_custom_category_group`);
    const input = document.getElementById(`${prefix}_custom_category`);
    if (!select || !group) return;

    if (select.value === "__NEW__") {
        group.style.display = "block";
        if (input) {
            input.required = true;
            input.focus();
        }
    } else {
        group.style.display = "none";
        if (input) {
            input.required = false;
            input.value = "";
        }
    }
}

// ---------------- MENU PAGE FUNCTIONS ---------------- //

// Add item to cart from Menu page
function addToCart(id, name, price) {
    const cart = getCart();
    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ id: id, name: name, price: parseFloat(price), qty: 1 });
    }

    saveCart(cart);

    // Visual feedback on the button
    const btn = document.getElementById(`add-btn-${id}`);
    if (btn) {
        const originalText = btn.innerHTML;
        btn.innerHTML = "✓ Added!";
        btn.classList.add("btn-secondary");
        btn.classList.remove("btn-primary");
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.add("btn-primary");
            btn.classList.remove("btn-secondary");
        }, 800);
    }
}

// Filter menu items by category pill
function filterCategory(category, buttonEl) {
    document.querySelectorAll(".category-pill").forEach(el => el.classList.remove("active"));
    if (buttonEl) buttonEl.classList.add("active");

    const cards = document.querySelectorAll(".food-card");
    let matchCount = 0;
    cards.forEach(card => {
        const itemCat = card.getAttribute("data-category");
        if (category === "all" || itemCat === category) {
            card.style.display = "flex";
            matchCount++;
        } else {
            card.style.display = "none";
        }
    });

    const emptyNotice = document.getElementById("noFilterResults");
    if (emptyNotice) {
        emptyNotice.style.display = matchCount === 0 ? "block" : "none";
    }
}

// Open modal to edit a menu item
function openEditModal(id, name, category, price) {
    const modal = document.getElementById("editItemModal");
    const form = document.getElementById("editItemForm");
    if (!modal || !form) return;

    form.action = `/menu/edit/${id}`;
    document.getElementById("edit_name").value = name;
    document.getElementById("edit_price").value = price;

    const select = document.getElementById("edit_category_select");
    const customGroup = document.getElementById("edit_custom_category_group");
    const customInput = document.getElementById("edit_custom_category");

    // Match dropdown option or select __NEW__
    let matched = false;
    for (let i = 0; i < select.options.length; i++) {
        if (select.options[i].value === category) {
            select.selectedIndex = i;
            matched = true;
            break;
        }
    }

    if (!matched) {
        select.value = "__NEW__";
        customGroup.style.display = "block";
        customInput.value = category;
        customInput.required = true;
    } else {
        customGroup.style.display = "none";
        customInput.value = "";
        customInput.required = false;
    }

    modal.classList.add("active");
}

function openAddModal() {
    const modal = document.getElementById("addItemModal");
    if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("active");
}

// ---------------- ORDER PAGE FUNCTIONS ---------------- //

// Render cart items on the Order page
function renderOrderCart() {
    const cartList = document.getElementById("orderCartList");
    const emptyMsg = document.getElementById("emptyCartMsg");
    const submitBtn = document.getElementById("placeOrderBtn");
    if (!cartList) return;

    const cart = getCart();
    cartList.innerHTML = "";

    if (cart.length === 0) {
        if (emptyMsg) emptyMsg.style.display = "block";
        if (submitBtn) submitBtn.disabled = true;
        updateBillTotals(0);
        return;
    }

    if (emptyMsg) emptyMsg.style.display = "none";
    if (submitBtn) submitBtn.disabled = false;

    let subtotal = 0;

    cart.forEach((item, index) => {
        const itemTotal = item.price * item.qty;
        subtotal += itemTotal;

        const li = document.createElement("li");
        li.className = "cart-item";
        li.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">₹${item.price.toFixed(2)} each</div>
            </div>
            <div class="qty-control">
                <button type="button" class="qty-btn" onclick="changeQty(${index}, -1)">-</button>
                <span class="qty-val">${item.qty}</span>
                <button type="button" class="qty-btn" onclick="changeQty(${index}, 1)">+</button>
            </div>
            <div style="font-weight: 600; min-width: 65px; text-align: right;">
                ₹${itemTotal.toFixed(2)}
            </div>
            <button type="button" class="btn btn-danger btn-sm" style="margin-left: 10px;" onclick="removeFromCart(${index})">
                &times;
            </button>
        `;
        cartList.appendChild(li);
    });

    updateBillTotals(subtotal);
    prepareOrderForm(cart, subtotal);
}

// Change quantity in cart
function changeQty(index, delta) {
    const cart = getCart();
    if (!cart[index]) return;

    cart[index].qty += delta;
    if (cart[index].qty <= 0) {
        cart.splice(index, 1);
    }

    saveCart(cart);
    renderOrderCart();
}

// Remove item from cart
function removeFromCart(index) {
    const cart = getCart();
    cart.splice(index, 1);
    saveCart(cart);
    renderOrderCart();
}

// Add an item from the dropdown selector on Order page
function addItemFromDropdown() {
    const select = document.getElementById("menuDropdown");
    if (!select || !select.value) return;

    const selectedOption = select.options[select.selectedIndex];
    const id = parseInt(select.value);
    const name = selectedOption.getAttribute("data-name");
    const price = parseFloat(selectedOption.getAttribute("data-price"));

    addToCart(id, name, price);
    renderOrderCart();
    select.value = ""; // Reset dropdown
}

// Calculate taxes and total bill
function updateBillTotals(subtotal) {
    const subtotalEl = document.getElementById("subtotalDisplay");
    const gstEl = document.getElementById("gstDisplay");
    const totalEl = document.getElementById("totalDisplay");

    const gst = subtotal * 0.05; // 5% GST
    const grandTotal = subtotal + gst;

    if (subtotalEl) subtotalEl.innerText = `₹${subtotal.toFixed(2)}`;
    if (gstEl) gstEl.innerText = `₹${gst.toFixed(2)}`;
    if (totalEl) totalEl.innerText = `₹${grandTotal.toFixed(2)}`;

    // Set hidden form input for grand total
    const hiddenTotal = document.getElementById("hiddenTotalBill");
    if (hiddenTotal) hiddenTotal.value = grandTotal.toFixed(2);
}

// Package items into a summary string for database
function prepareOrderForm(cart, subtotal) {
    const summaryInput = document.getElementById("hiddenItemsSummary");
    if (!summaryInput) return;

    const summaryStr = cart.map(item => `${item.name} (x${item.qty})`).join(", ");
    summaryInput.value = summaryStr;
}

// ---------------- RECENT ORDERS (LOCAL STORAGE) ---------------- //

const RECENT_ORDERS_KEY = "smartserve_recent_orders";

function getRecentOrders() {
    const data = localStorage.getItem(RECENT_ORDERS_KEY);
    return data ? JSON.parse(data) : [];
}

function saveRecentOrder(order) {
    const list = getRecentOrders();
    const existingIndex = list.findIndex(o => o.id === order.id);
    if (existingIndex >= 0) {
        list[existingIndex] = order;
    } else {
        list.unshift(order);
    }
    if (list.length > 15) list.pop();
    localStorage.setItem(RECENT_ORDERS_KEY, JSON.stringify(list));
    renderRecentOrders();
    renderAdminLocalStorageOrders();
}

function cancelRecentOrder(orderId) {
    if (!confirm(`Are you sure you want to cancel Order #${orderId}?`)) {
        return;
    }

    // Submit POST request to backend cancel endpoint
    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/order/cancel/${orderId}`;
    document.body.appendChild(form);

    // Update localStorage status
    const list = getRecentOrders();
    const item = list.find(o => o.id === orderId);
    if (item) {
        item.status = "Cancelled";
        localStorage.setItem(RECENT_ORDERS_KEY, JSON.stringify(list));
    }

    form.submit();
}

function editRecentOrder(orderId) {
    const list = getRecentOrders();
    const order = list.find(o => o.id === orderId);
    if (!order) return;

    // 1. Populate customer form fields
    const nameInput = document.getElementById("customer_name");
    const phoneInput = document.getElementById("customer_phone");
    const typeSelect = document.getElementById("order_type");
    const tableInput = document.getElementById("table_no");

    if (nameInput) nameInput.value = order.name;
    if (phoneInput) phoneInput.value = order.phone;
    if (typeSelect && order.orderType) typeSelect.value = order.orderType;
    if (tableInput && order.tableNo) tableInput.value = order.tableNo;

    // Call order type handler if present
    if (typeof handleOrderTypeChange === "function") {
        handleOrderTypeChange();
    }

    // 2. Parse ordered items into cart
    // e.g. "Paneer Tikka (x2), Cold Coffee (x1)"
    const newCart = [];
    if (order.items) {
        const itemParts = order.items.split(",");
        itemParts.forEach((part, idx) => {
            const trimmed = part.trim();
            const match = trimmed.match(/^(.*?)\s*\(x(\d+)\)$/);
            if (match) {
                const itemName = match[1].trim();
                const qty = parseInt(match[2]) || 1;
                // Attempt to find price from menu dropdown if available
                let itemPrice = 100.0;
                const dropdown = document.getElementById("menuDropdown");
                if (dropdown) {
                    for (let i = 0; i < dropdown.options.length; i++) {
                        if (dropdown.options[i].getAttribute("data-name") === itemName) {
                            itemPrice = parseFloat(dropdown.options[i].getAttribute("data-price")) || itemPrice;
                            break;
                        }
                    }
                }
                newCart.push({
                    id: Date.now() + idx,
                    name: itemName,
                    price: itemPrice,
                    qty: qty
                });
            }
        });
    }

    if (newCart.length > 0) {
        saveCart(newCart);
        renderOrderCart();
    }

    // Scroll up smoothly to order form
    window.scrollTo({ top: 0, behavior: "smooth" });
    alert(`Order #${orderId} items and details loaded into the order form! Modify items or quantities above and click 'Confirm & Place Order'.`);
}

function renderRecentOrders() {
    const container = document.getElementById("recentOrdersContainer");
    if (!container) return;

    const list = getRecentOrders();
    if (list.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="padding: 20px;">
                <p>📋 No recent orders placed from this device yet.</p>
                <p style="font-size: 0.85rem; margin-top: 4px;">Orders placed on this device will be stored here so you can easily modify or cancel them.</p>
            </div>
        `;
        return;
    }

    let html = `<div style="display: flex; flex-direction: column; gap: 12px;">`;

    list.forEach(order => {
        const isCancelled = order.status === "Cancelled";
        const statusBadge = isCancelled 
            ? `<span class="status-badge" style="background: #fee2e2; color: #dc2626;">❌ Cancelled</span>`
            : (order.status === "Completed"
                ? `<span class="status-badge status-completed">Completed</span>`
                : (order.status === "Preparing"
                    ? `<span class="status-badge status-preparing">Preparing</span>`
                    : `<span class="status-badge status-pending">Pending</span>`));

        html += `
            <div style="border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; background: #fff; box-shadow: var(--shadow-sm);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f3f4f6; padding-bottom: 6px;">
                    <div>
                        <strong>Order #${order.id}</strong> &bull; 
                        <span style="font-size: 0.9rem; color: var(--text-muted);">${order.name} (${order.phone})</span>
                    </div>
                    <div>${statusBadge}</div>
                </div>

                <div style="font-size: 0.9rem; margin-bottom: 6px;">
                    <strong>Items:</strong> ${order.items}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                    <div style="font-weight: 700; color: var(--primary); font-size: 1.05rem;">
                        ₹${parseFloat(order.total).toFixed(2)}
                        <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);">
                            (${order.orderType || 'Dine-In'} ${order.tableNo ? '• ' + order.tableNo : ''})
                        </span>
                    </div>

                    <div style="display: flex; gap: 8px;">
                        ${!isCancelled ? `
                            <button type="button" class="btn btn-secondary btn-sm" onclick="editRecentOrder(${order.id})" title="Change or edit your food items">
                                ✏️ Edit Items
                            </button>
                            <button type="button" class="btn btn-danger btn-sm" onclick="cancelRecentOrder(${order.id})" title="Cancel this order">
                                ❌ Cancel Order
                            </button>
                        ` : `
                            <button type="button" class="btn btn-secondary btn-sm" onclick="editRecentOrder(${order.id})" title="Reorder these items">
                                🔄 Re-order
                            </button>
                        `}
                    </div>
                </div>
            </div>
        `;
    });

    html += `</div>`;
    container.innerHTML = html;
}

// ---------------- ADMIN PAGE FUNCTIONS ---------------- //

// Open modal to edit customer details
function openEditCustomerModal(orderId, currentName, currentPhone) {
    const modal = document.getElementById("editCustomerModal");
    const form = document.getElementById("editCustomerForm");
    if (!modal || !form) return;

    form.action = `/admin/edit-customer/${orderId}`;
    document.getElementById("edit_order_id_display").innerText = `#${orderId}`;
    document.getElementById("edit_customer_name").value = currentName;
    document.getElementById("edit_customer_phone").value = currentPhone;

    modal.classList.add("active");
}

// Close modal when clicking outside modal box
window.addEventListener("click", function(event) {
    if (event.target.classList.contains("modal-backdrop")) {
        event.target.classList.remove("active");
    }
});

function syncAdminOrdersWithLocalStorage() {
    const tableBody = document.getElementById("adminOrdersTableBody");
    if (!tableBody) return;

    const localOrders = getRecentOrders();
    if (!localOrders || localOrders.length === 0) return;

    const existingIds = new Set();
    document.querySelectorAll("tr[data-order-id]").forEach(tr => {
        existingIds.add(tr.getAttribute("data-order-id"));
    });

    const emptyState = document.getElementById("adminEmptyState");
    const tableResponsive = document.getElementById("adminTableResponsive");

    localOrders.forEach(order => {
        const orderIdStr = String(order.id);
        if (!existingIds.has(orderIdStr)) {
            if (emptyState) emptyState.style.display = "none";
            if (tableResponsive) tableResponsive.style.display = "block";

            const tr = document.createElement("tr");
            tr.setAttribute("data-order-id", orderIdStr);
            const isCancelled = order.status === "Cancelled";
            const badgeClass = isCancelled ? "status-badge" : (order.status === "Completed" ? "status-badge status-completed" : (order.status === "Preparing" ? "status-badge status-preparing" : "status-badge status-pending"));
            const badgeStyle = isCancelled ? 'style="background: #fee2e2; color: #dc2626;"' : '';

            tr.innerHTML = `
                <td><strong>#${order.id}</strong> <span style="font-size:0.75rem; color:var(--primary); font-weight:600;">(Local)</span></td>
                <td><div style="font-weight: 600;">${order.name}</div></td>
                <td><code style="background: #f3f4f6; padding: 2px 6px; border-radius: 4px; font-weight: 600;">${order.phone}</code></td>
                <td><span class="status-badge" style="background: #e0f2fe; color: #0369a1;">${order.tableNo || order.orderType || 'Dine-In'}</span></td>
                <td style="max-width: 260px; word-break: break-word;">${order.items}</td>
                <td><strong style="color: var(--primary);">₹${parseFloat(order.total).toFixed(2)}</strong></td>
                <td><span class="${badgeClass}" ${badgeStyle}>${order.status}</span></td>
                <td>
                    <select class="status-select" onchange="updateRecentOrderStatus(${order.id}, this.value); location.reload();">
                        <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                        <option value="Preparing" ${order.status === 'Preparing' ? 'selected' : ''}>Preparing</option>
                        <option value="Completed" ${order.status === 'Completed' ? 'selected' : ''}>Completed</option>
                        <option value="Cancelled" ${order.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                    </select>
                </td>
                <td style="text-align: right;">
                    <button type="button" class="btn btn-danger btn-sm" onclick="cancelRecentOrder(${order.id}); location.reload();" title="Cancel/Delete">🗑️</button>
                </td>
            `;
            tableBody.appendChild(tr);
        }
    });
}

function updateRecentOrderStatus(orderId, newStatus) {
    const list = getRecentOrders();
    const item = list.find(o => String(o.id) === String(orderId));
    if (item) {
        item.status = newStatus;
        localStorage.setItem(RECENT_ORDERS_KEY, JSON.stringify(list));
        renderAdminLocalStorageOrders();
    }
}

// Render Local Storage Orders strictly for Admin Portal
function renderAdminLocalStorageOrders() {
    const container = document.getElementById("adminLocalStorageOrdersContainer");
    if (!container) return;

    const list = getRecentOrders();
    if (list.length === 0) {
        container.innerHTML = `
            <div class="empty-state" style="padding: 24px; text-align: center;">
                <p style="font-weight: 600; color: var(--text-main);">📋 No orders currently stored in browser local storage.</p>
                <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Orders placed on this device are automatically saved to local storage and listed here exclusively for the administrator.</p>
            </div>
        `;
        return;
    }

    let html = `<div style="display: flex; flex-direction: column; gap: 12px;">`;

    list.forEach(order => {
        const isCancelled = order.status === "Cancelled";
        const statusBadge = isCancelled 
            ? `<span class="status-badge" style="background: #fee2e2; color: #dc2626;">❌ Cancelled</span>`
            : (order.status === "Completed"
                ? `<span class="status-badge status-completed">Completed</span>`
                : (order.status === "Preparing"
                    ? `<span class="status-badge status-preparing">Preparing</span>`
                    : `<span class="status-badge status-pending">Pending</span>`));

        html += `
            <div style="border: 1px solid var(--border); border-radius: var(--radius); padding: 14px; background: #fff; box-shadow: var(--shadow-sm);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #f3f4f6; padding-bottom: 6px;">
                    <div>
                        <strong>Order #${order.id}</strong> &bull; 
                        <span style="font-size: 0.9rem; color: var(--text-muted);">${order.name} (${order.phone})</span>
                        <span style="background: #fed7aa; color: #9a3412; font-size: 0.75rem; padding: 2px 7px; border-radius: 4px; font-weight: 600; margin-left: 6px;">💾 Local Storage</span>
                    </div>
                    <div>${statusBadge}</div>
                </div>

                <div style="font-size: 0.9rem; margin-bottom: 6px;">
                    <strong>Items:</strong> ${order.items}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-top: 10px;">
                    <div style="font-weight: 700; color: var(--primary); font-size: 1.05rem;">
                        ₹${parseFloat(order.total).toFixed(2)}
                        <span style="font-size: 0.8rem; font-weight: normal; color: var(--text-muted);">
                            (${order.orderType || 'Dine-In'} ${order.tableNo ? '• ' + order.tableNo : ''})
                        </span>
                    </div>

                    <div style="display: flex; gap: 8px; align-items: center;">
                        <select class="status-select" onchange="updateRecentOrderStatus(${order.id}, this.value)" style="padding: 4px 8px; font-size: 0.85rem;">
                            <option value="Pending" ${order.status === 'Pending' ? 'selected' : ''}>Pending</option>
                            <option value="Preparing" ${order.status === 'Preparing' ? 'selected' : ''}>Preparing</option>
                            <option value="Completed" ${order.status === 'Completed' ? 'selected' : ''}>Completed</option>
                            <option value="Cancelled" ${order.status === 'Cancelled' ? 'selected' : ''}>Cancelled</option>
                        </select>
                        <button type="button" class="btn btn-danger btn-sm" onclick="deleteFromLocalStorage(${order.id})" title="Remove from local storage">
                            🗑️ Delete
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    html += `</div>`;
    container.innerHTML = html;
}

function clearLocalStorageOrders() {
    if (confirm("Are you sure you want to clear all orders from local storage?")) {
        localStorage.removeItem(RECENT_ORDERS_KEY);
        renderAdminLocalStorageOrders();
    }
}

function deleteFromLocalStorage(orderId) {
    if (confirm(`Remove Order #${orderId} from local storage?`)) {
        let list = getRecentOrders();
        list = list.filter(o => String(o.id) !== String(orderId));
        localStorage.setItem(RECENT_ORDERS_KEY, JSON.stringify(list));
        renderAdminLocalStorageOrders();
    }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", function() {
    updateCartBadge();

    // If on the order page, render cart
    if (document.getElementById("orderCartList")) {
        renderOrderCart();
    }
    // If on admin page, render local storage orders and sync table
    if (document.getElementById("adminLocalStorageOrdersContainer")) {
        renderAdminLocalStorageOrders();
    }
    if (document.getElementById("adminOrdersTableBody")) {
        syncAdminOrdersWithLocalStorage();
    }
});
