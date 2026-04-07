"""
Realistic Manchester United Premier League match data generator (2020–2024).
Uses real-world season context and opponent strength tiers.
"""
import random
import sqlite3
import pandas as pd
from datetime import date, timedelta

random.seed(42)

SEASONS = {
    "2020-21": {"start": date(2020, 9, 12), "finish_pos": 2,  "quality": "good"},
    "2021-22": {"start": date(2021, 8, 14), "finish_pos": 6,  "quality": "poor"},
    "2022-23": {"start": date(2022, 8,  7), "finish_pos": 3,  "quality": "average"},
    "2023-24": {"start": date(2023, 8, 14), "finish_pos": 8,  "quality": "poor"},
}

# Premier League opponents with strength tier
OPPONENTS = {
    "Manchester City":     "top6",
    "Liverpool":           "top6",
    "Chelsea":             "top6",
    "Arsenal":             "top6",
    "Tottenham Hotspur":   "top6",
    "Leicester City":      "mid",
    "West Ham United":     "mid",
    "Everton":             "mid",
    "Aston Villa":         "mid",
    "Leeds United":        "mid",
    "Wolverhampton":       "mid",
    "Crystal Palace":      "mid",
    "Brighton":            "mid",
    "Brentford":           "mid",
    "Newcastle United":    "mid",
    "Nottingham Forest":   "lower",
    "Burnley":             "lower",
    "Sheffield United":    "lower",
    "Luton Town":          "lower",
    "Bournemouth":         "lower",
}

# Win probability by quality vs opponent tier
WIN_PROB = {
    ("good",    "top6"):  0.38,
    ("good",    "mid"):   0.57,
    ("good",    "lower"): 0.72,
    ("average", "top6"):  0.22,
    ("average", "mid"):   0.45,
    ("average", "lower"): 0.60,
    ("poor",    "top6"):  0.15,
    ("poor",    "mid"):   0.36,
    ("poor",    "lower"): 0.52,
}

# Top scorers (realistic names & goal shares by season)
SCORERS_BY_SEASON = {
    "2020-21": [("Edinson Cavani", 17), ("Marcus Rashford", 21), ("Bruno Fernandes", 28),
                ("Mason Greenwood", 12), ("Anthony Martial", 10)],
    "2021-22": [("Cristiano Ronaldo", 24), ("Bruno Fernandes", 14), ("Marcus Rashford", 8),
                ("Jadon Sancho", 6),       ("Anthony Martial", 3)],
    "2022-23": [("Marcus Rashford", 30), ("Bruno Fernandes", 14), ("Antony", 8),
                ("Wout Weghorst", 2),     ("Anthony Martial", 3)],
    "2023-24": [("Rasmus Hojlund", 16), ("Bruno Fernandes", 10), ("Marcus Rashford", 7),
                ("Antony", 3),           ("Scott McTominay", 7)],
}


def _result(quality, opp_tier, home):
    wp = WIN_PROB[(quality, opp_tier)]
    if home:
        wp = min(wp + 0.07, 0.90)
    else:
        wp = max(wp - 0.07, 0.05)
    r = random.random()
    if r < wp:
        return "W"
    elif r < wp + 0.22:
        return "D"
    else:
        return "L"


def _score(result, home):
    if result == "W":
        gf = random.choice([1,1,2,2,2,3,3,4])
        ga = random.choice([0,0,0,1,1,2])
    elif result == "D":
        g = random.choice([0,1,1,1,2,2])
        gf, ga = g, g
    else:
        gf = random.choice([0,0,0,1,1,2])
        ga = random.choice([1,1,2,2,3])
    return gf, ga


def generate_matches():
    rows = []
    match_id = 1
    for season, meta in SEASONS.items():
        opp_list = list(OPPONENTS.keys())[:19]  # 19 unique opponents
        random.shuffle(opp_list)
        d = meta["start"]
        for opp in opp_list:
            tier = OPPONENTS[opp]
            quality = meta["quality"]
            for venue in ["Home", "Away"]:
                home = venue == "Home"
                res = _result(quality, tier, home)
                gf, ga = _score(res, home)
                rows.append({
                    "match_id":    match_id,
                    "season":      season,
                    "match_date":  d.isoformat(),
                    "opponent":    opp,
                    "venue":       venue,
                    "goals_for":   gf,
                    "goals_against": ga,
                    "result":      res,
                    "points":      3 if res=="W" else 1 if res=="D" else 0,
                })
                d += timedelta(days=random.randint(5, 18))
                match_id += 1
    return pd.DataFrame(rows)


def generate_scorers():
    rows = []
    scorer_id = 1
    for season, players in SCORERS_BY_SEASON.items():
        for name, goals in players:
            assists = max(0, goals // 2 + random.randint(-2, 3))
            rows.append({
                "scorer_id": scorer_id,
                "season":    season,
                "player":    name,
                "goals":     goals,
                "assists":   assists,
                "apps":      random.randint(max(goals, 20), 38),
            })
            scorer_id += 1
    return pd.DataFrame(rows)


def save_to_db(matches_df, scorers_df, db_path="outputs/data.db"):
    conn = sqlite3.connect(db_path)
    matches_df.to_sql("matches", conn, if_exists="replace", index=False)
    scorers_df.to_sql("scorers", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()


def query(sql, db_path="outputs/data.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df
