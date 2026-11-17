"""
SmartServe - Database Module
Connected to Supabase Cloud Database:
  URL: https://wkbjcjdoasthbqsfktzx.supabase.co
  KEY: sb_publishable_O3qdZffrJtd9NgX-S8ighw_3nAkp8zb

Includes seamless fallback to local SQLite so the app is always functional.
"""

import os
import sqlite3

# ================= SUPABASE CREDENTIALS =================
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://wkbjcjdoasthbqsfktzx.supabase.co").strip()
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_O3qdZffrJtd9NgX-S8ighw_3nAkp8zb").strip()

DATABASE_NAME = "restaurant.db"

# Initialize Supabase client
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[OK] Connected to Supabase Cloud Database:", SUPABASE_URL)
    except Exception as e:
        print(f"[WARNING] Supabase init warning: {e}. Falling back to SQLite.")
        supabase = None


def is_supabase_active():
    """Returns True if connected to Supabase Cloud Database, else False."""
    return supabase is not None


# ---------------- SQLITE HELPER FUNCTIONS ---------------- #

def get_db_connection():
    """Establishes and returns a connection to the local SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes tables and seeds 80 default items in local SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            order_type TEXT DEFAULT 'Dine-In',
            table_no TEXT DEFAULT '',
            items_summary TEXT NOT NULL,
            total_bill REAL NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM menu_items")
    count = cursor.fetchone()[0]

    if count < 80:
        cursor.execute("DELETE FROM menu_items")
        default_items = [
            # Group 1: Starters & Snacks (10 items)
            ("Paneer Tikka", "Starters & Snacks", 210.0),
            ("Hara Bhara Kabab", "Starters & Snacks", 160.0),
            ("Crispy Corn", "Starters & Snacks", 140.0),
            ("Veg Spring Rolls", "Starters & Snacks", 130.0),
            ("Cheese Garlic Bread", "Starters & Snacks", 120.0),
            ("Classic French Fries", "Starters & Snacks", 80.0),
            ("Peri Peri Fries", "Starters & Snacks", 100.0),
            ("Golden Onion Rings", "Starters & Snacks", 90.0),
            ("Dahi Ke Kabab", "Starters & Snacks", 180.0),
            ("Samosa Platter with Chutney", "Starters & Snacks", 70.0),

            # Group 2: Soups & Salads (10 items)
            ("Tomato Basil Soup", "Soups & Salads", 110.0),
            ("Sweet Corn Veg Soup", "Soups & Salads", 120.0),
            ("Hot and Sour Soup", "Soups & Salads", 130.0),
            ("Manchow Soup with Crispy Noodles", "Soups & Salads", 130.0),
            ("Cream of Mushroom Soup", "Soups & Salads", 150.0),
            ("Classic Caesar Salad", "Soups & Salads", 160.0),
            ("Greek Feta Salad", "Soups & Salads", 170.0),
            ("Fresh Green Garden Salad", "Soups & Salads", 90.0),
            ("Russian Vegetable Salad", "Soups & Salads", 140.0),
            ("Sprouted Moong Salad", "Soups & Salads", 100.0),

            # Group 3: Main Course - Veg (10 items)
            ("Paneer Butter Masala", "Main Course - Veg", 240.0),
            ("Kadhai Paneer", "Main Course - Veg", 230.0),
            ("Palak Paneer", "Main Course - Veg", 220.0),
            ("Dal Makhani", "Main Course - Veg", 190.0),
            ("Yellow Dal Tadka", "Main Course - Veg", 150.0),
            ("Malai Kofta", "Main Course - Veg", 250.0),
            ("Mix Vegetable Curry", "Main Course - Veg", 180.0),
            ("Shahi Paneer", "Main Course - Veg", 240.0),
            ("Aloo Gobi Masala", "Main Course - Veg", 160.0),
            ("Chana Masala", "Main Course - Veg", 170.0),

            # Group 4: Main Course - Non-Veg (10 items)
            ("Butter Chicken", "Main Course - Non-Veg", 290.0),
            ("Chicken Tikka Masala", "Main Course - Non-Veg", 280.0),
            ("Kadhai Chicken", "Main Course - Non-Veg", 270.0),
            ("Home Style Chicken Curry", "Main Course - Non-Veg", 250.0),
            ("Mutton Rogan Josh", "Main Course - Non-Veg", 360.0),
            ("Shahi Chicken Korma", "Main Course - Non-Veg", 290.0),
            ("Goan Fish Curry", "Main Course - Non-Veg", 310.0),
            ("Tandoori Chicken (Half)", "Main Course - Non-Veg", 220.0),
            ("Chicken Dum Biryani", "Main Course - Non-Veg", 240.0),
            ("Mutton Dum Biryani", "Main Course - Non-Veg", 350.0),

            # Group 5: Breads & Rice (10 items)
            ("Butter Naan", "Breads & Rice", 45.0),
            ("Garlic Naan", "Breads & Rice", 55.0),
            ("Tandoori Roti", "Breads & Rice", 20.0),
            ("Butter Roti", "Breads & Rice", 25.0),
            ("Laccha Paratha", "Breads & Rice", 50.0),
            ("Jeera Rice", "Breads & Rice", 120.0),
            ("Steamed Basmati Rice", "Breads & Rice", 90.0),
            ("Veg Pulao", "Breads & Rice", 150.0),
            ("Kashmiri Pulao", "Breads & Rice", 180.0),
            ("Stuffed Amritsari Kulcha", "Breads & Rice", 70.0),

            # Group 6: Chinese & Fast Food (10 items)
            ("Veg Hakka Noodles", "Chinese & Fast Food", 150.0),
            ("Chilli Garlic Noodles", "Chinese & Fast Food", 160.0),
            ("Veg Fried Rice", "Chinese & Fast Food", 150.0),
            ("Schezwan Fried Rice", "Chinese & Fast Food", 160.0),
            ("Veg Manchurian Gravy", "Chinese & Fast Food", 170.0),
            ("Chilli Paneer Dry", "Chinese & Fast Food", 210.0),
            ("Classic Veg Burger", "Chinese & Fast Food", 85.0),
            ("Cheese Overload Burger", "Chinese & Fast Food", 120.0),
            ("Margherita Pizza", "Chinese & Fast Food", 199.0),
            ("Farmhouse Veggie Pizza", "Chinese & Fast Food", 269.0),

            # Group 7: Beverages & Shakes (10 items)
            ("Special Masala Chai", "Beverages & Shakes", 30.0),
            ("Classic Cold Coffee", "Beverages & Shakes", 80.0),
            ("Cold Coffee with Ice Cream", "Beverages & Shakes", 110.0),
            ("Fresh Lime Soda", "Beverages & Shakes", 50.0),
            ("Virgin Mojito", "Beverages & Shakes", 95.0),
            ("Mango Thick Shake", "Beverages & Shakes", 110.0),
            ("Oreo Chocolate Shake", "Beverages & Shakes", 130.0),
            ("Strawberry Smoothie", "Beverages & Shakes", 120.0),
            ("Punjabi Sweet Lassi", "Beverages & Shakes", 60.0),
            ("Mineral Water (1 Litre)", "Beverages & Shakes", 20.0),

            # Group 8: Desserts & Sweets (10 items)
            ("Hot Gulab Jamun (2 Pcs)", "Desserts & Sweets", 60.0),
            ("Sponge Rasgulla (2 Pcs)", "Desserts & Sweets", 60.0),
            ("Chocolate Brownie with Ice Cream", "Desserts & Sweets", 130.0),
            ("Sizzling Chocolate Brownie", "Desserts & Sweets", 160.0),
            ("Vanilla Ice Cream", "Desserts & Sweets", 50.0),
            ("Belgian Chocolate Ice Cream", "Desserts & Sweets", 80.0),
            ("Kesar Pista Kulfi", "Desserts & Sweets", 70.0),
            ("Gajar Ka Halwa", "Desserts & Sweets", 90.0),
            ("Red Velvet Pastry", "Desserts & Sweets", 85.0),
            ("New York Cheesecake Slice", "Desserts & Sweets", 150.0),
        ]
        cursor.executemany(
            "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
            default_items
        )

    conn.commit()
    conn.close()


# ---------------- MENU ITEM FUNCTIONS ---------------- #

def get_menu_items():
    """Returns all menu items from Supabase if available, else SQLite."""
    if is_supabase_active():
        try:
            res = supabase.table("menu_items").select("*").order("id", desc=False).execute()
            if res.data and len(res.data) >= 80:
                return res.data
        except Exception as e:
            print(f"Supabase get_menu_items warning: {e}")

    conn = get_db_connection()
    items = conn.execute("SELECT * FROM menu_items ORDER BY id ASC").fetchall()
    conn.close()
    return items


def get_all_categories():
    """Returns sorted unique category names."""
    if is_supabase_active():
        try:
            res = supabase.table("menu_items").select("category").execute()
            if res.data and len(res.data) > 0:
                return sorted(list({item["category"] for item in res.data}))
        except Exception as e:
            print(f"Supabase get_all_categories warning: {e}")

    conn = get_db_connection()
    rows = conn.execute("SELECT DISTINCT category FROM menu_items ORDER BY category ASC").fetchall()
    conn.close()
    return [row["category"] for row in rows]


def get_menu_item(item_id):
    """Returns a single menu item by ID."""
    if is_supabase_active():
        try:
            res = supabase.table("menu_items").select("*").eq("id", item_id).execute()
            if res.data:
                return res.data[0]
        except Exception:
            pass

    conn = get_db_connection()
    item = conn.execute("SELECT * FROM menu_items WHERE id = ?", (item_id,)).fetchone()
    conn.close()
    return item


def add_menu_item(name, category, price):
    """Adds a new menu item to Supabase and local SQLite."""
    if is_supabase_active():
        try:
            supabase.table("menu_items").insert({
                "name": name.strip(),
                "category": category.strip(),
                "price": float(price)
            }).execute()
        except Exception as e:
            print(f"Supabase add_menu_item warning: {e}")

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO menu_items (name, category, price) VALUES (?, ?, ?)",
        (name.strip(), category.strip(), float(price))
    )
    conn.commit()
    conn.close()


def update_menu_item(item_id, name, category, price):
    """Updates an existing food menu item."""
    if is_supabase_active():
        try:
            supabase.table("menu_items").update({
                "name": name.strip(),
                "category": category.strip(),
                "price": float(price)
            }).eq("id", item_id).execute()
        except Exception as e:
            print(f"Supabase update_menu_item warning: {e}")

    conn = get_db_connection()
    conn.execute(
        "UPDATE menu_items SET name = ?, category = ?, price = ? WHERE id = ?",
        (name.strip(), category.strip(), float(price), item_id)
    )
    conn.commit()
    conn.close()


def delete_menu_item(item_id):
    """Deletes a food item from the menu."""
    if is_supabase_active():
        try:
            supabase.table("menu_items").delete().eq("id", item_id).execute()
        except Exception as e:
            print(f"Supabase delete_menu_item warning: {e}")

    conn = get_db_connection()
    conn.execute("DELETE FROM menu_items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()


# ---------------- ORDER FUNCTIONS ---------------- #

def get_all_orders():
    """Returns all customer orders merged from SQLite and Supabase so orders never disappear."""
    conn = get_db_connection()
    orders_map = {}

    # 1. Load from local SQLite
    try:
        sqlite_orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
        for row in sqlite_orders:
            orders_map[row["id"]] = dict(row)
    except Exception as e:
        print(f"SQLite orders load note: {e}")
    finally:
        conn.close()

    # 2. Merge from Supabase Cloud if available
    if is_supabase_active():
        try:
            res = supabase.table("orders").select("*").order("id", desc=True).execute()
            if res.data and len(res.data) > 0:
                for row in res.data:
                    orders_map[row["id"]] = row
        except Exception as e:
            print(f"Supabase get_all_orders note: {e}")

    # Return list sorted from newest to oldest
    orders_list = list(orders_map.values())
    orders_list.sort(key=lambda o: o.get("id", 0), reverse=True)
    return orders_list


def get_order(order_id):
    """Returns a single order by ID."""
    if is_supabase_active():
        try:
            res = supabase.table("orders").select("*").eq("id", order_id).execute()
            if res.data:
                return res.data[0]
        except Exception:
            pass

    conn = get_db_connection()
    order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    conn.close()
    return order


def create_order(customer_name, customer_phone, order_type, table_no, items_summary, total_bill):
    """Creates a new customer order in Supabase and SQLite."""
    order_id = None
    if is_supabase_active():
        try:
            res = supabase.table("orders").insert({
                "customer_name": customer_name.strip(),
                "customer_phone": customer_phone.strip(),
                "order_type": order_type.strip(),
                "table_no": table_no.strip(),
                "items_summary": items_summary.strip(),
                "total_bill": float(total_bill),
                "status": "Pending"
            }).execute()
            if res.data:
                order_id = res.data[0]["id"]
        except Exception as e:
            print(f"Supabase create_order warning: {e}")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO orders (customer_name, customer_phone, order_type, table_no, items_summary, total_bill, status)
        VALUES (?, ?, ?, ?, ?, ?, 'Pending')
        """,
        (
            customer_name.strip(),
            customer_phone.strip(),
            order_type.strip(),
            table_no.strip(),
            items_summary.strip(),
            float(total_bill)
        )
    )
    sqlite_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return order_id if order_id is not None else sqlite_id


def update_order_status(order_id, new_status):
    """Updates status of an order: Pending, Preparing, Completed, or Cancelled."""
    if is_supabase_active():
        try:
            supabase.table("orders").update({"status": new_status}).eq("id", order_id).execute()
        except Exception as e:
            print(f"Supabase update_order_status warning: {e}")

    conn = get_db_connection()
    conn.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (new_status, order_id)
    )
    conn.commit()
    conn.close()


def update_order_customer(order_id, customer_name, customer_phone, order_type, table_no):
    """Edits customer details on an existing order."""
    if is_supabase_active():
        try:
            supabase.table("orders").update({
                "customer_name": customer_name.strip(),
                "customer_phone": customer_phone.strip(),
                "order_type": order_type.strip(),
                "table_no": table_no.strip()
            }).eq("id", order_id).execute()
        except Exception as e:
            print(f"Supabase update_order_customer warning: {e}")

    conn = get_db_connection()
    conn.execute(
        """
        UPDATE orders 
        SET customer_name = ?, customer_phone = ?, order_type = ?, table_no = ?
        WHERE id = ?
        """,
        (customer_name.strip(), customer_phone.strip(), order_type.strip(), table_no.strip(), order_id)
    )
    conn.commit()
    conn.close()


def delete_order(order_id):
    """Deletes an order from the database."""
    if is_supabase_active():
        try:
            supabase.table("orders").delete().eq("id", order_id).execute()
        except Exception as e:
            print(f"Supabase delete_order warning: {e}")

    conn = get_db_connection()
    conn.execute("DELETE FROM orders WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
