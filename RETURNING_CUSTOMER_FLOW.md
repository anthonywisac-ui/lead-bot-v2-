# Returning Customer Flow Documentation

## Overview
Wild Bites now tracks returning customers and personalizes their experience within a 10-minute window. After 10 minutes, they're treated as new customers again.

## Customer Journey

### NEW CUSTOMER (First Time or After 10+ Minutes)

```
1️⃣ User sends any greeting (hi, hello, salam, etc.)
   ↓
2️⃣ Smart greeting appears:
   "🎉 Welcome to Wild Bites!"
   📍 {Country} | {Currency}
   
   [Button] 📦 View Catalog
   ↓
3️⃣ Customer taps "View Catalog"
   → Opens native WhatsApp catalog (PRIMARY)
   → Falls back to button-based menu (BACKUP)
   ↓
4️⃣ Customer selects items and quantity
   ↓
5️⃣ Delivery method selection:
   [🏠 Delivery] [🚗 Pickup] [🍽️ Dine-in]
   ↓
6️⃣ Depending on delivery type:
   - Home: Ask for address
   - Pickup: Proceed to order
   - Dine-in: Ask for table number
   ↓
7️⃣ Before confirmation:
   "👤 What's your name? (So we can greet you next time 😊)"
   → User enters name
   → Name saved to customer profile
   ↓
8️⃣ Order confirmation sent with AI summary
   → Customer receives order ID + summary
   → Manager receives structured alert
   ↓
9️⃣ Profile created/updated:
   - Name saved
   - Country code saved
   - First seen timestamp
   - Last order stored
   - Order count incremented
```

### RETURNING CUSTOMER (Within 10 Minutes)

```
1️⃣ Same customer sends any greeting within 10 minutes
   ↓
2️⃣ Smart greeting with personalization:
   "👋 Welcome back, {Name}!"
   📍 {Country} | {Currency}
   
   Shows last order:
   "🔄 Your Last Order:
   • item1
   • item2
   💰 Total: Rs 500"
   
   Quick options:
   [🔄 Repeat Order] [📦 New Order]
   ↓
3️⃣ Two paths:
   
   PATH A: Repeat Order
   - Last order restored to cart
   - Jump to delivery method selection
   - Name already known, skip name prompt
   - Fast checkout in 3 steps
   
   PATH B: New Order
   - Normal flow starts
   - Browse catalog again
   - Ask for name again (might update it)
   - Full flow as above
```

## Customer Profile Storage

### File: `customer_profiles.json`

```json
{
  "923001234567": {
    "name": "Ahmed",
    "country_code": "PK",
    "first_seen": 1691234567.89,
    "last_seen": 1691234589.12,
    "order_count": 5,
    "last_order_id": "WILD234567_ABC12345",
    "last_order_items": ["2x Chicken Biryani", "1x Raita"],
    "last_order_total": 1650.0,
    "last_order_time": 1691234589.12
  }
}
```

## Key Functions in `customer_profile.py`

### Core Operations

```python
# Get customer profile by phone
profile = get_customer_profile(phone)

# Save or update customer
save_customer_profile(phone, name, country_code)

# Check if returning (within 10 minutes)
is_returning, profile = is_returning_customer(phone, within_minutes=10)

# Update after order placed
update_customer_last_order(phone, order_id, items_list, total)

# Get saved name
name = get_customer_name(phone)

# Format last order for display
message = format_last_order(profile)
```

## Integration Points

### 1. Smart Greeting (On First Message)
**File**: `whatsapp_native_catalog_handler.py`
- **Function**: `smart_greeting(sender, country_code, session)`
- **Logic**: 
  - Check if returning customer
  - Show personalized greeting
  - Display repeat order option if available
  - Show "View Catalog" button

### 2. Order Flow (At Checkout)
**File**: `flow_smart.py`
- **Stage**: `ask_customer_name`
- **Logic**: Ask for name before order confirmation
- Save name to session → passed to `create_and_send_order()`

### 3. Order Confirmation (After Order Placed)
**File**: `complete_order_flow.py`
- **Function**: `create_and_send_order()`
- **Logic**:
  - After order created
  - Save customer profile with name
  - Update last order info

## Time Windows

### 10-Minute Window
- Session persists for 10 minutes
- If customer returns within window: **RETURNING FLOW**
- After 10 minutes: **NEW CUSTOMER FLOW**
- Window resets on each new message

```
T=0:00   Customer 1st message  → New flow
T=5:00   Customer 2nd message  → Still returning (5 min elapsed)
T=8:00   Customer places order → Returning flow
T=8:05   Customer sends msg    → Returning (within 10 min of LAST activity)
T=18:10  Customer sends msg    → NEW FLOW (10+ min since T=8:05)
```

## Backup Flow (When Catalog Unavailable)

If native WhatsApp catalog fails:

```
1. Show "View Catalog" button
2. User can tap alternative button-based menu
3. Button-based flow:
   - Show categories as list
   - Select items with quantities
   - Continue with delivery flow
4. All other steps remain same
```

## Testing Checklist

- [ ] New customer gets smart greeting with catalog button
- [ ] First message extracts name if provided (e.g., "Hi, I'm Ahmed")
- [ ] View Catalog button works (opens catalog or fallback)
- [ ] Order flow completes with name prompt
- [ ] Customer profile saved to `customer_profiles.json`
- [ ] Returning customer within 10 min shows name greeting
- [ ] Last order displays correctly (max 3 items + count)
- [ ] Repeat last order restores cart correctly
- [ ] After 10 minutes, customer is new again
- [ ] Different countries show correct currency in greeting
- [ ] Profile update on each order (order_count, last_order_time)

## Multi-Country Support

Each country shows correct info in greeting:

```
PK → "🎉 Welcome to Wild Bites!\n📍 Pakistan | Rs"
AE → "🎉 Welcome to Wild Bites!\n📍 United Arab Emirates | AED"
US → "🎉 Welcome to Wild Bites!\n📍 United States | $"
GB → "🎉 Welcome to Wild Bites!\n📍 United Kingdom | £"
```

## Known Behaviors

✅ **Names extracted from first message**
- "Hi, I'm Ahmed" → Name: Ahmed
- "Salam, Ahmed here" → Name: Ahmed
- "Hello" → Name: Not extracted (asked later)

✅ **Profile persistence**
- Survives session resets
- Survives server restarts
- Survives app crashes

✅ **Returning customer detection**
- Based on phone number
- 10-minute window
- Per-customer, not per-session

❌ **Limitations**
- Max 3 items shown in repeat order (saves space)
- Name must be entered during checkout (can't skip)
- Order history limited to last order (could expand to 5 last orders)

## Future Enhancements

1. **Loyalty Program**
   - Track order count
   - Unlock discounts at 5th, 10th order

2. **Order History**
   - Show last 5 orders
   - Quick repeat from history

3. **Personalization**
   - Remember favorite items
   - Suggest based on history

4. **Analytics**
   - Most frequent returning customers
   - Average repeat rate
   - Revenue per customer

5. **Smart Offers**
   - "Ahmed usually orders Biryani + Raita"
   - Suggest complimentary items

## Related Files

- `customer_profile.py` - Core profile management
- `whatsapp_native_catalog_handler.py` - Greeting + catalog
- `flow_smart.py` - Main flow orchestration
- `complete_order_flow.py` - Order confirmation + saving
- `customer_profiles.json` - Persistent storage
