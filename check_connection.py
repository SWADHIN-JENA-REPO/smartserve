"""
SmartServe - Database & Supabase Connection Checker
Run this anytime by typing:
    python check_connection.py
"""

import sys
import database

print("=" * 60)
print("   SMARTSERVE - DATABASE CONNECTION DIAGNOSTIC")
print("=" * 60)

print(f"\n1. Configured Supabase URL: {database.SUPABASE_URL}")
print(f"2. Configured Supabase Key: {database.SUPABASE_KEY[:10]}...{database.SUPABASE_KEY[-6:] if len(database.SUPABASE_KEY) > 16 else ''}")

# Check Supabase client initialization
if database.is_supabase_active():
    print("\n[OK] Supabase client initialized.")
    try:
        # Test reading menu_items from Supabase
        res = database.supabase.table("menu_items").select("*").limit(5).execute()
        count = len(res.data) if res.data else 0
        print(f"[OK] Connection to Supabase Cloud verified! (Read sample {count} items)")

        # Test total dishes in Supabase
        all_res = database.supabase.table("menu_items").select("id", count="exact").execute()
        total_in_cloud = all_res.count if hasattr(all_res, 'count') and all_res.count is not None else len(all_res.data)
        print(f"[INFO] Dishes currently in Supabase Cloud: {total_in_cloud}")

        if total_in_cloud == 0:
            print("\n> NOTE: Your Supabase cloud database is connected, but empty!")
            print("> To seed all 80 dishes and enable orders:")
            print("  1. Open your Supabase project in browser (supabase.com)")
            print("  2. Go to SQL Editor -> New Query")
            print("  3. Copy and run the contents of 'supabase_schema.sql'")
        else:
            print("\n[SUCCESS] Supabase Cloud Database is FULLY OPERATIONAL and SEEDED!")

    except Exception as e:
        print(f"\n[WARNING] Supabase query returned an error: {e}")
        if "row-level security" in str(e).lower():
            print("\n> FIX REQUIRED IN SUPABASE:")
            print("> Row Level Security (RLS) is currently blocking inserts.")
            print("> In your Supabase SQL Editor, run:")
            print("     ALTER TABLE menu_items DISABLE ROW LEVEL SECURITY;")
            print("     ALTER TABLE orders DISABLE ROW LEVEL SECURITY;")
else:
    print("\n[NOTICE] Supabase is NOT active. Running in local SQLite mode (restaurant.db).")

# Check Local SQLite Fallback
try:
    local_items = database.get_menu_items()
    print(f"\n[OK] Local SQLite fallback: {len(local_items)} dishes ready.")
except Exception as e:
    print(f"\n[ERROR] Local SQLite error: {e}")

print("\n" + "=" * 60)
