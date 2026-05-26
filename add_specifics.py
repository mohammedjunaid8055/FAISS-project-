import pandas as pd
import os

def main():
    csv_path = "data/products.csv"
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV not found at {csv_path}")
        return
        
    df = pd.read_csv(csv_path)
    
    # 3 highly specific products matching user descriptions
    specifics = [
        {
            "id": f"PROD_{len(df)+1:03d}",
            "title": "Puma Men's Red Cotton Polo T-Shirt",
            "category": "Fashion",
            "subcategory": "T-Shirt",
            "price": 1299.00,
            "platform": "Flipkart",
            "link": "https://www.flipkart.com/search?q=Puma+Mens+Red+Cotton+Polo+T-Shirt",
            "description": "Classic premium red cotton polo collar t-shirt with half sleeves and subtle logo detailing.",
            "unsplash_url": "https://images.unsplash.com/photo-placeholder",
            "local_path": f"data/images/prod_{len(df)+1:03d}_fashion.jpg"
        },
        {
            "id": f"PROD_{len(df)+2:03d}",
            "title": "Nike Men's Sleeveless Dry-Fit Training Tank Top",
            "category": "Fashion",
            "subcategory": "Activewear",
            "price": 1999.00,
            "platform": "Amazon",
            "link": "https://www.amazon.in/s?k=Nike+Mens+Sleeveless+Dry-Fit+Training+Tank+Top",
            "description": "High-performance athletic sleeveless training shirt featuring breathable dry-fit mesh fabrics.",
            "unsplash_url": "https://images.unsplash.com/photo-placeholder",
            "local_path": f"data/images/prod_{len(df)+2:03d}_fashion.jpg"
        },
        {
            "id": f"PROD_{len(df)+3:03d}",
            "title": "Allen Solly Men's Half Sleeve Checked Casual Shirt",
            "category": "Fashion",
            "subcategory": "Shirt",
            "price": 1499.00,
            "platform": "Flipkart",
            "link": "https://www.flipkart.com/search?q=Allen+Solly+Mens+Half+Sleeve+Checked+Casual+Shirt",
            "description": "Smart casual cotton checkered shirt with half sleeves, button-down collar and regular fit.",
            "unsplash_url": "https://images.unsplash.com/photo-placeholder",
            "local_path": f"data/images/prod_{len(df)+3:03d}_fashion.jpg"
        }
    ]
    
    new_df = pd.concat([df, pd.DataFrame(specifics)], ignore_index=True)
    new_df.to_csv(csv_path, index=False)
    print(f"[ShopSense AI] Successfully added user-specific products! Total catalog size: {len(new_df)}.")

if __name__ == "__main__":
    main()
