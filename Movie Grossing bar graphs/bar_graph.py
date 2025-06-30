import matplotlib.pyplot as plt
import pandas as pd
import pymysql

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    db='highestgrossingmovies',
    port=3306
)

query = """
WITH RankedMovies AS (
    SELECT 
        RANK() OVER (ORDER BY Grossing DESC) AS MovieRank,
        Movie,
        Year,
        Grossing
    FROM 
        Movies
)
SELECT 
    MovieRank AS `Rank`,
    Movie,
    Year,
    Grossing
FROM 
    RankedMovies
WHERE 
    Year = 2025;
"""

df = pd.read_sql(query, conn)
conn.close()

# Sort by grossing ascending for left-to-right smallest to largest
df = df.sort_values(by='Grossing').reset_index(drop=True)

# Set x positions
x = list(range(len(df)))

# Plot setup
plt.figure(figsize=(max(14, len(df) * 1.5), 6))
  # auto scale for # of movies
bars = plt.bar(x, df['Grossing'], color='steelblue')

# Add dollar-formatted labels above bars
for i, bar in enumerate(bars):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"${df['Grossing'][i]:,.0f}",
        ha='center',
        va='bottom',
        fontsize=9,
        rotation=45
    )

# Set x-ticks to movie titles aligned perfectly
plt.xticks(ticks=x, labels=df['Movie'], rotation=45, ha='right')

# Styling
plt.ylabel('Grossing ($)')
plt.title('Top Grossing Movies of 2025')
plt.tight_layout(pad=2)
plt.show()
