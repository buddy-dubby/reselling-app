#!/usr/bin/env python3
"""
Price Scraper Module v2.0
By: Buddy Dubby (Dub) 🫠

Now with REAL price scraping from eBay and Poshmark sold listings!
Plus estimated pricing based on retail prices.
"""

import re
import json
import ssl
import urllib.request
import urllib.parse
from dataclasses import dataclass
from typing import List, Optional, Dict
from statistics import mean, median

# SSL context for HTTPS requests
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
}

@dataclass
class PriceResult:
    platform: str
    title: str
    price: float
    url: str
    condition: str = "unknown"
    sold: bool = False

@dataclass 
class ScrapedListing:
    title: str
    price: float
    platform: str
    url: str

def fetch_url(url: str) -> Optional[str]:
    """Fetch a URL and return the content"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Fetch error: {e}")
        return None

def scrape_ebay_sold(query: str, limit: int = 15) -> List[ScrapedListing]:
    """Scrape eBay for SOLD listings"""
    listings = []
    encoded = urllib.parse.quote(query)
    url = f"https://www.ebay.com/sch/i.html?_nkw={encoded}&LH_Sold=1&LH_Complete=1&_sop=13"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # Extract prices
    price_pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
    prices_raw = re.findall(price_pattern, html)
    
    seen = set()
    for price_str in prices_raw[:limit * 3]:
        try:
            p = float(price_str.replace(',', ''))
            if 1 < p < 5000 and p not in seen:  # Filter outliers
                seen.add(p)
                listings.append(ScrapedListing(
                    title=f"eBay Sold Item",
                    price=p,
                    platform="eBay",
                    url=url
                ))
                if len(listings) >= limit:
                    break
        except ValueError:
            continue
    
    return listings

def scrape_poshmark_sold(query: str, limit: int = 15) -> List[ScrapedListing]:
    """Scrape Poshmark for SOLD listings"""
    listings = []
    encoded = urllib.parse.quote(query)
    url = f"https://poshmark.com/search?query={encoded}&availability=sold_out"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # Extract prices from JSON data
    pattern = r'"price"\s*:\s*(\d+(?:\.\d+)?)'
    prices = re.findall(pattern, html)
    
    seen = set()
    for price_str in prices[:limit * 2]:
        try:
            p = float(price_str)
            if 1 < p < 5000 and p not in seen:
                seen.add(p)
                listings.append(ScrapedListing(
                    title=f"Poshmark Sold Item",
                    price=p,
                    platform="Poshmark",
                    url=url
                ))
                if len(listings) >= limit:
                    break
        except ValueError:
            continue
    
    return listings

def scrape_depop_sold(query: str, limit: int = 15) -> List[ScrapedListing]:
    """
    Scrape sold listings from Depop.
    """
    listings = []
    search_query = urllib.parse.quote(query)
    url = f"https://www.depop.com/search/?q={search_query}"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # Depop price patterns
    patterns = [
        r'\$(\d+(?:\.\d{2})?)',
        r'"price":\s*{\s*"amount":\s*"?(\d+(?:\.\d{2})?)"?',
        r'data-price="(\d+(?:\.\d{2})?)"',
    ]
    
    seen = set()
    for pattern in patterns:
        prices = re.findall(pattern, html)
        for price_str in prices[:limit * 2]:
            try:
                p = float(price_str)
                if 1 < p < 5000 and p not in seen:
                    seen.add(p)
                    listings.append(ScrapedListing(
                        title=f"Depop Item",
                        price=p,
                        platform="Depop",
                        url=url
                    ))
                    if len(listings) >= limit:
                        return listings
            except ValueError:
                continue
    
    return listings

def scrape_mercari_sold(query: str, limit: int = 15) -> List[ScrapedListing]:
    """
    Scrape sold listings from Mercari.
    """
    listings = []
    search_query = urllib.parse.quote(query)
    url = f"https://www.mercari.com/search/?keyword={search_query}&status=sold_out"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # Mercari uses data attributes or JSON - try to extract prices
    # Pattern for Mercari price display
    patterns = [
        r'\$(\d+(?:\.\d{2})?)</span>',  # Standard price format
        r'"price":(\d+(?:\.\d{2})?)',    # JSON format
        r'data-price="(\d+(?:\.\d{2})?)"',  # Data attribute
    ]
    
    seen = set()
    for pattern in patterns:
        prices = re.findall(pattern, html)
        for price_str in prices[:limit * 2]:
            try:
                p = float(price_str)
                if 1 < p < 5000 and p not in seen:
                    seen.add(p)
                    listings.append(ScrapedListing(
                        title=f"Mercari Sold Item",
                        price=p,
                        platform="Mercari",
                        url=url
                    ))
                    if len(listings) >= limit:
                        return listings
            except ValueError:
                continue
    
    return listings

def get_real_market_prices(query: str) -> Optional[Dict]:
    """
    Get REAL prices from sold listings across platforms.
    Returns analysis with min, max, avg, median, and suggestions.
    """
    all_listings = []
    
    # Scrape all platforms
    all_listings.extend(scrape_ebay_sold(query))
    all_listings.extend(scrape_poshmark_sold(query))
    all_listings.extend(scrape_mercari_sold(query))
    all_listings.extend(scrape_depop_sold(query))
    
    if len(all_listings) < 3:
        return None  # Not enough data
    
    prices = [l.price for l in all_listings]
    
    # Filter out extreme outliers (> 3 std deviations)
    avg = mean(prices)
    filtered = [p for p in prices if p < avg * 3]
    if not filtered:
        filtered = prices
    
    med = median(filtered)
    
    return {
        "count": len(filtered),
        "min": min(filtered),
        "max": max(filtered),
        "avg": round(mean(filtered), 2),
        "median": round(med, 2),
        "quick_sale": round(med * 0.85, 2),  # 15% below median
        "fair_price": round(med, 2),
        "max_value": round(med * 1.2, 2),    # 20% above median
        "source": "live_scrape"
    }

def extract_price(text: str) -> Optional[float]:
    """Extract price from text like '$45.00' or '45.00 USD'"""
    patterns = [
        r'\$(\d+(?:\.\d{2})?)',
        r'(\d+(?:\.\d{2})?)\s*(?:USD|dollars?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None

def estimate_from_retail(retail_price: float, condition: str = "good") -> Dict[str, float]:
    """
    Estimate resale value based on retail price and condition.
    Based on common resale market data.
    """
    multipliers = {
        "new": (0.60, 0.85),      # 60-85% of retail for new with tags
        "excellent": (0.45, 0.65), # 45-65% for excellent condition
        "good": (0.30, 0.50),      # 30-50% for good condition  
        "fair": (0.15, 0.30),      # 15-30% for fair condition
    }
    
    low_mult, high_mult = multipliers.get(condition, (0.30, 0.50))
    
    return {
        "low": round(retail_price * low_mult, 2),
        "high": round(retail_price * high_mult, 2),
        "avg": round(retail_price * (low_mult + high_mult) / 2, 2)
    }

def get_platform_fees() -> Dict[str, Dict]:
    """Platform fee structures for profit calculation"""
    return {
        "poshmark": {
            "fee_under_15": 2.95,  # Flat $2.95 for sales under $15
            "fee_percent": 0.20,   # 20% for sales $15+
            "threshold": 15.00
        },
        "depop": {
            "fee_percent": 0.10,   # 10% selling fee
            "payment_fee": 0.029,  # 2.9% + $0.30 payment processing
            "payment_flat": 0.30
        },
        "mercari": {
            "fee_percent": 0.10,   # 10% selling fee
        },
        "ebay": {
            "fee_percent": 0.1315, # 13.15% for most categories
        },
        "xiaohongshu": {
            "fee_percent": 0.05,   # ~5% for individual sellers
        }
    }

def calculate_net_profit(sale_price: float, platform: str, item_cost: float = 0) -> Dict:
    """Calculate net profit after platform fees"""
    fees = get_platform_fees().get(platform, {"fee_percent": 0.10})
    
    if platform == "poshmark":
        if sale_price < fees["threshold"]:
            total_fee = fees["fee_under_15"]
        else:
            total_fee = sale_price * fees["fee_percent"]
    elif platform == "depop":
        selling_fee = sale_price * fees["fee_percent"]
        payment_fee = sale_price * fees["payment_fee"] + fees["payment_flat"]
        total_fee = selling_fee + payment_fee
    else:
        total_fee = sale_price * fees.get("fee_percent", 0.10)
    
    net = sale_price - total_fee
    profit = net - item_cost if item_cost else net
    
    return {
        "sale_price": sale_price,
        "platform_fee": round(total_fee, 2),
        "net_payout": round(net, 2),
        "profit": round(profit, 2),
        "profit_margin": round((profit / sale_price * 100) if sale_price else 0, 1)
    }

def generate_price_recommendation(
    item_name: str,
    brand: str = "",
    condition: str = "good",
    retail_price: float = None,
    item_cost: float = 0,
    use_live_data: bool = True
) -> Dict:
    """
    Generate pricing recommendations for an item.
    Now tries to get REAL market data first!
    """
    # Try to get real market prices first
    real_prices = None
    search_query = f"{brand} {item_name}".strip() if brand else item_name
    
    if use_live_data:
        try:
            real_prices = get_real_market_prices(search_query)
        except Exception as e:
            print(f"Live price fetch failed: {e}")
    
    # Use real data if available, otherwise fall back to estimates
    if real_prices and real_prices.get("count", 0) >= 3:
        quick_sale = real_prices["quick_sale"]
        fair_price = real_prices["fair_price"]
        max_value = real_prices["max_value"]
        data_source = f"live ({real_prices['count']} sold listings)"
        
        estimates = {
            "low": real_prices["min"],
            "high": real_prices["max"],
            "avg": real_prices["avg"]
        }
    elif retail_price:
        # Fall back to retail-based estimates
        estimates = estimate_from_retail(retail_price, condition)
        quick_sale = estimates["low"]
        fair_price = estimates["avg"]
        max_value = estimates["high"]
        data_source = "estimated from retail"
    else:
        # Default ranges
        estimates = {
            "low": 25.0,
            "high": 75.0,
            "avg": 50.0
        }
        quick_sale = estimates["low"]
        fair_price = estimates["avg"]
        max_value = estimates["high"]
        data_source = "default estimate"
    
    # Ensure we're above floor price (item cost)
    if item_cost:
        min_price = item_cost * 1.1  # At least 10% above cost
        quick_sale = max(quick_sale, min_price)
        fair_price = max(fair_price, min_price)
    
    # Platform breakdown
    platforms = {}
    for platform in ["poshmark", "depop", "mercari", "ebay"]:
        platforms[platform] = {
            "quick_sale": calculate_net_profit(quick_sale, platform, item_cost),
            "fair_price": calculate_net_profit(fair_price, platform, item_cost),
            "max_value": calculate_net_profit(max_value, platform, item_cost),
        }
    
    return {
        "item": item_name,
        "brand": brand,
        "condition": condition,
        "data_source": data_source,
        "market_data": real_prices if real_prices else None,
        "estimates": {
            "quick_sale": quick_sale,
            "fair_price": fair_price,
            "max_value": max_value
        },
        "platforms": platforms,
        "recommendation": f"List at ${fair_price:.2f} for fair value, or ${quick_sale:.2f} for quick sale"
    }

# Quick test
if __name__ == "__main__":
    print("🫠 Dub's Price Calculator")
    print("=" * 40)
    
    result = generate_price_recommendation(
        item_name="Dr. Martens Platform Heel Boots",
        brand="Dr. Martens",
        condition="good",
        retail_price=200.00,
        item_cost=50.00
    )
    
    print(f"\n{result['item']} ({result['condition']} condition)")
    print(f"Retail: $200.00 | You paid: $50.00")
    print(f"\nRecommended prices:")
    print(f"  Quick sale: ${result['estimates']['quick_sale']:.2f}")
    print(f"  Fair price: ${result['estimates']['fair_price']:.2f}")
    print(f"  Max value:  ${result['estimates']['max_value']:.2f}")
    
    print(f"\nNet profit at fair price by platform:")
    for platform, data in result['platforms'].items():
        fp = data['fair_price']
        print(f"  {platform}: ${fp['net_payout']:.2f} payout, ${fp['profit']:.2f} profit ({fp['profit_margin']}%)")
