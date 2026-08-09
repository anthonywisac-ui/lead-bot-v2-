# Country selector for multi-country menu system

COUNTRIES = {
    "PK": {"name": "🇵🇰 Pakistan", "code": "PK", "currency": "PKR"},
    "AE": {"name": "🇦🇪 United Arab Emirates", "code": "AE", "currency": "AED"},
    "SA": {"name": "🇸🇦 Saudi Arabia", "code": "SA", "currency": "SAR"},
    "QA": {"name": "🇶🇦 Qatar", "code": "QA", "currency": "QAR"},
    "KW": {"name": "🇰🇼 Kuwait", "code": "KW", "currency": "KWD"},
    "BH": {"name": "🇧🇭 Bahrain", "code": "BH", "currency": "BHD"},
    "OM": {"name": "🇴🇲 Oman", "code": "OM", "currency": "OMR"},
    "US": {"name": "🇺🇸 United States", "code": "US", "currency": "USD"},
    "GB": {"name": "🇬🇧 United Kingdom", "code": "GB", "currency": "GBP"},
    "CA": {"name": "🇨🇦 Canada", "code": "CA", "currency": "CAD"},
}

COUNTRY_SHORTCODES = {
    "1": "PK",
    "2": "AE",
    "3": "SA",
    "4": "QA",
    "5": "KW",
    "6": "BH",
    "7": "OM",
    "8": "US",
    "9": "GB",
    "10": "CA",
}

def get_country_list_message():
    """Generate message showing all countries with shortcodes"""
    msg = "🌍 Select Your Country:\n\n"
    for code, info in COUNTRY_SHORTCODES.items():
        country_data = COUNTRIES[info]
        msg += f"{code}️⃣ {country_data['name']}\n"
    msg += "\n📌 Reply with number (1-10) to select your country"
    return msg

def get_country_by_shortcode(shortcode):
    """Get country code from shortcode number"""
    return COUNTRY_SHORTCODES.get(shortcode)

def get_country_info(country_code):
    """Get country information"""
    return COUNTRIES.get(country_code, COUNTRIES["PK"])

def validate_country_code(code):
    """Check if country code is valid"""
    return code in COUNTRIES
