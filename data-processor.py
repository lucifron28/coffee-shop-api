# data_processor.py
import requests
import json
import re
import random
from typing import List, Dict, Optional

def fetch_and_clean_coffee_data():
    """
    Fetch coffee data from Swedish API and transform to English e-commerce data
    """
    print("Fetching coffee data from APIs...")
    
    # Fetch both hot and cold coffee data
    try:
        hot_response = requests.get("https://api.sampleapis.com/coffee/hot", timeout=10)
        cold_response = requests.get("https://api.sampleapis.com/coffee/iced", timeout=10)
        
        hot_data = hot_response.json()
        cold_data = cold_response.json()
        
        print(f"Fetched {len(hot_data)} hot coffees and {len(cold_data)} cold coffees")
        
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []
    
    def clean_item(item, category):
        # Skip items with missing critical data
        if not item.get('title') or not item.get('image') or not item.get('id'):
            return None
            
        # Skip broken images or test data
        image = item.get('image', '')
        if ('monjgofjaslekfj.com' in image or 
            item.get('title', '').lower() in ['tea'] or
            not image.startswith('http')):
            return None
            
        # Extract English name from Swedish title
        english_name = translate_title(item['title'])
        
        # Clean and enhance the data
        cleaned = {
            'id': item['id'],
            'name': english_name,
            'image': clean_image_url(image),
            'original_ingredients': item.get('ingredients', []),
            'ingredients': clean_ingredients(item.get('ingredients', [])),
            'category': category,
            'description': generate_description(english_name),
            'prices': generate_prices(english_name, category),
            'sizes': get_sizes(english_name, category),
            'caffeine_mg': estimate_caffeine(english_name),
            'calories': estimate_calories(english_name),
            'is_featured': False,  # We'll set some manually later
            'is_available': True,
            'preparation_time': estimate_prep_time(english_name),
            'customizations': get_customizations(english_name, category),
            'rating': round(random.uniform(4.2, 5.0), 1),
            'review_count': random.randint(15, 250)
        }
        
        return cleaned
    
    # Process both categories
    all_items = []
    
    for item in hot_data:
        cleaned = clean_item(item, "Hot Coffee")
        if cleaned:
            all_items.append(cleaned)
    
    for item in cold_data:
        cleaned = clean_item(item, "Iced Coffee")
        if cleaned:
            all_items.append(cleaned)
    
    # Remove duplicates based on name and ensure unique IDs
    seen_names = set()
    seen_ids = set()
    unique_products = []
    new_id = 1
    
    for product in all_items:
        name_key = f"{product['name']}_{product['category']}"
        
        if name_key not in seen_names:
            # Ensure unique ID
            while new_id in seen_ids or any(p.get('id') == new_id for p in unique_products):
                new_id += 1
            
            product['id'] = new_id
            seen_names.add(name_key)
            seen_ids.add(new_id)
            unique_products.append(product)
            new_id += 1
    
    print(f"Processed {len(unique_products)} unique coffee products")
    return unique_products

def translate_title(swedish_title: str) -> str:
    """Map Swedish coffee names to English"""
    if not swedish_title:
        return "Specialty Coffee"
        
    translations = {
        'Americano': 'Americano',
        'Americano1': 'Americano',
        'Americano123': 'Americano', 
        'Espresso': 'Espresso',
        'Cappuccino': 'Cappuccino',
        'Mocha': 'Mocha',
        'Mocka': 'Mocha',
        'Latte': 'Latte',
        'Islatte': 'Iced Latte',
        'Islatte Mocha': 'Iced Mocha Latte',
        'Chai Latte': 'Chai Latte',
        'Matcha Latte': 'Matcha Latte',
        'Hot Chocolate': 'Hot Chocolate',
        'Svart Te': 'Black Tea',
        'Frapino Caramel': 'Caramel Frappuccino',
        'Frapino Mocka': 'Mocha Frappuccino',
        'Seasonal Brew': 'Seasonal Coffee',
        'Latte Amaretto': 'Amaretto Latte'
    }
    
    # Clean the title first
    clean_title = re.sub(r'\d+$', '', swedish_title).strip()
    
    # Try exact match
    if clean_title in translations:
        return translations[clean_title]
    
    # Try partial matches
    for swedish, english in translations.items():
        if swedish.lower() in clean_title.lower():
            return english
    
    # Fallback: return cleaned original or default
    return clean_title if clean_title else 'Specialty Coffee'

def clean_image_url(image_url: str) -> str:
    """Clean and validate image URLs"""
    if not image_url or not image_url.startswith('http'):
        return "https://images.unsplash.com/photo-1447933601403-0c6688de566e?auto=format&fit=crop&q=80&w=800"
    
    # Ensure proper size parameters for Unsplash images
    if 'unsplash.com' in image_url:
        # Add consistent sizing parameters
        if '?' in image_url:
            base_url = image_url.split('?')[0]
        else:
            base_url = image_url
        return f"{base_url}?auto=format&fit=crop&q=80&w=800"
    
    return image_url

def clean_ingredients(ingredients: List[str]) -> List[str]:
    """Clean and translate ingredients from Swedish to English"""
    if not ingredients:
        return ['Coffee']
        
    ingredient_map = {
        'Espresso': 'Espresso',
        'Hett vattent': 'Hot Water', 
        'Hot Water': 'Hot Water',
        'Ångad mjölk': 'Steamed Milk',
        'Mjölkskum': 'Milk Foam',
        'Mjölk': 'Milk',
        'Milk': 'Milk',
        'Choklad': 'Chocolate',
        'Chocolate': 'Chocolate',
        'Choklad ': 'Chocolate',
        'Is': 'Ice',
        'Ice': 'Ice',
        'Sirap': 'Syrup',
        'Syrup': 'Syrup',
        'Karamellsirap': 'Caramel Syrup',
        'Te': 'Tea',
        'Tea': 'Tea',
        'Matcha-pulver': 'Matcha Powder',
        'Socker': 'Sugar',
        'Socker*': 'Sugar',
        'Sugar': 'Sugar',
        'Kaffe': 'Coffee',
        'Coffee': 'Coffee',
        'coffee': 'Coffee',
        'Cocoa': 'Cocoa',
        'Ingefära': 'Ginger',
        'Kardemumma': 'Cardamom',
        'Lait': 'Milk',
        'dryed tea': 'Tea',
        'worm water': 'Hot Water'
    }
    
    cleaned = []
    for ingredient in ingredients:
        if not ingredient:
            continue
        ingredient = ingredient.strip()
        if ingredient in ingredient_map:
            mapped = ingredient_map[ingredient]
            if mapped not in cleaned:  # Avoid duplicates
                cleaned.append(mapped)
        elif ingredient and len(ingredient) > 1:  # Keep original if reasonable
            cleaned.append(ingredient.title())
    
    return cleaned if cleaned else ['Coffee']

def generate_description(name: str) -> str:
    """Generate professional English descriptions for coffee drinks"""
    descriptions = {
        'Americano': 'A rich, bold coffee made by diluting espresso shots with hot water, creating a smooth and strong cup that rivals traditional drip coffee.',
        'Espresso': 'A concentrated coffee shot with rich flavor and golden crema. The foundation of all espresso-based drinks, perfect for purists.',
        'Cappuccino': 'A perfect balance of espresso, steamed milk, and velvety milk foam. This classic Italian coffee delivers a rich, creamy experience.',
        'Latte': 'Smooth espresso combined with steamed milk and a light layer of foam. Creamy, comforting, and perfectly balanced.',
        'Mocha': 'A delightful blend of rich espresso, premium chocolate, and steamed milk topped with whipped cream. Perfect for chocolate lovers.',
        'Iced Latte': 'Our signature latte served chilled over ice with cold milk. Refreshing, smooth, and perfect for warm days.',
        'Iced Mocha Latte': 'Rich chocolate and espresso served cold with milk and ice. A refreshing treat for mocha enthusiasts.',
        'Chai Latte': 'Aromatic spiced tea blended with steamed milk. Features warming spices of cardamom, cinnamon, and ginger.',
        'Matcha Latte': 'Premium matcha powder whisked with steamed milk. Earthy, creamy, and naturally energizing.',
        'Hot Chocolate': 'Rich, creamy chocolate drink made with premium cocoa and topped with whipped cream. A classic comfort drink.',
        'Black Tea': 'Premium black tea steeped to perfection. Rich, aromatic, and full of natural antioxidants.',
        'Caramel Frappuccino': 'Blended coffee drink with rich caramel flavoring, ice, and whipped cream topping. Sweet and refreshing.',
        'Mocha Frappuccino': 'Chocolate and coffee blended with ice and topped with whipped cream. The perfect cold treat.',
        'Seasonal Coffee': 'Our rotating seasonal blend featuring unique flavor profiles that capture the essence of each season.',
        'Amaretto Latte': 'Our signature latte enhanced with sweet amaretto syrup for a nutty, luxurious flavor experience.'
    }
    
    return descriptions.get(name, f'A delicious {name.lower()} crafted with care using premium ingredients and expert brewing techniques.')

def generate_prices(name: str, category: str) -> Dict[str, float]:
    """Generate realistic prices based on drink complexity and type"""
    
    # Special pricing for espresso (shot-based)
    if 'Espresso' in name:
        return {'single': 2.50, 'double': 3.50}
    
    # Base pricing tiers
    premium_drinks = ['Mocha', 'Caramel Frappuccino', 'Mocha Frappuccino', 'Amaretto Latte']
    specialty_drinks = ['Chai Latte', 'Matcha Latte', 'Seasonal Coffee']
    basic_drinks = ['Americano', 'Black Tea', 'Hot Chocolate']
    
    if any(premium in name for premium in premium_drinks):
        if 'Iced' in category or 'Frappuccino' in name:
            return {'small': 4.95, 'medium': 5.45, 'large': 5.95}
        else:
            return {'small': 4.75, 'medium': 5.25, 'large': 5.75}
    
    elif any(specialty in name for specialty in specialty_drinks):
        return {'small': 4.50, 'medium': 5.00, 'large': 5.50}
    
    elif any(basic in name for basic in basic_drinks):
        return {'small': 3.25, 'medium': 3.75, 'large': 4.25}
    
    else:  # Standard drinks (Latte, Cappuccino, etc.)
        if 'Iced' in category:
            return {'small': 4.25, 'medium': 4.75, 'large': 5.25}
        else:
            return {'small': 4.50, 'medium': 5.00, 'large': 5.50}

def get_sizes(name: str, category: str) -> List[str]:
    """Get appropriate sizes for each drink type"""
    if 'Espresso' in name:
        return ['Single Shot', 'Double Shot']
    elif 'Frappuccino' in name:
        return ['Tall (12oz)', 'Grande (16oz)', 'Venti (20oz)']
    else:
        return ['Small (8oz)', 'Medium (12oz)', 'Large (16oz)']

def estimate_caffeine(name: str) -> int:
    """Estimate caffeine content in mg"""
    caffeine_map = {
        'Espresso': 64,
        'Americano': 154,
        'Latte': 154,
        'Cappuccino': 154,
        'Mocha': 175,
        'Iced Latte': 154,
        'Iced Mocha Latte': 175,
        'Caramel Frappuccino': 95,
        'Mocha Frappuccino': 100,
        'Chai Latte': 47,
        'Matcha Latte': 70,
        'Black Tea': 42,
        'Hot Chocolate': 15,
        'Seasonal Coffee': 120,
        'Amaretto Latte': 154
    }
    
    return caffeine_map.get(name, 95)  # Default moderate caffeine

def estimate_calories(name: str) -> int:
    """Estimate calories for medium size"""
    calorie_map = {
        'Espresso': 2,
        'Americano': 5,
        'Latte': 190,
        'Cappuccino': 120,
        'Mocha': 290,
        'Iced Latte': 130,
        'Iced Mocha Latte': 250,
        'Caramel Frappuccino': 370,
        'Mocha Frappuccino': 340,
        'Chai Latte': 240,
        'Matcha Latte': 240,
        'Black Tea': 2,
        'Hot Chocolate': 320,
        'Seasonal Coffee': 150,
        'Amaretto Latte': 210
    }
    
    return calorie_map.get(name, 180)

def estimate_prep_time(name: str) -> int:
    """Estimate preparation time in minutes"""
    if 'Espresso' in name:
        return 1
    elif 'Frappuccino' in name:
        return 5
    elif any(x in name for x in ['Mocha', 'Specialty']):
        return 4
    elif any(x in name for x in ['Latte', 'Cappuccino']):
        return 3
    else:
        return 2

def get_customizations(name: str, category: str) -> List[str]:
    """Get available customizations for each drink"""
    base_customizations = ['Extra Shot', 'Decaf', 'Half-Caff']
    milk_options = ['Oat Milk', 'Almond Milk', 'Soy Milk', 'Coconut Milk', '2% Milk', 'Whole Milk']
    syrups = ['Vanilla', 'Caramel', 'Hazelnut', 'Sugar-Free Vanilla']
    
    customizations = base_customizations.copy()
    
    # Add milk options for milk-based drinks
    if any(x in name for x in ['Latte', 'Cappuccino', 'Mocha', 'Chai', 'Matcha']):
        customizations.extend(milk_options[:4])  # Add some milk options
    
    # Add syrups for most coffee drinks
    if not any(x in name for x in ['Espresso', 'Americano', 'Tea']):
        customizations.extend(syrups[:2])  # Add vanilla and caramel
    
    # Special additions
    if 'Mocha' in name:
        customizations.append('Extra Chocolate')
    if 'Frappuccino' in name:
        customizations.extend(['Whipped Cream', 'Extra Caramel Drizzle'])
    
    return customizations

if __name__ == "__main__":
    # Process the data
    processed_data = fetch_and_clean_coffee_data()
    
    if not processed_data:
        print("❌ No data was processed!")
        exit(1)
    
    # Mark some products as featured (pick diverse ones)
    featured_names = ['Americano', 'Cappuccino', 'Latte', 'Iced Latte', 'Mocha', 'Cold Brew']
    featured_count = 0
    
    for product in processed_data:
        if product['name'] in featured_names and featured_count < 6:
            product['is_featured'] = True
            featured_count += 1
    
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Save processed data
    with open('data/processed_coffee_products.json', 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully processed {len(processed_data)} unique coffee products!")
    print(f"✅ Featured products: {featured_count}")
    print("✅ Data saved to: data/processed_coffee_products.json")
    
    # Show sample products
    print(f"\n📋 Sample products:")
    for i, product in enumerate(processed_data[:8]):
        prices = product['prices']
        price_str = ', '.join([f"{k}: ${v}" for k, v in prices.items()])
        print(f"{i+1:2d}. {product['name']} ({product['category']})")
        print(f"     Prices: {price_str}")
        print(f"     Description: {product['description'][:60]}...")
    
    # Show categories summary
    categories = {}
    for product in processed_data:
        cat = product['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print(f"\n📊 Final Categories Summary:")
    for cat, count in categories.items():
        print(f"- {cat}: {count} products")
    
    # Show featured products
    featured_products = [p for p in processed_data if p.get('is_featured')]
    print(f"\n⭐ Featured Products:")
    for product in featured_products:
        print(f"- {product['name']} ({product['category']})")
        
    print(f"\n🎯 Ready for FastAPI! Run: python main.py")
