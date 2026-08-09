# 🛍️ Meta Catalog Setup Guide for WhatsApp

## What You Have
✅ **wild_bites_catalog.csv** - 47 Pakistani menu items in Meta Catalog format

---

## How to Upload to Meta (Facebook Business)

### Step 1: Go to Meta Business Suite
```
https://business.facebook.com
```

### Step 2: Navigate to Catalog Manager
```
Settings → Catalogs → Create Catalog
```

### Step 3: Select Catalog Type
- **Product Type:** Food & Restaurant
- **Catalog Name:** Wild Bites Restaurant Menu
- **Description:** Pakistani restaurant menu items for WhatsApp ordering

### Step 4: Upload CSV File
1. Click "Upload a File"
2. Select `wild_bites_catalog.csv`
3. Wait for Meta to process (2-5 minutes)

### Step 5: Verify Data
- Check that all 47 items uploaded
- Verify images are loading (GitHub raw URLs)
- Check prices are in PKR

---

## What's in the CSV

### 47 Menu Items Across 10 Categories:

| Category | Items | IDs |
|----------|-------|-----|
| **Deals & Combos** | 6 | DL1-DL6 |
| **Biryani & Rice** | 6 | BR1-BR6 |
| **Karahi & Curries** | 7 | KR1-KR7 |
| **BBQ & Grills** | 7 | BB1-BB7 |
| **Rolls & Wraps** | 7 | RL1-RL7 |
| **Chinese** | 8 | CH1-CH8 |
| **Naan & Bread** | 6 | BD1-BD6 |
| **Sides & Starters** | 7 | SD1-SD7 |
| **Drinks** | 7 | DR1-DR7 |
| **Desserts** | 5 | DS1-DS5 |

### Each Item Has:
✅ Unique ID (SKU)
✅ Title (item name)
✅ Description
✅ Price (in PKR)
✅ Availability (in stock)
✅ Condition (new)
✅ Link (menu page)
✅ Image (GitHub hosted)
✅ Brand (Wild Bites)
✅ Google & Facebook category
✅ Quantity (unlimited)

---

## WhatsApp Catalog Flow

Once uploaded to Meta, here's how it works on WhatsApp:

### Customer Experience:

```
Customer opens chat
   ↓
Customer: "Show me menu" or "Hi"
   ↓
Bot: Shows "📦 Catalog" button or link
   ↓
Customer: Taps catalog
   ↓
WhatsApp: Opens beautiful catalog UI with:
   - 10 category tabs
   - 47 products with images
   - Prices in PKR
   - Descriptions
   - Stock status
   
   ↓
Customer: Browses categories
   ↓
Customer: Taps item → See details
   ↓
Customer: Taps "Add to Cart" button
   ↓
Quantity selector: Customer chooses qty
   ↓
Cart builds up with selected items
   ↓
Customer: Taps "View Cart" or "Checkout"
   ↓
WhatsApp redirects to bot for:
   - Address collection
   - Delivery/Pickup/Dine-in selection
   - Payment
   - Order confirmation
```

---

## CSV Format Explanation

### Required Fields (Always included):
- **id**: Unique item ID (DL1, BR1, etc.)
- **title**: Product name
- **description**: 1-2 sentence description
- **availability**: "in stock" (hardcoded as always in stock)
- **condition**: "new" (always new)
- **price**: Amount + currency code (e.g., "850 PKR")
- **link**: Link to menu page
- **image_link**: GitHub raw image URL
- **brand**: Wild Bites Restaurant
- **google_product_category**: Food > Food Delivery
- **fb_product_category**: Food & Beverage
- **quantity_to_sell_on_facebook**: 100 (unlimited stock)

### Optional Fields (For better experience):
- **color**: Item color (for visuals)
- **size**: N/A for food
- **material**: Main ingredient

---

## How to Use with WhatsApp Bot

### Option 1: Direct Catalog Link (Recommended)
Update bot to send catalog link:

```python
await send_text_message(sender, """
Browse our full menu with images and prices!

Tap below: 👇
""")

# Send catalog button
catalog_url = "https://www.facebook.com/wild-bites/products/"

button = {
    "id": "catalog",
    "title": "📦 BROWSE MENU"
}
```

### Option 2: Catalog in Messages
WhatsApp automatically shows catalog when user interacts with your page.

### Option 3: Hybrid (Best UX)
1. Bot shows simple category menu
2. User selects category
3. Bot opens catalog filtered to that category
4. User selects items with quantities
5. Bot completes order in chat

---

## Advantages of Meta Catalog

✅ **Beautiful UI**: Professional catalog view
✅ **No Coding**: Customers use standard WhatsApp interface
✅ **Images**: All product images display beautifully
✅ **Stock Management**: Easy inventory updates
✅ **Cart Building**: Native cart in WhatsApp
✅ **Mobile Optimized**: Works perfectly on phones
✅ **Fast Browsing**: Quick category navigation
✅ **Professional Look**: Looks like a real restaurant

---

## CSV Upload Status

📁 **File:** `wild_bites_catalog.csv`
📊 **Items:** 47 dishes
💵 **Currency:** PKR (Pakistani Rupee)
🖼️ **Images:** GitHub hosted (public URLs)
📱 **Platform:** Meta Business / WhatsApp

---

## Next Steps

1. **Upload CSV to Meta**
   - Go to Meta Business Suite → Catalogs
   - Upload the CSV file
   - Wait for processing

2. **Verify Catalog**
   - Check all items appear
   - Verify images load
   - Check prices display correctly

3. **Connect to WhatsApp**
   - Link catalog to WhatsApp Business account
   - Set up catalog sharing in messages

4. **Test on WhatsApp**
   - Send test message to your number
   - Verify catalog appears
   - Browse items and test add-to-cart

5. **Update Bot Logic**
   - Integrate catalog link in greeting
   - Or use hybrid approach (bot menu + catalog)
   - Complete order process after catalog selection

---

## Troubleshooting

### Images Not Loading
❌ Check GitHub URLs are public
✅ Re-upload CSV with correct URLs

### Items Not Appearing
❌ Check CSV formatting
✅ Verify column headers match Meta format

### Wrong Currency
❌ Price format was incorrect
✅ Use format: "amount CURRENCY_CODE" (e.g., "850 PKR")

### Items Not Searchable
❌ Descriptions too short
✅ Use longer, keyword-rich descriptions

---

## That's It! 🎉

Your catalog is ready for WhatsApp! Customers will now be able to:
- 📱 Browse beautiful menu with images
- 💵 See prices clearly
- 🛒 Add items to cart easily
- ⚡ Quick and intuitive experience
- 🎯 Multiple items at once!

Much better UX than text-based ordering! 🚀
