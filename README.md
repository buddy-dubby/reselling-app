# 📦 Reselling App

*AI-powered tool to help Dian sell clothes across multiple platforms.*
*Built by Buddy Dubby 🫠*

## Status: 🚀 Working MVP!

**Web app running at:** http://localhost:5050

## Features

### ✅ Working Now
- **Inventory Management** - Add, view, edit, delete items
- **Photo Upload** - Drag & drop with preview
- **Price Calculator** - Real fee calculations for each platform
- **Status Tracking** - Unlisted → Listed → Sold
- **Quick Stats Dashboard** - Total value, counts by status

### 🚧 Coming Soon
- [x] AI description generator ✅ (added 2026-02-08!)
- [x] Image background removal ✅
- [x] Listing exporter (copy-paste ready text) ✅ (added 2026-02-11!)
- [ ] Cross-posting to multiple platforms
- [ ] Real-time price scraping from sold listings

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

*Started: 2026-02-07*
*Last update: 2026-02-07*

## Future: 小红书 Integration

**Options researched:**
- Apify XiaoHongShu Scraper (paid, requires account)
- Official 小红书 API (requires business registration)

For now, 小红书 would need manual pricing research until we have API access.

