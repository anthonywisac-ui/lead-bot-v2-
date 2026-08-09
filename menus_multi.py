# Multi-country restaurant menus with pricing
# Each country has independent menu, pricing, and currency

MENUS = {
    "PK": {
        "country": "Pakistan",
        "code": "PK",
        "currency": "PKR",
        "symbol": "Rs",
        "categories": {
            "deals": {
                "name": "🔥 Deals & Combos",
                "items": {
                    "DL1": {"name": "Chicken Biryani Combo", "price": 850, "desc": "Biryani + Naan + Drink"},
                    "DL2": {"name": "Chicken Karahi Combo", "price": 1650, "desc": "Karahi + Naan + Raita"},
                    "DL3": {"name": "BBQ Platter Deal", "price": 2250, "desc": "Mixed BBQ + Rice + Sides"},
                    "DL4": {"name": "Family Biryani Deal", "price": 2999, "desc": "2 Biryani + 2 Naan + Drinks"},
                    "DL5": {"name": "2 Person Karahi Deal", "price": 2499, "desc": "Karahi + Rice + Naan + Raita"},
                    "DL6": {"name": "Burger & Fries Combo", "price": 750, "desc": "Burger + Fries + Drink"},
                }
            },
            "biryani": {
                "name": "🍚 Biryani & Rice",
                "items": {
                    "BR1": {"name": "Chicken Biryani", "price": 650, "desc": "Aromatic basmati rice with spiced chicken"},
                    "BR2": {"name": "Beef Biryani", "price": 750, "desc": "Tender beef biryani"},
                    "BR3": {"name": "Mutton Biryani", "price": 950, "desc": "Premium mutton biryani"},
                    "BR4": {"name": "Chicken Pulao", "price": 600, "desc": "Simple pulao with chicken"},
                    "BR5": {"name": "Chicken Fried Rice", "price": 650, "desc": "Indo-Chinese style"},
                    "BR6": {"name": "Plain Rice", "price": 300, "desc": "Steamed basmati rice"},
                }
            },
            "karahi": {
                "name": "🍛 Karahi & Curries",
                "items": {
                    "KR1": {"name": "Chicken Karahi", "price": 1400, "desc": "Spiced chicken in karahi"},
                    "KR2": {"name": "Mutton Karahi", "price": 2100, "desc": "Premium mutton karahi"},
                    "KR3": {"name": "Beef Nihari", "price": 950, "desc": "Slow-cooked beef"},
                    "KR4": {"name": "Chicken Handi", "price": 1450, "desc": "Creamy chicken handi"},
                    "KR5": {"name": "Butter Chicken", "price": 1300, "desc": "Creamy butter chicken"},
                    "KR6": {"name": "Daal Makhani", "price": 650, "desc": "Creamy lentils"},
                    "KR7": {"name": "Chana Masala", "price": 550, "desc": "Chickpea curry"},
                }
            },
            "bbq": {
                "name": "🍖 BBQ & Grills",
                "items": {
                    "BB1": {"name": "Chicken Tikka", "price": 650, "desc": "Marinated chicken pieces"},
                    "BB2": {"name": "Chicken Seekh Kebab", "price": 700, "desc": "Minced chicken kebab"},
                    "BB3": {"name": "Beef Seekh Kebab", "price": 750, "desc": "Spiced beef kebab"},
                    "BB4": {"name": "Chicken Boti", "price": 750, "desc": "Chunks of grilled chicken"},
                    "BB5": {"name": "Malai Boti", "price": 850, "desc": "Creamy chicken pieces"},
                    "BB6": {"name": "Chicken Tandoori", "price": 750, "desc": "Tandoori roasted chicken"},
                    "BB7": {"name": "Mixed Grill Platter", "price": 1650, "desc": "Assorted grilled meats"},
                }
            },
            "rolls": {
                "name": "🌯 Rolls & Wraps",
                "items": {
                    "RL1": {"name": "Chicken Paratha Roll", "price": 450, "desc": "Crispy paratha wrap"},
                    "RL2": {"name": "Beef Paratha Roll", "price": 500, "desc": "Beef in paratha"},
                    "RL3": {"name": "Chicken Cheese Roll", "price": 500, "desc": "Cheese chicken roll"},
                    "RL4": {"name": "Zinger Roll", "price": 500, "desc": "Spicy chicken roll"},
                    "RL5": {"name": "Malai Boti Roll", "price": 550, "desc": "Creamy chicken roll"},
                    "RL6": {"name": "BBQ Chicken Roll", "price": 500, "desc": "BBQ flavored roll"},
                    "RL7": {"name": "Mayo Garlic Roll", "price": 400, "desc": "Garlic mayo roll"},
                }
            },
            "chinese": {
                "name": "🥢 Chinese",
                "items": {
                    "CH1": {"name": "Chicken Chow Mein", "price": 750, "desc": "Stir-fried noodles"},
                    "CH2": {"name": "Chicken Manchurian", "price": 850, "desc": "Crispy chicken in sauce"},
                    "CH3": {"name": "Chicken Chili", "price": 850, "desc": "Spicy chicken"},
                    "CH4": {"name": "Chicken Shashlik", "price": 900, "desc": "Skewered chicken"},
                    "CH5": {"name": "Chicken Fried Rice", "price": 650, "desc": "Indo-Chinese rice"},
                    "CH6": {"name": "Egg Fried Rice", "price": 550, "desc": "Egg fried rice"},
                    "CH7": {"name": "Vegetable Chow Mein", "price": 600, "desc": "Vegetable noodles"},
                    "CH8": {"name": "Chicken Schezwan Rice", "price": 800, "desc": "Spicy schezwan rice"},
                }
            },
            "bread": {
                "name": "🍞 Naan & Bread",
                "items": {
                    "BR1": {"name": "Plain Naan", "price": 100, "desc": "Simple naan"},
                    "BR2": {"name": "Garlic Naan", "price": 180, "desc": "Garlic flavored"},
                    "BR3": {"name": "Butter Naan", "price": 180, "desc": "Buttery naan"},
                    "BR4": {"name": "Cheese Naan", "price": 350, "desc": "Cheese stuffed"},
                    "BR5": {"name": "Roghni Naan", "price": 200, "desc": "Oil brushed naan"},
                    "BR6": {"name": "Tandoori Roti", "price": 70, "desc": "Whole wheat roti"},
                }
            },
            "sides": {
                "name": "🍟 Sides & Starters",
                "items": {
                    "SD1": {"name": "Samosa", "price": 100, "desc": "Crispy samosa"},
                    "SD2": {"name": "Chicken Samosa", "price": 150, "desc": "Chicken samosa"},
                    "SD3": {"name": "Pakora", "price": 250, "desc": "Fried fritters"},
                    "SD4": {"name": "Chicken Wings", "price": 550, "desc": "Spicy wings"},
                    "SD5": {"name": "Masala Fries", "price": 350, "desc": "Spiced fries"},
                    "SD6": {"name": "Chana Chaat", "price": 350, "desc": "Street chaat"},
                    "SD7": {"name": "Dahi Bhalla", "price": 350, "desc": "Yogurt dumplings"},
                }
            },
            "drinks": {
                "name": "🥤 Drinks",
                "items": {
                    "DR1": {"name": "Mango Lassi", "price": 350, "desc": "Sweet mango lassi"},
                    "DR2": {"name": "Sweet Lassi", "price": 250, "desc": "Yogurt drink"},
                    "DR3": {"name": "Salted Lassi", "price": 250, "desc": "Salted yogurt"},
                    "DR4": {"name": "Rooh Afza Milk", "price": 300, "desc": "Rose milk"},
                    "DR5": {"name": "Chai", "price": 180, "desc": "Hot tea"},
                    "DR6": {"name": "Soft Drink", "price": 150, "desc": "Soda"},
                    "DR7": {"name": "Bottled Water", "price": 100, "desc": "Pure water"},
                }
            },
            "desserts": {
                "name": "🍰 Desserts",
                "items": {
                    "DS1": {"name": "Gulab Jamun", "price": 250, "desc": "Sweet dumplings"},
                    "DS2": {"name": "Kheer", "price": 300, "desc": "Rice pudding"},
                    "DS3": {"name": "Gajar Halwa", "price": 350, "desc": "Carrot halwa"},
                    "DS4": {"name": "Rasmalai", "price": 350, "desc": "Cheese dessert"},
                    "DS5": {"name": "Jalebi", "price": 250, "desc": "Sweet spirals"},
                }
            },
        }
    },

    "AE": {
        "country": "United Arab Emirates",
        "code": "AE",
        "currency": "AED",
        "symbol": "AED",
        "categories": {
            "deals": {
                "name": "🔥 Deals",
                "items": {
                    "DL1": {"name": "Chicken Biryani Combo", "price": 32, "desc": "Biryani + Bread + Drink"},
                    "DL2": {"name": "Chicken Mandi Combo", "price": 38, "desc": "Mandi + Salad + Drink"},
                    "DL3": {"name": "Shawarma Combo", "price": 25, "desc": "Shawarma + Fries + Drink"},
                    "DL4": {"name": "Mixed Grill Deal", "price": 65, "desc": "Assorted grills"},
                    "DL5": {"name": "Family Rice Deal", "price": 89, "desc": "2 Rice + Sides"},
                    "DL6": {"name": "Burger Combo", "price": 29, "desc": "Burger + Fries + Drink"},
                }
            },
            "mains": {
                "name": "🍚 Rice & Mains",
                "items": {
                    "MN1": {"name": "Chicken Mandi", "price": 32, "desc": "Fragrant rice with chicken"},
                    "MN2": {"name": "Mutton Mandi", "price": 49, "desc": "Premium mutton mandi"},
                    "MN3": {"name": "Chicken Kabsa", "price": 34, "desc": "Spiced rice with chicken"},
                    "MN4": {"name": "Mutton Kabsa", "price": 52, "desc": "Mutton kabsa"},
                    "MN5": {"name": "Chicken Machboos", "price": 35, "desc": "Gulf style rice"},
                    "MN6": {"name": "Chicken Biryani", "price": 32, "desc": "Indian style biryani"},
                    "MN7": {"name": "Beef Biryani", "price": 38, "desc": "Beef biryani"},
                }
            },
            "grills": {
                "name": "🍖 Grills",
                "items": {
                    "GR1": {"name": "Chicken Tikka", "price": 29, "desc": "Marinated tikka"},
                    "GR2": {"name": "Chicken Shish Tawook", "price": 32, "desc": "Garlic chicken"},
                    "GR3": {"name": "Beef Seekh Kebab", "price": 35, "desc": "Spiced beef"},
                    "GR4": {"name": "Chicken Kebab", "price": 30, "desc": "Grilled chicken"},
                    "GR5": {"name": "Mixed Grill", "price": 65, "desc": "All grills"},
                    "GR6": {"name": "Grilled Chicken", "price": 32, "desc": "Flame grilled"},
                }
            },
            "shawarma": {
                "name": "🌯 Shawarma & Wraps",
                "items": {
                    "SW1": {"name": "Chicken Shawarma", "price": 12, "desc": "Wrapped chicken"},
                    "SW2": {"name": "Beef Shawarma", "price": 15, "desc": "Wrapped beef"},
                    "SW3": {"name": "Chicken Arabic Shawarma", "price": 22, "desc": "Full Arabic wrap"},
                    "SW4": {"name": "Beef Arabic Shawarma", "price": 25, "desc": "Premium beef wrap"},
                    "SW5": {"name": "Chicken Saj Wrap", "price": 18, "desc": "Saj wrapped"},
                    "SW6": {"name": "Falafel Wrap", "price": 12, "desc": "Vegetarian wrap"},
                }
            },
            "starters": {
                "name": "🥗 Starters",
                "items": {
                    "ST1": {"name": "Hummus", "price": 15, "desc": "Chickpea dip"},
                    "ST2": {"name": "Moutabal", "price": 16, "desc": "Eggplant dip"},
                    "ST3": {"name": "Falafel", "price": 12, "desc": "Fried falafel"},
                    "ST4": {"name": "Samosa", "price": 12, "desc": "Crispy samosa"},
                    "ST5": {"name": "Fattoush", "price": 16, "desc": "Fresh salad"},
                    "ST6": {"name": "Arabic Salad", "price": 14, "desc": "Tabbouleh salad"},
                }
            },
            "chinese": {
                "name": "🥢 Chinese",
                "items": {
                    "CH1": {"name": "Chicken Fried Rice", "price": 25, "desc": "Stir fried rice"},
                    "CH2": {"name": "Chicken Chow Mein", "price": 27, "desc": "Chow mein noodles"},
                    "CH3": {"name": "Chicken Manchurian", "price": 29, "desc": "Spicy manchurian"},
                    "CH4": {"name": "Chicken Chili", "price": 29, "desc": "Chili chicken"},
                    "CH5": {"name": "Sweet & Sour Chicken", "price": 29, "desc": "Sweet & sour"},
                    "CH6": {"name": "Vegetable Noodles", "price": 22, "desc": "Vegetable noodles"},
                }
            },
            "bread": {
                "name": "🍞 Bread & Sides",
                "items": {
                    "BR1": {"name": "Naan", "price": 5, "desc": "Plain naan"},
                    "BR2": {"name": "Garlic Naan", "price": 7, "desc": "Garlic naan"},
                    "BR3": {"name": "Arabic Bread", "price": 3, "desc": "Pita bread"},
                    "BR4": {"name": "French Fries", "price": 10, "desc": "Crispy fries"},
                    "BR5": {"name": "Masala Fries", "price": 14, "desc": "Spiced fries"},
                    "BR6": {"name": "Onion Rings", "price": 14, "desc": "Fried onions"},
                }
            },
            "drinks": {
                "name": "🥤 Drinks",
                "items": {
                    "DR1": {"name": "Mango Lassi", "price": 15, "desc": "Mango yogurt"},
                    "DR2": {"name": "Sweet Lassi", "price": 12, "desc": "Sweet yogurt"},
                    "DR3": {"name": "Fresh Orange Juice", "price": 16, "desc": "Fresh juice"},
                    "DR4": {"name": "Lemon Mint", "price": 15, "desc": "Cool lemonade"},
                    "DR5": {"name": "Karak Chai", "price": 5, "desc": "Gulf tea"},
                    "DR6": {"name": "Soft Drink", "price": 5, "desc": "Soda"},
                    "DR7": {"name": "Water", "price": 3, "desc": "Bottled water"},
                }
            },
            "desserts": {
                "name": "🍰 Desserts",
                "items": {
                    "DS1": {"name": "Kunafa", "price": 18, "desc": "Sweet kunafa"},
                    "DS2": {"name": "Umm Ali", "price": 16, "desc": "Bread pudding"},
                    "DS3": {"name": "Gulab Jamun", "price": 12, "desc": "Sweet dumplings"},
                    "DS4": {"name": "Rice Pudding", "price": 12, "desc": "Creamy pudding"},
                    "DS5": {"name": "Baklava", "price": 15, "desc": "Pastry dessert"},
                }
            },
        }
    },

    "SA": {
        "country": "Saudi Arabia",
        "code": "SA",
        "currency": "SAR",
        "symbol": "SAR",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Chicken Mandi Combo", "price": 35, "desc": "Mandi + Bread"}, "DL2": {"name": "Chicken Kabsa Combo", "price": 38, "desc": "Kabsa combo"}, "DL3": {"name": "Shawarma Combo", "price": 24, "desc": "Shawarma + Fries"}, "DL4": {"name": "Mixed Grill Deal", "price": 69, "desc": "All grills"}, "DL5": {"name": "Family Mandi Deal", "price": 95, "desc": "Family pack"}, "DL6": {"name": "Burger Combo", "price": 28, "desc": "Burger + Fries"}}},
            "mains": {"name": "🍚 Rice & Mains", "items": {"MN1": {"name": "Chicken Mandi", "price": 32, "desc": "Mandi chicken"}, "MN2": {"name": "Mutton Mandi", "price": 48, "desc": "Mutton mandi"}, "MN3": {"name": "Chicken Kabsa", "price": 34, "desc": "Kabsa chicken"}, "MN4": {"name": "Mutton Kabsa", "price": 50, "desc": "Kabsa mutton"}, "MN5": {"name": "Chicken Madghout", "price": 36, "desc": "Madghout rice"}, "MN6": {"name": "Chicken Biryani", "price": 30, "desc": "Biryani"}, "MN7": {"name": "Meat Kabsa", "price": 48, "desc": "Premium kabsa"}}},
            "grills": {"name": "🍖 Grills", "items": {"GR1": {"name": "Chicken Tikka", "price": 30, "desc": "Tikka"}, "GR2": {"name": "Shish Tawook", "price": 32, "desc": "Tawook"}, "GR3": {"name": "Beef Kebab", "price": 35, "desc": "Beef kebab"}, "GR4": {"name": "Chicken Kebab", "price": 30, "desc": "Chicken kebab"}, "GR5": {"name": "Mixed Grill", "price": 65, "desc": "All grills"}, "GR6": {"name": "Grilled Chicken", "price": 32, "desc": "Grilled"}}},
            "shawarma": {"name": "🌯 Shawarma", "items": {"SW1": {"name": "Chicken Shawarma", "price": 10, "desc": "Chicken wrap"}, "SW2": {"name": "Beef Shawarma", "price": 12, "desc": "Beef wrap"}, "SW3": {"name": "Arabic Chicken Shawarma", "price": 18, "desc": "Full wrap"}, "SW4": {"name": "Arabic Beef Shawarma", "price": 20, "desc": "Premium wrap"}, "SW5": {"name": "Chicken Saj", "price": 15, "desc": "Saj wrap"}, "SW6": {"name": "Falafel Sandwich", "price": 8, "desc": "Falafel wrap"}}},
            "starters": {"name": "🥗 Starters", "items": {"ST1": {"name": "Hummus", "price": 12, "desc": "Hummus"}, "ST2": {"name": "Moutabal", "price": 13, "desc": "Moutabal"}, "ST3": {"name": "Falafel", "price": 9, "desc": "Falafel"}, "ST4": {"name": "Fattoush", "price": 14, "desc": "Salad"}, "ST5": {"name": "Samosa", "price": 10, "desc": "Samosa"}, "ST6": {"name": "Arabic Salad", "price": 12, "desc": "Salad"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CH1": {"name": "Chicken Fried Rice", "price": 22, "desc": "Fried rice"}, "CH2": {"name": "Chicken Chow Mein", "price": 24, "desc": "Chow mein"}, "CH3": {"name": "Chicken Manchurian", "price": 26, "desc": "Manchurian"}, "CH4": {"name": "Chicken Chili", "price": 26, "desc": "Chili"}, "CH5": {"name": "Sweet & Sour Chicken", "price": 26, "desc": "Sweet & sour"}, "CH6": {"name": "Vegetable Noodles", "price": 20, "desc": "Noodles"}}},
            "sides": {"name": "🍞 Sides", "items": {"SD1": {"name": "Naan", "price": 4, "desc": "Naan"}, "SD2": {"name": "Garlic Naan", "price": 6, "desc": "Garlic naan"}, "SD3": {"name": "French Fries", "price": 8, "desc": "Fries"}, "SD4": {"name": "Masala Fries", "price": 12, "desc": "Spiced fries"}, "SD5": {"name": "Onion Rings", "price": 12, "desc": "Onion rings"}, "SD6": {"name": "Arabic Bread", "price": 3, "desc": "Bread"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Mango Lassi", "price": 14, "desc": "Lassi"}, "DR2": {"name": "Fresh Orange Juice", "price": 15, "desc": "Juice"}, "DR3": {"name": "Lemon Mint", "price": 14, "desc": "Lemon mint"}, "DR4": {"name": "Arabic Tea", "price": 5, "desc": "Tea"}, "DR5": {"name": "Soft Drink", "price": 5, "desc": "Soda"}, "DR6": {"name": "Water", "price": 2, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Kunafa", "price": 16, "desc": "Kunafa"}, "DS2": {"name": "Umm Ali", "price": 15, "desc": "Umm Ali"}, "DS3": {"name": "Baklava", "price": 14, "desc": "Baklava"}, "DS4": {"name": "Gulab Jamun", "price": 10, "desc": "Gulab jamun"}, "DS5": {"name": "Rice Pudding", "price": 10, "desc": "Pudding"}}},
        }
    },

    "QA": {
        "country": "Qatar",
        "code": "QA",
        "currency": "QAR",
        "symbol": "QAR",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Chicken Mandi Combo", "price": 38, "desc": "Combo"}, "DL2": {"name": "Chicken Biryani Combo", "price": 35, "desc": "Combo"}, "DL3": {"name": "Shawarma Combo", "price": 25, "desc": "Combo"}, "DL4": {"name": "Mixed Grill Deal", "price": 65, "desc": "Deal"}, "DL5": {"name": "Family Rice Deal", "price": 95, "desc": "Family"}, "DL6": {"name": "Burger Combo", "price": 29, "desc": "Combo"}}},
            "mains": {"name": "🍚 Mains", "items": {"MN1": {"name": "Chicken Mandi", "price": 35, "desc": "Mandi"}, "MN2": {"name": "Mutton Mandi", "price": 50, "desc": "Mandi"}, "MN3": {"name": "Chicken Kabsa", "price": 37, "desc": "Kabsa"}, "MN4": {"name": "Mutton Kabsa", "price": 52, "desc": "Kabsa"}, "MN5": {"name": "Chicken Machboos", "price": 38, "desc": "Machboos"}, "MN6": {"name": "Chicken Biryani", "price": 32, "desc": "Biryani"}, "MN7": {"name": "Beef Biryani", "price": 38, "desc": "Biryani"}}},
            "grills": {"name": "🍖 Grills", "items": {"GR1": {"name": "Chicken Tikka", "price": 30, "desc": "Tikka"}, "GR2": {"name": "Shish Tawook", "price": 32, "desc": "Tawook"}, "GR3": {"name": "Beef Kebab", "price": 35, "desc": "Kebab"}, "GR4": {"name": "Chicken Kebab", "price": 30, "desc": "Kebab"}, "GR5": {"name": "Mixed Grill", "price": 65, "desc": "Grill"}, "GR6": {"name": "Grilled Chicken", "price": 32, "desc": "Grilled"}}},
            "shawarma": {"name": "🌯 Shawarma", "items": {"SW1": {"name": "Chicken Shawarma", "price": 10, "desc": "Wrap"}, "SW2": {"name": "Beef Shawarma", "price": 13, "desc": "Wrap"}, "SW3": {"name": "Arabic Shawarma", "price": 20, "desc": "Arabic"}, "SW4": {"name": "Chicken Saj", "price": 16, "desc": "Saj"}, "SW5": {"name": "Falafel Wrap", "price": 10, "desc": "Wrap"}, "SW6": {"name": "Chicken Wrap", "price": 17, "desc": "Wrap"}}},
            "starters": {"name": "🥗 Starters", "items": {"ST1": {"name": "Hummus", "price": 14, "desc": "Hummus"}, "ST2": {"name": "Moutabal", "price": 15, "desc": "Moutabal"}, "ST3": {"name": "Falafel", "price": 10, "desc": "Falafel"}, "ST4": {"name": "Fattoush", "price": 15, "desc": "Salad"}, "ST5": {"name": "Samosa", "price": 10, "desc": "Samosa"}, "ST6": {"name": "Arabic Salad", "price": 13, "desc": "Salad"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CH1": {"name": "Chicken Fried Rice", "price": 23, "desc": "Rice"}, "CH2": {"name": "Chicken Chow Mein", "price": 25, "desc": "Mein"}, "CH3": {"name": "Chicken Manchurian", "price": 27, "desc": "Manchurian"}, "CH4": {"name": "Chicken Chili", "price": 27, "desc": "Chili"}, "CH5": {"name": "Sweet & Sour Chicken", "price": 27, "desc": "Sweet"}, "CH6": {"name": "Vegetable Noodles", "price": 21, "desc": "Noodles"}}},
            "sides": {"name": "🍞 Sides", "items": {"SD1": {"name": "Naan", "price": 4, "desc": "Naan"}, "SD2": {"name": "Garlic Naan", "price": 6, "desc": "Naan"}, "SD3": {"name": "French Fries", "price": 9, "desc": "Fries"}, "SD4": {"name": "Masala Fries", "price": 13, "desc": "Fries"}, "SD5": {"name": "Onion Rings", "price": 13, "desc": "Rings"}, "SD6": {"name": "Arabic Bread", "price": 3, "desc": "Bread"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Mango Lassi", "price": 14, "desc": "Lassi"}, "DR2": {"name": "Fresh Orange Juice", "price": 16, "desc": "Juice"}, "DR3": {"name": "Lemon Mint", "price": 15, "desc": "Mint"}, "DR4": {"name": "Karak Tea", "price": 5, "desc": "Tea"}, "DR5": {"name": "Soft Drink", "price": 5, "desc": "Drink"}, "DR6": {"name": "Water", "price": 2, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Kunafa", "price": 17, "desc": "Kunafa"}, "DS2": {"name": "Umm Ali", "price": 15, "desc": "Ali"}, "DS3": {"name": "Baklava", "price": 14, "desc": "Baklava"}, "DS4": {"name": "Gulab Jamun", "price": 10, "desc": "Jamun"}, "DS5": {"name": "Rice Pudding", "price": 10, "desc": "Pudding"}}},
        }
    },

    "KW": {
        "country": "Kuwait",
        "code": "KW",
        "currency": "KWD",
        "symbol": "KWD",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Chicken Mandi Combo", "price": 3.25, "desc": "Combo"}, "DL2": {"name": "Chicken Biryani Combo", "price": 2.95, "desc": "Combo"}, "DL3": {"name": "Shawarma Combo", "price": 2.25, "desc": "Combo"}, "DL4": {"name": "Mixed Grill Deal", "price": 5.95, "desc": "Deal"}, "DL5": {"name": "Family Rice Deal", "price": 8.50, "desc": "Family"}, "DL6": {"name": "Burger Combo", "price": 2.50, "desc": "Combo"}}},
            "mains": {"name": "🍚 Mains", "items": {"MN1": {"name": "Chicken Mandi", "price": 2.95, "desc": "Mandi"}, "MN2": {"name": "Mutton Mandi", "price": 4.50, "desc": "Mandi"}, "MN3": {"name": "Chicken Kabsa", "price": 3.10, "desc": "Kabsa"}, "MN4": {"name": "Mutton Kabsa", "price": 4.75, "desc": "Kabsa"}, "MN5": {"name": "Chicken Machboos", "price": 3.20, "desc": "Machboos"}, "MN6": {"name": "Chicken Biryani", "price": 2.75, "desc": "Biryani"}, "MN7": {"name": "Beef Biryani", "price": 3.25, "desc": "Biryani"}}},
            "grills": {"name": "🍖 Grills", "items": {"GR1": {"name": "Chicken Tikka", "price": 2.75, "desc": "Tikka"}, "GR2": {"name": "Shish Tawook", "price": 2.95, "desc": "Tawook"}, "GR3": {"name": "Beef Kebab", "price": 3.25, "desc": "Kebab"}, "GR4": {"name": "Chicken Kebab", "price": 2.75, "desc": "Kebab"}, "GR5": {"name": "Mixed Grill", "price": 5.75, "desc": "Grill"}, "GR6": {"name": "Grilled Chicken", "price": 2.95, "desc": "Grilled"}}},
            "shawarma": {"name": "🌯 Shawarma", "items": {"SW1": {"name": "Chicken Shawarma", "price": 0.85, "desc": "Wrap"}, "SW2": {"name": "Beef Shawarma", "price": 1.10, "desc": "Wrap"}, "SW3": {"name": "Arabic Shawarma", "price": 1.65, "desc": "Arabic"}, "SW4": {"name": "Chicken Saj", "price": 1.25, "desc": "Saj"}, "SW5": {"name": "Falafel Wrap", "price": 0.75, "desc": "Wrap"}, "SW6": {"name": "Chicken Wrap", "price": 1.35, "desc": "Wrap"}}},
            "starters": {"name": "🥗 Starters", "items": {"ST1": {"name": "Hummus", "price": 0.95, "desc": "Hummus"}, "ST2": {"name": "Moutabal", "price": 1.05, "desc": "Moutabal"}, "ST3": {"name": "Falafel", "price": 0.75, "desc": "Falafel"}, "ST4": {"name": "Fattoush", "price": 1.10, "desc": "Salad"}, "ST5": {"name": "Samosa", "price": 0.75, "desc": "Samosa"}, "ST6": {"name": "Arabic Salad", "price": 0.95, "desc": "Salad"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CH1": {"name": "Chicken Fried Rice", "price": 2.10, "desc": "Rice"}, "CH2": {"name": "Chicken Chow Mein", "price": 2.25, "desc": "Mein"}, "CH3": {"name": "Chicken Manchurian", "price": 2.45, "desc": "Manchurian"}, "CH4": {"name": "Chicken Chili", "price": 2.45, "desc": "Chili"}, "CH5": {"name": "Sweet & Sour Chicken", "price": 2.45, "desc": "Sweet"}, "CH6": {"name": "Vegetable Noodles", "price": 1.85, "desc": "Noodles"}}},
            "sides": {"name": "🍞 Sides", "items": {"SD1": {"name": "Naan", "price": 0.30, "desc": "Naan"}, "SD2": {"name": "Garlic Naan", "price": 0.45, "desc": "Naan"}, "SD3": {"name": "French Fries", "price": 0.70, "desc": "Fries"}, "SD4": {"name": "Masala Fries", "price": 1.00, "desc": "Fries"}, "SD5": {"name": "Onion Rings", "price": 1.00, "desc": "Rings"}, "SD6": {"name": "Arabic Bread", "price": 0.20, "desc": "Bread"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Mango Lassi", "price": 1.15, "desc": "Lassi"}, "DR2": {"name": "Fresh Orange Juice", "price": 1.25, "desc": "Juice"}, "DR3": {"name": "Lemon Mint", "price": 1.15, "desc": "Mint"}, "DR4": {"name": "Karak Tea", "price": 0.40, "desc": "Tea"}, "DR5": {"name": "Soft Drink", "price": 0.35, "desc": "Drink"}, "DR6": {"name": "Water", "price": 0.15, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Kunafa", "price": 1.35, "desc": "Kunafa"}, "DS2": {"name": "Umm Ali", "price": 1.25, "desc": "Ali"}, "DS3": {"name": "Baklava", "price": 1.15, "desc": "Baklava"}, "DS4": {"name": "Gulab Jamun", "price": 0.85, "desc": "Jamun"}, "DS5": {"name": "Rice Pudding", "price": 0.85, "desc": "Pudding"}}},
        }
    },

    "BH": {
        "country": "Bahrain",
        "code": "BH",
        "currency": "BHD",
        "symbol": "BHD",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Chicken Mandi Combo", "price": 3.50, "desc": "Combo"}, "DL2": {"name": "Chicken Kabsa Combo", "price": 3.75, "desc": "Combo"}, "DL3": {"name": "Shawarma Combo", "price": 2.50, "desc": "Combo"}, "DL4": {"name": "Mixed Grill Deal", "price": 6.00, "desc": "Deal"}, "DL5": {"name": "Family Rice Deal", "price": 9.00, "desc": "Family"}, "DL6": {"name": "Burger Combo", "price": 2.75, "desc": "Combo"}}},
            "mains": {"name": "🍚 Mains", "items": {"MN1": {"name": "Chicken Mandi", "price": 3.20, "desc": "Mandi"}, "MN2": {"name": "Mutton Mandi", "price": 4.80, "desc": "Mandi"}, "MN3": {"name": "Chicken Kabsa", "price": 3.40, "desc": "Kabsa"}, "MN4": {"name": "Mutton Kabsa", "price": 5.00, "desc": "Kabsa"}, "MN5": {"name": "Chicken Machboos", "price": 3.50, "desc": "Machboos"}, "MN6": {"name": "Chicken Biryani", "price": 3.00, "desc": "Biryani"}, "MN7": {"name": "Beef Biryani", "price": 3.50, "desc": "Biryani"}}},
            "grills": {"name": "🍖 Grills", "items": {"GR1": {"name": "Chicken Tikka", "price": 3.00, "desc": "Tikka"}, "GR2": {"name": "Shish Tawook", "price": 3.25, "desc": "Tawook"}, "GR3": {"name": "Beef Kebab", "price": 3.50, "desc": "Kebab"}, "GR4": {"name": "Chicken Kebab", "price": 3.00, "desc": "Kebab"}, "GR5": {"name": "Mixed Grill", "price": 6.00, "desc": "Grill"}, "GR6": {"name": "Grilled Chicken", "price": 3.25, "desc": "Grilled"}}},
            "shawarma": {"name": "🌯 Shawarma", "items": {"SW1": {"name": "Chicken Shawarma", "price": 0.95, "desc": "Wrap"}, "SW2": {"name": "Beef Shawarma", "price": 1.20, "desc": "Wrap"}, "SW3": {"name": "Arabic Shawarma", "price": 1.80, "desc": "Arabic"}, "SW4": {"name": "Chicken Saj", "price": 1.40, "desc": "Saj"}, "SW5": {"name": "Falafel Wrap", "price": 0.85, "desc": "Wrap"}, "SW6": {"name": "Chicken Wrap", "price": 1.50, "desc": "Wrap"}}},
            "starters": {"name": "🥗 Starters", "items": {"ST1": {"name": "Hummus", "price": 1.05, "desc": "Hummus"}, "ST2": {"name": "Moutabal", "price": 1.15, "desc": "Moutabal"}, "ST3": {"name": "Falafel", "price": 0.85, "desc": "Falafel"}, "ST4": {"name": "Fattoush", "price": 1.25, "desc": "Salad"}, "ST5": {"name": "Samosa", "price": 0.85, "desc": "Samosa"}, "ST6": {"name": "Arabic Salad", "price": 1.05, "desc": "Salad"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CH1": {"name": "Chicken Fried Rice", "price": 2.30, "desc": "Rice"}, "CH2": {"name": "Chicken Chow Mein", "price": 2.50, "desc": "Mein"}, "CH3": {"name": "Chicken Manchurian", "price": 2.70, "desc": "Manchurian"}, "CH4": {"name": "Chicken Chili", "price": 2.70, "desc": "Chili"}, "CH5": {"name": "Sweet & Sour Chicken", "price": 2.70, "desc": "Sweet"}, "CH6": {"name": "Vegetable Noodles", "price": 2.00, "desc": "Noodles"}}},
            "sides": {"name": "🍞 Sides", "items": {"SD1": {"name": "Naan", "price": 0.40, "desc": "Naan"}, "SD2": {"name": "Garlic Naan", "price": 0.55, "desc": "Naan"}, "SD3": {"name": "French Fries", "price": 0.85, "desc": "Fries"}, "SD4": {"name": "Masala Fries", "price": 1.15, "desc": "Fries"}, "SD5": {"name": "Onion Rings", "price": 1.15, "desc": "Rings"}, "SD6": {"name": "Arabic Bread", "price": 0.30, "desc": "Bread"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Mango Lassi", "price": 1.30, "desc": "Lassi"}, "DR2": {"name": "Fresh Orange Juice", "price": 1.45, "desc": "Juice"}, "DR3": {"name": "Lemon Mint", "price": 1.30, "desc": "Mint"}, "DR4": {"name": "Karak Tea", "price": 0.50, "desc": "Tea"}, "DR5": {"name": "Soft Drink", "price": 0.45, "desc": "Drink"}, "DR6": {"name": "Water", "price": 0.20, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Kunafa", "price": 1.50, "desc": "Kunafa"}, "DS2": {"name": "Umm Ali", "price": 1.40, "desc": "Ali"}, "DS3": {"name": "Baklava", "price": 1.30, "desc": "Baklava"}, "DS4": {"name": "Gulab Jamun", "price": 0.95, "desc": "Jamun"}, "DS5": {"name": "Rice Pudding", "price": 0.95, "desc": "Pudding"}}},
        }
    },

    "OM": {
        "country": "Oman",
        "code": "OM",
        "currency": "OMR",
        "symbol": "OMR",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Chicken Mandi Combo", "price": 3.00, "desc": "Combo"}, "DL2": {"name": "Chicken Shuwa Combo", "price": 3.50, "desc": "Combo"}, "DL3": {"name": "Shawarma Combo", "price": 2.25, "desc": "Combo"}, "DL4": {"name": "Mixed Grill Deal", "price": 5.50, "desc": "Deal"}, "DL5": {"name": "Family Rice Deal", "price": 8.50, "desc": "Family"}, "DL6": {"name": "Burger Combo", "price": 2.50, "desc": "Combo"}}},
            "mains": {"name": "🍚 Mains", "items": {"MN1": {"name": "Chicken Mandi", "price": 2.80, "desc": "Mandi"}, "MN2": {"name": "Mutton Mandi", "price": 4.20, "desc": "Mandi"}, "MN3": {"name": "Chicken Shuwa", "price": 3.00, "desc": "Shuwa"}, "MN4": {"name": "Chicken Kabsa", "price": 3.10, "desc": "Kabsa"}, "MN5": {"name": "Chicken Machboos", "price": 3.20, "desc": "Machboos"}, "MN6": {"name": "Chicken Biryani", "price": 2.70, "desc": "Biryani"}, "MN7": {"name": "Beef Biryani", "price": 3.10, "desc": "Biryani"}}},
            "grills": {"name": "🍖 Grills", "items": {"GR1": {"name": "Chicken Tikka", "price": 2.70, "desc": "Tikka"}, "GR2": {"name": "Shish Tawook", "price": 2.90, "desc": "Tawook"}, "GR3": {"name": "Beef Kebab", "price": 3.10, "desc": "Kebab"}, "GR4": {"name": "Chicken Kebab", "price": 2.70, "desc": "Kebab"}, "GR5": {"name": "Mixed Grill", "price": 5.50, "desc": "Grill"}, "GR6": {"name": "Grilled Chicken", "price": 2.90, "desc": "Grilled"}}},
            "shawarma": {"name": "🌯 Shawarma", "items": {"SW1": {"name": "Chicken Shawarma", "price": 0.80, "desc": "Wrap"}, "SW2": {"name": "Beef Shawarma", "price": 1.05, "desc": "Wrap"}, "SW3": {"name": "Arabic Shawarma", "price": 1.55, "desc": "Arabic"}, "SW4": {"name": "Chicken Saj", "price": 1.20, "desc": "Saj"}, "SW5": {"name": "Falafel Wrap", "price": 0.70, "desc": "Wrap"}, "SW6": {"name": "Chicken Wrap", "price": 1.25, "desc": "Wrap"}}},
            "starters": {"name": "🥗 Starters", "items": {"ST1": {"name": "Hummus", "price": 0.90, "desc": "Hummus"}, "ST2": {"name": "Moutabal", "price": 0.95, "desc": "Moutabal"}, "ST3": {"name": "Falafel", "price": 0.70, "desc": "Falafel"}, "ST4": {"name": "Fattoush", "price": 1.00, "desc": "Salad"}, "ST5": {"name": "Samosa", "price": 0.70, "desc": "Samosa"}, "ST6": {"name": "Arabic Salad", "price": 0.90, "desc": "Salad"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CH1": {"name": "Chicken Fried Rice", "price": 2.00, "desc": "Rice"}, "CH2": {"name": "Chicken Chow Mein", "price": 2.15, "desc": "Mein"}, "CH3": {"name": "Chicken Manchurian", "price": 2.35, "desc": "Manchurian"}, "CH4": {"name": "Chicken Chili", "price": 2.35, "desc": "Chili"}, "CH5": {"name": "Sweet & Sour Chicken", "price": 2.35, "desc": "Sweet"}, "CH6": {"name": "Vegetable Noodles", "price": 1.75, "desc": "Noodles"}}},
            "sides": {"name": "🍞 Sides", "items": {"SD1": {"name": "Naan", "price": 0.30, "desc": "Naan"}, "SD2": {"name": "Garlic Naan", "price": 0.45, "desc": "Naan"}, "SD3": {"name": "French Fries", "price": 0.70, "desc": "Fries"}, "SD4": {"name": "Masala Fries", "price": 0.95, "desc": "Fries"}, "SD5": {"name": "Onion Rings", "price": 0.95, "desc": "Rings"}, "SD6": {"name": "Arabic Bread", "price": 0.20, "desc": "Bread"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Mango Lassi", "price": 1.10, "desc": "Lassi"}, "DR2": {"name": "Fresh Orange Juice", "price": 1.20, "desc": "Juice"}, "DR3": {"name": "Lemon Mint", "price": 1.10, "desc": "Mint"}, "DR4": {"name": "Karak Tea", "price": 0.40, "desc": "Tea"}, "DR5": {"name": "Soft Drink", "price": 0.35, "desc": "Drink"}, "DR6": {"name": "Water", "price": 0.15, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Kunafa", "price": 1.25, "desc": "Kunafa"}, "DS2": {"name": "Umm Ali", "price": 1.15, "desc": "Ali"}, "DS3": {"name": "Baklava", "price": 1.05, "desc": "Baklava"}, "DS4": {"name": "Gulab Jamun", "price": 0.80, "desc": "Jamun"}, "DS5": {"name": "Rice Pudding", "price": 0.80, "desc": "Pudding"}}},
        }
    },

    "US": {
        "country": "United States",
        "code": "US",
        "currency": "USD",
        "symbol": "$",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Burger Combo", "price": 14.99, "desc": "Burger + Fries + Drink"}, "DL2": {"name": "Chicken Sandwich Combo", "price": 13.99, "desc": "Chicken + Fries + Drink"}, "DL3": {"name": "Wings & Fries Deal", "price": 16.99, "desc": "6 Wings + Fries"}, "DL4": {"name": "Pizza & Wings Deal", "price": 22.99, "desc": "Pizza + Wings"}, "DL5": {"name": "Family Meal Deal", "price": 34.99, "desc": "Feeds 4"}, "DL6": {"name": "Burger Family Deal", "price": 29.99, "desc": "2 Burgers combo"}}},
            "burgers": {"name": "🍔 Burgers", "items": {"BG1": {"name": "Classic Smash Burger", "price": 12.99, "desc": "Double patty, special sauce"}, "BG2": {"name": "Double Smash Burger", "price": 15.99, "desc": "Massive burger"}, "BG3": {"name": "BBQ Bacon Burger", "price": 14.99, "desc": "BBQ + Bacon"}, "BG4": {"name": "Spicy Jalapeno Burger", "price": 14.49, "desc": "Spicy kick"}, "BG5": {"name": "Mushroom Swiss Burger", "price": 14.99, "desc": "Mushroom + Swiss"}, "BG6": {"name": "Crispy Chicken Burger", "price": 12.99, "desc": "Fried chicken"}}},
            "chicken": {"name": "🍗 Chicken", "items": {"CH1": {"name": "Crispy Chicken Sandwich", "price": 12.99, "desc": "Fried chicken sandwich"}, "CH2": {"name": "Chicken Tenders", "price": 11.99, "desc": "4 Crispy tenders"}, "CH3": {"name": "Buffalo Wings 6pc", "price": 10.99, "desc": "Buffalo sauce wings"}, "CH4": {"name": "Buffalo Wings 12pc", "price": 18.99, "desc": "Dozen wings"}, "CH5": {"name": "Nashville Hot Chicken", "price": 13.99, "desc": "Hot & spicy"}, "CH6": {"name": "Grilled Chicken Sandwich", "price": 12.99, "desc": "Healthy option"}}},
            "pizza": {"name": "🍕 Pizza", "items": {"PZ1": {"name": "Margherita", "price": 13.99, "desc": "Classic pizza"}, "PZ2": {"name": "Pepperoni", "price": 15.99, "desc": "Pepperoni pizza"}, "PZ3": {"name": "BBQ Chicken", "price": 16.99, "desc": "BBQ chicken pizza"}, "PZ4": {"name": "Meat Lovers", "price": 18.99, "desc": "All meats"}, "PZ5": {"name": "Veggie Supreme", "price": 15.99, "desc": "Vegetables"}, "PZ6": {"name": "Buffalo Chicken", "price": 17.99, "desc": "Spicy chicken"}}},
            "wraps": {"name": "🌯 Wraps", "items": {"WR1": {"name": "Crispy Chicken Wrap", "price": 11.99, "desc": "Crispy wrap"}, "WR2": {"name": "Buffalo Chicken Wrap", "price": 12.99, "desc": "Spicy wrap"}, "WR3": {"name": "Grilled Chicken Wrap", "price": 11.99, "desc": "Grilled"}, "WR4": {"name": "Beef Shawarma Wrap", "price": 12.99, "desc": "Beef wrap"}, "WR5": {"name": "Chicken Shawarma Wrap", "price": 11.99, "desc": "Chicken wrap"}, "WR6": {"name": "Falafel Wrap", "price": 10.99, "desc": "Vegetarian"}}},
            "sides": {"name": "🍟 Sides", "items": {"SD1": {"name": "French Fries", "price": 4.49, "desc": "Crispy fries"}, "SD2": {"name": "Loaded Fries", "price": 7.99, "desc": "Topped fries"}, "SD3": {"name": "Onion Rings", "price": 5.99, "desc": "Crispy rings"}, "SD4": {"name": "Mozzarella Sticks", "price": 7.99, "desc": "Fried cheese"}, "SD5": {"name": "Mac & Cheese Bites", "price": 6.99, "desc": "Crispy bites"}, "SD6": {"name": "Coleslaw", "price": 4.49, "desc": "Fresh slaw"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CN1": {"name": "Chicken Fried Rice", "price": 12.99, "desc": "Fried rice"}, "CN2": {"name": "Chicken Chow Mein", "price": 13.99, "desc": "Chow mein"}, "CN3": {"name": "Orange Chicken", "price": 14.99, "desc": "Sweet orange"}, "CN4": {"name": "Sweet & Sour Chicken", "price": 14.99, "desc": "Sweet sauce"}, "CN5": {"name": "Chicken Teriyaki", "price": 14.99, "desc": "Teriyaki sauce"}, "CN6": {"name": "Beef & Broccoli", "price": 15.99, "desc": "Beef dish"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Coca Cola", "price": 2.99, "desc": "Cold soda"}, "DR2": {"name": "Pepsi", "price": 2.99, "desc": "Cold soda"}, "DR3": {"name": "Lemonade", "price": 3.99, "desc": "Fresh lemonade"}, "DR4": {"name": "Iced Tea", "price": 3.49, "desc": "Iced tea"}, "DR5": {"name": "Milkshake", "price": 6.99, "desc": "Thick shake"}, "DR6": {"name": "Bottled Water", "price": 1.99, "desc": "Pure water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Chocolate Cake", "price": 6.99, "desc": "Rich chocolate"}, "DS2": {"name": "NY Cheesecake", "price": 6.99, "desc": "Classic cheesecake"}, "DS3": {"name": "Brownie Sundae", "price": 7.99, "desc": "Warm brownie"}, "DS4": {"name": "Apple Pie", "price": 5.99, "desc": "Fresh apple"}, "DS5": {"name": "Oreo Milkshake", "price": 7.99, "desc": "Oreo shake"}}},
        }
    },

    "GB": {
        "country": "United Kingdom",
        "code": "GB",
        "currency": "GBP",
        "symbol": "£",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Burger Meal", "price": 11.99, "desc": "Burger combo"}, "DL2": {"name": "Chicken Burger Meal", "price": 10.99, "desc": "Chicken combo"}, "DL3": {"name": "Fish & Chips Deal", "price": 12.99, "desc": "Fish combo"}, "DL4": {"name": "Wings & Fries Deal", "price": 13.99, "desc": "Wings combo"}, "DL5": {"name": "Family Meal", "price": 27.99, "desc": "Family pack"}, "DL6": {"name": "Pizza & Wings Deal", "price": 19.99, "desc": "Pizza combo"}}},
            "burgers": {"name": "🍔 Burgers", "items": {"BG1": {"name": "Classic Smash Burger", "price": 9.99, "desc": "Classic burger"}, "BG2": {"name": "Double Smash Burger", "price": 12.49, "desc": "Double burger"}, "BG3": {"name": "BBQ Bacon Burger", "price": 11.49, "desc": "BBQ burger"}, "BG4": {"name": "Spicy Chicken Burger", "price": 10.99, "desc": "Spicy"}, "BG5": {"name": "Crispy Chicken Burger", "price": 9.99, "desc": "Crispy"}, "BG6": {"name": "Mushroom Burger", "price": 10.99, "desc": "Mushroom"}}},
            "chicken": {"name": "🍗 Chicken", "items": {"CH1": {"name": "Chicken Tenders", "price": 8.99, "desc": "Tenders"}, "CH2": {"name": "Chicken Wings 6pc", "price": 8.49, "desc": "Wings"}, "CH3": {"name": "Chicken Wings 12pc", "price": 14.99, "desc": "Dozen wings"}, "CH4": {"name": "Nashville Chicken", "price": 10.99, "desc": "Hot"}, "CH5": {"name": "Grilled Chicken", "price": 10.49, "desc": "Grilled"}, "CH6": {"name": "Chicken Strips", "price": 8.99, "desc": "Strips"}}},
            "fish": {"name": "🐟 Fish & Chips", "items": {"FS1": {"name": "Cod & Chips", "price": 11.99, "desc": "Cod"}, "FS2": {"name": "Haddock & Chips", "price": 12.99, "desc": "Haddock"}, "FS3": {"name": "Fish Burger", "price": 9.99, "desc": "Burger"}, "FS4": {"name": "Scampi & Chips", "price": 10.99, "desc": "Scampi"}, "FS5": {"name": "Fish Goujons", "price": 8.99, "desc": "Goujons"}}},
            "pizza": {"name": "🍕 Pizza", "items": {"PZ1": {"name": "Margherita", "price": 10.99, "desc": "Classic"}, "PZ2": {"name": "Pepperoni", "price": 12.99, "desc": "Pepperoni"}, "PZ3": {"name": "BBQ Chicken", "price": 13.99, "desc": "BBQ"}, "PZ4": {"name": "Meat Feast", "price": 14.99, "desc": "Meat"}, "PZ5": {"name": "Veggie Supreme", "price": 12.99, "desc": "Veggie"}, "PZ6": {"name": "Buffalo Chicken", "price": 13.99, "desc": "Buffalo"}}},
            "wraps": {"name": "🌯 Wraps", "items": {"WR1": {"name": "Chicken Shawarma Wrap", "price": 8.99, "desc": "Wrap"}, "WR2": {"name": "Beef Shawarma Wrap", "price": 9.49, "desc": "Wrap"}, "WR3": {"name": "Chicken Kebab", "price": 9.99, "desc": "Kebab"}, "WR4": {"name": "Chicken Tikka Wrap", "price": 8.99, "desc": "Tikka"}, "WR5": {"name": "Falafel Wrap", "price": 7.99, "desc": "Falafel"}, "WR6": {"name": "Mixed Kebab", "price": 11.99, "desc": "Mixed"}}},
            "sides": {"name": "🍟 Sides", "items": {"SD1": {"name": "Chips", "price": 3.49, "desc": "Chips"}, "SD2": {"name": "Loaded Fries", "price": 5.99, "desc": "Loaded"}, "SD3": {"name": "Onion Rings", "price": 4.49, "desc": "Rings"}, "SD4": {"name": "Mozzarella Sticks", "price": 5.99, "desc": "Cheese"}, "SD5": {"name": "Coleslaw", "price": 2.99, "desc": "Slaw"}, "SD6": {"name": "Garlic Bread", "price": 3.99, "desc": "Bread"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CN1": {"name": "Chicken Fried Rice", "price": 9.99, "desc": "Rice"}, "CN2": {"name": "Chicken Chow Mein", "price": 10.99, "desc": "Mein"}, "CN3": {"name": "Sweet & Sour Chicken", "price": 11.49, "desc": "Sweet"}, "CN4": {"name": "Orange Chicken", "price": 11.49, "desc": "Orange"}, "CN5": {"name": "Chicken Teriyaki", "price": 11.99, "desc": "Teriyaki"}, "CN6": {"name": "Vegetable Noodles", "price": 8.99, "desc": "Noodles"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Coca Cola", "price": 2.49, "desc": "Soda"}, "DR2": {"name": "Pepsi", "price": 2.49, "desc": "Soda"}, "DR3": {"name": "Lemonade", "price": 2.99, "desc": "Lemonade"}, "DR4": {"name": "Iced Tea", "price": 2.99, "desc": "Tea"}, "DR5": {"name": "Milkshake", "price": 5.49, "desc": "Shake"}, "DR6": {"name": "Water", "price": 1.49, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "Cheesecake", "price": 5.49, "desc": "Cheesecake"}, "DS2": {"name": "Chocolate Brownie", "price": 5.49, "desc": "Brownie"}, "DS3": {"name": "Apple Pie", "price": 4.49, "desc": "Pie"}, "DS4": {"name": "Chocolate Cake", "price": 5.49, "desc": "Cake"}, "DS5": {"name": "Oreo Milkshake", "price": 6.49, "desc": "Shake"}}},
        }
    },

    "CA": {
        "country": "Canada",
        "code": "CA",
        "currency": "CAD",
        "symbol": "CAD $",
        "categories": {
            "deals": {"name": "🔥 Deals", "items": {"DL1": {"name": "Burger Combo", "price": 16.99, "desc": "Combo"}, "DL2": {"name": "Chicken Combo", "price": 15.99, "desc": "Combo"}, "DL3": {"name": "Wings & Fries", "price": 18.99, "desc": "Wings"}, "DL4": {"name": "Pizza & Wings", "price": 25.99, "desc": "Pizza"}, "DL5": {"name": "Family Meal", "price": 39.99, "desc": "Family"}, "DL6": {"name": "Burger Family Deal", "price": 34.99, "desc": "Deal"}}},
            "burgers": {"name": "🍔 Burgers", "items": {"BG1": {"name": "Classic Smash Burger", "price": 14.99, "desc": "Classic"}, "BG2": {"name": "Double Smash Burger", "price": 17.99, "desc": "Double"}, "BG3": {"name": "BBQ Bacon Burger", "price": 16.99, "desc": "BBQ"}, "BG4": {"name": "Spicy Chicken Burger", "price": 15.99, "desc": "Spicy"}, "BG5": {"name": "Crispy Chicken Burger", "price": 14.99, "desc": "Crispy"}, "BG6": {"name": "Mushroom Swiss Burger", "price": 16.49, "desc": "Mushroom"}}},
            "chicken": {"name": "🍗 Chicken", "items": {"CH1": {"name": "Chicken Tenders", "price": 12.99, "desc": "Tenders"}, "CH2": {"name": "Buffalo Wings 6pc", "price": 12.99, "desc": "Wings"}, "CH3": {"name": "Buffalo Wings 12pc", "price": 21.99, "desc": "Dozen"}, "CH4": {"name": "Crispy Chicken Sandwich", "price": 14.99, "desc": "Crispy"}, "CH5": {"name": "Grilled Chicken Sandwich", "price": 14.99, "desc": "Grilled"}, "CH6": {"name": "Nashville Chicken", "price": 15.99, "desc": "Hot"}}},
            "pizza": {"name": "🍕 Pizza", "items": {"PZ1": {"name": "Margherita", "price": 15.99, "desc": "Classic"}, "PZ2": {"name": "Pepperoni", "price": 17.99, "desc": "Pepperoni"}, "PZ3": {"name": "BBQ Chicken", "price": 19.99, "desc": "BBQ"}, "PZ4": {"name": "Meat Lovers", "price": 21.99, "desc": "Meat"}, "PZ5": {"name": "Veggie Supreme", "price": 18.99, "desc": "Veggie"}, "PZ6": {"name": "Buffalo Chicken", "price": 19.99, "desc": "Buffalo"}}},
            "poutine": {"name": "🍟 Poutine & Sides", "items": {"PT1": {"name": "Classic Poutine", "price": 8.99, "desc": "Poutine"}, "PT2": {"name": "Chicken Poutine", "price": 12.99, "desc": "Poutine"}, "PT3": {"name": "Loaded Fries", "price": 9.99, "desc": "Loaded"}, "PT4": {"name": "French Fries", "price": 5.49, "desc": "Fries"}, "PT5": {"name": "Onion Rings", "price": 6.99, "desc": "Rings"}, "PT6": {"name": "Mozzarella Sticks", "price": 8.99, "desc": "Sticks"}}},
            "wraps": {"name": "🌯 Wraps", "items": {"WR1": {"name": "Chicken Shawarma Wrap", "price": 11.99, "desc": "Wrap"}, "WR2": {"name": "Beef Shawarma Wrap", "price": 12.99, "desc": "Wrap"}, "WR3": {"name": "Crispy Chicken Wrap", "price": 11.99, "desc": "Crispy"}, "WR4": {"name": "Buffalo Chicken Wrap", "price": 12.99, "desc": "Buffalo"}, "WR5": {"name": "Falafel Wrap", "price": 10.99, "desc": "Falafel"}, "WR6": {"name": "Grilled Chicken Wrap", "price": 11.99, "desc": "Grilled"}}},
            "chinese": {"name": "🥢 Chinese", "items": {"CN1": {"name": "Chicken Fried Rice", "price": 14.99, "desc": "Rice"}, "CN2": {"name": "Chicken Chow Mein", "price": 15.99, "desc": "Mein"}, "CN3": {"name": "Orange Chicken", "price": 16.99, "desc": "Orange"}, "CN4": {"name": "Sweet & Sour Chicken", "price": 16.99, "desc": "Sweet"}, "CN5": {"name": "Chicken Teriyaki", "price": 16.99, "desc": "Teriyaki"}, "CN6": {"name": "Beef & Broccoli", "price": 17.99, "desc": "Beef"}}},
            "drinks": {"name": "🥤 Drinks", "items": {"DR1": {"name": "Coca Cola", "price": 3.49, "desc": "Soda"}, "DR2": {"name": "Pepsi", "price": 3.49, "desc": "Soda"}, "DR3": {"name": "Lemonade", "price": 4.49, "desc": "Lemonade"}, "DR4": {"name": "Iced Tea", "price": 3.99, "desc": "Tea"}, "DR5": {"name": "Milkshake", "price": 7.49, "desc": "Shake"}, "DR6": {"name": "Bottled Water", "price": 2.49, "desc": "Water"}}},
            "desserts": {"name": "🍰 Desserts", "items": {"DS1": {"name": "NY Cheesecake", "price": 7.49, "desc": "Cheesecake"}, "DS2": {"name": "Chocolate Brownie", "price": 6.99, "desc": "Brownie"}, "DS3": {"name": "Chocolate Cake", "price": 7.49, "desc": "Cake"}, "DS4": {"name": "Apple Pie", "price": 5.99, "desc": "Pie"}, "DS5": {"name": "Oreo Milkshake", "price": 8.49, "desc": "Shake"}}},
        }
    },
}

def get_menu(country_code):
    """Get complete menu for a country"""
    return MENUS.get(country_code, MENUS["PK"])

def get_country_from_phone(phone):
    """Detect country from phone number format"""
    # Remove + and spaces
    phone_clean = phone.replace("+", "").replace(" ", "")

    country_codes = {
        "92": "PK",
        "971": "AE",
        "966": "SA",
        "974": "QA",
        "965": "KW",
        "973": "BH",
        "968": "OM",
        "44": "GB",
    }

    # Check which country code matches
    for code, country in country_codes.items():
        if phone_clean.startswith(code):
            return country

    # For North America (+1), default to US (can enhance with area codes later)
    if phone_clean.startswith("1"):
        return "US"  # Default to US, could be CA

    # Default to Pakistan if unknown
    return "PK"

def get_currency_symbol(country_code):
    """Get currency symbol for country"""
    menu = get_menu(country_code)
    return menu.get("symbol", "Rs")

def get_currency_code(country_code):
    """Get currency code for country"""
    menu = get_menu(country_code)
    return menu.get("currency", "PKR")

def format_price(country_code, price):
    """Format price with currency"""
    menu = get_menu(country_code)
    symbol = menu.get("symbol", "")

    if country_code in ["US", "CA"]:
        return f"{symbol} {price:.2f}"
    elif country_code == "GB":
        return f"{symbol} {price:.2f}"
    elif country_code in ["KW", "BH", "OM"]:
        return f"{symbol} {price:.2f}"
    else:
        # For PKR, AED, SAR, QAR
        return f"{symbol} {price:,.0f}" if isinstance(price, int) else f"{symbol} {price}"

def get_category_list(country_code):
    """Get list of categories for a country"""
    menu = get_menu(country_code)
    categories = menu.get("categories", {})
    return [(key, value.get("name", key)) for key, value in categories.items()]

def get_category_items(country_code, category_key):
    """Get all items in a category"""
    menu = get_menu(country_code)
    categories = menu.get("categories", {})
    if category_key in categories:
        return categories[category_key].get("items", {})
    return {}
