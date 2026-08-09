# Smart Detection System
# Auto-detect customer type, name, preferences from first message

import re
from order_manager import get_customer_last_order

# Keywords for detection
RETURNING_KEYWORDS = [
    "hi", "hello", "hey", "salam", "salaam", "assalam", "assalamu alaikum",
    "hola", "namaste", "sup", "whats up", "yo", "oi", "howdy"
]

B2B_KEYWORDS = ["client", "business", "corporate", "bulk", "catering", "wholesale"]
NEW_KEYWORDS = ["new", "first time", "fresh", "start", "begin"]

def extract_name_from_message(message):
    """Extract name from message like 'Hi, I am John' or 'Salam, Ahmed here'"""
    text = message.lower()

    # Patterns: "name is X", "I am X", "it's X", "call me X"
    patterns = [
        r"(?:my name is|name is|i am|im|i\'m|call me|it\'s|its)\s+([a-z]+)",
        r"(?:hi|hello|salam)[\s,]+([a-z]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            name = match.group(1).capitalize()
            return name

    return None

def detect_customer_type(message):
    """Detect customer type from message"""
    text = message.lower().strip()

    # Check for exact keywords first
    if text in ["client"]:
        return "client"
    if text in ["new"]:
        return "new"
    if text in RETURNING_KEYWORDS or any(kw in text for kw in RETURNING_KEYWORDS):
        return "returning"

    # Default: new customer
    return "new"

def detect_location_preference(message):
    """Detect country/location preference from message"""
    text = message.lower()

    country_keywords = {
        "pk": ["pakistan", "lahore", "karachi", "islamabad", "urdu"],
        "ae": ["uae", "dubai", "abu dhabi", "emirates"],
        "sa": ["saudi", "riyadh", "jeddah"],
        "qa": ["qatar", "doha"],
        "us": ["usa", "america", "united states", "english"],
        "gb": ["uk", "london", "britain", "english"],
        "ca": ["canada", "toronto", "vancouver"],
    }

    for country, keywords in country_keywords.items():
        if any(kw in text for kw in keywords):
            return country

    return None

async def smart_greet_customer(sender, name=None, customer_type="new"):
    """Generate personalized greeting based on customer type"""
    from whatsapp_interactive import send_text_message

    if customer_type == "returning" and name:
        greet = f"""👋 Welcome back, {name}!

Great to see you again! 😊

What would you like to do?"""
        return greet

    elif customer_type == "returning":
        greet = f"""👋 Welcome back!

Great to see you again! 😊

What would you like to do?"""
        return greet

    elif customer_type == "client":
        greet = """👔 Welcome, Business Partner!

Let's set up your B2B account.
Please provide your manager/business number:

Format: +923xxxxxxxxx or 03xxxxxxxxx"""
        return greet

    else:  # new
        greet = """👋 Welcome to Wild Bites!

Let's get you started! 🍽️"""
        return greet

def get_greeting_options(customer_type):
    """Get button options for greeting based on customer type"""
    if customer_type == "returning":
        return [
            {"id": "repeat_last_order", "title": "🔁 Last Order"},
            {"id": "new_order", "title": "📝 New Order"},
        ]
    elif customer_type == "client":
        return []  # Will ask for manager number instead
    else:  # new
        return []  # Go straight to menu

async def process_first_message(sender, message, session):
    """
    Smart processing of customer's first message

    Detects:
    - Customer type (new/returning/client)
    - Customer name (if provided)
    - Location preference (if mentioned)
    - Intent (order type)
    """

    # Detect customer type
    customer_type = detect_customer_type(message)

    # Extract name if provided
    name = extract_name_from_message(message)
    if name:
        session["customer_name"] = name

    # Detect location preference
    location = detect_location_preference(message)

    # Check if returning customer (if detected type is returning)
    if customer_type == "returning":
        last_order = get_customer_last_order(sender)
        if last_order:
            session["last_order_info"] = last_order
        else:
            # Not actually returning, just said "hi"
            customer_type = "new"

    # Update session
    session["customer_type"] = customer_type
    session["detected_location"] = location

    # Generate greeting
    greeting = await smart_greet_customer(sender, name, customer_type)

    return {
        "customer_type": customer_type,
        "name": name,
        "location": location,
        "greeting": greeting,
        "options": get_greeting_options(customer_type)
    }
