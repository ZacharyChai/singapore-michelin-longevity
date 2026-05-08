# Singapore Michelin Longevity
 
A longitudinal study of Michelin star retention across Singapore's fine dining scene — tracking which restaurants earned stars, kept them, lost them, and closed over nine editions (2016–2025).
 
**[→ Live Dashboard](https://zacharychai.github.io/singapore-michelin-longevity)**
 
---
 
## Why Longevity?
 
Most Michelin data projects look at a single snapshot — who has stars right now, which cuisines dominate, how Singapore compares to Tokyo or Paris. This project asks a different question: **who keeps their stars?**
 
Star retention is a harder and more interesting metric. A restaurant that holds a star for nine consecutive years is telling a fundamentally different story than one that earns and loses it within two editions.
 
---
 
## Key Findings
 
- **14 restaurants** have held a star across all 9 editions — led by Les Amis, Odette, Shoukouwa, Burnt Ends, and Hill Street Tai Hwa Pork Noodle
- **Only 2 demotions** in Singapore's entire Michelin history: Shisen Hanten (2★→1★ in 2023) and Waku Ghin (2★→1★ in 2024) — stars are remarkably sticky once awarded
- **9 promotions** total, with the biggest wave in 2019 (Les Amis and Odette to 3★) and 2022 (Cloudstreet and Thevar to 2★)
- **Chinese cuisine** has the highest average tenure (7.75 years), ahead of Japanese (5.46) and French (5.23)
- The guide grew from **29 starred restaurants in 2016 to 42 in 2025**, with a dip during the post-COVID 2021 edition
---
 
## Dashboard
 
The interactive dashboard (`index.html`) runs entirely in the browser — no server, no dependencies.
 
| Tab | What it shows |
|-----|--------------|
| Overview | Key stats + stacked bar chart of the guide's growth by edition |
| Timeline | Gantt-style grid of every restaurant's star history, filterable by status and searchable by name |
| Longevity | All 63 restaurants ranked by tenure, colour-coded by peak star tier |
| Promotions & Losses | Every star movement catalogued — promotions, demotions, and closures |
| By Cuisine | Average tenure ranked by cuisine type |
 
---
 
## Data
 
### Coverage
- **63 restaurants**, 9 editions: 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025
- Note: the 2020 edition was not published due to COVID-19
### Sources
- Official Michelin Guide Singapore press releases (guide.michelin.com)
- HungryGoWhere annual recap articles
- Tatler Asia Singapore Michelin coverage
- SG Magazine annual star announcements
- SCMP and Eatbook for spot verification of specific events
### Methodology
Year-by-year restaurant lists were compiled from authoritative sources for each edition. Yearly totals were verified against official Michelin announcement counts:
 
| Edition | Starred Restaurants |
|---------|-------------------|
| 2016 | 29 |
| 2017 | 38 |
| 2018 | 39 |
| 2019 | 44 |
| 2021 | 49 |
| 2022 | 52 |
| 2023 | 55 |
| 2024 | 51 |
| 2025 | 42 |
 
Individual restaurant entries were cross-referenced against primary source lists. Promotion and demotion events were verified against multiple news sources.
 
### Files
 
| File | Description |
|------|-------------|
| `index.html` | Standalone interactive dashboard |
| `sg_michelin_wide.csv` | Master dataset — one row per restaurant, one column per edition |
| `sg_michelin_panel.csv` | Long-format panel — one row per restaurant-year |
| `sg_michelin_tenure.csv` | Pre-computed longevity rankings |
| `sg_michelin_data.py` | Data pipeline — builds all CSVs and exports JSON for the dashboard |
 
---
 
## Caveats
 
- Yearly totals match authoritative source counts exactly. Individual cells for specific restaurants in specific middle years are cross-referenced but not exhaustively verified against every primary source.
- Restaurant name variants (e.g. Shinji by Kanesaka across two outlets) are tracked as separate entries.
- "Closure" in this dataset means the restaurant no longer appears in the Michelin Guide — this covers both physical closures and star losses without closure.
---
 
## Running Locally
 
No build step required. Open `index.html` directly in any browser.
 
To regenerate the data:
 
```bash
pip install pandas
python sg_michelin_data.py
```
 
---
 
*Data compiled from public sources. Not affiliated with Michelin.*
 
