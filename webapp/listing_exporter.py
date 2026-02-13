#!/usr/bin/env python3
"""
Listing Exporter - Generate platform-ready listing text
By: Buddy Dubby 🫠

Creates copy-paste ready listings for each platform with proper formatting.
"""

from datetime import datetime

def format_poshmark_listing(item: dict) -> str:
    """
    Format item for Poshmark listing.
    Poshmark tips:
    - 500 character limit for title (but keep it readable)
    - Description has no real limit
    - Use keywords naturally
    - Include measurements
    """
    name = item.get('name', 'Item')
    brand = item.get('brand', '')
    size = item.get('size', '')
    color = item.get('color', '')
    condition = item.get('condition', 'good').title()
    measurements = item.get('measurements', '')
    notes = item.get('notes', '')
    target_price = item.get('target_price', 0)
    
    # Build title
    title_parts = []
    if brand:
        title_parts.append(brand)
    title_parts.append(name)
    if color:
        title_parts.append(color)
    if size:
        title_parts.append(f"Size {size}")
    
    title = " ".join(title_parts)
    
    # Build description
    desc_lines = []
    desc_lines.append(f"✨ {name.upper()} ✨")
    desc_lines.append("")
    
    if brand:
        desc_lines.append(f"Brand: {brand}")
    if size:
        desc_lines.append(f"Size: {size}")
    if color:
        desc_lines.append(f"Color: {color}")
    desc_lines.append(f"Condition: {condition}")
    
    if measurements:
        desc_lines.append("")
        desc_lines.append("📏 MEASUREMENTS:")
        desc_lines.append(measurements)
    
    if notes:
        desc_lines.append("")
        desc_lines.append("📝 NOTES:")
        desc_lines.append(notes)
    
    desc_lines.append("")
    desc_lines.append("💕 Bundle to save on shipping!")
    desc_lines.append("✅ Ships within 1-2 business days")
    desc_lines.append("❓ Questions? Just ask!")
    
    return {
        "title": title[:500],
        "description": "\n".join(desc_lines),
        "suggested_price": target_price,
        "platform": "Poshmark"
    }


def format_depop_listing(item: dict) -> str:
    """
    Format item for Depop listing.
    Depop tips:
    - Use hashtags (up to 5)
    - Younger, trendier vibe
    - 1000 character description limit
    - Measurements important
    """
    name = item.get('name', 'Item')
    brand = item.get('brand', '')
    size = item.get('size', '')
    color = item.get('color', '')
    condition = item.get('condition', 'good').title()
    measurements = item.get('measurements', '')
    notes = item.get('notes', '')
    target_price = item.get('target_price', 0)
    category = item.get('category', '').lower()
    
    # Build description (more casual, Gen Z vibe)
    desc_lines = []
    
    # Opening
    opening = f"{brand} {name}" if brand else name
    desc_lines.append(f"🔥 {opening}")
    desc_lines.append("")
    
    # Quick specs
    specs = []
    if size:
        specs.append(f"Size {size}")
    if color:
        specs.append(color)
    specs.append(f"{condition} condition")
    desc_lines.append(" • ".join(specs))
    
    if measurements:
        desc_lines.append("")
        desc_lines.append(f"Measurements: {measurements}")
    
    if notes:
        desc_lines.append("")
        desc_lines.append(notes)
    
    desc_lines.append("")
    desc_lines.append("DM for questions 💬")
    
    # Generate hashtags
    hashtags = []
    if brand:
        hashtags.append(f"#{brand.lower().replace(' ', '')}")
    if category:
        hashtags.append(f"#{category.replace(' ', '')}")
    hashtags.extend(["#vintage", "#thrift", "#y2k"])  # Common Depop tags
    
    desc_lines.append("")
    desc_lines.append(" ".join(hashtags[:5]))
    
    description = "\n".join(desc_lines)
    
    return {
        "title": f"{brand} {name}".strip()[:60],  # Depop has shorter title limit
        "description": description[:1000],
        "suggested_price": target_price,
        "platform": "Depop"
    }


def format_mercari_listing(item: dict) -> str:
    """
    Format item for Mercari listing.
    Mercari tips:
    - Title max 80 characters
    - Description max 1000 characters
    - Be specific about condition
    - Include measurements
    """
    name = item.get('name', 'Item')
    brand = item.get('brand', '')
    size = item.get('size', '')
    color = item.get('color', '')
    condition = item.get('condition', 'good')
    measurements = item.get('measurements', '')
    notes = item.get('notes', '')
    target_price = item.get('target_price', 0)
    
    # Condition mapping for Mercari
    condition_map = {
        'new': 'New with tags',
        'like new': 'Like new',
        'excellent': 'Like new',
        'very good': 'Good',
        'good': 'Good',
        'fair': 'Fair',
        'poor': 'Poor'
    }
    mercari_condition = condition_map.get(condition.lower(), 'Good')
    
    # Build title (concise, keywords first)
    title_parts = []
    if brand:
        title_parts.append(brand)
    title_parts.append(name)
    if size:
        title_parts.append(f"Size {size}")
    
    title = " ".join(title_parts)
    
    # Build description
    desc_lines = []
    desc_lines.append(f"{brand} {name}".strip() if brand else name)
    desc_lines.append("")
    
    if size:
        desc_lines.append(f"• Size: {size}")
    if color:
        desc_lines.append(f"• Color: {color}")
    desc_lines.append(f"• Condition: {mercari_condition}")
    
    if measurements:
        desc_lines.append("")
        desc_lines.append("Measurements:")
        desc_lines.append(measurements)
    
    if notes:
        desc_lines.append("")
        desc_lines.append("Additional Notes:")
        desc_lines.append(notes)
    
    desc_lines.append("")
    desc_lines.append("Ships quickly! Thanks for looking.")
    
    return {
        "title": title[:80],
        "description": "\n".join(desc_lines)[:1000],
        "suggested_price": target_price,
        "platform": "Mercari",
        "mercari_condition": mercari_condition
    }


def format_ebay_listing(item: dict) -> str:
    """
    Format item for eBay listing.
    eBay tips:
    - Title max 80 characters (every word matters for search)
    - Use keywords buyers search for
    - Be very specific in description
    - Include defects explicitly
    """
    name = item.get('name', 'Item')
    brand = item.get('brand', '')
    size = item.get('size', '')
    color = item.get('color', '')
    condition = item.get('condition', 'good')
    measurements = item.get('measurements', '')
    notes = item.get('notes', '')
    target_price = item.get('target_price', 0)
    
    # eBay condition mapping
    condition_map = {
        'new': 'New with tags',
        'like new': 'New without tags',
        'excellent': 'Pre-owned',
        'very good': 'Pre-owned',
        'good': 'Pre-owned',
        'fair': 'Pre-owned',
        'poor': 'For parts or not working'
    }
    ebay_condition = condition_map.get(condition.lower(), 'Pre-owned')
    
    # Build search-optimized title
    title_parts = [brand] if brand else []
    title_parts.append(name)
    if color:
        title_parts.append(color)
    if size:
        title_parts.append(f"Size {size}")
    
    title = " ".join(title_parts)
    
    # Build description (more formal, thorough)
    desc_lines = []
    desc_lines.append(f"<h2>{brand} {name}</h2>" if brand else f"<h2>{name}</h2>")
    desc_lines.append("")
    desc_lines.append("<b>Item Details:</b><br>")
    
    if brand:
        desc_lines.append(f"• Brand: {brand}<br>")
    if size:
        desc_lines.append(f"• Size: {size}<br>")
    if color:
        desc_lines.append(f"• Color: {color}<br>")
    desc_lines.append(f"• Condition: {ebay_condition}<br>")
    
    if measurements:
        desc_lines.append("")
        desc_lines.append("<b>Measurements:</b><br>")
        desc_lines.append(measurements.replace('\n', '<br>'))
    
    if notes:
        desc_lines.append("")
        desc_lines.append("<b>Notes:</b><br>")
        desc_lines.append(notes.replace('\n', '<br>'))
    
    desc_lines.append("")
    desc_lines.append("<br><b>Shipping:</b><br>")
    desc_lines.append("• Ships within 1-2 business days<br>")
    desc_lines.append("• Combined shipping available<br>")
    
    return {
        "title": title[:80],
        "description": "\n".join(desc_lines),
        "description_plain": "\n".join(desc_lines).replace('<br>', '\n').replace('<b>', '').replace('</b>', '').replace('<h2>', '').replace('</h2>', ''),
        "suggested_price": target_price,
        "platform": "eBay",
        "ebay_condition": ebay_condition
    }


def export_all_platforms(item: dict) -> dict:
    """Export listing text for all platforms"""
    return {
        "item_id": item.get('id'),
        "item_name": item.get('name'),
        "exported_at": datetime.now().isoformat(),
        "platforms": {
            "poshmark": format_poshmark_listing(item),
            "depop": format_depop_listing(item),
            "mercari": format_mercari_listing(item),
            "ebay": format_ebay_listing(item)
        }
    }


if __name__ == "__main__":
    # Test with sample item
    test_item = {
        "id": "test123",
        "name": "Platform Ankle Boots",
        "brand": "Dr. Martens",
        "category": "shoes",
        "condition": "good",
        "color": "Black",
        "size": "8",
        "measurements": "4 inch heel, fits true to size",
        "notes": "Minor scuffs on sole, barely noticeable",
        "target_price": 95
    }
    
    result = export_all_platforms(test_item)
    
    print("=" * 60)
    print("LISTING EXPORT TEST")
    print("=" * 60)
    
    for platform, listing in result["platforms"].items():
        print(f"\n{'='*20} {platform.upper()} {'='*20}\n")
        print(f"TITLE: {listing['title']}")
        print(f"\nDESCRIPTION:\n{listing.get('description_plain', listing['description'])}")
        print(f"\nSUGGESTED PRICE: ${listing['suggested_price']}")
