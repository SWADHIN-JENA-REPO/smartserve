# SmartServe - Restaurant Order Management System
> **3rd Semester B.Tech CSE Project**  
> Built with **Python Flask**, **Supabase Cloud Database** (with local SQLite fallback), **HTML**, **CSS**, and **JavaScript**.

---

## 📱 Will It Show on Others' Phones and Laptops?
### **YES! Absolutely 100%!**

Once you deploy SmartServe to **Render** and connect **Supabase Cloud Database**:
1. **Universal Access**: Any friend, teacher, or customer can open your Render link (`https://your-app.onrender.com`) on **any smartphone (iPhone/Android)** or **any laptop (Mac/Windows/Linux)** from anywhere in the world.
2. **Real-Time Cross-Device Data Sync**:
   - When a customer places an order from their **mobile phone** at Table 4...
   - The order is instantly saved to **Supabase Cloud**.
   - When you (the Admin) open the **Admin Dashboard on your laptop**, that new order appears instantly in your dashboard!
   - When you change the status from **Pending ➔ Preparing ➔ Completed**, anyone viewing the order status sees the update immediately because both devices communicate with the **same central Supabase cloud database**!

---

## 🚀 Part 1: Setting Up Your Free Supabase Database (2 Minutes)

### Step 1: Create a Free Account
1. Go to [supabase.com](https://supabase.com) and click **Start your project** (Sign in with GitHub).
2. Click **New Project**, name it **`SmartServe`**, choose a secure database password, and select region **Singapore / Mumbai / Central**.
3. Click **Create new project** (takes ~1 minute to spin up).

### Step 2: Run the Database Schema & Seed 80 Dishes
1. On the left sidebar in Supabase, click **SQL Editor** (icon looks like `>_`).
2. Click **New Query**.
3. Open the file [`supabase_schema.sql`](supabase_schema.sql) from your project folder, copy all contents, paste it into the Supabase SQL Editor, and click **Run** (or press `Ctrl + Enter`).
4. You will see: `Success. No rows returned`.
   *(Your cloud database now has both `menu_items` and `orders` tables, with all 80 dishes pre-seeded!)*

### Step 3: Get Your API Credentials
1. In Supabase, go to **Project Settings** (gear icon at bottom-left) ➔ **API**.
2. Copy these two values:
   - **Project URL** (e.g. `https://xyzcompany.supabase.co`)
   - **Project API Keys** ➔ copy the **`anon` `public`** key

---

## ☁️ Part 2: Deploying to Render.com (3 Minutes)

### Step 1: Push Your Project to GitHub
In VS Code terminal (`Ctrl + ~`), run:
```bash
git init
git add .
git commit -m "SmartServe with Supabase and Render setup"
git branch -M main
git remote add origin https://github.com/<YOUR-GITHUB-USERNAME>/SmartServe.git
git push -u origin main
```

### Step 2: Create Web Service on Render
1. Go to [render.com](https://render.com) and sign in with **GitHub**.
2. Click **New +** ➔ **Web Service**.
3. Connect your **`SmartServe`** repository.
4. Settings:
   - **Name**: `smartserve-restaurant`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: `Free`

### Step 3: Add Your Supabase Keys to Render
Under **Environment Variables** in Render, add these 2 variables:
- `SUPABASE_URL` = *(Paste your Project URL from Supabase)*
- `SUPABASE_KEY` = *(Paste your `anon` `public` key from Supabase)*

Click **Deploy Web Service**!

---

## 🌐 Testing on Phones & Laptops
Render will build the app and give you a live link:
👉 **`https://smartserve-restaurant.onrender.com`**

- Send this link to anyone on WhatsApp, open it on your phone, place an order, and watch it show up on the Admin Dashboard on your laptop!

---

## 🔐 Admin Authentication
- **URL**: `https://your-app.onrender.com/admin`
- **Default Password**: `admin123`
- Only the Admin can add new dishes, create new categories, update order statuses, and delete records.
