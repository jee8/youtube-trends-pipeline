import pandas as pd
import os
import yaml
from sqlalchemy import create_engine

# Load config
config_path = os.path.join(os.path.dirname(__file__), "../../pipeline_config.yaml")
with open(config_path, "r") as file:
    config = yaml.safe_load(file)

DATABASE_URL = config["database_url"]

# Load cleaned data
df = pd.read_csv("data/processed/cleaned_trending.csv")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Load data into DB
df.to_sql("trending_videos", engine, if_exists="replace", index=False)

print("✅ Data loaded into database table: trending_videos")
