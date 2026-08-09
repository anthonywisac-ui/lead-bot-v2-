# ========================================
# Customer Profile Management
# ========================================
# Save customer names, track returning customers, show shortcuts

import json
import os
import time
from typing import Dict, Optional, Tuple
from menus_multi import get_country_from_phone

CUSTOMER_DB_PATH = "customer_profiles.json"

# ========================================
# CUSTOMER DATABASE
# ========================================

def load_customer_db() -> Dict:
    """Load customer database from JSON file"""
    if os.path.exists(CUSTOMER_DB_PATH):
        try:
            with open(CUSTOMER_DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_customer_db(db: Dict):
    """Save customer database to JSON file"""
    try:
        with open(CUSTOMER_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"❌ Error saving customer DB: {e}")


def get_customer_profile(phone: str) -> Optional[Dict]:
    """Get customer profile by phone number"""
    db = load_customer_db()
    return db.get(phone)


def save_customer_profile(phone: str, name: str, country_code: str):
    """Save customer profile with name"""
    db = load_customer_db()

    if phone not in db:
        db[phone] = {
            "name": name,
            "country_code": country_code,
            "first_seen": time.time(),
            "last_seen": time.time(),
            "order_count": 0,
            "orders": []
        }
    else:
        db[phone]["last_seen"] = time.time()
        if name:
            db[phone]["name"] = name

    save_customer_db(db)


def update_customer_last_order(phone: str, order_id: str, items: list, total: float):
    """Update customer's last order"""
    db = load_customer_db()

    if phone in db:
        db[phone]["last_order_id"] = order_id
        db[phone]["last_order_items"] = items
        db[phone]["last_order_total"] = total
        db[phone]["last_order_time"] = time.time()
        db[phone]["order_count"] = db[phone].get("order_count", 0) + 1
        db[phone]["last_seen"] = time.time()

    save_customer_db(db)


# ========================================
# RETURNING CUSTOMER DETECTION
# ========================================

def is_returning_customer(phone: str, within_minutes: int = 10) -> Tuple[bool, Optional[Dict]]:
    """
    Check if customer is returning within time window.

    Returns:
        (is_returning, customer_profile)
    """
    profile = get_customer_profile(phone)

    if not profile:
        return False, None

    # Check if they've been seen before
    if "first_seen" not in profile:
        return False, None

    # If they visited within time window, they're returning
    last_seen = profile.get("last_seen", 0)
    current_time = time.time()
    time_diff_minutes = (current_time - last_seen) / 60

    if time_diff_minutes < within_minutes:
        return True, profile
    else:
        return False, profile


def get_customer_name(phone: str) -> Optional[str]:
    """Get customer name by phone"""
    profile = get_customer_profile(phone)
    return profile.get("name") if profile else None


def format_last_order(profile: Dict) -> Optional[str]:
    """Format last order for display"""
    if "last_order_items" not in profile:
        return None

    items = profile.get("last_order_items", [])
    total = profile.get("last_order_total", 0)

    msg = "🔄 **Your Last Order:**\n\n"
    for item in items[:3]:  # Show max 3 items
        msg += f"• {item}\n"

    if len(items) > 3:
        msg += f"• +{len(items) - 3} more items\n"

    msg += f"\n💰 Total: Rs {total:.0f}"

    return msg
