import pandas as pd

ori = pd.read_csv("data/raw/video_list.csv")

deleted = [
  "k7lZDu6_GnU",
  "FHfsqDhQBZQ",
  "2gIvxSs0HO0"
]

filtered = ori[~ori["video_id"].isin(deleted)]

filtered.to_csv(
    "data/raw/video_list_filtered.csv",
    index=False,
    encoding="utf-8-sig"
)

print(len(filtered))