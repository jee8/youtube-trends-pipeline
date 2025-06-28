import pandas as pd
import os

# Load raw CSV
raw_path = os.path.join("data", "raw", "trending.csv")
df = pd.read_csv(raw_path)

# Convert datetime column
df["published_at"] = pd.to_datetime(df["published_at"])

# Convert numeric columns
numeric_cols = ["view_count", "like_count", "comment_count"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

# Sort by view count
df = df.sort_values(by="view_count", ascending=False)

# Save cleaned data
processed_path = os.path.join("data", "processed", "cleaned_trending.csv")
df.to_csv(processed_path, index=False)

print("✅ Cleaned data saved to data/processed/cleaned_trending.csv")
