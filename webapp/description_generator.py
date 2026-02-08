#!/usr/bin/env python3
"""
Description Generator Module
By: Buddy Dubby (Dub) 🫠

Generates listing descriptions for resale items.
"""

from typing import Dict, Optional

def generate_description(
    name: str,
    brand: str = "",
    category: str = "",
    condition: str = "good",
    color: str = "",
    size: str = "",
    measurements: str = "",
    notes: str = "",
    style: str = "casual"  # casual, professional, trendy
) -> Dict[str, str]:
    """
    Generate platform-specific descriptions.
    Returns descriptions optimized for each platform.
    """
    
    # Condition descriptions
    condition_text = {
        "new": "Brand new with tags, never worn!",
        "excellent": "Like new condition, minimal to no signs of wear.",
        "good": "Gently used, in great condition with light wear.",
        "fair": "Pre-loved with visible signs of wear. Please see photos for details."
    }
    
    # Category emoji
    category_emoji = {
        "tops": "👕",
        "bottoms": "👖",
        "dresses": "👗",
        "outerwear": "🧥",
        "shoes": "👟",
        "bags": "👜",
        "accessories": "💍",
        "other": "✨"
    }
    
    emoji = category_emoji.get(category, "✨")
    cond_desc = condition_text.get(condition, condition_text["good"])
    
    # Build title (avoid duplicating brand if it's already in the name)
    title_parts = []
    if brand and brand.lower() not in name.lower():
        title_parts.append(brand)
    title_parts.append(name)
    if size:
        title_parts.append(f"Size {size}")
    
    title = " ".join(title_parts)
    
    # Base description
    base_desc = f"{emoji} {title}\n\n"
    if brand:
        base_desc += f"Brand: {brand}\n"
    if color:
        base_desc += f"Color: {color}\n"
    if size:
        base_desc += f"Size: {size}\n"
    if measurements:
        base_desc += f"Measurements: {measurements}\n"
    base_desc += f"\nCondition: {cond_desc}\n"
    if notes:
        base_desc += f"\n{notes}\n"
    
    # Platform-specific versions
    
    # Poshmark - longer, story-driven
    poshmark_desc = base_desc + """
💕 Bundle to save on shipping!
📦 Ships within 1-2 business days
❓ Questions? Just ask!

#"""
    if brand:
        poshmark_desc += brand.lower().replace(" ", "") + " "
    if category:
        poshmark_desc += category + " "
    poshmark_desc += "resale thrift secondhand"
    
    # Depop - shorter, more casual/trendy
    depop_desc = f"{emoji} {title}\n\n{cond_desc}\n"
    if measurements:
        depop_desc += f"📏 {measurements}\n"
    depop_desc += "\n✨ dm me with any questions!"
    
    # eBay - professional, detailed
    ebay_desc = f"""<h2>{title}</h2>
<p><strong>Brand:</strong> {brand or 'Unbranded'}</p>
<p><strong>Condition:</strong> {cond_desc}</p>
"""
    if color:
        ebay_desc += f"<p><strong>Color:</strong> {color}</p>\n"
    if size:
        ebay_desc += f"<p><strong>Size:</strong> {size}</p>\n"
    if measurements:
        ebay_desc += f"<p><strong>Measurements:</strong> {measurements}</p>\n"
    if notes:
        ebay_desc += f"<p>{notes}</p>\n"
    ebay_desc += """
<p>Please review all photos carefully. Feel free to message with any questions!</p>
<p>Ships within 1-2 business days with tracking.</p>"""
    
    # Mercari - concise but friendly
    mercari_desc = f"{title}\n\n{cond_desc}\n"
    if size:
        mercari_desc += f"Size: {size}\n"
    if measurements:
        mercari_desc += f"Measurements: {measurements}\n"
    mercari_desc += "\nMessage me with any questions! Ships fast 📦"
    
    # 小红书 (Xiaohongshu) - Chinese, trendy vibes
    xiaohongshu_desc = f"""✨ {title}

品牌: {brand or '无品牌'}
状态: {'全新带标签' if condition == 'new' else '九成新' if condition == 'excellent' else '八成新' if condition == 'good' else '有使用痕迹'}
"""
    if size:
        xiaohongshu_desc += f"尺码: {size}\n"
    if color:
        xiaohongshu_desc += f"颜色: {color}\n"
    xiaohongshu_desc += """
🏷️ 闲置转让 价格可小刀
💬 有问题可以私信~"""
    
    return {
        "title": title,
        "poshmark": poshmark_desc,
        "depop": depop_desc,
        "ebay": ebay_desc,
        "mercari": mercari_desc,
        "xiaohongshu": xiaohongshu_desc,
        "generic": base_desc
    }


# Quick test
if __name__ == "__main__":
    print("🫠 Dub's Description Generator")
    print("=" * 40)
    
    result = generate_description(
        name="Platform Heel Boots",
        brand="Dr. Martens",
        category="shoes",
        condition="good",
        color="Black",
        size="US 8",
        measurements="Heel height: 3 inches",
        notes="Super comfortable chunky platform. Perfect for fall!"
    )
    
    print(f"\nTitle: {result['title']}")
    print("\n--- Poshmark ---")
    print(result['poshmark'])
    print("\n--- Depop ---")
    print(result['depop'])
    print("\n--- 小红书 ---")
    print(result['xiaohongshu'])
