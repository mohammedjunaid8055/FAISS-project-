import re
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

def get_amazon_image(url):
    print(f"Fetching Amazon: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"  Amazon status: {r.status_code}")
            return None
        
        # 1. Look for landingImage tag or dynamic image JSON
        soup = BeautifulSoup(r.text, "html.parser")
        img_tag = soup.find("img", id="landingImage")
        if img_tag and img_tag.get("data-a-dynamic-image"):
            dyn_data = img_tag.get("data-a-dynamic-image")
            try:
                img_urls = json.loads(dyn_data)
                # Find the largest image (highest resolution)
                largest_url = max(img_urls.keys(), key=lambda x: img_urls[x][0] * img_urls[x][1])
                return largest_url
            except Exception as e:
                print(f"  Failed parsing dynamic image JSON: {e}")
        
        # 2. Try raw regex search for landingImage or other high-res image structures
        match = re.search(r'\"landingImage\"\s*:\s*\{\s*\"(https://[^\"]+?)\"', r.text)
        if match:
            return match.group(1)
            
        match_any = re.search(r'\"(https://m\.media-amazon\.com/images/I/[a-zA-Z0-9\-_%]+?\.[a-zA-Z]{3,4})\"', r.text)
        if match_any:
            return match_any.group(1)
            
        # 3. Look for regular landingImage src
        if img_tag and img_tag.get("src"):
            return img_tag.get("src")
            
    except Exception as e:
        print(f"  Amazon scraping error: {e}")
    return None

def get_flipkart_image(url):
    print(f"Fetching Flipkart: {url}")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"  Flipkart status: {r.status_code}")
            return None
            
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Look for images starting with rukminim2.flixcart.com/image/
        # Check all img tags
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src and "rukminim2.flixcart.com/image/" in src:
                # Replace sizing (e.g. 128/128 or 416/416) with 832/832 for high res
                high_res = re.sub(r'/image/\d+/\d+/', '/image/832/832/', src)
                return high_res
                
        # Regex search for flixcart image
        match = re.search(r'\"(https://rukminim\d\.flixcart\.com/image/[^\"]+?)\"', r.text)
        if match:
            src = match.group(1)
            high_res = re.sub(r'/image/\d+/\d+/', '/image/832/832/', src)
            return high_res
            
    except Exception as e:
        print(f"  Flipkart scraping error: {e}")
    return None

# Let's test on a few target URLs!
test_urls = [
    ("Neutrogena", "https://www.amazon.in/dp/B00NR1YQHM"),
    ("The Derma Co", "https://www.flipkart.com/the-derma-co-10-niacinamide-face-serum-acne-marks-spots/p/itm535f299166f2c"),
    ("Minimalist", "https://www.amazon.in/dp/B0CW1M1BC1"),
    ("Nivea Soft", "https://www.amazon.in/dp/B00E96N6O8"),
    ("Ponds Gel", "https://www.amazon.in/dp/B09Z6T8H41")
]

print("Testing scraper...")
for name, url in test_urls:
    if "amazon" in url:
        img_url = get_amazon_image(url)
    else:
        img_url = get_flipkart_image(url)
    print(f"RESULT: {name} -> {img_url}\n")
