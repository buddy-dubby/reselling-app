#!/usr/bin/env python3
"""
Real Price Scraper - Actually fetches sold listing data
By: Buddy Dubby (Dub) 🫠

Supports:
- Poshmark (sold listings)
- eBay (completed sales)
"""

import urllib.request
import urllib.parse
import re
import json
import ssl
from dataclasses import dataclass
from typing import Optional
from statistics import mean, median

# Bypass SSL verification for some sites
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

@dataclass
class SoldListing:
    title: str
    price: float
    platform: str
    url: str
    
    def __repr__(self):
        return f"${self.price:.2f} - {self.title[:40]}... ({self.platform})"

@dataclass
class PriceAnalysis:
    query: str
    listings: list
    min_price: float
    max_price: float
    avg_price: float
    median_price: float
    suggested_price: float  # Sweet spot for quick sale
    suggested_range: tuple  # (low, high)
    
    def __repr__(self):
        return f"""
📊 Price Analysis: "{self.query}"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found {len(self.listings)} sold listings

Price Range: ${self.min_price:.2f} - ${self.max_price:.2f}
Average: ${self.avg_price:.2f}
Median: ${self.median_price:.2f}

💰 Suggested Quick Sale: ${self.suggested_price:.2f}
📈 Suggested Range: ${self.suggested_range[0]:.2f} - ${self.suggested_range[1]:.2f}
"""

def fetch_url(url: str) -> Optional[str]:
    """Fetch a URL and return the content"""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def scrape_poshmark(query: str, limit: int = 20) -> list[SoldListing]:
    """
    Scrape Poshmark for sold listings
    Uses their availability filter for sold items
    """
    listings = []
    encoded = urllib.parse.quote(query)
    
    # Poshmark search with sold filter
    # availability=sold_out shows completed sales
    url = f"https://poshmark.com/search?query={encoded}&availability=sold_out&type=listings"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # Parse the JSON data embedded in the page
    # Poshmark includes listing data in a script tag
    pattern = r'"price"\s*:\s*(\d+(?:\.\d+)?)'
    prices = re.findall(pattern, html)
    
    # Also try to find title patterns
    title_pattern = r'"title"\s*:\s*"([^"]+)"'
    titles = re.findall(title_pattern, html)
    
    # Extract listing URLs
    url_pattern = r'href="(/listing/[^"]+)"'
    urls = re.findall(url_pattern, html)
    
    for i, price in enumerate(prices[:limit]):
        try:
            p = float(price)
            if p > 0 and p < 10000:  # Sanity check
                title = titles[i] if i < len(titles) else f"Poshmark Listing #{i+1}"
                listing_url = f"https://poshmark.com{urls[i]}" if i < len(urls) else url
                listings.append(SoldListing(
                    title=title,
                    price=p,
                    platform="Poshmark",
                    url=listing_url
                ))
        except (ValueError, IndexError):
            continue
    
    return listings

def scrape_ebay_sold(query: str, limit: int = 20) -> list[SoldListing]:
    """
    Scrape eBay completed/sold listings
    Uses LH_Sold=1 and LH_Complete=1 parameters
    """
    listings = []
    encoded = urllib.parse.quote(query)
    
    # eBay sold listings search
    url = f"https://www.ebay.com/sch/i.html?_nkw={encoded}&LH_Sold=1&LH_Complete=1&_sop=13"
    
    html = fetch_url(url)
    if not html:
        return listings
    
    # eBay shows sold prices in specific patterns
    # Look for s-item__price spans
    price_pattern = r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)'
    prices_raw = re.findall(price_pattern, html)
    
    # Extract titles
    title_pattern = r'class="s-item__title"[^>]*>(?:<span[^>]*>)?([^<]+)'
    titles = re.findall(title_pattern, html)
    
    # Extract item URLs  
    url_pattern = r'class="s-item__link"[^>]*href="([^"]+)"'
    urls = re.findall(url_pattern, html)
    
    seen_prices = set()
    for i, price_str in enumerate(prices_raw[:limit * 2]):
        try:
            # Remove commas
            p = float(price_str.replace(',', ''))
            if p > 0 and p < 10000 and p not in seen_prices:
                seen_prices.add(p)
                title = titles[i] if i < len(titles) else f"eBay Listing #{i+1}"
                if "Shop on eBay" in title:
                    continue  # Skip ads
                listing_url = urls[i] if i < len(urls) else url
                listings.append(SoldListing(
                    title=title,
                    price=p,
                    platform="eBay",
                    url=listing_url
                ))
                if len(listings) >= limit:
                    break
        except (ValueError, IndexError):
            continue
    
    return listings

def analyze_prices(query: str) -> Optional[PriceAnalysis]:
    """
    Search multiple platforms and analyze sold prices
    """
    print(f"🔍 Searching for: {query}")
    print("━" * 40)
    
    all_listings = []
    
    # Try eBay first (usually more reliable)
    print("📦 Checking eBay sold listings...")
    ebay_results = scrape_ebay_sold(query)
    all_listings.extend(ebay_results)
    print(f"   Found {len(ebay_results)} eBay results")
    
    # Try Poshmark
    print("👗 Checking Poshmark sold listings...")
    posh_results = scrape_poshmark(query)
    all_listings.extend(posh_results)
    print(f"   Found {len(posh_results)} Poshmark results")
    
    if not all_listings:
        print("❌ No sold listings found")
        return None
    
    prices = [l.price for l in all_listings]
    
    avg = mean(prices)
    med = median(prices)
    min_p = min(prices)
    max_p = max(prices)
    
    # Suggested price: slightly below median for quick sale
    suggested = med * 0.9
    
    # Suggested range: 10th to 75th percentile
    sorted_prices = sorted(prices)
    low_idx = len(sorted_prices) // 10
    high_idx = int(len(sorted_prices) * 0.75)
    suggested_range = (sorted_prices[low_idx], sorted_prices[high_idx])
    
    return PriceAnalysis(
        query=query,
        listings=all_listings,
        min_price=min_p,
        max_price=max_p,
        avg_price=avg,
        median_price=med,
        suggested_price=suggested,
        suggested_range=suggested_range
    )

def main():
    """Demo the price scraper"""
    print("🫠 Dub's Price Scraper v2.0")
    print("=" * 50)
    print()
    
    # Test searches
    queries = [
        "dr martens platform heel boots black",
        "vintage levi's 501 jeans",
    ]
    
    for query in queries:
        result = analyze_prices(query)
        if result:
            print(result)
            print("\nTop 5 listings found:")
            for listing in result.listings[:5]:
                print(f"  • {listing}")
        print("\n" + "=" * 50 + "\n")

if __name__ == "__main__":
    main()
