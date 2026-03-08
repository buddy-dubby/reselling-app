# 📦 Reselling App

*AI-powered tool to help Dian sell clothes across multiple platforms.*
*Built by Buddy Dubby 🫠*

## Vision: The Authenticity Advantage

In a world where AI can generate perfect product photos, flawless copy, and convincing reviews — **provenance becomes the moat.**

"This actually existed. Someone actually wore this. There's a real story here."

Reselling is accidentally positioned in the one corner of commerce that gets *stronger* the faker everything else becomes. Like vinyl in a digital world — the inefficiency IS the point.

### Core Features (In Development)

| Feature | Status | Description |
|---------|--------|-------------|
| **Story Mode** | ✅ Built | Generate narrative descriptions that sell identity, not specs |
| **Listing Voice** | 💡 Idea | Detect & maintain your signature seller style |
| **Ghost Inventory** | 💡 Idea | A/B analytics for relisted items |
| **Provenance Tracking** | 💡 Idea | Document purchase history as authentication |

The throughline: **WHO you are as a seller matters more than WHAT you're selling.**

---

## Status: 🚀 Working MVP!

**Web app running at:** http://localhost:5050

## Features

### ✅ Working Now
- **Inventory Management** - Add, view, edit, delete items
- **Photo Upload** - Drag & drop with preview
- **Price Calculator** - Real fee calculations for each platform
- **Status Tracking** - Unlisted → Listed → Sold
- **Quick Stats Dashboard** - Total value, counts by status
- **QR Code Labels** - Print labels with QR codes for physical inventory tracking

### 🚧 Coming Soon
- [x] AI description generator ✅ (added 2026-02-08!)
- [x] Image background removal ✅
- [x] Listing exporter (copy-paste ready text) ✅ (added 2026-02-11!)
- [x] Story Mode CLI ✅ (added 2026-03-07!)
- [ ] Listing Voice - brand consistency detector
- [ ] Ghost Inventory - A/B analytics for relists
- [ ] Cross-posting to multiple platforms
- [ ] Real-time price scraping from sold listings
- [ ] Provenance tracking - documented purchase history

## Quick Start

```bash
cd projects/reselling-app/webapp
source venv/bin/activate
python app.py
```

Open http://localhost:5050 (or http://192.168.1.201:5050 from your phone)

## Platform Fees Built In

| Platform | Fee |
|----------|-----|
| Poshmark | $2.95 under $15, 20% over $15 |
| Depop | 10% + payment processing |
| Mercari | 10% |
| eBay | 13.15% |
| 小红书 | ~5% |

## Tech Stack

- **Backend:** Python/Flask
- **Frontend:** Jinja2 templates, vanilla CSS
- **Storage:** JSON (upgrading to SQLite later)
- **No external frameworks** - fast, simple, works

## Files

```
webapp/
├── app.py              # Main Flask app
├── price_scraper.py    # Price calculator module
├── inventory.json      # Item data
├── uploads/            # Photo storage
└── templates/          # HTML templates
    ├── base.html       # Layout
    ├── index.html      # Inventory view
    ├── add.html        # Add item form
    ├── item.html       # Item detail view
    └── edit.html       # Edit item form
```

## API Endpoints

- `GET /` - Inventory dashboard
- `GET /add` - Add item form
- `POST /add` - Create item
- `GET /item/<id>` - View item
- `GET /item/<id>/edit` - Edit form
- `POST /item/<id>/edit` - Update item
- `POST /item/<id>/delete` - Delete item
- `POST /api/price-check` - Get price recommendations
- `GET /api/inventory` - JSON inventory dump

---

## Story Mode CLI

Generate narrative descriptions that sell stories, not specs.

```bash
cd src
python story-mode.py -c shoes -b "Dr. Martens" -s 8 --condition "like new" -n 3
```

**Example output:**
> "these saw exactly one perfect night - a dinner party in brooklyn. got compliments the whole time but they don't fit my vibe anymore"
> 
> Dr. Martens · size 8 · like new

**Why it works:** The best Depop/Poshmark listings sell identity transfer, not product specs. "Wore this once to a gallery opening" beats "black boots, good condition" because it creates FOMO + social proof + aspirational identity.

**Options:**
- `-c, --category` - shoes, outerwear, dress, vintage
- `-b, --brand` - Brand name
- `-s, --size` - Size
- `--condition` - Condition description
- `-n, --count` - Generate multiple variants
- `--demo` - Show example outputs

---

*Started: 2026-02-07*
*Last update: 2026-03-08*

## Future: 小红书 Integration

**Options researched:**
- Apify XiaoHongShu Scraper (paid, requires account)
- Official 小红书 API (requires business registration)

For now, 小红书 would need manual pricing research until we have API access.

