import pandas as pd
import yaml

df = pd.read_csv("Network_Data/phisingData.csv")

schema = {
    "columns": list(df.columns)
}

with open("data_schema/schema.yaml", "w") as f:
    yaml.dump(schema, f)

print("✅ schema.yaml created automatically")