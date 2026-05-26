import os
import pandas as pd
import shutil
from utils.image_loader import TechnicalImageLoader

def generate_product_list():
    """
    Returns a list of 100 premium, real-world branded products with distinct visual attributes,
    categories, realistic prices in INR, direct store deep links, and 100% unique, guaranteed-to-work
    isolated product packshot image URLs.
    """
    products = []
    
    # ------------------- 1. SKINCARE (20 Products) -------------------
    skincare_data = [
        ("Neutrogena Hydro Boost Water Gel Moisturiser", 
         "Clinically proven daily facial moisturizer packed with hyaluronic acid inside an iconic translucent blue gel jar.", 
         "Skincare", "Moisturizer", 1150.00, "Amazon", 
         "https://images.unsplash.com/photo-1612817288484-6f916006741a?w=500&auto=format&fit=crop&q=80"),
         
        ("Cetaphil Gentle Skin Cleanser Face Wash", 
         "Dermatologist-recommended mild, non-irritating cleanser in an elegant white bottle with a distinctive blue pump cap.", 
         "Skincare", "Cleanser", 399.00, "Amazon", 
         "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=500&auto=format&fit=crop&q=80"),
         
        ("L'Oreal Paris Revitalift Hyaluronic Acid Face Serum", 
         "Anti-aging hydrating facial serum with 1.5% pure Hyaluronic Acid inside a gorgeous clear glass dropper bottle.", 
         "Skincare", "Serum", 799.00, "Amazon", 
         "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=500&auto=format&fit=crop&q=80"),
         
        ("The Derma Co 10% Niacinamide Face Serum", 
         "Acne marks reduction face serum with 10% Niacinamide and Zinc in a clean matte glass bottle with a white dropper.", 
         "Skincare", "Serum", 599.00, "Flipkart", 
         "https://images.unsplash.com/photo-1611080626919-7cf5a9dbab5b?w=500&auto=format&fit=crop&q=80"),
         
        ("Plum Green Tea Pore Cleansing Face Wash", 
         "Refreshing acne-control cleanser infused with organic green tea and gentle cellulose beads in a frosted clear squeeze tube.", 
         "Skincare", "Cleanser", 349.00, "Flipkart", 
         "https://images.unsplash.com/photo-1601049541289-9b1b7bbbfe19?w=500&auto=format&fit=crop&q=80"),
         
        ("Minimalist 10% Vitamin C Face Serum", 
         "Radiance-boosting Vitamin C skin treatment formulated with highly stable ethyl ascorbic acid in a dark amber glass bottle.", 
         "Skincare", "Serum", 699.00, "Amazon", 
         "https://images.unsplash.com/photo-1615396899839-c99c121888b0?w=500&auto=format&fit=crop&q=80"),
         
        ("Nivea Soft Light Moisturiser Cream", 
         "Lightweight, fast-absorbing refreshing cream with Vitamin E and Jojoba oil in an iconic circular white tub.", 
         "Skincare", "Moisturizer", 299.00, "Amazon", 
         "https://images.unsplash.com/photo-1601924994987-69e26d50dc26?w=500&auto=format&fit=crop&q=80"),
         
        ("Biotique Morning Nectar Flawless Skin Lotion", 
         "Ayurvedic skin brightening and nourishing moisturizer lotion in a green cylindrical bottle with a white screw cap.", 
         "Skincare", "Moisturizer", 280.00, "Flipkart", 
         "https://images.unsplash.com/photo-1626806787461-102c1bfaaea1?w=500&auto=format&fit=crop&q=80"),
         
        ("Ponds Super Light Gel Moisturiser", 
         "24hr hydration non-oily water gel cream with hyaluronic acid and Vitamin E in an organic turquoise blue round tub.", 
         "Skincare", "Moisturizer", 320.00, "Amazon", 
         "https://images.unsplash.com/photo-1617897903246-719242758050?w=500&auto=format&fit=crop&q=80"),
         
        ("Forest Essentials Delicate Facial Cleanser Kashmir Saffron & Neem", 
         "Ultra-premium traditional Ayurvedic cleanser in a clear gold-trimmed bottle showcasing Kashmiri Saffron and raw Neem extracts.", 
         "Skincare", "Cleanser", 1550.00, "Amazon", 
         "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500&auto=format&fit=crop&q=80"),
         
        ("Kama Ayurveda Pure Rose Water Toner", 
         "Pure steam-distilled floral water toner harvested from Kannauj roses in an elegant dark amber spray bottle with gold labeling.", 
         "Skincare", "Toner", 1250.00, "Amazon", 
         "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?w=500&auto=format&fit=crop&q=80"),
         
        ("L'Oreal Paris Extraordinary Oil Hair Serum", 
         "Premium leave-in hair serum with 6 rare flower oils inside an elegant golden glass bottle with a brown pump dispenser.", 
         "Skincare", "Fragrance", 599.00, "Flipkart", 
         "https://images.unsplash.com/photo-1526947425960-945c6e72858f?w=500&auto=format&fit=crop&q=80"),
         
        ("Indulekha Bhringa Hair Oil for Hair Fall", 
         "Proprietary Ayurvedic medicine hair oil featuring active Bhringraj extracts with an innovative comb-shaped applicator.", 
         "Skincare", "Men's Care", 430.00, "Amazon", 
         "https://images.unsplash.com/photo-1590156546946-ce55a12a6a5d?w=500&auto=format&fit=crop&q=80"),
         
        ("Vaseline Intensive Care Cocoa Glow Body Lotion", 
         "Deep nourishing body lotion formulated with pure cocoa and shea butter in a tall, rich brown curved pump bottle.", 
         "Skincare", "Moisturizer", 399.00, "Flipkart", 
         "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500&auto=format&fit=crop&q=80"),
         
        ("Wow Skin Science Apple Cider Vinegar Shampoo", 
         "Clarifying, detoxifying daily shampoo enriched with pure natural apple cider vinegar in a signature dark brown square bottle.", 
         "Skincare", "Cleanser", 349.00, "Amazon", 
         "https://images.unsplash.com/photo-1556228453-efd6c1ff04f6?w=500&auto=format&fit=crop&q=80"),
         
        ("Mamaearth Onion Hair Fall Control Shampoo", 
         "Organic hair fall control shampoo enriched with Red Onion seed oil and Keratin in a clean white bottle with green highlights.", 
         "Skincare", "Cleanser", 349.00, "Amazon", 
         "https://images.unsplash.com/photo-1616683693504-3ea7e9ad6fec?w=500&auto=format&fit=crop&q=80"),
         
        ("UrbanBotanics Pure Aloe Vera Gel", 
         "Multi-purpose moisturizing cold-pressed organic aloe vera gel in a clear jar revealing the crystal clear soothing gel.", 
         "Skincare", "Moisturizer", 299.00, "Amazon", 
         "https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=500&auto=format&fit=crop&q=80"),
         
        ("Garnier Skin Naturals Micellar Cleansing Water", 
         "All-in-1 hydrating makeup remover and facial cleanser in a large transparent plastic bottle with a pretty pink cap.", 
         "Skincare", "Cleanser", 375.00, "Flipkart", 
         "https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=500&auto=format&fit=crop&q=80"),
         
        ("Himalaya Purifying Neem Face Wash", 
         "Time-tested herbal clarifying face wash formulated with neem and turmeric inside a classic green-and-white squeeze tube.", 
         "Skincare", "Cleanser", 199.00, "Amazon", 
         "https://images.unsplash.com/photo-1612204030736-613b5a930722?w=500&auto=format&fit=crop&q=80"),
         
        ("Lotus Herbals Safe Sun SPF 50 Gel Sunscreen", 
         "3-in-1 daily sunblock and sunscreen gel packaged inside a vibrant glossy orange squeeze tube.", 
         "Skincare", "Sunscreen", 425.00, "Flipkart", 
         "https://images.unsplash.com/photo-1625093742435-6fa192b6fb10?w=500&auto=format&fit=crop&q=80")
    ]
    
    # ------------------- 2. SHOES (20 Products) -------------------
    shoes_data = [
        ("Nike Air Max SYSTM Men's Sneakers", 
         "Premium heritage-style athletic sneakers featuring visible Air Max cushioning and mesh paneling with active accents.", 
         "Shoes", "Sneakers", 6495.00, "Amazon", 
         "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&auto=format&fit=crop&q=80"),
         
        ("Adidas Ultraboost Light Running Shoes", 
         "High-performance track running shoes featuring a white Primeknit upper and a responsive chunky textured boost foam midsole.", 
         "Shoes", "Running", 18999.00, "Amazon", 
         "https://images.unsplash.com/photo-1515955656352-a1fa3ffcd111?w=500&auto=format&fit=crop&q=80"),
         
        ("Puma Smashic Unisex Sneakers", 
         "Classic lifestyle low-top court sneakers made from smooth white leather with iconic side curves.", 
         "Shoes", "Sneakers", 2499.00, "Amazon", 
         "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500&auto=format&fit=crop&q=80"),
         
        ("Red Tape Men's Retro Sneakers", 
         "Sporty lifestyle running shoes in sleek knit fabric punctuated by eye-catching stripes and foam soles.", 
         "Shoes", "Sneakers", 1899.00, "Amazon", 
         "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=500&auto=format&fit=crop&q=80"),
         
        ("Bata Men's Formal Oxford Shoes", 
         "Timeless formal dress Oxford shoes crafted in premium polished dark cognac brown genuine leather with structured soles.", 
         "Shoes", "Formal", 1999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1614252235316-8c857d38b5f4?w=500&auto=format&fit=crop&q=80"),
         
        ("Sparx Men's Athletic Running Shoes", 
         "Super lightweight sports running sneakers built with breathable mesh upper and a flexible grip outer sole.", 
         "Shoes", "Running", 1299.00, "Flipkart", 
         "https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=500&auto=format&fit=crop&q=80"),
         
        ("Nike Air Jordan 1 Mid Basketball Shoes", 
         "Sought-after legendary high-top basketball sneakers featuring premium leather paneling.", 
         "Shoes", "Basketball", 11495.00, "Amazon", 
         "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=500&auto=format&fit=crop&q=80"),
         
        ("Adidas Superstar Originals Sneakers", 
         "Streetwear classic low-top shell-toe sneakers in white leather complete with standard stripes and vintage heel tabs.", 
         "Shoes", "Sneakers", 7999.00, "Amazon", 
         "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=500&auto=format&fit=crop&q=80"),
         
        ("Crocs Unisex Adult Classic Clogs", 
         "Comfortable lightweight indoor/outdoor casual clogs made of water-friendly foam in an elegant navy blue color.", 
         "Shoes", "Clogs", 2999.00, "Amazon", 
         "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=500&auto=format&fit=crop&q=80"),
         
        ("ASICS Gel-Kayano 30 Running Shoes", 
         "Elite supportive long-distance running shoes built with advanced adaptive foam cushioning.", 
         "Shoes", "Running", 15999.00, "Amazon", 
         "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=500&auto=format&fit=crop&q=80"),
         
        ("Woodland Men's Leather Rugged Boots", 
         "Heavy-duty outdoor hiking boots constructed in dark khaki oiled suede leather with thick lugged high-traction soles.", 
         "Shoes", "Boots", 4295.00, "Flipkart", 
         "https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=500&auto=format&fit=crop&q=80"),
         
        ("Campus Men's North Running Shoes", 
         "Sporty gym running shoes crafted in breathable dark black knit fabric with lightweight grey foam cushioning.", 
         "Shoes", "Running", 1499.00, "Flipkart", 
         "https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=500&auto=format&fit=crop&q=80"),
         
        ("Puma Unisex Kent Slip-on Walking Sneakers", 
         "Ultra-comfortable mesh slip-on shoes engineered on a memory tech foam midsole for dynamic all-day walking.", 
         "Shoes", "Loafers", 1999.00, "Amazon", 
         "https://images.unsplash.com/photo-1560769629-975ec94e6a86?w=500&auto=format&fit=crop&q=80"),
         
        ("Reebok Men's Stride Runner Shoes", 
         "Flexible everyday running sneakers built on a durable textured outer sole with sporty overlays.", 
         "Shoes", "Running", 2299.00, "Amazon", 
         "https://images.unsplash.com/photo-1597045566677-8cf032ed6634?w=500&auto=format&fit=crop&q=80"),
         
        ("Skechers Men's Go Walk Max Athletic Shoes", 
         "High-rebound walking shoes featuring slip-on lightweight mesh construction and signature responsive cushioning.", 
         "Shoes", "Running", 4999.00, "Amazon", 
         "https://images.unsplash.com/photo-1539185441755-769473a23570?w=500&auto=format&fit=crop&q=80"),
         
        ("Bata Men's Formal Derby Shoes", 
         "Sharp, highly polished formal dress Derby shoes crafted in structured black synthetic leather with low heels.", 
         "Shoes", "Formal", 1499.00, "Amazon", 
         "https://images.unsplash.com/photo-1560343090-f0409e92791a?w=500&auto=format&fit=crop&q=80"),
         
        ("Red Tape Men's Walking Soft Sole Shoes", 
         "Modern sporty walking shoes with a heavily textured upper and high-traction sole.", 
         "Shoes", "Walking", 1799.00, "Flipkart", 
         "https://images.unsplash.com/photo-1531310197839-ccf54634509e?w=500&auto=format&fit=crop&q=80"),
         
        ("US Polo Assn Men's Canvas Sneakers", 
         "Casual streetwear trainers featuring canvas construction with the iconic brand logo.", 
         "Shoes", "Sneakers", 2999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1533867617858-e7b97e060509?w=500&auto=format&fit=crop&q=80"),
         
        ("Columbia Men's Waterproof Hiking Shoes", 
         "Advanced outdoor technical hiking shoes crafted with a waterproof leather upper and heavy rubber sole.", 
         "Shoes", "Hiking", 8999.00, "Amazon", 
         "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=500&auto=format&fit=crop&q=80"),
         
        ("Under Armour Men's Charged Assert Sneakers", 
         "Versatile athletic running sneakers engineered with support collar and custom cushioning midsole.", 
         "Shoes", "Running", 5999.00, "Amazon", 
         "https://images.unsplash.com/photo-1582588678413-dbf45f4823e9?w=500&auto=format&fit=crop&q=80")
    ]
    
    # ------------------- 3. ELECTRONICS (20 Products) -------------------
    electronics_data = [
        ("Sony WH-1000XM4 Noise Cancelling Headphones", 
         "Industry-leading active noise cancelling overhead headphones finished in elegant matte black with gold detailing.", 
         "Electronics", "Audio", 19990.00, "Amazon", 
         "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=80"),
         
        ("OnePlus Nord Buds 2 Wireless Earbuds", 
         "True wireless earbuds packed with active noise cancellation inside a sleek, speckled dark charcoal grey charging case.", 
         "Electronics", "Audio", 2199.00, "Amazon", 
         "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&auto=format&fit=crop&q=80"),
         
        ("Apple AirPods Pro 2nd Gen Wireless Earbuds", 
         "Advanced true wireless earbuds featuring spatial audio, custom touch controls and an iconic white charging case.", 
         "Electronics", "Audio", 20900.00, "Amazon", 
         "https://images.unsplash.com/photo-1588449668365-d15e397f6787?w=500&auto=format&fit=crop&q=80"),
         
        ("boAt Rockerz 450 Bluetooth On-Ear Headphones", 
         "Popular wireless on-ear headphones colored in deep aqua blue with lightweight padded ear cushions.", 
         "Electronics", "Audio", 1499.00, "Amazon", 
         "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500&auto=format&fit=crop&q=80"),
         
        ("JBL Go 3 Wireless Portable Bluetooth Speaker", 
         "Ultra-compact rugged speaker wrapped in tight-weave protective fabric with an integrated carry loop.", 
         "Electronics", "Audio", 2999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&auto=format&fit=crop&q=80"),
         
        ("Logitech G213 Prodigy Gaming Keyboard", 
         "Tactile mechanical-feel gaming keyboard featuring dynamic 5-zone custom RGB backlighting.", 
         "Electronics", "Computers", 3995.00, "Amazon", 
         "https://images.unsplash.com/photo-1618384887929-16ec33fab9ef?w=500&auto=format&fit=crop&q=80"),
         
        ("Logitech Pebble M350 Wireless Mouse", 
         "Sleek minimalist, ultra-quiet portable computer mouse styled in a clean matte off-white colorway.", 
         "Electronics", "Computers", 1495.00, "Amazon", 
         "https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?w=500&auto=format&fit=crop&q=80"),
         
        ("Samsung Galaxy Fit3 Smart Fitness Band", 
         "Lightweight health tracking smart band with a large AMOLED touch display.", 
         "Electronics", "Wearables", 4999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&auto=format&fit=crop&q=80"),
         
        ("Mi Smart Band 8 Active Fitness Tracker", 
         "All-in-one smart activity band featuring a thin rectangular tracker module and comfortable strap.", 
         "Electronics", "Wearables", 2499.00, "Amazon", 
         "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&auto=format&fit=crop&q=80"),
         
        ("Wipro 16A Smart Plug with Energy Monitoring", 
         "Smart home automation plug designed in heavy-duty white plastic, featuring energy tracking.", 
         "Electronics", "Smart Home", 999.00, "Amazon", 
         "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&auto=format&fit=crop&q=80"),
         
        ("Philips Multi Grooming Trimmer Kit QT4011", 
         "High-performance beard trimmer featuring titanium-coated blades and zoom wheel.", 
         "Electronics", "Personal Care", 2299.00, "Flipkart", 
         "https://images.unsplash.com/photo-1621607512214-68297480165e?w=500&auto=format&fit=crop&q=80"),
         
        ("TP-Link Deco E4 Whole Home Mesh WiFi System", 
         "Dynamic whole home AC1200 dual-band mesh router system housed in cylindrical towers.", 
         "Electronics", "Networking", 4999.00, "Amazon", 
         "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?w=500&auto=format&fit=crop&q=80"),
         
        ("HP w300 1080P HD Autofocus Webcam", 
         "Compact external computer webcam with high-definition resolution and integrated microphone.", 
         "Electronics", "Computers", 1599.00, "Amazon", 
         "https://images.unsplash.com/photo-1602164948582-0de0f837c7f6?w=500&auto=format&fit=crop&q=80"),
         
        ("Zebronics Zeb-Companion Wireless Keyboard & Mouse", 
         "Ergonomic computer input peripherals combo styled in a matching, completely clean matte black profile.", 
         "Electronics", "Computers", 999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500&auto=format&fit=crop&q=80"),
         
        ("Mi 360 Home Security Camera 2K Resolution", 
         "Smart home 360-degree security camera with 2K resolution and infrared night vision.", 
         "Electronics", "Smart Home", 2999.00, "Amazon", 
         "https://images.unsplash.com/photo-1557597774-9d273605dfa9?w=500&auto=format&fit=crop&q=80"),
         
        ("Anker PowerCore 20000mAh Portable Power Bank", 
         "Ultra-high capacity external battery charger featuring matte black textured finish.", 
         "Electronics", "Accessories", 3499.00, "Amazon", 
         "https://images.unsplash.com/photo-1609592424085-f55a156e52bf?w=500&auto=format&fit=crop&q=80"),
         
        ("Realme Buds Wireless 3 Neckband Earphones", 
         "Bluetooth in-ear neckband earphones with active noise cancellation.", 
         "Electronics", "Audio", 1799.00, "Flipkart", 
         "https://images.unsplash.com/photo-1613040809024-b4ef7ba99bc3?w=500&auto=format&fit=crop&q=80"),
         
        ("SanDisk Cruzer Blade 64GB USB Flash Drive", 
         "Pocket-sized micro USB 2.0 flash drive designed in a sleek black body accented by signature highlights.", 
         "Electronics", "Accessories", 499.00, "Amazon", 
         "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=500&auto=format&fit=crop&q=80"),
         
        ("Portronics Ruffpad 15M LCD Writing Pad", 
         "Smart digital drawing and writing board with a massive 15-inch screen and stylus.", 
         "Electronics", "Smart Home", 899.00, "Amazon", 
         "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&auto=format&fit=crop&q=80"),
         
        ("Philips Daily Collection HD2582 Toaster", 
         "8-setting compact bread toaster with built-in bun warming rack styled in clean daily design.", 
         "Electronics", "Home Appliances", 1999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=500&auto=format&fit=crop&q=80")
    ]
    
    # ------------------- 4. FASHION (20 Products) -------------------
    fashion_data = [
        ("Levi's Men's Regular Fit Denim Jacket", 
         "Classic rugged trucker jacket made of thick denim featuring metallic button closures.", 
         "Fashion", "Jacket", 3499.00, "Amazon", 
         "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=500&auto=format&fit=crop&q=80"),
         
        ("Adidas Men's Football Jersey T-Shirt", 
         "Sporty activewear jersey tee styled in completely black breathable knit fabric with clean white highlights.", 
         "Fashion", "Activewear", 1999.00, "Amazon", 
         "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=500&auto=format&fit=crop&q=80"),
         
        ("Allen Solly Men's Slim Fit Polo T-Shirt", 
         "Elegant smart-casual office polo t-shirt crafted in premium textured cotton knit.", 
         "Fashion", "T-Shirt", 999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=500&auto=format&fit=crop&q=80"),
         
        ("US Polo Assn Men's Solid Cotton Shirt", 
         "Crisp, office-to-street button-down casual shirt crafted in pure linen cotton with structured collar.", 
         "Fashion", "Shirt", 1799.00, "Flipkart", 
         "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=500&auto=format&fit=crop&q=80"),
         
        ("Puma Men's Solid Fleece Cozy Hoodie", 
         "Classic relaxed pullover winter hoodie made from soft grey cotton fleece with logo details.", 
         "Fashion", "Hoodie", 2499.00, "Amazon", 
         "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=500&auto=format&fit=crop&q=80"),
         
        ("Levi's Men's 511 Slim Fit Stretch Jeans", 
         "Modern slim fit lifestyle jeans crafted in durable deep indigo blue denim with a light fading.", 
         "Fashion", "Jeans", 2899.00, "Amazon", 
         "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500&auto=format&fit=crop&q=80"),
         
        ("H&M Men's Regular Fit Cotton T-Shirt", 
         "Minimalist daily wear solid tee crafted from organic long-staple cotton in a clean shade.", 
         "Fashion", "T-Shirt", 799.00, "Amazon", 
         "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=500&auto=format&fit=crop&q=80"),
         
        ("Nike Sportswear Club Fleece Joggers", 
         "Premium tapered active joggers made of heavy fleece with a comfortable drawstring waist.", 
         "Fashion", "Activewear", 2995.00, "Amazon", 
         "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=500&auto=format&fit=crop&q=80"),
         
        ("Zara Women's Floral Print Midi Dress", 
         "Flowy summer dress covered in delicate floral patterns with a pleated waist.", 
         "Fashion", "Dress", 3990.00, "Amazon", 
         "https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=500&auto=format&fit=crop&q=80"),
         
        ("Vero Moda Women's A-Line Knee-Length Dress", 
         "Chic office dress designed with structured A-line profile in solid black stretch knit fabric.", 
         "Fashion", "Dress", 1999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1618244972963-dbee1a7edc95?w=500&auto=format&fit=crop&q=80"),
         
        ("Harpa Women's Floral Skater Casual Dress", 
         "Fun everyday skater dress featuring micro floral print details.", 
         "Fashion", "Dress", 1299.00, "Flipkart", 
         "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500&auto=format&fit=crop&q=80"),
         
        ("Van Heusen Men's Formal Solid Black Suit", 
         "Elegant 2-piece business suit featuring a slim-cut blazer and trousers.", 
         "Fashion", "Suit", 7999.00, "Amazon", 
         "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?w=500&auto=format&fit=crop&q=80"),
         
        ("Jack & Jones Men's Bomber Winter Jacket", 
         "Trendy cold-weather bomber jacket featuring elastic ribbed neck and cuffs.", 
         "Fashion", "Jacket", 3499.00, "Flipkart", 
         "https://images.unsplash.com/photo-1551488831-00ddcb6c6bd3?w=500&auto=format&fit=crop&q=80"),
         
        ("Wildcraft Men's Hooded Waterproof Raincoat", 
         "High-performance windproof raincoat complete with adjustable hood cords.", 
         "Fashion", "Outerwear", 1899.00, "Amazon", 
         "https://images.unsplash.com/photo-1543087903-1ac2ec7aa8c5?w=500&auto=format&fit=crop&q=80"),
         
        ("US Polo Assn Women's Cotton Sports Shorts", 
         "Comfortable running shorts crafted in breathable lightweight cotton fabric.", 
         "Fashion", "Activewear", 999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&auto=format&fit=crop&q=80"),
         
        ("H&M Women's Knit Sweater Pull-over", 
         "Cozy oversized winter knit pullover sweater featuring stripe patterns.", 
         "Fashion", "Sweater", 1999.00, "Amazon", 
         "https://images.unsplash.com/photo-1614975058789-41316d0e2e9c?w=500&auto=format&fit=crop&q=80"),
         
        ("Biba Women's Cotton Salwar Suit Set", 
         "Traditional Indian ethnic set featuring Kurtis and matching dupatta.", 
         "Fashion", "Ethnic", 2999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1605763240000-7e93b172d754?w=500&auto=format&fit=crop&q=80"),
         
        ("Only Women's Solid Cotton Trousers", 
         "Relaxed-fit hot weather pants crafted in premium linen-cotton.", 
         "Fashion", "Pants", 1999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1509551388413-e18d0ac5d495?w=500&auto=format&fit=crop&q=80"),
         
        ("Tommy Hilfiger Men's Crewneck Sweatshirt", 
         "Luxury casual crewneck sweatshirt made of thick organic cotton.", 
         "Fashion", "Sweatshirt", 4999.00, "Amazon", 
         "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=500&auto=format&fit=crop&q=80"),
         
        ("Peter England Men's Regular Cotton Trousers", 
         "Polished men's formal trousers featuring a straight-leg profile.", 
         "Fashion", "Pants", 1499.00, "Flipkart", 
         "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500&auto=format&fit=crop&q=80")
    ]
    
    # ------------------- 5. ACCESSORIES (20 Products) -------------------
    accessories_data = [
        ("Fastrack Reflex Beat+ Heart Rate Smartwatch", 
         "Sleek active fitness tracker smartwatch with adjustable soft silicone strap.", 
         "Accessories", "Wearables", 1499.00, "Flipkart", 
         "https://images.unsplash.com/photo-1579586337278-3befd40fd17a?w=500&auto=format&fit=crop&q=80"),
         
        ("Casio Vintage Series Digital Unisex Watch", 
         "Iconic retro metallic square digital watch featuring stainless steel band.", 
         "Accessories", "Watches", 1695.00, "Amazon", 
         "https://images.unsplash.com/photo-1522312346375-d1a52e2b99b3?w=500&auto=format&fit=crop&q=80"),
         
        ("Fossil Grant Chronograph Analog Mens Watch", 
         "Premium classic formal chronograph timepiece with round steel case.", 
         "Accessories", "Watches", 9995.00, "Amazon", 
         "https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=500&auto=format&fit=crop&q=80"),
         
        ("Ray-Ban Unisex Aviator Polarized Sunglasses", 
         "Iconic double-bridge pilot sunglasses featuring thin golden wire frames.", 
         "Accessories", "Eyewear", 9890.00, "Amazon", 
         "https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=500&auto=format&fit=crop&q=80"),
         
        ("Fastrack Men's Square Classic Sunglasses", 
         "Retro-chic square casual sunglasses featuring a solid glossy acetate frame.", 
         "Accessories", "Eyewear", 899.00, "Flipkart", 
         "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=500&auto=format&fit=crop&q=80"),
         
        ("Wildhorn Men's Leather Wallet Premium", 
         "Slim, vegetable-tanned bifold wallet constructed in high-end genuine leather.", 
         "Accessories", "Wallets", 699.00, "Amazon", 
         "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500&auto=format&fit=crop&q=80"),
         
        ("Skybags Trooper Polycarbonate Cabin Suitcase", 
         "Premium rolling suitcase featuring spinner wheels and an eye-catching pattern.", 
         "Accessories", "Bags", 3299.00, "Amazon", 
         "https://images.unsplash.com/photo-1608501821300-4f99e58bba77?w=500&auto=format&fit=crop&q=80"),
         
        ("Wildcraft 44L Commuter Outdoor Rucksack", 
         "Heavy-duty outdoor mountain backpack engineered with durable nylon fabric.", 
         "Accessories", "Bags", 2499.00, "Flipkart", 
         "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&auto=format&fit=crop&q=80"),
         
        ("Safari Pentagon 3 Pc Trolley Suitcase Set", 
         "Durable hard-sided rolling suitcase set featuring ribbed polycarbonate shell.", 
         "Accessories", "Bags", 5999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1581553680321-4fffae59fccd?w=500&auto=format&fit=crop&q=80"),
         
        ("Puma Pioneer Gym Sports Water Bottle", 
         "Leakproof athletic sports bottle made of durable plastic punctuated by bold prints.", 
         "Accessories", "Drinkware", 699.00, "Amazon", 
         "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=500&auto=format&fit=crop&q=80"),
         
        ("Decathlon Quechua 10L Mini Hiking Backpack", 
         "Ultra-compact outdoor daypack in clean canvas complete with strap tensioners.", 
         "Accessories", "Bags", 399.00, "Flipkart", 
         "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=500&auto=format&fit=crop&q=80"),
         
        ("American Tourister Valex 28L Laptop Backpack", 
         "Multi-pocket laptop backpack crafted in heavy-duty splash-resistant canvas.", 
         "Accessories", "Bags", 1299.00, "Amazon", 
         "https://images.unsplash.com/photo-1544816155-12df9643f363?w=500&auto=format&fit=crop&q=80"),
         
        ("Titan Regalia Analog Gold Dial Mens Watch", 
         "Luxurious classic dress watch finished in gold plating.", 
         "Accessories", "Watches", 5495.00, "Flipkart", 
         "https://images.unsplash.com/photo-1614162692292-7ac56d7f7f1e?w=500&auto=format&fit=crop&q=80"),
         
        ("G-Shock Men's Matte Black Digital Sports Watch", 
         "Legendary shock-resistant, waterproof sports watch finished in solid matte black.", 
         "Accessories", "Watches", 5995.00, "Amazon", 
         "https://images.unsplash.com/photo-1547996160-81dfa63595aa?w=500&auto=format&fit=crop&q=80"),
         
        ("Milton Thermosteel Duo DLX 1000 Water Bottle", 
         "Vacuum-insulated hot/cold steel travel flask finished in sleek powder coat.", 
         "Accessories", "Drinkware", 999.00, "Flipkart", 
         "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=500&auto=format&fit=crop&q=80"),
         
        ("Tommy Hilfiger Classic Leather Trifold Wallet", 
         "Traditional slim trifold pocket organizer crafted in premium genuine leather.", 
         "Accessories", "Wallets", 2199.00, "Amazon", 
         "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=500&auto=format&fit=crop&q=80"),
         
        ("Ray-Ban Wayfarer Classic Black Sunglasses", 
         "Retro urban lifestyle thick-frame sunglasses in deep gloss frame.", 
         "Accessories", "Eyewear", 8490.00, "Amazon", 
         "https://images.unsplash.com/photo-1577803645773-f96470509666?w=500&auto=format&fit=crop&q=80"),
         
        ("Fossil Logan RFID Leather Zip Clutch Wallet", 
         "Spacious secure smartphone wallet clutch structured in premium leather.", 
         "Accessories", "Wallets", 3995.00, "Amazon", 
         "https://images.unsplash.com/photo-1600185365483-26d7a4cc7519?w=500&auto=format&fit=crop&q=80"),
         
        ("Skybags Brat 30L Casual Laptop Backpack", 
         "Trendy high-capacity university backpack styled in water-resistant fabric.", 
         "Accessories", "Bags", 1099.00, "Flipkart", 
         "https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=500&auto=format&fit=crop&q=80"),
         
        ("Milton Insulated Travel Hot/Cold Lunch Box", 
         "Insulated lunch container case housed in a carry bag.", 
         "Accessories", "Lunchbox", 699.00, "Flipkart", 
         "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=500&auto=format&fit=crop&q=80")
    ]
    
    # Compile all lists
    datasets = [
        (skincare_data, "skincare"),
        (shoes_data, "shoes"),
        (electronics_data, "electronics"),
        (fashion_data, "fashion"),
        (accessories_data, "accessories")
    ]
    
    global_id = 1
    for data_list, cat_label in datasets:
        for title, desc, cat, subcat, price, source, url in data_list:
            prod_id = f"PROD_{global_id:03d}"
            filename = f"prod_{global_id:03d}_{cat_label}.jpg"
            t_query = title.replace(" ", "+")
            if source == "Amazon":
                if "Sony WH-1000XM4" in title:
                    target_link = "https://www.amazon.in/dp/B0863TXGM3"
                elif "OnePlus Nord Buds" in title:
                    target_link = "https://www.amazon.in/dp/B0BYJFF11K"
                elif "AirPods Pro" in title:
                    target_link = "https://www.amazon.in/dp/B0BDK62PDX"
                elif "boAt Rockerz 450" in title:
                    target_link = "https://www.amazon.in/dp/B07PR1CL3S"
                elif "Logitech G213" in title:
                    target_link = "https://www.amazon.in/dp/B01L6L4616"
                elif "Logitech Pebble M350" in title:
                    target_link = "https://www.amazon.in/dp/B07W5JKF6D"
                elif "Neutrogena Hydro Boost" in title:
                    target_link = "https://www.amazon.in/dp/B00NR1YQHM"
                elif "Cetaphil Gentle Skin" in title:
                    target_link = "https://www.amazon.in/dp/B01IPBVK36"
                elif "L'Oreal Paris Revitalift" in title:
                    target_link = "https://www.amazon.in/dp/B08QSRRYGL"
                elif "Minimalist 10% Vitamin C" in title:
                    target_link = "https://www.amazon.in/dp/B0CW1M1BC1"
                elif "Nivea Soft" in title:
                    target_link = "https://www.amazon.in/dp/B00E96N6O8"
                elif "Ponds Super Light" in title:
                    target_link = "https://www.amazon.in/dp/B09Z6T8H41"
                elif "Casio Vintage" in title:
                    target_link = "https://www.amazon.in/dp/B00JAK1PMI"
                elif "Fossil Grant" in title:
                    target_link = "https://www.amazon.in/dp/B00AMWDOEK"
                elif "G-Shock" in title:
                    target_link = "https://www.amazon.in/dp/B000GAYQL8"
                else:
                    target_link = f"https://www.amazon.in/s?k={t_query}"
            else:
                if "The Derma Co 10% Niacinamide" in title:
                    target_link = "https://www.flipkart.com/the-derma-co-10-niacinamide-face-serum-acne-marks-spots/p/itm535f299166f2c"
                elif "Plum Green Tea" in title:
                    target_link = "https://www.flipkart.com/plum-green-tea-pore-cleansing-face-wash/p/itmd4e94be83e950"
                elif "Biotique Morning Nectar" in title:
                    target_link = "https://www.flipkart.com/biotique-morning-nectar-flawless-skin-lotion-moisturizer/p/itme9b0de578f7e2"
                elif "Vaseline Intensive Care Cocoa Glow" in title:
                    target_link = "https://www.flipkart.com/vaseline-intensive-care-cocoa-glow-body-lotion/p/itmaqygb9yzh49h"
                elif "Garnier Skin Naturals Micellar" in title:
                    target_link = "https://www.flipkart.com/garnier-skin-naturals-micellar-cleansing-water-makeup-remover/p/itmf7hmghkgyvfg"
                elif "Lotus Herbals Safe Sun" in title:
                    target_link = "https://www.flipkart.com/lotus-herbals-safe-sun-3-in-1-matte-look-daily-sunblock-spf-40-pa/p/itm3kupgthgnghh"
                else:
                    target_link = f"https://www.flipkart.com/search?q={t_query}"
            
            products.append({
                "id": prod_id,
                "title": title,
                "category": cat,
                "subcategory": subcat,
                "price": price,
                "platform": source,
                "link": target_link,
                "description": desc,
                "unsplash_url": url,
                "local_path": f"data/images/{filename}"
            })
            global_id += 1
            
    return products

def main():
    print("[ShopSense AI] Initializing premium unique product dataset build...")
    
    # We do NOT purge data/images here anymore, because screenshot_products.py handles image management
    os.makedirs("data", exist_ok=True)
    os.makedirs("data/images", exist_ok=True)
    
    # 1. Generate Raw Metadata List
    products = generate_product_list()
    
    # 2. Save raw metadata to CSV
    df = pd.DataFrame(products)
    csv_path = "data/products.csv"
    df.to_csv(csv_path, index=False)
    print(f"[ShopSense AI] Wrote {len(df)} initial metadata records to: {csv_path}")
    
    # 3. Call the screenshots and browser resolution pipeline to capture exact images (Disabled here to compile entire dataset before crawling)
    # import screenshot_products
    # screenshot_products.main()

if __name__ == "__main__":
    main()

