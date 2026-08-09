# 🤖 Gemini AI + WhatsApp Catalog Integration Guide

## What This Does

When customers browse your catalog on WhatsApp and send questions, Gemini AI **analyzes their request** and **suggests the perfect items** automatically!

### Examples:

```
Customer: "Kaunsi cheez sust hai?"
Gemini: "Mehnge wali items dekh rahe ho! Yeh sab sust hain:
  1. 🍞 Tandoori Roti - PKR 70 (Healthiest & cheapest!)
  2. 🍟 Masala Fries - PKR 350 (Crispy & filling)
  3. 🍜 Egg Fried Rice - PKR 550 (Best value meal)"

---

Customer: "Ek family ke liye?"
Gemini: "2-4 log ke liye yeh deals perfect hain:
  1. 👨‍👩‍👧‍👦 Family Biryani Deal - PKR 2999 (2 portions!)
  2. 👥 2 Person Karahi Deal - PKR 2499 (Complete meal)"

---

Customer: "Vegetarian options?"
Gemini: "Yeh sab veg hain:
  1. 🍛 Daal Makhani - PKR 650
  2. 🥔 Masala Fries - PKR 350
  3. 🌾 Chana Masala - PKR 550"
```

---

## How It Works

### Flow:

```
1️⃣ Customer browses catalog on WhatsApp
2️⃣ Customer sends message: "vegetarian options?"
3️⃣ Bot detects it's a catalog question
4️⃣ Gemini analyzes: "They want veg items"
5️⃣ Bot extracts relevant items from menu
6️⃣ Gemini suggests top 3-5 matches
7️⃣ Customer taps "Add" buttons to add to cart
8️⃣ Checkout!
```

---

## Integration Points

### 1. **Main Message Handler** (in main.py or your webhook)

```python
from catalog_gemini_integration import handle_catalog_message

# In your message processing:
async def process_message(sender, message, country_code, session):
    
    # If browsing catalog, try Gemini analysis
    if session.get("stage") == "catalog_browsing":
        handled = await handle_catalog_message(
            sender, 
            message, 
            country_code, 
            session
        )
        if handled:
            return  # Gemini handled the request
    
    # Fall back to regular flow
    await handle_regular_message(sender, message, country_code, session)
```

### 2. **After Customer Adds to Cart** (Smart Upsell)

```python
from catalog_gemini_integration import suggest_based_on_cart

# When items added to cart:
await suggest_based_on_cart(
    sender,
    session.get("cart"),
    country_code,
    session
)
```

---

## Features

### ✨ **Smart Suggestions**
- "Kaunsi cheap hai?" → Cheapest items
- "Spicy?" → Spicy dishes
- "Vegetarian?" → Veg-only items
- "Kids ke liye?" → Family deals
- "Quick order?" → Fast items

### 🎯 **Personalized**
- Based on customer's actual question
- Real-time menu scanning
- Prices in their country's currency

### 🛒 **Cart Integration**
- When they add biryani → Suggest raita + lassi + pickle
- When they add burger → Suggest fries + drink + sauce
- Auto-upsell complementary items

### 💬 **Natural Language**
- Understands Urdu, English, mixed language
- Casual conversational style
- Helpful tone

---

## Setup

### 1. **Copy Files**
```bash
cp catalog_gemini_integration.py /your/bot/dir/
```

### 2. **Update Imports** (in main.py or webhook handler)
```python
from catalog_gemini_integration import (
    handle_catalog_message,
    suggest_based_on_cart
)
```

### 3. **Add to Message Flow**
See "Integration Points" section above.

### 4. **Test**
Send message while browsing catalog:
- "sust option?"
- "veg kya hai?"
- "kids menu?"
- "best deal?"

---

## Prompts Gemini Uses

### Query Analysis
```
Customer is browsing catalog. They asked: "{message}"
Based on our menu, suggest 3-5 BEST items.
Return JSON: {"understanding": "...", "suggestions": [...]}
```

### Cart Upsell
```
Customer ordered: {items}
Suggest 2-3 complementary sides/drinks/desserts.
Keep it brief and appetizing.
```

---

## Customization

### Change Suggestion Count
In `catalog_gemini_integration.py`:
```python
for item_data in suggestions['suggestions'][:5]:  # Change 5 to your number
```

### Add More Keywords
In `handle_catalog_message()`:
```python
catalog_keywords = [
    "kaunsi", "which", "best", "cheapest",
    # Add more here
]
```

### Adjust Catalog Context Size
In `_build_catalog_summary()`:
```python
for item_id, item in list(items.items())[:20]:  # Increase from 15 to 20
```

---

## Performance Notes

- ✅ **Fast**: Gemini responds in 1-3 seconds
- ✅ **Smart**: Understands context and preferences
- ✅ **Reliable**: Falls back gracefully if API fails
- ✅ **Cost**: Only called when customer asks questions (not for every message)

---

## Example Conversation

```
Customer: Hi! 👋
Bot: Assalaam! 🍲 Welcome to Wild Bites!
     Browse menu: 📦 Catalog

Customer: [Opens catalog, browses items]

Customer: Vegetarian options kya hain?
Gemini: ✨ Vegetarian items perfect for you:
        1. 🍛 Daal Makhani - PKR 650 (Creamy & delicious)
        2. 🌾 Chana Masala - PKR 550 (Light & healthy)
        3. 🍟 Masala Fries - PKR 350 (Quick snack)
        
        Want to add any? Tap the item!

Customer: [Adds Daal Makhani]
Bot: ✅ Added 1x Daal Makhani
     
Gemini: Perfect choice! 💡 Goes great with:
        - 🍞 Garlic Naan - PKR 180
        - 🥛 Sweet Lassi - PKR 250
        
        Add any? 📦 Browse more

Customer: [Adds Garlic Naan, checks out]
Bot: 🎉 Order confirmed!
```

---

## Troubleshooting

### Gemini not responding?
- Check GEMINI_API_KEY is set
- Check internet connection
- Bot will fall back gracefully

### Suggestions not relevant?
- Improve catalog descriptions
- Add more keywords for items
- Train Gemini with more examples

### Too slow?
- Reduce catalog context size
- Cache menu data
- Use shorter prompts

---

## Next Steps

1. ✅ Catalog setup (DONE!)
2. ✅ Product sets created (DONE!)
3. 🔄 **Integrate Gemini** (THIS STEP)
4. Test with real customers
5. Refine based on feedback

---

## Questions?

This integration makes your bot **feel like a real person** who knows the menu!

Customers will love the smart suggestions. 🚀
