# Multi-country flow with country detection and Gemini AI
import asyncio
from menus_multi import get_country_from_phone, get_menu, get_currency_symbol, get_category_list
from country_selector import get_country_list_message, get_country_by_shortcode, COUNTRIES
from gemini_ai import get_ai_response
from whatsapp_handlers import send_text_message, send_main_menu
from db import customer_sessions, customer_profiles

async def handle_initial_greeting(sender, text):
    """Handle initial greeting and country detection"""

    # Try to detect country from phone
    detected_country = get_country_from_phone(sender)

    # Check if user said "owner" keyword
    if text.lower() in ["owner", "countries", "select country"]:
        # Show country selection list
        country_list = get_country_list_message()
        await send_text_message(sender, country_list)
        return

    # Check if user is selecting country by shortcode (1-10)
    if text.strip().isdigit():
        country_code = get_country_by_shortcode(text.strip())
        if country_code:
            # Save country selection to session
            session = customer_sessions.get(sender, {})
            session["country_code"] = country_code
            session["detected_from"] = "user_selection"
            customer_sessions[sender] = session

            country_info = COUNTRIES.get(country_code)
            msg = f"✅ Selected: {country_info['name']}\n\n"
            msg += "🍽️ Welcome to Wild Bites!\n\n"
            msg += "What would you like to order today?"

            await send_text_message(sender, msg)
            # Show main menu for selected country
            await show_main_menu(sender, country_code)
            return

    # Use detected country if not specified
    if sender not in customer_sessions:
        customer_sessions[sender] = {}

    session = customer_sessions[sender]
    session["country_code"] = detected_country
    session["detected_from"] = "phone_number"

    country_info = COUNTRIES.get(detected_country)

    # Send welcome message
    welcome = f"👋 Welcome to Wild Bites!\n\n"
    welcome += f"📍 Detected Location: {country_info['name']}\n\n"
    welcome += "🍽️ What would you like to order?\n\n"
    welcome += "Type 'owner' or 'countries' to change your location."

    await send_text_message(sender, welcome)
    await show_main_menu(sender, detected_country)

async def show_main_menu(sender, country_code):
    """Show main menu for a country"""
    menu = get_menu(country_code)
    categories = get_category_list(country_code)

    msg = "🛍️ SELECT A CATEGORY:\n\n"
    for i, (key, name) in enumerate(categories, 1):
        msg += f"{i}️⃣ {name}\n"

    msg += "\n📌 Tap or reply with number"
    await send_text_message(sender, msg)

async def handle_flow_multi(sender, text, is_button=False):
    """Main flow handler for multi-country system"""

    # Get or create session
    if sender not in customer_sessions:
        customer_sessions[sender] = {}

    session = customer_sessions[sender]
    stage = session.get("stage", "greeting")
    country_code = session.get("country_code", "PK")

    # Stage 1: Initial greeting
    if stage == "greeting" or "country_code" not in session:
        await handle_initial_greeting(sender, text)
        session["stage"] = "menu_browse"
        customer_sessions[sender] = session
        return

    # Stage 2: Menu browsing with AI chat enabled
    if stage == "menu_browse":
        # Use Gemini AI to understand user intent
        menu = get_menu(country_code)
        menu_summary = "\n".join([f"- {cat['name']}" for cat in menu['categories'].values()])

        ai_response = await get_ai_response(
            sender,
            text,
            restaurant="Wild Bites Restaurant",
            lang=session.get("lang", "en"),
            menu=menu_summary
        )

        if ai_response.get("success"):
            await send_text_message(sender, ai_response["message"])
        else:
            # Fallback to regular menu
            await show_main_menu(sender, country_code)

        return

    # Keep existing flow logic for other stages
    # This integrates with the original flow.py logic
    print(f"[Multi-Country] {sender} | Country: {country_code} | Text: {text}")
