#!/usr/bin/env python3
"""
Story Mode Description Generator
Transforms boring product listings into narrative-driven descriptions.

The insight: "wore this once to a gallery opening" sells better than "black boots, size 8"
Because it transfers identity + creates FOMO + provides social proof.

Usage:
    python story-mode.py --category shoes --brand "Dr. Martens" --size 8 --condition "like new"
    python story-mode.py -c dress -b "Reformation" -s M
    python story-mode.py --demo
"""

import argparse
import random
import sys

# Story templates by category
STORY_TEMPLATES = {
    "shoes": [
        "these saw exactly one perfect night - {occasion}. got compliments the whole time but they don't fit my vibe anymore",
        "bought for {occasion}, ended up being way too cute to actually wear more than twice. your gain",
        "okay real talk I have too many shoes and these deserve someone who'll actually wear them",
        "impulse bought, wore maybe 3 times?? they're incredible I just have commitment issues with footwear",
        "these were my going-out shoes for like a month. now I'm in my quiet era. your chaos era awaits",
    ],
    "outerwear": [
        "this jacket has witnessed some things. {occasion}. now it needs new adventures",
        "got this for {occasion} and it became my whole personality for a season. time to evolve",
        "layering season is coming. I already have 47 jackets. you should have 1 more",
        "bought this thinking I'd become a different person. I did not. jacket is still incredible tho",
    ],
    "dress": [
        "wore this exactly once - {occasion}. got asked where I got it like 4 times",
        "this was giving main character energy but I already have a main character dress. you can have this one",
        "got this for {occasion} and then realized I don't go to those things lol",
        "closet purge! this deserves someone who actually goes outside",
    ],
    "vintage": [
        "found this at {location}. it has that energy that only actual vintage has",
        "this has a previous life. I'm just the current custodian. you could be next",
        "the kind of piece you can't find anymore. literally. I've tried",
        "someone cooler than me wore this in the 90s/00s/whenever. now it's your turn",
    ],
    "default": [
        "impulse bought this, wore it {times}, now it lives in my closet judging me. free it",
        "this deserves someone who'll actually use it. I clearly am not that person",
        "decluttering because I have problems. this is not a problem, it's a solution for you",
        "my style evolved but this is still perfect for someone",
    ]
}

OCCASIONS = [
    "a gallery opening in soho",
    "a first date that actually went well",
    "my friend's birthday at that rooftop bar",
    "a job interview (got it btw)",
    "a wedding where I was definitely overdressed",
    "a random tuesday when I decided to be that person",
    "brunch with people I was trying to impress",
    "a concert where I stood for 4 hours",
    "a friend's art show",
    "a dinner party in brooklyn",
]

LOCATIONS = [
    "a vintage shop in the village",
    "that goodwill that actually has good stuff",
    "a thrift store in LA",
    "an estate sale (the good kind)",
    "a flea market in brooklyn",
    "depop before it got weird",
]

TIMES = ["once", "twice", "maybe 3 times??", "like a handful of times", "more than I'll admit"]


def generate_story_description(category: str, brand: str = None, condition: str = None, size: str = None) -> str:
    """Generate a narrative description for an item."""
    
    # Pick template category
    template_key = category.lower() if category.lower() in STORY_TEMPLATES else "default"
    template = random.choice(STORY_TEMPLATES[template_key])
    
    # Fill in variables
    story = template.format(
        occasion=random.choice(OCCASIONS),
        location=random.choice(LOCATIONS),
        times=random.choice(TIMES)
    )
    
    # Add specs naturally at the end
    specs = []
    if brand:
        specs.append(brand)
    if size:
        specs.append(f"size {size}")
    if condition:
        specs.append(condition)
    
    if specs:
        story += f"\n\n{' · '.join(specs)}"
    
    return story


def demo():
    """Run demo with example items."""
    print("=" * 60)
    print("STORY MODE - Description Generator")
    print("=" * 60)
    print()
    
    examples = [
        {"category": "shoes", "brand": "Dr. Martens Kendra", "size": "8", "condition": "like new"},
        {"category": "dress", "brand": "Reformation", "size": "S", "condition": "worn once"},
        {"category": "outerwear", "brand": "Vintage Levi's", "size": "M", "condition": "great condition"},
    ]
    
    for ex in examples:
        print(f"INPUT: {ex['brand']}, size {ex['size']}, {ex['condition']}")
        print("-" * 40)
        print(generate_story_description(**ex))
        print()


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate story-driven reselling descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -c shoes -b "Dr. Martens" -s 8 --condition "like new"
  %(prog)s --category dress --brand "Reformation" --size M
  %(prog)s --demo

Categories: shoes, outerwear, dress, vintage (or any for default templates)
        """
    )
    parser.add_argument("-c", "--category", help="Item category (shoes, outerwear, dress, vintage)")
    parser.add_argument("-b", "--brand", help="Brand name")
    parser.add_argument("-s", "--size", help="Size")
    parser.add_argument("--condition", help="Condition (like new, good, worn)")
    parser.add_argument("-n", "--count", type=int, default=1, help="Number of variants to generate")
    parser.add_argument("--demo", action="store_true", help="Run demo with example items")
    
    args = parser.parse_args()
    
    if args.demo:
        demo()
        return
    
    if not args.category:
        parser.print_help()
        print("\nError: --category is required (or use --demo)")
        sys.exit(1)
    
    for i in range(args.count):
        if args.count > 1:
            print(f"--- Option {i+1} ---")
        print(generate_story_description(
            category=args.category,
            brand=args.brand,
            size=args.size,
            condition=args.condition
        ))
        if i < args.count - 1:
            print()


if __name__ == "__main__":
    main()
