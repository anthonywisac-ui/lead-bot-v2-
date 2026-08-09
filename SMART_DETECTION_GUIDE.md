# 🧠 SMART AUTO-DETECTION SYSTEM

## Overview

Bot now **automatically detects** everything from first message:
- ✅ Customer type (new/returning/B2B client)
- ✅ Customer name (if provided)
- ✅ Location preference (if mentioned)
- ✅ Intent (order type)

**No need for manual keyword commands!**

---

## 🎯 How It Works

### SCENARIO 1: Returning Customer

```
CUSTOMER: "Hi, it's Ahmed"
BOT DETECTS:
  ✅ Type: RETURNING (keyword "hi")
  ✅ Name: Ahmed (extracted from message)
  ✅ Last order: Saved in database
  
BOT RESPONDS:
👋 Welcome back, Ahmed!
Great to see you again! 😊

[🔁 Last Order] [📝 New Order]
```

### SCENARIO 2: B2B Client

```
CUSTOMER: "Client"
BOT DETECTS:
  ✅ Type: CLIENT (keyword "client")
  
BOT RESPONDS:
👔 Welcome, Business Partner!
Let's set up your B2B account.

Please provide your manager number:
Format: +923xxxxxxxxx or 03xxxxxxxxx

CUSTOMER: "+923219876543"
BOT:
✅ Manager: +923219876543
📋 Let's get your order ready!
[Shows menu]

→ All orders sent to +923219876543
```

### SCENARIO 3: New Customer

```
CUSTOMER: "New customer here" 
         OR "Hi" (but no last order)
         OR "Hello" (with no history)

BOT DETECTS:
  ✅ Type: NEW (or returning without order)
  ✅ Auto-detects location: Pakistan (from phone +92)
  
BOT RESPONDS:
👋 Welcome to Wild Bites!
Let's get you started! 🍽️

[Shows menu categories]
```

---

## 🔤 Keywords Detected

### Returning Customer Keywords
```
hi, hello, hey, salam, salaam, assalam, assalamu alaikum,
hola, namaste, sup, whats up, yo, oi, howdy
```

### B2B Client Keywords
```
client, business, corporate, bulk, catering, wholesale
```

### New Customer Keywords
```
new, first time, fresh, start, begin
```

### Location Keywords
```
Pakistan: lahore, karachi, islamabad, urdu
UAE: dubai, abu dhabi, emirates
USA: america, united states
UK: london, britain
etc.
```

---

## 👤 Name Extraction

Bot automatically extracts names from patterns:

```
"Hi, I'm Ahmed"          → Name: Ahmed
"Salam, Ahmed here"      → Name: Ahmed
"Hello, my name is Ali"  → Name: Ali
"Hi Ahmed"               → Name: Ahmed
"Call me Sara"           → Name: Sara
```

---

## 🖼️ GitHub Images

### How to Add Images

**Step 1: Create folder structure**
```
images/
├── biryani/
│   ├── chicken_biryani.jpg
│   ├── beef_biryani.jpg
│   └── pulao.jpg
├── karahi/
│   └── chicken_karahi.jpg
├── rolls/
├── burgers/
├── pizza/
└── [etc]
```

**Step 2: Upload to GitHub**
- Commit images to `/images/` directory
- Push to main branch

**Step 3: Get Public URLs**
Format:
```
https://raw.githubusercontent.com/anthonywisac-ui/lead-bot-v2-/main/images/[category]/[filename]
```

Example:
```
https://raw.githubusercontent.com/anthonywisac-ui/lead-bot-v2-/main/images/biryani/chicken_biryani.jpg
```

**Step 4: Update menus_multi.py**
```python
"BR1": {
    "name": "Chicken Biryani",
    "price": 650,
    "desc": "Aromatic basmati rice",
    "image": "https://raw.githubusercontent.com/anthonywisac-ui/lead-bot-v2-/main/images/biryani/chicken_biryani.jpg"
}
```

**Step 5: Images show in bot!**

---

## 📱 Complete Test Flow

### TEST 1: Returning Customer With Name
```
SEND: "Hi, I'm Ahmed"

BOT:
👋 Welcome back, Ahmed!
Great to see you again! 😊

[🔁 Last Order] [📝 New Order]

CLICK: [🔁 Last Order]
→ Cart loads with previous items
→ Ready to checkout
```

### TEST 2: B2B Client
```
SEND: "Client"

BOT:
👔 Welcome, Business Partner!
Let's set up your B2B account.

Please provide manager number:

SEND: "+923219876543"

BOT:
✅ Manager: +923219876543
📋 Let's get your order ready!

[Shows menu]

CHECKOUT:
→ Order sent to +923219876543
→ Not to default manager
```

### TEST 3: New Customer
```
SEND: "Hola" 
     OR "First time here"
     OR "Start new order"

BOT:
👋 Welcome to Wild Bites!
Let's get you started! 🍽️

[Shows menu categories]
```

---

## 🎨 Greeting Templates

### Returning Customer WITH name:
```
👋 Welcome back, [NAME]!
Great to see you again! 😊

What would you like to do?
```

### Returning Customer WITHOUT name:
```
👋 Welcome back!
Great to see you again! 😊

What would you like to do?
```

### B2B Client:
```
👔 Welcome, Business Partner!
Let's set up your B2B account.

Please provide your manager/business number:
Format: +923xxxxxxxxx or 03xxxxxxxxx
```

### New Customer:
```
👋 Welcome to Wild Bites!
Let's get you started! 🍽️
```

---

## 🔍 Smart Detection Features

| Feature | What It Does | Example |
|---------|-------------|---------|
| **Type Detection** | Identifies customer type from message | "client" → B2B |
| **Name Extraction** | Pulls name from greeting | "Hi Ahmed" → Ahmed |
| **Location Detection** | Identifies country preference | "Dubai order" → UAE |
| **Keyword Matching** | 20+ keywords for each type | "Salam" → Returning |
| **Last Order Check** | Loads previous order if returning | Shows [🔁 Last Order] |
| **Personalization** | Greets by name | "Welcome back, Ahmed!" |

---

## ✅ NEW SYSTEM STATUS

- [x] Smart type detection (new/returning/client)
- [x] Name extraction from message
- [x] Location preference detection
- [x] Personalized greetings with name
- [x] B2B client flow with custom manager
- [x] GitHub image hosting ready
- [x] Public URLs for images
- [x] Image integration in menu

---

## 📋 Quick Start

### For Testing:
1. Send any greeting: "Hi", "Hello", "Salam"
2. Bot detects if returning + greets by name
3. Or send "Client" for B2B setup
4. Or send "New" for fresh order

### For Adding Images:
1. Create folder: `images/[category]/`
2. Add image files
3. Commit & push to GitHub
4. Update menus_multi.py with URL
5. Images appear in bot!

---

## 🚀 Ready to Deploy!

All smart detection features are **LIVE** and **READY**!

Test the new system now! 🎉
