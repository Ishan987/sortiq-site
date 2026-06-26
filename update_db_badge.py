import sqlite3
import json

db_path = 'C:/Users/ASUS/Desktop/sortiq_clone/sortiq.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get current site_layout value
cursor.execute("SELECT value FROM site_settings WHERE key = 'site_layout'")
row = cursor.fetchone()
if row:
    layout = json.loads(row[0])
    # Find the ISO 9001 badge and update its image path to png
    updated = False
    for badge in layout.get('footer_badges', []):
        if badge.get('label') == 'ISO 9001' or 'iso-certified.webp' in badge.get('image', ''):
            badge['image'] = '/static/images/iso-certified.png'
            updated = True
            print("Updated badge image to png in site_layout object")
            
    if updated:
        cursor.execute("UPDATE site_settings SET value = ? WHERE key = 'site_layout'", (json.dumps(layout),))
        conn.commit()
        print("Successfully updated database!")
    else:
        print("ISO 9001 badge not found or already updated.")
else:
    print("site_layout settings row not found.")

conn.close()
