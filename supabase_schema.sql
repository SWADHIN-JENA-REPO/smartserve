-- ====================================================================
-- SmartServe - Supabase Database Schema & Seed Data
-- Run this in Supabase: SQL Editor -> New Query -> Paste -> Run
-- ====================================================================

-- 1. Create table for Food Menu Items
CREATE TABLE IF NOT EXISTS menu_items (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Create table for Customer Orders
CREATE TABLE IF NOT EXISTS orders (
    id BIGSERIAL PRIMARY KEY,
    customer_name TEXT NOT NULL,
    customer_phone TEXT NOT NULL,
    order_type TEXT DEFAULT 'Dine-In',
    table_no TEXT DEFAULT '',
    items_summary TEXT NOT NULL,
    total_bill NUMERIC(10, 2) NOT NULL,
    status TEXT DEFAULT 'Pending',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. DISABLE Row Level Security (RLS) so the publishable key can read & write
ALTER TABLE menu_items DISABLE ROW LEVEL SECURITY;
ALTER TABLE orders DISABLE ROW LEVEL SECURITY;

-- 4. Clear existing items to avoid duplicates
DELETE FROM menu_items;

-- 5. Seed the 80 Food Items across 8 Category Groups
INSERT INTO menu_items (name, category, price) VALUES
-- Group 1: Starters & Snacks (10 items)
('Paneer Tikka', 'Starters & Snacks', 210.0),
('Hara Bhara Kabab', 'Starters & Snacks', 160.0),
('Crispy Corn', 'Starters & Snacks', 140.0),
('Veg Spring Rolls', 'Starters & Snacks', 130.0),
('Cheese Garlic Bread', 'Starters & Snacks', 120.0),
('Classic French Fries', 'Starters & Snacks', 80.0),
('Peri Peri Fries', 'Starters & Snacks', 100.0),
('Golden Onion Rings', 'Starters & Snacks', 90.0),
('Dahi Ke Kabab', 'Starters & Snacks', 180.0),
('Samosa Platter with Chutney', 'Starters & Snacks', 70.0),

-- Group 2: Soups & Salads (10 items)
('Tomato Basil Soup', 'Soups & Salads', 110.0),
('Sweet Corn Veg Soup', 'Soups & Salads', 120.0),
('Hot and Sour Soup', 'Soups & Salads', 130.0),
('Manchow Soup with Crispy Noodles', 'Soups & Salads', 130.0),
('Cream of Mushroom Soup', 'Soups & Salads', 150.0),
('Classic Caesar Salad', 'Soups & Salads', 160.0),
('Greek Feta Salad', 'Soups & Salads', 170.0),
('Fresh Green Garden Salad', 'Soups & Salads', 90.0),
('Russian Vegetable Salad', 'Soups & Salads', 140.0),
('Sprouted Moong Salad', 'Soups & Salads', 100.0),

-- Group 3: Main Course - Veg (10 items)
('Paneer Butter Masala', 'Main Course - Veg', 240.0),
('Kadhai Paneer', 'Main Course - Veg', 230.0),
('Palak Paneer', 'Main Course - Veg', 220.0),
('Dal Makhani', 'Main Course - Veg', 190.0),
('Yellow Dal Tadka', 'Main Course - Veg', 150.0),
('Malai Kofta', 'Main Course - Veg', 250.0),
('Mix Vegetable Curry', 'Main Course - Veg', 180.0),
('Shahi Paneer', 'Main Course - Veg', 240.0),
('Aloo Gobi Masala', 'Main Course - Veg', 160.0),
('Chana Masala', 'Main Course - Veg', 170.0),

-- Group 4: Main Course - Non-Veg (10 items)
('Butter Chicken', 'Main Course - Non-Veg', 290.0),
('Chicken Tikka Masala', 'Main Course - Non-Veg', 280.0),
('Kadhai Chicken', 'Main Course - Non-Veg', 270.0),
('Home Style Chicken Curry', 'Main Course - Non-Veg', 250.0),
('Mutton Rogan Josh', 'Main Course - Non-Veg', 360.0),
('Shahi Chicken Korma', 'Main Course - Non-Veg', 290.0),
('Goan Fish Curry', 'Main Course - Non-Veg', 310.0),
('Tandoori Chicken (Half)', 'Main Course - Non-Veg', 220.0),
('Chicken Dum Biryani', 'Main Course - Non-Veg', 240.0),
('Mutton Dum Biryani', 'Main Course - Non-Veg', 350.0),

-- Group 5: Breads & Rice (10 items)
('Butter Naan', 'Breads & Rice', 45.0),
('Garlic Naan', 'Breads & Rice', 55.0),
('Tandoori Roti', 'Breads & Rice', 20.0),
('Butter Roti', 'Breads & Rice', 25.0),
('Laccha Paratha', 'Breads & Rice', 50.0),
('Jeera Rice', 'Breads & Rice', 120.0),
('Steamed Basmati Rice', 'Breads & Rice', 90.0),
('Veg Pulao', 'Breads & Rice', 150.0),
('Kashmiri Pulao', 'Breads & Rice', 180.0),
('Stuffed Amritsari Kulcha', 'Breads & Rice', 70.0),

-- Group 6: Chinese & Fast Food (10 items)
('Veg Hakka Noodles', 'Chinese & Fast Food', 150.0),
('Chilli Garlic Noodles', 'Chinese & Fast Food', 160.0),
('Veg Fried Rice', 'Chinese & Fast Food', 150.0),
('Schezwan Fried Rice', 'Chinese & Fast Food', 160.0),
('Veg Manchurian Gravy', 'Chinese & Fast Food', 170.0),
('Chilli Paneer Dry', 'Chinese & Fast Food', 210.0),
('Classic Veg Burger', 'Chinese & Fast Food', 85.0),
('Cheese Overload Burger', 'Chinese & Fast Food', 120.0),
('Margherita Pizza', 'Chinese & Fast Food', 199.0),
('Farmhouse Veggie Pizza', 'Chinese & Fast Food', 269.0),

-- Group 7: Beverages & Shakes (10 items)
('Special Masala Chai', 'Beverages & Shakes', 30.0),
('Classic Cold Coffee', 'Beverages & Shakes', 80.0),
('Cold Coffee with Ice Cream', 'Beverages & Shakes', 110.0),
('Fresh Lime Soda', 'Beverages & Shakes', 50.0),
('Virgin Mojito', 'Beverages & Shakes', 95.0),
('Mango Thick Shake', 'Beverages & Shakes', 110.0),
('Oreo Chocolate Shake', 'Beverages & Shakes', 130.0),
('Strawberry Smoothie', 'Beverages & Shakes', 120.0),
('Punjabi Sweet Lassi', 'Beverages & Shakes', 60.0),
('Mineral Water (1 Litre)', 'Beverages & Shakes', 20.0),

-- Group 8: Desserts & Sweets (10 items)
('Hot Gulab Jamun (2 Pcs)', 'Desserts & Sweets', 60.0),
('Sponge Rasgulla (2 Pcs)', 'Desserts & Sweets', 60.0),
('Chocolate Brownie with Ice Cream', 'Desserts & Sweets', 130.0),
('Sizzling Chocolate Brownie', 'Desserts & Sweets', 160.0),
('Vanilla Ice Cream', 'Desserts & Sweets', 50.0),
('Belgian Chocolate Ice Cream', 'Desserts & Sweets', 80.0),
('Kesar Pista Kulfi', 'Desserts & Sweets', 70.0),
('Gajar Ka Halwa', 'Desserts & Sweets', 90.0),
('Red Velvet Pastry', 'Desserts & Sweets', 85.0),
('New York Cheesecake Slice', 'Desserts & Sweets', 150.0);
