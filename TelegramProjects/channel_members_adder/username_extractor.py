import json
import pandas as pd

df1 = pd.read_excel("res/SolCharactersAirdrop.xlsx")
# df2 = pd.read_excel("res/bnfts_distribution.xlsx")
df1 = df1[df1["User Name"] != ""]

users = df1["User Name"].str[1:].dropna().drop_duplicates()

with open("res/SolCharactersAirdropUsers.json", "w") as fh:
	json.dump(users.tolist(), fh)