import pandas as pd
import json

class FewShots:
    def __init__(self,file_path="data/processed.json"):
        self.df=None
        self.unique_tags=None
        self.load_post(file_path)

    def load_post(self,file_path):
        with open(file_path,encoding="utf-8") as f:
            posts = json.load(f)
            df=pd.json_normalize(posts)
            df["length"] = df["line_count"].apply(self.category_length)
            all_tags=df["tags"].apply(lambda x:x).sum()
            self.unique_tags=set(list(all_tags))
            self.df=df
    def category_length(self,line_count):
        if line_count<10:
            return "Short"
        elif 10<=line_count<=30:
            return "Medium"
        else:
            return "Long"
    def get_tags(self):
        return self.unique_tags
    def get_filtered_posts(self,length,language,tag):
        df_filtered = self.df[
            (self.df['length']==length) &
            (self.df['language']==language)&
            (self.df['tags'].apply(lambda tags:tag in tags))
        ]


        return  df_filtered.to_dict(orient="records")

if __name__=="__main__":
    fs=FewShots()
    posts=fs.get_filtered_posts("Long","English","Motivation")
    for post in posts:
        post_text=post["text"]
        print(post_text)
    pass