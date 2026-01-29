import sys, os
sys.path.insert(0, 'src')
os.makedirs('outputs', exist_ok=True)

from data_generator import generate_matches, generate_scorers, save_to_db, query

print("=" * 55)
print("  Manchester United Performance Analytics (2020-2024)")
print("=" * 55)

matches  = generate_matches()
scorers  = generate_scorers()
save_to_db(matches, scorers)

total = len(matches)
print(f"\n  Matches loaded : {total}")
print(f"  Seasons        : 4  (2020-21 → 2023-24)")
print(f"  Scorers loaded : {len(scorers)}")

# ── Season summary
print("\n--- Season-by-Season Record ---")
r = query("""
    SELECT season,
           SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) AS wins,
           SUM(CASE WHEN result='D' THEN 1 ELSE 0 END) AS draws,
           SUM(CASE WHEN result='L' THEN 1 ELSE 0 END) AS losses,
           SUM(goals_for)     AS goals_for,
           SUM(goals_against) AS goals_against,
           SUM(points)        AS points
    FROM matches
    GROUP BY season
    ORDER BY season
""")
print(r.to_string(index=False))

# ── Home vs Away
print("\n--- Home vs Away Performance ---")
r2 = query("""
    SELECT venue,
           COUNT(*) AS played,
           SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) AS wins,
           ROUND(AVG(goals_for), 2)     AS avg_goals_scored,
           ROUND(AVG(goals_against), 2) AS avg_goals_conceded,
           SUM(points) AS total_points
    FROM matches
    GROUP BY venue
""")
print(r2.to_string(index=False))

# ── Top 10 opponents by win rate (min 4 matches)
print("\n--- Win Rate by Opponent (top 10, min 4 matches) ---")
r3 = query("""
    SELECT opponent,
           COUNT(*) AS played,
           SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) AS wins,
           ROUND(100.0 * SUM(CASE WHEN result='W' THEN 1 ELSE 0 END) / COUNT(*), 1) AS win_pct
    FROM matches
    GROUP BY opponent
    HAVING played >= 4
    ORDER BY win_pct DESC
    LIMIT 10
""")
print(r3.to_string(index=False))

# ── Top scorers overall
print("\n--- Top Scorers Across All Seasons ---")
r4 = query("""
    SELECT player,
           SUM(goals)   AS total_goals,
           SUM(assists) AS total_assists,
           SUM(apps)    AS apps
    FROM scorers
    GROUP BY player
    ORDER BY total_goals DESC
""")
print(r4.to_string(index=False))

# ── Goals scored vs conceded by season
print("\n--- Goals For vs Against by Season ---")
r5 = query("""
    SELECT season,
           SUM(goals_for)                         AS gf,
           SUM(goals_against)                     AS ga,
           SUM(goals_for) - SUM(goals_against)    AS goal_diff
    FROM matches
    GROUP BY season
    ORDER BY season
""")
print(r5.to_string(index=False))

print("\n✓  Analysis complete. Database saved to outputs/data.db")
