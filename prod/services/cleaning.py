import pandas as pd
import numpy as np
df = pd.read_excel(r"/Users/youssefabdelhamid/Desktop/data cleaning/CustomerCallList.xlsx")
print(df)



df = pd.read_csv("./BL-Flickr-Images-Book.csv")
print(df.head())

to_drop = [
    "Edition Statement",
    "Corporate Author",
    "Corporate Contributors",
    "Former owner",
    "Engraver",
    "Contributors",
    "Issuance type",
    "Shelfmarks",
]
#df.drop(to_drop, inplace=True, axis=1)
df.drop(columns=to_drop, inplace=True)
print(df.head())

