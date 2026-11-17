"""
SmartServe - Restaurant Order Management System
Backend built with Python Flask and SQLite.
Key Rules:
- Customers can ONLY view menu, add to cart, and place orders with validated 10-digit phone.
- Only authenticated Admin can add new food items, add new food types, edit, or delete items.
- Admin portal is password-protected without displaying passwords.
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import database

app = Flask(__name__)
app.secret_key = "smartserve_college_secret_key_2026"

# Admin Password
ADMIN_PASSWORD = "admin123"

# Ensure database tables are created, migrated and seeded on startup
database.init_db()


# ---------------- PAGE 1: HOME / MENU (CUSTOMER FACING) ---------------- #

@app.route("/")
def index():
    """
    Page 1: Customer Food Menu.
    Customers can ONLY browse food items, filter categories, and add items to cart.
    No adding/editing/deleting food from here.
    """
    menu_items = database.get_menu_items()
    categories = database.get_all_categories()
    return render_template("menu.html", menu_items=menu_items, categories=categories)


# ---------------- PAGE 2: ORDER (CUSTOMER FACING) ---------------- #

@app.route("/order", methods=["GET", "POST"])
def order():
    """
    Page 2: Customer Order Placement.
    Requires:
    1. Customer Name
    2. Exactly 10-digit valid mobile number
    3. Dining option (Dine-In vs Takeaway / Parcel - go home and eat)
    4. Table Number (for Dine-In)
    5. Selected food items with automatic bill calculation
    """
    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        customer_phone = request.form.get("customer_phone", "").strip()
        order_type = request.form.get("order_type", "Dine-In").strip()
        table_no = request.form.get("table_no", "").strip()
        items_summary = request.form.get("items_summary", "").strip()
        total_bill = request.form.get("total_bill", "").strip()

        # Validation: Name required
        if not customer_name:
            flash("Please enter customer name.", "error")
            return redirect(url_for("order"))

        # Validation: Phone must be EXACTLY 10 digits
        if not (customer_phone.isdigit() and len(customer_phone) == 10):
            flash("Mobile number must be exactly 10 digits. Anything else is not accepted.", "error")
            return redirect(url_for("order"))

        # Validation: Items & Bill
        if not items_summary or not total_bill:
            flash("Please select at least one food item for your order.", "error")
            return redirect(url_for("order"))

        # Handle Table / Takeaway details
        if "Takeaway" in order_type:
            table_no = "Takeaway (Go Home)"
        elif not table_no:
            table_no = "Table (Unspecified)"

        try:
            bill_float = float(total_bill)
            order_id = database.create_order(
                customer_name, customer_phone, order_type, table_no, items_summary, bill_float
            )
            confirmed_order = {
                "id": order_id,
                "customer_name": customer_name,
                "customer_phone": customer_phone,
                "order_type": order_type,
                "table_no": table_no,
                "items_summary": items_summary,
                "total_bill": bill_float,
                "status": "Pending"
            }
            flash("Order placed successfully!", "success")
            menu_items = database.get_menu_items()
            categories = database.get_all_categories()
            return render_template(
                "order.html",
                menu_items=menu_items,
                categories=categories,
                confirmed_order=confirmed_order
            )
        except Exception as e:
            flash(f"Error placing order: {e}", "error")
            return redirect(url_for("order"))

    menu_items = database.get_menu_items()
    categories = database.get_all_categories()
    return render_template("order.html", menu_items=menu_items, categories=categories, confirmed_order=None)


@app.route("/order/cancel/<int:order_id>", methods=["POST"])
def cancel_order(order_id):
    """Allows customers or staff to cancel an order."""
    try:
        database.update_order_status(order_id, "Cancelled")
        flash(f"Order #{order_id} has been cancelled successfully.", "info")
    except Exception as e:
        flash(f"Error cancelling order: {e}", "error")
    return redirect(url_for("order"))


# ---------------- PAGE 3: ADMIN DASHBOARD (ADMIN ONLY) ---------------- #

@app.route("/admin")
def admin():
    """
    Page 3: Authenticated Admin Dashboard.
    Only admin can view orders, track revenue, and manage the food menu items.
    """
    is_authenticated = session.get("admin_logged_in", False)

    if not is_authenticated:
        return render_template("admin.html", authenticated=False)

    orders = database.get_all_orders()
    menu_items = database.get_menu_items()
    categories = database.get_all_categories()

    # Calculate statistics for the dashboard
    total_orders = len(orders)
    pending_count = sum(1 for o in orders if o["status"] == "Pending")
    preparing_count = sum(1 for o in orders if o["status"] == "Preparing")
    completed_count = sum(1 for o in orders if o["status"] == "Completed")
    total_revenue = sum(o["total_bill"] for o in orders)

    stats = {
        "total": total_orders,
        "pending": pending_count,
        "preparing": preparing_count,
        "completed": completed_count,
        "revenue": round(total_revenue, 2),
        "total_items": len(menu_items),
        "total_categories": len(categories)
    }

    return render_template(
        "admin.html",
        authenticated=True,
        orders=orders,
        stats=stats,
        menu_items=menu_items,
        categories=categories
    )


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    """Validates admin password or displays admin authentication screen."""
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            flash("Admin login successful. Welcome!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Incorrect admin password. Please try again.", "error")
            return redirect(url_for("admin_login"))

    # If already logged in, redirect to admin dashboard, else show login screen
    if session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    return render_template("admin.html", authenticated=False)


@app.route("/admin/logout")
def admin_logout():
    """Logs out admin and locks the dashboard."""
    session.pop("admin_logged_in", None)
    flash("Admin logged out successfully.", "info")
    return redirect(url_for("admin"))


# ---------------- ADMIN ONLY: FOOD & MENU MANAGEMENT ---------------- #

@app.route("/admin/menu/add", methods=["POST"])
def add_item():
    """Admin-only: Adds a new food item and optional new food category type."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Only the admin can add new food items.", "error")
        return redirect(url_for("admin"))

    name = request.form.get("name")
    selected_category = request.form.get("category")
    custom_category = request.form.get("custom_category", "").strip()
    price = request.form.get("price")

    category = custom_category if custom_category else selected_category

    if not name or not category or not price:
        flash("Please provide food name, category type, and price.", "error")
        return redirect(url_for("admin"))

    try:
        database.add_menu_item(name, category, float(price))
        flash(f"New dish '{name}' ({category}) added to menu successfully!", "success")
    except Exception as e:
        flash(f"Error adding item: {e}", "error")

    return redirect(url_for("admin"))


@app.route("/admin/menu/edit/<int:item_id>", methods=["POST"])
def edit_item(item_id):
    """Admin-only: Edits an existing food item and its category."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Only the admin can edit food items.", "error")
        return redirect(url_for("admin"))

    name = request.form.get("name")
    selected_category = request.form.get("category")
    custom_category = request.form.get("custom_category", "").strip()
    price = request.form.get("price")

    category = custom_category if custom_category else selected_category

    if not name or not category or not price:
        flash("Please provide all required fields to update.", "error")
        return redirect(url_for("admin"))

    try:
        database.update_menu_item(item_id, name, category, float(price))
        flash(f"'{name}' updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating item: {e}", "error")

    return redirect(url_for("admin"))


@app.route("/admin/menu/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    """Admin-only: Deletes a food item from the menu."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Only the admin can delete food items.", "error")
        return redirect(url_for("admin"))

    try:
        database.delete_menu_item(item_id)
        flash("Food item removed from menu.", "success")
    except Exception as e:
        flash(f"Error deleting item: {e}", "error")

    return redirect(url_for("admin"))


# ---------------- ADMIN ONLY: ORDER STATUS & CUSTOMER MANAGEMENT ---------------- #

@app.route("/admin/status/<int:order_id>", methods=["POST"])
def update_status(order_id):
    """Admin-only: Updates order status: Pending, Preparing, Completed."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Please log in as admin.", "error")
        return redirect(url_for("admin"))

    new_status = request.form.get("status")
    if new_status in ["Pending", "Preparing", "Completed"]:
        database.update_order_status(order_id, new_status)
        flash(f"Order #{order_id} status updated to '{new_status}'.", "success")
    else:
        flash("Invalid status selected.", "error")

    return redirect(url_for("admin"))


@app.route("/admin/edit-customer/<int:order_id>", methods=["POST"])
def edit_customer(order_id):
    """Admin-only: Edits customer details on an order."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Please log in as admin.", "error")
        return redirect(url_for("admin"))

    customer_name = request.form.get("customer_name", "").strip()
    customer_phone = request.form.get("customer_phone", "").strip()
    order_type = request.form.get("order_type", "Dine-In").strip()
    table_no = request.form.get("table_no", "").strip()

    if not customer_name:
        flash("Customer name cannot be empty.", "error")
        return redirect(url_for("admin"))

    if not (customer_phone.isdigit() and len(customer_phone) == 10):
        flash("Customer phone must be exactly 10 digits.", "error")
        return redirect(url_for("admin"))

    try:
        database.update_order_customer(order_id, customer_name, customer_phone, order_type, table_no)
        flash(f"Order #{order_id} customer details updated.", "success")
    except Exception as e:
        flash(f"Error updating customer details: {e}", "error")

    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:order_id>", methods=["POST"])
def delete_order(order_id):
    """Admin-only: Deletes a customer order."""
    if not session.get("admin_logged_in"):
        flash("Unauthorized. Please log in as admin.", "error")
        return redirect(url_for("admin"))

    try:
        database.delete_order(order_id)
        flash(f"Order #{order_id} deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting order: {e}", "error")

    return redirect(url_for("admin"))


# ---------------- API HELPER ---------------- #

@app.route("/api/menu-items")
def api_menu():
    """Returns menu items as JSON for client-side JavaScript."""
    items = database.get_menu_items()
    items_list = [dict(item) for item in items]
    return jsonify(items_list)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
