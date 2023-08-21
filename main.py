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
        #self.post_sorting=self.configurationData["post_sorting"]

    def generate(self):

            subreddit = self.reddit.subreddit(self.subreddit)
            top_posts = subreddit.top(limit=self.total_post, time_filter='all')
            output_directory = 'comment_csv_files'


        # Iterate through the top posts and create CSV files for comments
            count=1
        # try:
            for post in top_posts:
                post_title = post.title
                df=[]
                # Get comments from the post
                #post.comments.replace_more(limit=None)  # Load all comments
                submission=self.reddit.submission(post.id)
                #comments = post.comments.list()
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    #if hasattr(comment,'body'):
                    df.append([post.title,comment.body,comment.author,len(comment.replies.list()),comment.score])
                df=pd.DataFrame(df, columns=['title','comment','author','total_replies','upvotes'])
                # Create a CSV file for the post's comments
                csv_filename = f"post_{count}.csv"
                csv_path = os.path.join(output_directory, csv_filename)
                f = open(csv_path, "w")
                df.to_csv(csv_path, index=True)
                f.close()
                count+=1
                print(f"CSV file created for post '{post_title}'")
        # except:
        #     print("exception occurred")

redit_instance=ReditScrape()
redit_instance.initialize()
redit_instance.generate()





