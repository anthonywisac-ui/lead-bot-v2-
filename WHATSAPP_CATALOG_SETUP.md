# 🛍️ WhatsApp Native Catalog Setup Guide

## ✅ Complete Flow: Native Catalog → Order Creation

Your bot now supports the **FULL NATIVE WHATSAPP CATALOG FLOW**:

```
Customer                          WhatsApp Catalog              Your Bot              Manager
    |
    | Say "Hi"
    |------->
                                                        Show greeting + catalog icon
                                                        <----------|
    |
    | Tap catalog icon
    |------->
                    [Beautiful native catalog opens]
                    - 47 items in 10 categories
                    - Images, prices, descriptions
                    - Add to cart, set quantities
                    <----------|
    |
    | Select items + tap "Checkout"
    |------->
                    [WhatsApp sends "order" message with items]
                                                        Bot receives order:
                                                        {
                                                          "type": "order",
                                                          "order": {
                                                            "product_items": [
                                                              {
                                                                "product_retailer_id": "BR1",
                                                                "quantity": 2
                                                              },
                                                              {
                                                                "product_retailer_id": "KR1",
                                                                "quantity": 1
                                                              }
                                                            ]
                                                          }
                                                        }
                                                        
                                                        Bot populates cart
                                                        Shows summary
                                                        Asks delivery method
                                                        <----------|
    |
    | Select "🏠 Delivery"
    |------->
                                                        Bot asks for address
                                                        <----------|
    |
    | Type address
    |------->
                                                        Bot shows order summary
                                                        Creates order
                                                        <----------|                    🔔 NEW ORDER
                                                                                        
                                                                                        Items:
                                                                                        - 2x BR1
                                                                                        - 1x KR1
                                                                                        
                                                                                        Total + Address
                                                                                        ←---------|
    |
    | Receive confirmation
    |------->
                                                        ✅ Order confirmed!
                                                        <----------|
```

---

## 📦 Meta Catalog Setup (CRITICAL)

Your **product_retailer_id** in the catalog CSV MUST match the item_ids in your menu system:

### Item IDs by Category

| Category | Item IDs |
|----------|----------|
| Deals | DL1, DL2, DL3, DL4, DL5, DL6 |
| Biryani | BR1, BR2, BR3, BR4, BR5, BR6 |
| Karahi | KR1, KR2, KR3, KR4, KR5, KR6, KR7 |
| BBQ | BB1, BB2, BB3, BB4, BB5, BB6, BB7 |
| Rolls | RL1, RL2, RL3, RL4, RL5, RL6, RL7 |
| Chinese | CH1, CH2, CH3, CH4, CH5, CH6, CH7, CH8 |
| Bread | BD1, BD2, BD3, BD4, BD5, BD6 |
| Sides | SD1, SD2, SD3, SD4, SD5, SD6, SD7 |
| Drinks | DR1, DR2, DR3, DR4, DR5, DR6, DR7 |
| Desserts | DS1, DS2, DS3, DS4, DS5 |

### Example Catalog CSV Row

```csv
id,title,description,availability,condition,price,link,image_link,brand,product_category
BR1,Chicken Biryani,"Aromatic basmati rice with spiced chicken, cooked to perfection",in stock,new,650,https://wild-bites.com/br1,https://example.com/br1.jpg,Wild Bites,🍚 Biryani & Rice
```

**IMPORTANT**: The `id` column must match your item_ids exactly (BR1, KR1, DL1, etc.)

---

## 🔧 How It Works in Code

### Step 1: Customer Sees Catalog
When user says "Hi", they see a message with the catalog icon:

```
🎉 Welcome to Wild Bites!

📍 Pakistan | PKR

Select a category to browse items:
```

WhatsApp automatically shows the catalog button because it's linked to your business number.

### Step 2: Customer Selects Items
Customer:
1. Taps catalog icon
2. Sees all 47 items with images, descriptions, prices
3. Selects items and sets quantities
4. Taps "Checkout"

### Step 3: WhatsApp Sends Order Message
WhatsApp sends to your bot:

```python
{
  "type": "order",  # ← Key identifier
  "order": {
    "catalog_id": "12345",
    "product_items": [
      {
        "product_retailer_id": "BR1",  # ← Item ID
        "quantity": 2,
        "item_price": 650,
        "currency": "PKR"
      },
      {
        "product_retailer_id": "KR1",
        "quantity": 1,
        "item_price": 1400,
        "currency": "PKR"
      }
    ]
  }
}
```

### Step 4: Bot Processes Order
Your `main.py` webhook now:

```python
# Detect order message
if msg_type == "order":
    order_data = message.get("order", {})
    product_items = order_data.get("product_items", [])
    
    # Extract each selected item
    for item in product_items:
        sku = item.get("product_retailer_id")  # BR1, KR1, etc.
        qty = item.get("quantity")  # 2, 1, etc.
        
        # Add to cart
        session["cart"][sku] = qty
    
    # Show cart summary
    await show_cart_summary(sender, country_code, session)
    
    # Ask delivery method
    await ask_delivery_method_complete(sender)
```

### Step 5: Continue with Delivery
Bot asks:
```
How would you like to receive your order?

🏠 Delivery    🚗 Pickup    🍽️ Dine-in
```

Rest of flow continues as normal.

---

## 📋 Complete Item List

### Pakistan Menu (PKR)

**Deals (DL)**
- DL1: Chicken Biryani Combo - 850 PKR
- DL2: Chicken Karahi Combo - 1650 PKR
- DL3: BBQ Platter Deal - 2250 PKR
- DL4: Family Biryani Deal - 2999 PKR
- DL5: 2 Person Karahi Deal - 2499 PKR
- DL6: Burger & Fries Combo - 750 PKR

**Biryani (BR)**
- BR1: Chicken Biryani - 650 PKR
- BR2: Beef Biryani - 750 PKR
- BR3: Mutton Biryani - 950 PKR
- BR4: Chicken Pulao - 600 PKR
- BR5: Chicken Fried Rice - 650 PKR
- BR6: Plain Rice - 300 PKR

**Karahi (KR)**
- KR1: Chicken Karahi - 1400 PKR
- KR2: Mutton Karahi - 2100 PKR
- KR3: Beef Nihari - 950 PKR
- KR4: Chicken Handi - 1450 PKR
- KR5: Butter Chicken - 1300 PKR
- KR6: Daal Makhani - 650 PKR
- KR7: Chana Masala - 550 PKR

**BBQ (BB)**
- BB1: Chicken Tikka - 650 PKR
- BB2: Chicken Seekh Kebab - 700 PKR
- BB3: Beef Seekh Kebab - 750 PKR
- BB4: Chicken Boti - 750 PKR
- BB5: Malai Boti - 850 PKR
- BB6: Chicken Tandoori - 750 PKR
- BB7: Mixed Grill Platter - 1650 PKR

**Rolls (RL)**
- RL1: Chicken Paratha Roll - 450 PKR
- RL2: Beef Paratha Roll - 500 PKR
- RL3: Chicken Cheese Roll - 500 PKR
- RL4: Zinger Roll - 500 PKR
- RL5: Malai Boti Roll - 550 PKR
- RL6: BBQ Chicken Roll - 500 PKR
- RL7: Mayo Garlic Roll - 400 PKR

**Chinese (CH)**
- CH1: Chicken Chow Mein - 750 PKR
- CH2: Chicken Manchurian - 850 PKR
- CH3: Chicken Chili - 850 PKR
- CH4: Chicken Shashlik - 900 PKR
- CH5: Chicken Fried Rice - 650 PKR
- CH6: Egg Fried Rice - 550 PKR
- CH7: Vegetable Chow Mein - 600 PKR
- CH8: Chicken Schezwan Rice - 800 PKR

**Bread (BD)**
- BD1: Plain Naan - 100 PKR
- BD2: Garlic Naan - 180 PKR
- BD3: Butter Naan - 180 PKR
- BD4: Cheese Naan - 350 PKR
- BD5: Roghni Naan - 200 PKR
- BD6: Tandoori Roti - 70 PKR

**Sides (SD)**
- SD1: Samosa - 100 PKR
- SD2: Chicken Samosa - 150 PKR
- SD3: Pakora - 250 PKR
- SD4: Chicken Wings - 550 PKR
- SD5: Masala Fries - 350 PKR
- SD6: Chana Chaat - 350 PKR
- SD7: Dahi Bhalla - 350 PKR

**Drinks (DR)**
- DR1: Mango Lassi - 350 PKR
- DR2: Sweet Lassi - 250 PKR
- DR3: Salted Lassi - 250 PKR
- DR4: Rooh Afza Milk - 300 PKR
- DR5: Chai - 180 PKR
- DR6: Soft Drink - 150 PKR
- DR7: Bottled Water - 100 PKR

**Desserts (DS)**
- DS1: Gulab Jamun - 250 PKR
- DS2: Kheer - 300 PKR
- DS3: Gajar Halwa - 350 PKR
- DS4: Rasmalai - 350 PKR
- DS5: Jalebi - 250 PKR

---

## 🚀 Deployment Steps

### 1. Update Meta Catalog CSV
Upload catalog with correct SKUs to Meta Business Manager:
- Go to Meta Business Manager → Catalog
- Create/edit catalog with all 47 items
- **CRITICAL**: Use item IDs as product_retailer_id (DL1, BR1, KR1, etc.)

### 2. Link Catalog to WhatsApp Number
- In WhatsApp Manager → Settings → Catalog
- Select your catalog
- Link to your business number

### 3. Deploy Code
```bash
git push origin main  # Railway auto-deploys
```

### 4. Test in WhatsApp
1. Send "Hi"
2. See catalog icon
3. Tap catalog
4. Select items
5. Tap Checkout
6. Bot receives order automatically
7. Shows cart summary
8. Asks delivery method
9. Completes order

---

## ✅ What's Integrated

✅ **Native Catalog UI** - WhatsApp's beautiful catalog  
✅ **Order Messages** - Automatic cart population from catalog selections  
✅ **Cart Summary** - Shows selected items with totals  
✅ **Delivery Methods** - Home, Pickup, Dine-in  
✅ **Order Creation** - Manager gets notification  
✅ **Multi-Country** - PKR, AED, SAR, QAR, KWD, BHD, OMR, USD, GBP, CAD  
✅ **All 47 Items** - Complete menu across all 10 categories  

---

## 🔍 Troubleshooting

### "Bot receives order message"
**Solution**: Webhook must handle `msg_type == "order"`. Check `main.py` has the order message handler.

### "Items not in cart"
**Reason**: product_retailer_id in CSV doesn't match item IDs (BR1, KR1, etc.)  
**Solution**: Verify your catalog CSV has exact item IDs

### "Catalog not showing"
**Reason**: Catalog not linked to WhatsApp number in Business Manager  
**Solution**: Go to WhatsApp Manager → Catalog → Link catalog to your number

### "Wrong prices showing"
**Reason**: Prices in catalog CSV don't match menus_multi.py  
**Solution**: Make sure catalog prices match the menu system

---

## 📊 Order Flow Summary

```
Flow: Hi → Catalog → Select → Order Message → Cart → Delivery → Confirm

1. User: "Hi"
2. Bot: Shows greeting + catalog icon
3. User: Taps catalog
4. User: Selects items in catalog UI
5. User: Taps "Checkout"
6. WhatsApp: Sends order message with items
7. Bot: Extracts items from order message
8. Bot: Populates cart
9. Bot: Shows cart summary
10. Bot: Asks delivery method
11. User: Selects delivery/pickup/dine-in
12. User: Provides address/table
13. Bot: Shows complete order summary
14. Bot: Creates order
15. Manager: Receives notification
16. Customer: Gets confirmation
```

---

## 🎯 That's It!

Your bot now has a **COMPLETE PROFESSIONAL WHATSAPP ORDERING SYSTEM** with native catalog integration! 

**Deploy and test now!** 🚀
