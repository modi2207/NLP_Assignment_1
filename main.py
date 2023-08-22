import json
import praw
import os
import csv
import pandas as pd
class ReditScrape:

    def __init__(self):
        file=open('client_secrets.json')
        self.configurationData=json.load(file)
        file.close()

    def initialize(self):
        self.reddit = praw.Reddit(
            client_id=self.configurationData["client_id"],
            client_secret=self.configurationData["client_secret"],
            #password=self.configurationData["password"],
            user_agent=self.configurationData["user_agent"],
            #username=self.configurationData["username"]
        )
        self.subreddit=self.configurationData["subreddit"]
        self.total_post=self.configurationData["total_post"]

    def create_dir(self,path):
        if not os.path.exists(path):
            os.makedirs(path)

    def generate(self):

            subreddit = self.reddit.subreddit(self.subreddit)
            top_posts = subreddit.top(limit=self.total_post, time_filter='all')
            comments_path = os.path.join(os.getcwd(),'Submission\\comments')

            self.create_dir(comments_path)

            post_df=[]
            for post in top_posts:
                post_title = post.title
                comment_df=[]
                submission=self.reddit.submission(post.id)
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    comment_df.append([comment.id,comment.body,comment.score,comment.depth,comment.created_utc,len(comment.replies.list()),comment.author])
                comment_df=pd.DataFrame(comment_df, columns=['ID','Text','Upvotes','Depth','Created Timestamp','Replies','Author'])
                csv_filename = f"{post.id}.csv"
                csv_path = os.path.join(comments_path, csv_filename)
                f = open(csv_path, "w")
                comment_df.to_csv(csv_path, index=True)
                f.close()
                post_df.append([post.title,post.id,post.url,post.score,post.num_comments,post.created_utc,post.subreddit.display_name,post.author,post.selftext])
                print(f"CSV file created for post '{post.id}'")
            post_df=pd.DataFrame(post_df,columns=['Title','ID','URL','Upvotes','Comments','Created Timestamp','Subreddit Name','Author','Text'])
            csv_filename = f"posts.csv"
            csv_path = os.path.join(os.path.join(os.getcwd(),'Submission'), csv_filename)
            f = open(csv_path, "w")
            post_df.to_csv(csv_path, index=True)
            f.close()
redit_instance=ReditScrape()
redit_instance.initialize()
redit_instance.generate()





