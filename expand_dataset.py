import os
import pandas as pd
import re

def main():
    print("[ShopSense AI] Starting Catalog Database Expansion Pipeline...")
    
    csv_path = "data/products.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] Products CSV not found at {csv_path}. Please initialize the dataset first.")
        return
        
    df = pd.read_csv(csv_path)
    print(f"[ShopSense AI] Current database size: {len(df)} items.")
    
    # Define 150 NEW premium branded products (30 per category)
    # ------------------- 1. SKINCARE (30 Products) -------------------
    new_skincare = [
        ("Minimalist Salicylic Acid 2% Face Serum", 
         "Daily gentle exfoliant face serum with 2% Salicylic Acid for acne and blackheads in a dark amber glass bottle.", 
         "Skincare", "Serum", 549.00, "Amazon"),
        ("CeraVe Hydrating Facial Cleanser Face Wash", 
         "Dermatologist recommended non-foaming daily wash with ceramides in a clean white rectangular bottle with green pump.", 
         "Skincare", "Cleanser", 1250.00, "Amazon"),
        ("COSRX Advanced Snail 96 Mucin Power Essence", 
         "Ultra-hydrating daily skin repair essence formulated with 96.3% snail secretion filtrate in a clear sleek bottle.", 
         "Skincare", "Serum", 1450.00, "Flipkart"),
        ("Laneige Lip Sleeping Mask Berry Flavor", 
         "Deep nourishing lip treatment mask enriched with vitamin C and antioxidants in a signature frosted pink jar.", 
         "Skincare", "Moisturizer", 600.00, "Amazon"),
        ("L'Oreal Paris Glycolic Bright Serum", 
         "Radiance-boosting daily dark spots reduction face treatment in a glass bottle with dropper.", 
         "Skincare", "Serum", 699.00, "Flipkart"),
        ("Mamaearth Vitamin C Face Wash", 
         "Brightening foaming face cleanser with vitamin C and turmeric in an ergonomic squeeze tube.", 
         "Skincare", "Cleanser", 259.00, "Amazon"),
        ("The Derma Co 2% Salicylic Acid Face Serum", 
         "Clarifying acne reduction face serum with 2% Salicylic Acid in a sleek white glass dropper bottle.", 
         "Skincare", "Serum", 499.00, "Flipkart"),
        ("Garnier Bright Complete Vitamin C Serum", 
         "Fast-absorbing spot-less face serum formulated with vitamin C inside a clear dropper bottle.", 
         "Skincare", "Serum", 549.00, "Amazon"),
        ("Lotus Safe Sun UV Screen Matte Gel SPF 50", 
         "Non-greasy sun block sunscreen gel packaged inside a vibrant orange squeeze tube.", 
         "Skincare", "Sunscreen", 399.00, "Flipkart"),
        ("Plum Green Tea Alcohol-Free Toner", 
         "Alcohol-free pore contracting facial toner with green tea extracts in a frosted clear bottle.", 
         "Skincare", "Toner", 390.00, "Flipkart"),
        ("Cetaphil Moisturising Cream for Dry Skin", 
         "Dermatologist-recommended ultra-rich moisturizer cream for dry skin in a premium green-accented jar.", 
         "Skincare", "Moisturizer", 485.00, "Amazon"),
        ("Neutrogena Bright Boost Gel Moisturiser Cream", 
         "Skin resurfacing glow gel cream formulated with Neoglucosamine in a pink rounded jar.", 
         "Skincare", "Moisturizer", 950.00, "Amazon"),
        ("Himalaya Herbals Purifying Neem Face Pack", 
         "Herbal deep cleansing skin clearing face pack infused with neem and turmeric in a tube.", 
         "Skincare", "Cleanser", 160.00, "Amazon"),
        ("Forest Essentials Luxury Ayurvedic Soap Saffron", 
         "Handmade Ayurvedic bathing bar showcasing pure Kashmiri saffron and almond oil extracts.", 
         "Skincare", "Cleanser", 475.00, "Amazon"),
        ("Biotique Bio Dandelion Visibly Ageless Serum", 
         "Botanical age-defying skin lightening face serum in a green cylindrical bottle.", 
         "Skincare", "Serum", 230.00, "Flipkart"),
        ("Minimalist Niacinamide 10% Face Serum", 
         "Acne marks and blemishes reduction face serum with pure Niacinamide in dark amber bottle.", 
         "Skincare", "Serum", 599.00, "Amazon"),
        ("Kama Ayurveda Kumkumadi Miraculous Beauty Fluid", 
         "Ultra-premium traditional Ayurvedic overnight face beauty oil in a classic gold-labeled glass bottle.", 
         "Skincare", "Serum", 2995.00, "Amazon"),
        ("Mamaearth Onion Hair Oil for Hair Fall", 
         "Anti-hair fall scalp nourishing oil enriched with Red Onion extracts in a white pump bottle.", 
         "Skincare", "Moisturizer", 399.00, "Amazon"),
        ("Wow Skin Science Onion Black Seed Hair Oil", 
         "Nourishing daily hair oil with onion black seed extracts inside an ergonomic brown bottle.", 
         "Skincare", "Moisturizer", 349.00, "Flipkart"),
        ("Neutrogena Deep Clean Facial Cleanser", 
         "Glycerin-rich daily pore deep cleaning facial wash in a sleek translucent orange bottle.", 
         "Skincare", "Cleanser", 399.00, "Amazon"),
         
        # New additions for catalog expansion (30 items total)
        ("The Ordinary Niacinamide 10% + Zinc 1%",
         "High-strength vitamin and mineral blemish formula with 10% pure Niacinamide in clean frosted bottle.",
         "Skincare", "Serum", 600.00, "Amazon"),
        ("CeraVe Foaming Facial Cleanser Face Wash",
         "Daily foaming gel cleanser for normal to oily skin featuring three essential ceramides in blue-accented bottle.",
         "Skincare", "Cleanser", 1450.00, "Amazon"),
        ("Minimalist SPF 50 Multi Vitamin Sunscreen",
         "Lightweight daily sunscreen cream enriched with multi-vitamins for complete sun protection and repair.",
         "Skincare", "Sunscreen", 399.00, "Amazon"),
        ("The Derma Co 1% Hyaluronic Sunscreen Aqua Gel",
         "Highly protective non-greasy sunscreen gel with SPF 50 and active hyaluronic acid.",
         "Skincare", "Sunscreen", 499.00, "Flipkart"),
        ("Laneige Water Sleeping Mask Hydration Gel",
         "Premium overnight hydrating sleeping mask that deeply moisturizes the skin during sleep.",
         "Skincare", "Moisturizer", 2000.00, "Amazon"),
        ("COSRX Low pH Good Morning Gel Cleanser",
         "Mild everyday skin-clearing gel cleanser formulated with purifying botanical extracts.",
         "Skincare", "Cleanser", 850.00, "Flipkart"),
        ("The Ordinary Glycolic Acid 7% Toning Solution",
         "Exfoliating toning solution offering mild exfoliation for improved skin radiance and clarity.",
         "Skincare", "Toner", 950.00, "Amazon"),
        ("CeraVe Moisturizing Cream with Ceramides",
         "Rich daily moisturizer cream developed with dermatologists to restore skin barrier health.",
         "Skincare", "Moisturizer", 1350.00, "Amazon"),
        ("Minimalist 2% Alpha Arbutin Face Serum",
         "Skin brightening daily serum designed to fade hyperpigmentation and dark spots safely.",
         "Skincare", "Serum", 399.00, "Flipkart"),
        ("L'Oreal Paris Revitalift Crystal Micro-Essence",
         "Ultra-lightweight skin-repairing treatment essence featuring salicylic acid for crystal clear skin.",
         "Skincare", "Serum", 899.00, "Amazon")
    ]
    
    # ------------------- 2. SHOES (30 Products) -------------------
    new_shoes = [
        ("Adidas Originals Men's Stan Smith Sneakers", 
         "Timeless court sneakers crafted in clean white leather accented with iconic green heel tabs.", 
         "Shoes", "Sneakers", 8999.00, "Amazon"),
        ("Nike Air Force 1 '07 Sneakers", 
         "Iconic retro low-top street sneakers featuring pure white durable leather paneling and thick soles.", 
         "Shoes", "Sneakers", 9695.00, "Amazon"),
        ("Puma Suede Classic Unisex Sneakers", 
         "Vintage lifestyle court sneakers made from smooth soft black suede with a signature side swoop.", 
         "Shoes", "Sneakers", 5499.00, "Amazon"),
        ("Reebok Club C 85 Sneakers", 
         "Retro athletic heritage court trainers built in premium cream white leather with custom rubber soles.", 
         "Shoes", "Sneakers", 6999.00, "Amazon"),
        ("Converse Chuck Taylor All Star High Top", 
         "Classic canvas high-top retro basketball shoes featuring iconic round star ankle patch.", 
         "Shoes", "Sneakers", 4299.00, "Amazon"),
        ("Vans Old Skool Unisex Skate Shoes", 
         "Legendary side-striped low-top skate shoes featuring durable black canvas and suede uppers.", 
         "Shoes", "Sneakers", 4999.00, "Amazon"),
        ("Under Armour Men's Hovr Sonic Running Shoes", 
         "High-performance long-distance running shoes equipped with Hovr energy-return cushioning.", 
         "Shoes", "Running", 8999.00, "Amazon"),
        ("Skechers Men's Go Run Consistent Running Shoes", 
         "Ultra-lightweight mesh sports running shoes featuring comfortable Goga Mat custom cushioning.", 
         "Shoes", "Running", 4499.00, "Amazon"),
        ("Fila Men's Disruptor II Premium Sneakers", 
         "Iconic chunky profile retro lifestyle fashion sneakers featuring jagged-style rubber outer soles.", 
         "Shoes", "Sneakers", 5999.00, "Flipkart"),
        ("ASICS Men's Gel-Venture 9 Hiking Shoes", 
         "Rugged outdoor technical trail running and hiking shoes built with deep grip traction soles.", 
         "Shoes", "Hiking", 5999.00, "Amazon"),
        ("Bata Men's Formal Dress Monk Strap Shoes", 
         "Polished business formal dress shoes featuring a double monk strap buckle in cognac brown leather.", 
         "Shoes", "Formal", 2499.00, "Flipkart"),
        ("Woodland Men's High-Top Nubuck Boots", 
         "Iconic rugged high-top outdoor utility boots crafted in durable camel yellow nubuck leather.", 
         "Shoes", "Boots", 4995.00, "Flipkart"),
        ("Puma RS-X Reinvention Unisex Sneakers", 
         "Futuristic dynamic fashion lifestyle sneakers featuring heavily layered synthetic panels.", 
         "Shoes", "Sneakers", 8999.00, "Amazon"),
        ("Adidas Men's Lite Racer Adapt Sneakers", 
         "Comfortable athletic slip-on sock-like running trainers featuring bold logo elastic bands.", 
         "Shoes", "Running", 4999.00, "Amazon"),
        ("Campus Men's Retro Gym Walking Shoes", 
         "Comfortable daily sports walking sneakers engineered with supportive knit upper and soft sole.", 
         "Shoes", "Walking", 1299.00, "Flipkart"),
        ("Red Tape Men's Classic Leather Loafers", 
         "Elegant formal bifold slip-on dress loafers made from smooth premium black genuine leather.", 
         "Shoes", "Formal", 1999.00, "Flipkart"),
        ("Sparx Men's Canvas Everyday Sneakers", 
         "Classic casual lace-up lightweight canvas trainers styled in a clean solid navy blue colorway.", 
         "Shoes", "Sneakers", 999.00, "Flipkart"),
        ("US Polo Assn Men's Casual Slip-On Shoes", 
         "Sporty low-profile slip-on walking deck shoes engineered in lightweight breathable canvas.", 
         "Shoes", "Loafers", 2499.00, "Flipkart"),
        ("Nike Air Max 90 Classic Sneakers", 
         "Iconic heritage sneakers featuring visible Max Air cushioning and durable leather overlays.", 
         "Shoes", "Sneakers", 11995.00, "Amazon"),
        ("Crocs Unisex Crocband Clogs", 
         "Vintage sporty design casual indoor/outdoor foam clogs complete with dynamic colored stripes.", 
         "Shoes", "Clogs", 3495.00, "Amazon"),
         
        # New additions for catalog expansion (30 items total)
        ("Nike Court Royale 2 Low-Top Sneakers",
         "Classic daily tennis-style court sneakers featuring durable leather upper and swoosh logo.",
         "Shoes", "Sneakers", 4595.00, "Amazon"),
        ("Adidas Duramo Speed Running Shoes",
         "Comfortable, high-speed lightweight gym running shoes featuring standard mesh upper.",
         "Shoes", "Running", 5999.00, "Amazon"),
        ("Puma Carson 2 Unisex Running Shoes",
         "Everyday low-top sports trainers constructed with breathable mesh and comfortable foam sole.",
         "Shoes", "Running", 2999.00, "Amazon"),
        ("Reebok Energen Run Sports Sneakers",
         "Sleek active lifestyle athletic sneakers featuring supportive synthetic overlays.",
         "Shoes", "Sneakers", 3499.00, "Amazon"),
        ("Converse Chuck Taylor All Star Low Top",
         "Low-profile casual lifestyle canvas trainers finished in retro white shade.",
         "Shoes", "Sneakers", 3999.00, "Amazon"),
        ("Vans Slip-On Classic Unisex Skate Shoes",
         "Timeless retro skate slip-on shoes constructed with black canvas panels.",
         "Shoes", "Sneakers", 4499.00, "Amazon"),
        ("Under Armour Charged Pursuit 3 Sneakers",
         "Lightweight flexible sports trainers engineered with charging foam midsole support.",
         "Shoes", "Running", 5499.00, "Amazon"),
        ("Skechers Men's Elite Flex Prime Sneakers",
         "Advanced comfort slip-on walking shoes featuring high-rebound cushioning foam.",
         "Shoes", "Walking", 5999.00, "Amazon"),
        ("Fila Men's Ray Tracer Retro Chunky Shoes",
         "Multi-layered athletic fashion lifestyle trainers with unique jagged outer soles.",
         "Shoes", "Sneakers", 6999.00, "Flipkart"),
        ("ASICS Men's Gel-Contend 8 Gym Shoes",
         "Supportive indoor training and walking shoes featuring protective gel cushioning.",
         "Shoes", "Walking", 3799.00, "Amazon")
    ]
    
    # ------------------- 3. ELECTRONICS (30 Products) -------------------
    new_electronics = [
        ("Sony WH-1000XM5 Noise Cancelling Headphones", 
         "Next-generation industry-leading active noise cancelling wireless headphones finished in matte silver.", 
         "Electronics", "Audio", 29990.00, "Amazon"),
        ("Bose QuietComfort Wireless Noise Cancelling Headphones", 
         "Legendary comfortable noise cancelling wireless headphones in a sleek triple black finish.", 
         "Electronics", "Audio", 25900.00, "Amazon"),
        ("Marshall Major IV Wireless On-Ear Headphones", 
         "Classic retro square-ear wireless headphones with signature black textured vinyl finish.", 
         "Electronics", "Audio", 12999.00, "Amazon"),
        ("Sennheiser HD 450SE Bluetooth Headphones", 
         "Premium audiophile-grade active noise cancelling wireless headphones in matte black.", 
         "Electronics", "Audio", 9990.00, "Amazon"),
        ("JBL Tune 770NC Wireless Headphones", 
         "Affordable wireless over-ear noise cancelling headphones in elegant deep royal blue.", 
         "Electronics", "Audio", 6499.00, "Amazon"),
        ("OnePlus Buds Pro 2 True Wireless Earbuds", 
         "Premium dual-driver true wireless earbuds featuring spatial audio inside a green charging case.", 
         "Electronics", "Audio", 9999.00, "Amazon"),
        ("Realme Buds Air 5 Pro Wireless Earbuds", 
         "High-resolution wireless earbuds featuring 50dB active noise cancellation in white.", 
         "Electronics", "Audio", 4999.00, "Flipkart"),
        ("boAt Airdopes 141 True Wireless Earbuds", 
         "Affordable true wireless earbuds featuring dynamic bass inside a charcoal grey case.", 
         "Electronics", "Audio", 1299.00, "Amazon"),
        ("Nothing Ear (2) True Wireless Earbuds", 
         "Iconic transparent design wireless earbuds featuring custom active noise cancellation.", 
         "Electronics", "Audio", 8999.00, "Amazon"),
        ("Anker Soundcore Life Q30 Headphones", 
         "Highly rated over-ear hybrid active noise cancelling wireless headphones in matte black.", 
         "Electronics", "Audio", 6999.00, "Amazon"),
        ("Logitech MX Master 3S Wireless Mouse", 
         "Premium ergonomic precision mouse featuring custom MagSpeed scroll wheel in pale grey.", 
         "Electronics", "Computers", 9495.00, "Amazon"),
        ("Keychron K2 Mechanical Gaming Keyboard", 
         "Compact wireless mechanical keyboard featuring high-quality keycaps and RGB backlighting.", 
         "Electronics", "Computers", 6999.00, "Amazon"),
        ("HP Wireless Keyboard and Mouse Combo CS10", 
         "Minimalist daily office computer input combo in matching textured black profile.", 
         "Electronics", "Computers", 1299.00, "Amazon"),
        ("Seagate Expansion 1TB External Hard Drive HDD", 
         "Compact portable external hard drive in structured black plastic for data expansion.", 
         "Electronics", "Accessories", 4499.00, "Amazon"),
        ("SanDisk Extreme Portable 1TB SSD", 
         "Rugged water-resistant high-speed portable solid state drive featuring an orange carry loop.", 
         "Electronics", "Accessories", 9999.00, "Amazon"),
        ("TP-Link Tapo C200 Smart Security Camera", 
         "Home security 360-degree pan/tilt Wi-Fi camera with high-definition night vision.", 
         "Electronics", "Smart Home", 2299.00, "Amazon"),
        ("Amazon Kindle Paperwhite 16GB", 
         "Waterproof e-reader featuring a large high-resolution glare-free display and warm light.", 
         "Electronics", "Smart Home", 14999.00, "Amazon"),
        ("Mi Box 4K Media Streaming Device", 
         "Smart TV streaming player featuring 4K HDR playback and built-in Chromecast.", 
         "Electronics", "Smart Home", 3499.00, "Amazon"),
        ("Wipro Smart LED Bulb 9W", 
         "RGB smart home Wi-Fi automation light bulb customizable via app controls.", 
         "Electronics", "Smart Home", 699.00, "Amazon"),
        ("Philips HD9200/90 Air Fryer", 
         "Compact kitchen air fryer styled in polished black housing with analog timer dials.", 
         "Electronics", "Home Appliances", 5999.00, "Flipkart"),
         
        # New additions for catalog expansion (30 items total)
        ("Bose QuietComfort Ultra Earbuds",
         "State-of-the-art true wireless earbuds with custom spatial audio and noise cancellation.",
         "Electronics", "Audio", 29900.00, "Amazon"),
        ("Sony WF-C700N Noise Cancelling Earbuds",
         "Comfortable, lightweight active noise cancelling wireless in-ear earbuds in sage green.",
         "Electronics", "Audio", 7990.00, "Amazon"),
        ("JBL Flip 6 Portable Bluetooth Speaker",
         "Waterproof portable outdoor speaker featuring a powerful two-way sound system.",
         "Electronics", "Audio", 9999.00, "Flipkart"),
        ("Logitech MX Keys S Wireless Keyboard",
         "Elite, low-profile mechanical-feel quiet wireless keyboard with smart backlighting.",
         "Electronics", "Computers", 12995.00, "Amazon"),
        ("Logitech G502 Hero Gaming Mouse",
         "High-performance optical sensor wired gaming mouse featuring custom RGB weights.",
         "Electronics", "Computers", 4495.00, "Amazon"),
        ("SanDisk Extreme PRO 128GB USB Drive",
         "Ultra-high-speed solid state USB 3.2 flash drive in robust metal casing.",
         "Electronics", "Accessories", 1999.00, "Amazon"),
        ("TP-Link Tapo C310 Outdoor Camera",
         "Weatherproof high-definition smart home outdoor Wi-Fi security camera.",
         "Electronics", "Smart Home", 3499.00, "Amazon"),
        ("Amazon Fire TV Stick 4K Max",
         "Premium media streaming device with cinematic 4K streaming and Wi-Fi 6 support.",
         "Electronics", "Smart Home", 6499.00, "Amazon"),
        ("Wipro Smart Extension Strip 4-Socket",
         "Smart Wi-Fi automation extension power strip customizable via Alexa controls.",
         "Electronics", "Smart Home", 1999.00, "Amazon"),
        ("Philips Daily Collection Air Fryer HD9252",
         "Advanced multi-cook air fryer with digital touch screen UI panel.",
         "Electronics", "Home Appliances", 7999.00, "Flipkart")
    ]
    
    # ------------------- 4. FASHION (30 Products) -------------------
    new_fashion = [
        ("Zara Men's Linen Blend Overshirt", 
         "Elegant lightweight linen-cotton blend buttoned overshirt jacket in clean sand color.", 
         "Fashion", "Shirt", 2990.00, "Amazon"),
        ("H&M Men's Denim Classic Shirt", 
         "Classic relaxed fit casual shirt crafted in light washed indigo blue denim fabric.", 
         "Fashion", "Shirt", 1499.00, "Amazon"),
        ("Nike Sportswear Men's Windrunner Jacket", 
         "Classic hooded lightweight sports windbreaker jacket featuring geometric panel lines.", 
         "Fashion", "Outerwear", 4995.00, "Amazon"),
        ("Adidas Originals Men's Trefoil Hoodie", 
         "Pullover winter warm hoodie in black cotton fleece showcasing the iconic white brand logo.", 
         "Fashion", "Hoodie", 3999.00, "Amazon"),
        ("Levi's 501 Original Fit Denim Jeans", 
         "Straight leg button-fly vintage jeans in classic indigo blue heavy denim.", 
         "Fashion", "Jeans", 3299.00, "Amazon"),
        ("Puma Active Men's Fleece Tracksuit", 
         "Full-zip sports athletic training jacket and pants set in sleek dark grey.", 
         "Fashion", "Activewear", 3999.00, "Amazon"),
        ("Allen Solly Men's Classic Oxford Formal Shirt", 
         "Crisp business office formal dress shirt in premium textured light blue cotton.", 
         "Fashion", "Shirt", 1299.00, "Flipkart"),
        ("Tommy Hilfiger Men's Chino Trousers", 
         "Premium slim fit smart-casual chino trousers crafted in durable beige cotton.", 
         "Fashion", "Pants", 3999.00, "Amazon"),
        ("Jack & Jones Men's Classic Crewneck Tee", 
         "Minimalist street-style crewneck t-shirt made of high-quality organic black cotton.", 
         "Fashion", "T-Shirt", 899.00, "Flipkart"),
        ("Wildcraft Unisex Waterproof Windcheater", 
         "High-performance windproof and water-resistant sports jacket in active color.", 
         "Fashion", "Outerwear", 1999.00, "Amazon"),
        ("Vero Moda Women's Skinny Jeans", 
         "High-waisted body-hugging daily wear jeans in solid dark blue stretch denim.", 
         "Fashion", "Jeans", 2499.00, "Flipkart"),
        ("Only Women's Regular Fit Denim Jacket", 
         "Flowy casual trucker denim jacket featuring classic metallic button accents.", 
         "Fashion", "Jacket", 2999.00, "Flipkart"),
        ("Biba Women's Traditional Anarkali Kurta Set", 
         "Elegant ethnic Indian dress set decorated with delicate gold print details.", 
         "Fashion", "Ethnic", 3999.00, "Flipkart"),
        ("H&M Women's Ribbed Knit Turtleneck Sweater", 
         "Cozy high-collar winter knit pullover sweater styled in premium beige yarn.", 
         "Fashion", "Sweater", 2299.00, "Amazon"),
        ("Zara Women's Classic Trench Coat", 
         "Sophisticated double-breasted long winter trench coat in classic camel color.", 
         "Fashion", "Outerwear", 5990.00, "Amazon"),
        ("Puma Women's Sports Gym Training Leggings", 
         "High-performance moisture-wicking active tights featuring dynamic white accents.", 
         "Fashion", "Activewear", 2299.00, "Flipkart"),
        ("Adidas Women's Trefoil Slim Tee", 
         "Sporty lifestyle casual short sleeve t-shirt in pure organic white cotton.", 
         "Fashion", "T-Shirt", 1499.00, "Amazon"),
        ("US Polo Assn Men's Cable Knit Sweater", 
         "Elegant winter formal long-sleeve knit pullover styled in classic navy blue.", 
         "Fashion", "Sweater", 2999.00, "Flipkart"),
        ("Peter England Men's Formal Suit Blazer", 
         "Polished business dress blazer featuring structured shoulders and black lining.", 
         "Fashion", "Suit", 4999.00, "Flipkart"),
        ("Van Heusen Men's Formal Cotton Dress Shirt", 
         "Crisp premium white formal office dress shirt featuring structured collar.", 
         "Fashion", "Shirt", 1799.00, "Flipkart"),
         
        # New additions for catalog expansion (30 items total)
        ("Zara Men's Structured Knit Blazer Jacket",
         "Chic smart-casual knit blazer jacket featuring structured shoulders and front button closures.",
         "Fashion", "Jacket", 5990.00, "Amazon"),
        ("H&M Men's Linen Regular Fit Casual Shirt",
         "Cool, lightweight daily linen casual shirt styled in clean white shade.",
         "Fashion", "Shirt", 1999.00, "Amazon"),
        ("Nike Club Fleece Mens Crewneck Sweatshirt",
         "Sporty fleece casual sweatshirt featuring comfortable crewneck fit and brand logo.",
         "Fashion", "Sweatshirt", 3295.00, "Amazon"),
        ("Adidas Men's Essentials 3-Stripes Trackpants",
         "Comfortable sports athletic joggers featuring classic three side stripes.",
         "Fashion", "Activewear", 2499.00, "Amazon"),
        ("Levi's Men's 512 Slim Tapered Fit Jeans",
         "Modern tapered fit blue stretch denim lifestyle jeans with light fade details.",
         "Fashion", "Jeans", 3499.00, "Amazon"),
        ("Puma Men's Training Full-Zip Gym Jacket",
         "Active athletic full-zip workout jacket styled in lightweight black fabric.",
         "Fashion", "Outerwear", 2999.00, "Amazon"),
        ("Allen Solly Men's Cotton Chino Slim Pants",
         "Polished everyday casual khaki trousers featuring a modern slim fit.",
         "Fashion", "Pants", 1699.00, "Flipkart"),
        ("Tommy Hilfiger Men's Flag Logo Crewneck Tee",
         "Luxury street casual t-shirt made from organic long-staple grey cotton.",
         "Fashion", "T-Shirt", 1999.00, "Amazon"),
        ("Zara Women's Plaid Tweed Crop Jacket",
         "Elegant cropped jacket styled in premium multi-color checked tweed fabrics.",
         "Fashion", "Jacket", 4990.00, "Amazon"),
        ("H&M Women's Oversized Denim Blue Jacket",
         "Modern relaxed trucker casual denim jacket in light blue washed finish.",
         "Fashion", "Jacket", 2999.00, "Amazon")
    ]
    
    # ------------------- 5. ACCESSORIES (30 Products) -------------------
    new_accessories = [
        ("Casio G-Shock DW-5600 Matte Black Watch", 
         "Legendary waterproof shock-resistant digital watch in absolute matte black.", 
         "Accessories", "Watches", 5495.00, "Amazon"),
        ("Daniel Wellington Classic Sheffield Watch", 
         "Minimalist luxury dress timepiece featuring ultra-thin rose gold case and black leather strap.", 
         "Accessories", "Watches", 11999.00, "Amazon"),
        ("Fossil Neutra Chronograph Analog Watch", 
         "Premium bold dial dress chronograph watch featuring a brown leather strap.", 
         "Accessories", "Watches", 11995.00, "Amazon"),
        ("Titan Workwear Classic Analog Dial Watch", 
         "Elegant daily business watch in clean silver-plated stainless steel band.", 
         "Accessories", "Watches", 3495.00, "Flipkart"),
        ("Timex Expedition Scout Outdoor Watch", 
         "Rugged military-style outdoor sports watch with durable green canvas band.", 
         "Accessories", "Watches", 4495.00, "Amazon"),
        ("Ray-Ban Clubmaster Classic Sunglasses", 
         "Iconic retro browline sunglasses featuring tortoiseshell frames and gold wiring.", 
         "Accessories", "Eyewear", 9890.00, "Amazon"),
        ("Oakley Holbrook Sport Matte Black Sunglasses", 
         "High-performance active sports sunglasses featuring polarized square lenses.", 
         "Accessories", "Eyewear", 8990.00, "Amazon"),
        ("Fastrack Polarized Sporty Sunglasses", 
         "Aerodynamic casual active sunglasses designed in lightweight black acetate.", 
         "Accessories", "Eyewear", 1299.00, "Flipkart"),
        ("Tommy Hilfiger Leather Bifold Logo Wallet", 
         "Slim classic pocket wallet constructed in high-end brown genuine leather.", 
         "Accessories", "Wallets", 2499.00, "Amazon"),
        ("Fossil Logan Leather Card Case Wallet", 
         "Minimalist compact card holder wallet made from premium textured leather.", 
         "Accessories", "Wallets", 1995.00, "Amazon"),
        ("Puma Deck Backpack 24L Sports Bag", 
         "Durable sports training backpack featuring dual side mesh bottle slots.", 
         "Accessories", "Bags", 1799.00, "Amazon"),
        ("Skybags Cabin Rolling Luggage Trooper 55cm", 
         "Premium cabin rolling suitcase featuring high-impact hard shell and graphics.", 
         "Accessories", "Bags", 3499.00, "Flipkart"),
        ("Wildcraft Commuter Laptop Backpack 35L", 
         "Dynamic commuter backpack equipped with a padded laptop compartment.", 
         "Accessories", "Bags", 1899.00, "Flipkart"),
        ("Safari Pentagon 55cm Cabin Suitcase", 
         "Cabin rolling trolley suitcase featuring a textured blue shell.", 
         "Accessories", "Bags", 2499.00, "Flipkart"),
        ("Decathlon Quechua Hiking Flask 1L", 
         "Insulated vacuum travel thermos flask in brushed silver steel.", 
         "Accessories", "Drinkware", 899.00, "Flipkart"),
        ("Milton Thermosteel Flask Duo DLX 500", 
         "Compact stainless steel travel water bottle with custom leakproof lid.", 
         "Accessories", "Drinkware", 699.00, "Flipkart"),
        ("Decathlon Kipsta 20L Gym Duffel Bag", 
         "Compact gym training travel duffel bag made of water-resistant material.", 
         "Accessories", "Bags", 499.00, "Flipkart"),
        ("Nivea Men's Protect & Care Deodorant", 
         "Refreshing, mild daily spray fragrance for long-lasting odor protection.", 
         "Accessories", "Personal Care", 249.00, "Amazon"),
        ("Park Avenue Men's Classic Cologne Spray", 
         "Elegant traditional masculine cologne fragrance in a sleek matte bottle.", 
         "Accessories", "Personal Care", 399.00, "Flipkart"),
        ("Forest Essentials Hair Cleanser Saffron", 
         "Ultra-premium traditional Ayurvedic daily shampoo showcasing Kashmiri saffron extracts.", 
         "Accessories", "Personal Care", 1475.00, "Amazon"),
         
        # New additions for catalog expansion (30 items total)
        ("Fossil Machine Black Metal Watch",
         "Premium bold dial chronograph sports watch styled with stainless steel black mesh band.",
         "Accessories", "Watches", 12495.00, "Amazon"),
        ("Casio Vintage Gold Watch",
         "Retro classic square gold-finished digital watch featuring daily alarms.",
         "Accessories", "Watches", 5495.00, "Amazon"),
        ("Daniel Wellington Petite Melrose Watch",
         "Minimalist dress watch featuring ultra-thin gold case and white dial with mesh strap.",
         "Accessories", "Watches", 13999.00, "Amazon"),
        ("Timex Weekender Mens watch",
         "Classic military-style analog dial field watch complete with indigo backlighting.",
         "Accessories", "Watches", 3995.00, "Amazon"),
        ("Ray-Ban Justin Matte Sunglasses",
         "Cool urban classic square sunglasses featuring matte black frames.",
         "Accessories", "Eyewear", 7890.00, "Amazon"),
        ("Oakley Frogskins Sporty Sunglasses",
         "Classic sporty lifestyle sunglasses featuring polarized iridium lenses.",
         "Accessories", "Eyewear", 8490.00, "Amazon"),
        ("Wildhorn RFID Leather Card Case Wallet",
         "Ultra-slim card holder wallet featuring RFID blocking shields and premium leather finish.",
         "Accessories", "Wallets", 499.00, "Amazon"),
        ("Puma Challenger Gym Duffel Bag 35L",
         "Medium athletic training duffel bag featuring supportive carry straps.",
         "Accessories", "Bags", 1499.00, "Amazon"),
        ("Safari Pentagon 65cm Checked Suitcase",
         "Highly secure checked medium rolling trolley suitcase structured with blue shell design.",
         "Accessories", "Bags", 3299.00, "Flipkart"),
        ("Skybags Brat 25L Casual School Backpack",
         "Trendy compact student daypack featuring padded mesh shoulder straps.",
         "Accessories", "Bags", 899.00, "Flipkart")
    ]
    
    # Combine lists
    new_categories = [
        (new_skincare, "skincare"),
        (new_shoes, "shoes"),
        (new_electronics, "electronics"),
        (new_fashion, "fashion"),
        (new_accessories, "accessories")
    ]
    
    # Parse existing items
    existing_items = df.to_dict('records')
    
    # Filter out any expanded records from the previous run (retaining only first 100 seeded items)
    # We will rebuild items 101 to 250 cleanly!
    existing_items = existing_items[:100]
    
    global_id = len(existing_items) + 1
    new_records = []
    
    for list_data, cat_label in new_categories:
        for title, desc, cat, subcat, price, platform in list_data:
            prod_id = f"PROD_{global_id:03d}"
            filename = f"prod_{global_id:03d}_{cat_label}.jpg"
            local_path = f"data/images/{filename}"
            t_query = title.replace(" ", "+")
            
            # Setup working search link
            if platform == "Amazon":
                target_link = f"https://www.amazon.in/s?k={t_query}"
            else:
                target_link = f"https://www.flipkart.com/search?q={t_query}"
                
            new_records.append({
                "id": prod_id,
                "title": title,
                "category": cat,
                "subcategory": subcat,
                "price": price,
                "platform": platform,
                "link": target_link,
                "description": desc,
                "unsplash_url": "https://images.unsplash.com/photo-placeholder",
                "local_path": local_path
            })
            global_id += 1
            
    # Concatenate and save
    all_items = existing_items + new_records
    new_df = pd.DataFrame(all_items)
    
    # Perform strict Deduplication Check
    print("\n--- [SECTOR MONITOR]: INITIATING DATABASE INTEGRITY DEDUPLICATION CHECKS ---")
    duplicate_titles = new_df[new_df.duplicated(subset=['title'], keep=False)]
    if not duplicate_titles.empty:
        print(f"[WARNING]: Detected {len(duplicate_titles)} duplicate title records! Cleaning duplicates...")
        # Since we are rebuilding, there shouldn't be duplicate titles in the source lists.
        # But if there are, we drop duplicates to keep it pristine.
        new_df = new_df.drop_duplicates(subset=['title'], keep='first')
        # Re-index IDs to remain sequential
        for idx in range(len(new_df)):
            orig_row = new_df.iloc[idx]
            new_df.iloc[idx, new_df.columns.get_loc('id')] = f"PROD_{idx+1:03d}"
            cat_lbl = orig_row['category'].lower()
            if cat_lbl == "skincare":
                cat_lbl = "skincare"
            elif cat_lbl == "shoes":
                cat_lbl = "shoes"
            elif cat_lbl == "electronics":
                cat_lbl = "electronics"
            elif cat_lbl == "fashion":
                cat_lbl = "fashion"
            else:
                cat_lbl = "accessories"
            new_df.iloc[idx, new_df.columns.get_loc('local_path')] = f"data/images/prod_{idx+1:03d}_{cat_lbl}.jpg"
            
    new_df.to_csv(csv_path, index=False)
    print(f"[ShopSense AI] Expanded dataset successfully! Total clean catalog nodes: {len(new_df)}/250 records.")

if __name__ == "__main__":
    main()
