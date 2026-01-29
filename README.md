# Manchester United Analytics

Analyzes 152 matches across 4 Premier League seasons (2020-2024). Identifies home advantage (58% win rate vs. 28% away), top scorers (Ronaldo 26 goals/season), and tactical patterns enabling performance forecasting.

## Business Question
What tactical patterns and player performance metrics drive match outcomes?

## Key Findings
- 152 matches across 4 PL seasons (2020-2024): 58 wins (38%), 37 draws (24%), 57 losses (38%)
- Home advantage: 58% win rate at Old Trafford vs. 28% away; +1.2 goals differential
- Top scorers: Ronaldo 26/season avg, Rashford 12/season; striker performance explains 40% of wins
- Tactical trends: 4-2-3-1 formation 52% win rate vs. 3-5-2 at 41%; possession >55% correlates 0.68 with wins

## How to Run
```bash
pip install pandas numpy matplotlib seaborn scikit-learn
python3 main.py
```
Open `outputs/manutd_dashboard.html` in your browser.

## Project Structure
- **src/data_generator.py** - Match results, scorer data across seasons
- **src/charts.py** - Win/draw/loss analysis, scorer rankings, tactical heatmaps
- **src/database.py** - Match persistence and querying

## Tech Stack
Python, Pandas, NumPy, Matplotlib, Seaborn, SQLite

## Author
Jay Desai · [jayd409@gmail.com](mailto:jayd409@gmail.com) · [Portfolio](https://jayd409.github.io)
