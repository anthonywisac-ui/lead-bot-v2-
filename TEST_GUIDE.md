# 🧪 WhatsApp Bot Automated Testing Guide

## 📋 Overview

Two test scripts to validate all features of the Wild Bites WhatsApp bot:

| Script | Purpose | Type |
|--------|---------|------|
| `test_e2e_flows.py` | Show all features that should be tested | 📝 Documentation |
| `automated_tester.py` | **ACTUAL automated testing** (sends real messages) | 🚀 Live Testing |

---

## 🚀 **AUTOMATED TESTER** (RECOMMENDED)

### Setup

```bash
# Install dependencies
pip install aiohttp python-dotenv

# Update .env with WhatsApp credentials
echo "WHATSAPP_TOKEN=your_token_here" >> .env
echo "WHATSAPP_PHONE_ID=your_phone_id_here" >> .env
```

### Run Tests

```bash
python automated_tester.py
```

### What It Tests

✅ **14 Comprehensive Tests:**

1. **New Customer Detection**
   - Send: "New"
   - Expected: Welcome greeting + category menu

2. **Category Browsing**
   - Select: "Deals"
   - Expected: deals-image.png (clean) + items list

3. **Item Selection & Quantity**
   - Select item: DL2
   - Set quantity: 3x
   - Expected: Cart updated

4. **Upsell Suggestions**
   - Add Biryani
   - Expected: Upsell buttons (Raita, Lassi, Pickle)

5. **Home Delivery**
   - Checkout → Home Delivery
   - Provide address
   - Expected: ✅ AUTO-APPROVED instantly

6. **Pickup Order**
   - Checkout → Pickup
   - Expected: ✅ AUTO-APPROVED instantly

7. **Dine-in Order**
   - Checkout → Dine-in
   - Provide table number
   - Expected: ⏳ Waits for manager approval
   - Then: Manager approves → Customer gets ✅ approval

8. **B2B Client Account**
   - Send: "Client"
   - Provide manager number
   - Expected: Orders go to custom manager

9. **Returning Customer**
   - Send: "Hi Ahmed"
   - Expected: "Welcome back, Ahmed!" + Last Order button

10. **Order Status**
    - Send: "Where is my order"
    - Expected: Current order status

11. **Country Selection**
    - Send: "owner"
    - Select country (1-10)
    - Expected: Currency changes, new menu

12. **Multi-language Support**
    - Salam, Assalam, Hola, order kahan hai
    - Expected: All understood

13. **Cart Operations**
    - Add multiple items
    - Clear cart
    - Expected: Proper cart management

14. **Image Verification**
    - Check GitHub URLs
    - Expected: All images HTTPS, from GitHub raw

---

## 📊 Test Output Example

```
======================================================================
  WILD BITES WHATSAPP BOT - AUTOMATED E2E TESTER
======================================================================

Configuration:
  Test Phone: 923351021321
  WhatsApp API: https://graph.instagram.com/v18.0/...
  Start Time: 2026-08-09 15:20:45

TEST 1: New Customer Smart Detection
✓ Sent (New Customer): New...

TEST 2: Category Browsing with Images
→ Button (Select Deals): cat_deals
✓ Image displayed: deals-image.png

...

======================================================================
  TEST RESULTS SUMMARY
======================================================================

✅ PASS - New Customer Detection
✅ PASS - Category Browsing
✅ PASS - Item Selection & Quantity
✅ PASS - Upsell Suggestions
✅ PASS - Delivery Flow Auto-Approval
✅ PASS - Pickup Flow Auto-Approval
✅ PASS - Dine-in Manager Approval
✅ PASS - B2B Client Setup
✅ PASS - Returning Customer Detection
✅ PASS - Order Status Check
✅ PASS - Country Selection
✅ PASS - Multi-language Support
✅ PASS - Cart Operations
✅ PASS - Image URL Verification

Statistics:
  Total Tests: 14
  Passed: 14
  Failed: 0
  Messages Sent: 28
  Pass Rate: 100.0%

🎉 ALL TESTS PASSED! BOT IS WORKING PERFECTLY!

  End Time: 2026-08-09 15:21:30
```

---

## 🔍 **DOCUMENTATION TEST SCRIPT**

Run this to see ALL features that should be tested:

```bash
python test_e2e_flows.py
```

This shows:
- 15 comprehensive test scenarios
- Step-by-step breakdown
- Expected results for each step
- Great for manual testing verification

---

## 📝 Manual Testing Checklist

If you want to test manually, here's the flow:

```
1. Send "New" → Bot greets + shows menu
2. Select "Deals" → Image appears + items shown
3. Select item → Add to cart, show upsell
4. Click upsell → Add to cart
5. Checkout → Choose Delivery/Pickup/Dine-in
6. Delivery: Enter address → Auto-approve
7. Pickup: Select pickup → Auto-approve
8. Dine-in: Enter table → Wait for manager approval
9. Manager approves → Customer gets confirmation
10. Send "Where is my order" → Status appears
11. Send "owner" → Change country
12. Send "Client" → B2B setup
13. Send "Hi Ahmed" → Personalized greeting
```

---

## 🐛 Debugging

### If tests fail:

```bash
# 1. Check credentials
echo $WHATSAPP_TOKEN
echo $WHATSAPP_PHONE_ID

# 2. Check bot is running
curl http://localhost:8000/health

# 3. Check logs
tail -f Railway_logs.txt

# 4. Verify phone number
# Use real WhatsApp number for testing, not fake numbers
```

---

## ✅ What Gets Tested

| Feature | Status |
|---------|--------|
| Smart detection (new/returning/client) | ✅ |
| Welcome image display | ✅ |
| Category images | ✅ |
| Menu browsing | ✅ |
| Item selection | ✅ |
| Quantity selection (2x-6x + custom) | ✅ |
| Upsell suggestions | ✅ |
| Smart suggestions by item type | ✅ |
| Cart management (add/clear) | ✅ |
| Delivery auto-approval | ✅ |
| Pickup auto-approval | ✅ |
| Dine-in manager approval | ✅ |
| Manager rejection with phone | ✅ |
| B2B client custom manager | ✅ |
| Returning customer detection | ✅ |
| Name extraction | ✅ |
| Order status checking | ✅ |
| Country selection (1-10) | ✅ |
| Multi-language support | ✅ |
| Image URLs (GitHub raw) | ✅ |
| Minimum order validation | ✅ |
| Delivery charge calculation | ✅ |
| All 10 countries | ✅ |

---

## 🎯 Next Steps

1. **Run automated tester**: `python automated_tester.py`
2. **Check test results**: Look for "✅ PASS" on all tests
3. **If any fail**: Check logs and debug
4. **Once 100% pass**: Bot is production ready!

---

## 📞 Support

If tests fail:
- Check `.env` file has correct WhatsApp credentials
- Verify bot is running: `http://localhost:8000/health`
- Check Railway logs for errors
- Test with a real WhatsApp number (not fake)

---

**Happy Testing! 🎉**
