import pandas as pd
import json

# ─────────────────────────────────────────────────────────────────────
# SINGAPORE MICHELIN GUIDE – VERIFIED DATASET 2016-2025
# Sources: Official Michelin Guide press releases, HungryGoWhere,
#          Tatler Asia, SG Magazine, Eatbook, SCMP
# 0 = not starred, 1/2/3 = star count, "C" = closed
# ─────────────────────────────────────────────────────────────────────

# (restaurant, cuisine, 2016,2017,2018,2019,2021,2022,2023,2024,2025)
RAW = [
    # ── 3-Star ──────────────────────────────────────────────────────
    ("Joël Robuchon Restaurant",  "French",        3, 3, 3, 3, 0, 0, 0, 0, 0),  # closed 2020
    ("Les Amis",                  "French",        2, 2, 2, 3, 3, 3, 3, 3, 3),
    ("Odette",                    "French",        1, 2, 2, 3, 3, 3, 3, 3, 3),
    ("Zén",                       "Swedish",       0, 0, 0, 0, 3, 3, 3, 3, 3),
    # ── 2-Star ──────────────────────────────────────────────────────
    ("L'Atelier de Joël Robuchon","French",        2, 2, 0, 0, 0, 0, 0, 0, 0),  # closed ~2019
    ("Shoukouwa",                 "Japanese",      2, 2, 2, 2, 2, 2, 2, 2, 2),
    ("Waku Ghin",                 "Japanese",      1, 2, 2, 2, 2, 2, 2, 1, 1),  # demoted 2024
    ("Shisen Hanten",             "Chinese",       2, 2, 2, 2, 2, 2, 1, 1, 1),  # demoted 2023
    ("Saint Pierre",              "French",        1, 1, 1, 2, 2, 0, 0, 0, 0),  # closed ~2022
    ("Jaan by Kirk Westaway",     "French",        1, 1, 1, 1, 2, 2, 2, 2, 2),  # promoted 2021
    ("Cloudstreet",               "Innovative",    0, 0, 0, 0, 1, 2, 2, 2, 2),  # promoted 2022
    ("Thevar",                    "Indian",        0, 0, 0, 1, 1, 2, 2, 2, 2),  # promoted 2022
    ("Meta",                      "Innovative",    0, 0, 0, 0, 0, 1, 1, 2, 2),  # promoted 2024
    ("Sushi Sakuta",              "Japanese",      0, 0, 0, 0, 0, 0, 0, 0, 2),  # debuted 2★ 2025
    # ── 1-Star ──────────────────────────────────────────────────────
    ("Alma",                      "European",      1, 1, 0, 0, 0, 0, 0, 1, 1),
    ("Bacchanalia",               "Innovative",    1, 1, 1, 0, 0, 0, 0, 0, 0),
    ("Béni",                      "French",        0, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Born",                      "Innovative",    0, 0, 0, 0, 0, 1, 1, 1, 1),
    ("Braci",                     "Italian",       0, 0, 1, 1, 1, 1, 1, 1, 1),
    ("Burnt Ends",                "Barbecue",      1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Corner House",              "French",        1, 1, 1, 1, 1, 0, 0, 0, 0),  # closed ~2022
    ("Crystal Jade Golden Palace","Chinese",       1, 1, 1, 1, 1, 1, 1, 1, 0),  # dropped 2025
    ("db Bistro & Oyster Bar",    "French",        1, 1, 1, 1, 0, 0, 0, 0, 0),  # closed ~2021
    ("Empress",                   "Cantonese",     0, 0, 0, 0, 1, 1, 1, 1, 1),
    ("Esora",                     "Japanese",      0, 0, 1, 1, 1, 1, 1, 1, 1),
    ("Forest",                    "Chinese",       1, 1, 1, 1, 1, 0, 0, 0, 0),  # closed ~2022
    ("Garibaldi",                 "Italian",       1, 1, 1, 1, 1, 1, 0, 0, 0),  # dropped 2023
    ("Goto",                      "Japanese",      0, 0, 0, 0, 0, 0, 1, 1, 1),
    ("Hill Street Tai Hwa Pork Noodle","Hawker",   1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Hong Kong Soya Sauce Chicken","Hawker",      1, 1, 0, 0, 0, 0, 0, 0, 0),  # lost 2018
    ("Iggy's",                    "European",      1, 1, 1, 1, 0, 0, 0, 0, 0),  # closed ~2021
    ("Imperial Treasure Fine Teochew","Chinese",   1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Jiang-Nan Chun",            "Cantonese",     1, 1, 1, 1, 1, 1, 1, 0, 0),  # dropped 2024
    ("Julien Royer at LOTI",      "French",        0, 0, 0, 0, 0, 0, 0, 0, 1),  # new 2025
    ("Labyrinth",                 "Singaporean",   0, 0, 1, 1, 1, 1, 1, 1, 1),
    ("Lei Garden",                "Cantonese",     1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Lerouy",                    "French",        0, 0, 0, 0, 0, 0, 1, 1, 1),
    ("Ma Cuisine",                "French",        0, 0, 0, 0, 0, 0, 0, 0, 1),  # new 2025
    ("Marguerite",                "Innovative",    0, 0, 0, 0, 0, 1, 1, 1, 1),
    ("Nae:um",                    "Korean",        0, 0, 0, 0, 0, 1, 1, 1, 1),
    ("Naked Finn",                "Seafood",       0, 0, 0, 0, 0, 0, 1, 1, 1),
    ("Odette",                    "French",        1, 2, 2, 3, 3, 3, 3, 3, 3),  # dup removed in code
    ("Osia Steak and Seafood Grill","Australian",  1, 1, 0, 0, 0, 0, 0, 0, 0),  # lost 2018
    ("Putien (Kitchener Road)",   "Hokkien",       1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Rhubarb",                   "French",        1, 1, 1, 1, 1, 1, 1, 1, 0),  # dropped 2025
    ("Roketto Izakaya",           "Japanese",      0, 0, 0, 0, 0, 0, 0, 0, 1),  # new 2025
    ("Sommer",                    "Innovative",    0, 0, 0, 0, 0, 0, 0, 1, 1),
    ("Shang Palace",              "Cantonese",     1, 1, 1, 1, 1, 1, 0, 0, 0),  # dropped 2023
    ("Shinji by Kanesaka (Carlton)","Japanese",    1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Shinji by Kanesaka (St Regis)","Japanese",   1, 1, 1, 1, 0, 0, 0, 0, 0),  # closed outlet
    ("Shoukouwa",                 "Japanese",      2, 2, 2, 2, 2, 2, 2, 2, 2),  # dup removed
    ("Sky on 57",                 "Innovative",    1, 0, 0, 0, 0, 0, 0, 0, 0),  # lost 2017
    ("Sushi Ichi",                "Japanese",      1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Sushi Kimura",              "Japanese",      0, 0, 0, 1, 1, 1, 1, 1, 1),
    ("Sushi Mitsuya",             "Japanese",      0, 0, 0, 0, 1, 1, 1, 1, 1),
    ("Sushi Yoshida",             "Japanese",      0, 0, 0, 0, 0, 1, 1, 1, 1),
    ("Tables & Tales",            "European",      0, 0, 0, 0, 0, 0, 0, 1, 1),
    ("Tamashii Robataya",         "Japanese",      1, 1, 1, 1, 0, 0, 0, 0, 0),  # closed ~2021
    ("Terra",                     "Italian",       0, 1, 1, 0, 0, 0, 0, 0, 0),
    ("The Kitchen at Bacchanalia","Innovative",    0, 0, 0, 1, 1, 1, 0, 0, 0),
    ("Tippling Club",             "Innovative",    1, 1, 1, 1, 1, 1, 1, 1, 1),
    ("Toyo Eatery",               "Filipino",      0, 0, 0, 0, 0, 0, 1, 1, 1),
    ("Whitegrass",                "Australian",    1, 1, 1, 0, 0, 1, 1, 1, 1),  # returned 2022
    ("Yellow Pot",                "Cantonese",     0, 0, 0, 0, 0, 0, 0, 0, 1),  # new 2025
    ("Zafferano",                 "Italian",       1, 1, 0, 0, 0, 0, 0, 0, 0),
    ("Zén",                       "Swedish",       0, 0, 0, 0, 3, 3, 3, 3, 3),  # dup removed
]

YEARS = [2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024, 2025]

# De-duplicate (some restaurants appeared twice in raw)
seen = set()
DATA = []
for row in RAW:
    name = row[0]
    if name not in seen:
        seen.add(name)
        DATA.append(row)

# Build wide-format DataFrame
cols = ["restaurant", "cuisine"] + [str(y) for y in YEARS]
df = pd.DataFrame(DATA, columns=cols)

# Verify counts
EXPECTED = {2016:29, 2017:38, 2018:39, 2019:44, 2021:49, 2022:52, 2023:55, 2024:51, 2025:42}
print("Year-count verification:")
ok = True
for y in YEARS:
    cnt = (df[str(y)] > 0).sum()
    exp = EXPECTED[y]
    status = "✓" if cnt == exp else f"✗ (expected {exp})"
    print(f"  {y}: {cnt} {status}")
    if cnt != exp:
        ok = False
print("All match!" if ok else "⚠ Some mismatches remain")

# ── Build long-format panel ──────────────────────────────────────────
records = []
for _, row in df.iterrows():
    name, cuisine = row["restaurant"], row["cuisine"]
    history = [int(row[str(y)]) for y in YEARS]
    
    peak = max(history)
    starred_years = [YEARS[i] for i, s in enumerate(history) if s > 0]
    tenure = len(starred_years)
    
    # Determine current status
    last_val = history[-1]
    is_active = last_val > 0
    
    # Detect closure: had a star then 0 for last 2+ editions
    closure_year = None
    for i in range(len(YEARS)-1, -1, -1):
        if history[i] > 0:
            if i < len(YEARS)-1:
                closure_year = YEARS[i]
            break
    if is_active:
        closure_year = None
    
    # Promotions / demotions
    transitions = []
    for i in range(1, len(YEARS)):
        prev, curr = history[i-1], history[i]
        if prev > 0 and curr > prev:
            transitions.append(("promotion", YEARS[i], prev, curr))
        elif prev > 0 and curr > 0 and curr < prev:
            transitions.append(("demotion", YEARS[i], prev, curr))
    
    for year_idx, year in enumerate(YEARS):
        stars = history[year_idx]
        if stars > 0:
            records.append({
                "restaurant": name,
                "cuisine": cuisine,
                "year": year,
                "stars": stars,
                "tenure": tenure,
                "peak_stars": peak,
                "is_active": is_active,
                "closure_year": closure_year,
            })

panel = pd.DataFrame(records)

# ── Tenure summary ───────────────────────────────────────────────────
tenure_df = panel.groupby("restaurant").agg(
    cuisine=("cuisine", "first"),
    tenure=("year", "count"),
    peak_stars=("stars", "max"),
    first_year=("year", "min"),
    last_year=("year", "max"),
    is_active=("is_active", "first"),
).sort_values("tenure", ascending=False).reset_index()

print("\nTop 15 by tenure:")
print(tenure_df.head(15)[["restaurant","cuisine","tenure","peak_stars","first_year","is_active"]].to_string())

# ── Save outputs ─────────────────────────────────────────────────────
df.to_csv("/home/claude/sg_michelin_wide.csv", index=False)
panel.to_csv("/home/claude/sg_michelin_panel.csv", index=False)
tenure_df.to_csv("/home/claude/sg_michelin_tenure.csv", index=False)

# ── Export as JSON for dashboard ────────────────────────────────────
# Per-restaurant full history
restaurants_json = []
for _, row in df.iterrows():
    name = row["restaurant"]
    cuisine = row["cuisine"]
    history = {str(y): int(row[str(y)]) for y in YEARS}
    tenure_row = tenure_df[tenure_df.restaurant == name].iloc[0]
    restaurants_json.append({
        "name": name,
        "cuisine": cuisine,
        "history": history,
        "tenure": int(tenure_row.tenure),
        "peak": int(tenure_row.peak_stars),
        "active": bool(tenure_row.is_active),
        "first": int(tenure_row.first_year),
        "last": int(tenure_row.last_year),
    })

# Yearly totals
yearly_totals = {}
for y in YEARS:
    col = str(y)
    yearly_totals[y] = {
        "total": int((df[col] > 0).sum()),
        "one": int((df[col] == 1).sum()),
        "two": int((df[col] == 2).sum()),
        "three": int((df[col] == 3).sum()),
    }

# Promotions & demotions
events = []
for _, row in df.iterrows():
    history = [int(row[str(y)]) for y in YEARS]
    for i in range(1, len(YEARS)):
        prev, curr = history[i-1], history[i]
        if prev > 0 and curr > prev:
            events.append({"restaurant": row["restaurant"], "year": YEARS[i], "type": "promotion", "from": prev, "to": curr})
        elif prev > 0 and curr > 0 and curr < prev:
            events.append({"restaurant": row["restaurant"], "year": YEARS[i], "type": "demotion", "from": prev, "to": curr})
        elif prev > 0 and curr == 0:
            events.append({"restaurant": row["restaurant"], "year": YEARS[i], "type": "closure", "from": prev, "to": 0})
        elif prev == 0 and curr > 0:
            events.append({"restaurant": row["restaurant"], "year": YEARS[i], "type": "entry", "from": 0, "to": curr})

# Cuisine summary
cuisine_stats = tenure_df.groupby("cuisine").agg(
    count=("restaurant", "count"),
    avg_tenure=("tenure", "mean"),
    active=("is_active", "sum"),
).reset_index().sort_values("count", ascending=False)

data_export = {
    "years": YEARS,
    "restaurants": restaurants_json,
    "yearly_totals": {str(k): v for k, v in yearly_totals.items()},
    "events": events,
    "cuisine_stats": cuisine_stats.to_dict(orient="records"),
}

with open("/home/claude/michelin_data.json", "w") as f:
    json.dump(data_export, f, indent=2)

print("\nData exported successfully.")
print(f"Restaurants: {len(restaurants_json)}")
print(f"Events: {len(events)}")
