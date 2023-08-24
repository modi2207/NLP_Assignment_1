import json
import numpy as np
import os
import pandas as pd
import requests
class LabelComments:

    def __init__(self):
        file=open('client_secrets.json')
        self.configurationData=json.load(file)
        file.close()


    def getlabel(self, comment: object, type: object) -> object:
        payload={"inputs": comment}
        if type=="seethal":
            response = requests.post(self.configurationData["seethal_url"], headers={"Authorization":self.configurationData["hugging_face_token"]}, json=payload)
            return response.json()
        if type=="twitter":
            response = requests.post(self.configurationData["tweeter_roberta_url"], headers={"Authorization":self.configurationData["hugging_face_token"]}, json=payload)
            return response.json()
        if type=="finiteautomata":
            response = requests.post(self.configurationData["finiteautomata_url"], headers={"Authorization":self.configurationData["hugging_face_token"]}, json=payload)
            return response.json()
    def generateLabel(self):
        self.processedComments=pd.read_csv(os.path.join(os.getcwd(),"Submission\\preprocessed_comments.csv"))
        self.mergedComments=pd.read_csv(os.path.join(os.getcwd(),"Submission\\merged_comments.csv"))

        self.mergedComments["seethal positive"]=np.NAN
        self.mergedComments["seethal nagative"]=np.NAN
        self.mergedComments["seethal neutral"] = np.NAN
        self.mergedComments["twitter positive"] = np.NAN
        self.mergedComments["twitter nagative"] = np.NAN
        self.mergedComments["twitter neutral"] = np.NAN
        self.mergedComments["finiteautomata positive"] = np.NAN
        self.mergedComments["finiteautomata nagative"] = np.NAN
        self.mergedComments["finiteautomata neutral"] = np.NAN
        self.mergedComments["seethal label"] = np.NAN
        self.mergedComments["twitter label"] = np.NAN
        self.mergedComments["finiteautomata label"] = np.NAN
        self.mergedComments["final label"] = np.NAN

        for i in range(0,len(self.processedComments)):
            try:
                comment=str(self.processedComments.iloc[i,0])
                if len(comment)==0:
                    continue
                res=self.getlabel(comment,"twitter")
                if not isinstance(res,list):
                    if str(res['error']).startswith("Rate limit reached"):
                        break
                print("response from twitter: ",res)
                if res:
                    try:
                        for j in range(0,len(res[0])):
                                if j==0:
                                    self.mergedComments.iloc[i,24]=res[0][j]['label']
                                if res[0][j]['label']=='positive':
                                    self.mergedComments.iloc[i,17] = res[0][j]['score']
                                elif res[0][j]['label']=='negative':
                                    self.mergedComments.iloc[i,18] = res[0][j]['score']
                                else:
                                    self.mergedComments.iloc[i,19] = res[0][j]['score']
                    except Exception as err:
                        print("exception occurred: ",err)

                res = self.getlabel(comment, "seethal")
                if not isinstance(res, list):
                    if str(res['error']).startswith("Rate limit reached"):
                        break
                print("response from seethal: ",res)
                if res:
                    try:
                        for j in range(0,len(res[0])):
                            if j==0:
                                self.mergedComments.iloc[i,23]='positive' if res[0][j]['label']=='LABEL_2' else 'nagative' if res[0][j]['label']=='LABEL_0' else 'neutral'
                            if res[0][j]['label']=='LABEL_2':
                                self.mergedComments.iloc[i,14] = res[0][j]['score']
                            elif res[0][j]['label']=='LABEL_0':
                                self.mergedComments.iloc[i,15] = res[0][j]['score']
                            else:
                                self.mergedComments.iloc[i,16] = res[0][j]['score']
                    except Exception as err:
                        print("exception occurred: ",err)

                res = self.getlabel(comment, "finiteautomata")
                if not isinstance(res, list):
                    if str(res['error']).startswith("Rate limit reached"):
                        break
                print("response from finiteautomata: ", res)
                if res:
                    try:
                        for j in range(0,len(res[0])):
                            if j==0:
                                self.mergedComments.iloc[i,25]='positive' if res[0][j]['label']=='POS' else 'nagative' if res[0][j]['label']=='NAG' else 'neutral'
                            if res[0][j]['label']=='POS':
                                self.mergedComments.iloc[i,20] = res[0][j]['score']
                            elif res[0][j]['label']=='NEG':
                                self.mergedComments.iloc[i,21] = res[0][j]['score']
                            else:
                                self.mergedComments.iloc[i,22] = res[0][j]['score']
                    except Exception as err:
                        print("exception occurred: ",err)
                li=[self.mergedComments.iloc[i,23], self.mergedComments.iloc[i,24],self.mergedComments.iloc[i,25]]
                print(li)
                self.mergedComments.iloc[i,26]=max(li,key=li.count)
            except Exception as error:
                print("exception occurred ",error)

        self.mergedComments.to_csv(os.path.join(os.getcwd(), f'Submission\\merged_comments.csv'), index=False)
    def extractComments(self):
        self.mergedComments=pd.read_csv(os.path.join(os.getcwd(),"Submission\\merged_comments.csv"))
        for i in range(0,len(self.mergedComments)):
            if len(str(self.mergedComments.iloc[i,25]))==0:
                self.mergedComments.drop(i,axis=0,inplace=True)

        self.positiveComments=self.mergedComments.loc[self.mergedComments['final label']=='positive']
        self.nagativeComments=self.mergedComments.loc[self.mergedComments['final label']=='nagative']
        self.neutralComments=self.mergedComments.loc[self.mergedComments['final label']=='neutral']
        self.mergedComments.to_csv(os.path.join(os.getcwd(), f'Submission\\merged_comments.csv'), index=False)
        self.positiveComments.to_csv(os.path.join(os.getcwd(), f'Submission\\postive_comments.csv'), index=False)
        self.neutralComments.to_csv(os.path.join(os.getcwd(), f'Submission\\neutral_comments.csv'), index=False)
        self.nagativeComments.to_csv(os.path.join(os.getcwd(), f'Submission\\nagative_comments.csv'), index=False)
        count=0
        j=0
        i=0
        df=[]
        for index,row in self.positiveComments.iterrows():
            if j==i:
                if row["Text Length"]>100:
                    continue
                i += 5
                count += 1
                df.append([row.ID,row.Text,row.Upvotes,row.Depth,row["Created Timestamp(UTC)"],row.Replies,row.Author,row["Post ID"],row["Parrant Comment ID"],row["Text Length"],row["Edited"],row["Is Submitter"],row["Subreddit Name"],row["seethal positive"],row["seethal nagative"],row["seethal neutral"],row["twitter positive"],row["twitter nagative"],row["twitter neutral"],row["finiteautomata positive"],row["finiteautomata nagative"],row["finiteautomata neutral"],row["seethal label"],row["twitter label"],row["finiteautomata label"],row["final label"]])
            j+=1
            if count==33:
                break
        i=0
        j=0
        for index,row in self.nagativeComments.iterrows():
            if j == i:
                if row["Text Length"]>200:
                    continue
                i += 5
                df.append(
                    [row.ID, row.Text, row.Upvotes, row.Depth, row["Created Timestamp(UTC)"], row.Replies, row.Author,
                     row["Post ID"], row["Parrant Comment ID"], row["Text Length"],row["Edited"], row["Is Submitter"],
                     row["Subreddit Name"], row["seethal positive"], row["seethal nagative"], row["seethal neutral"],
                     row["twitter positive"], row["twitter nagative"], row["twitter neutral"],
                     row["finiteautomata positive"], row["finiteautomata nagative"], row["finiteautomata neutral"],
                     row["seethal label"], row["twitter label"], row["finiteautomata label"], row["final label"]])
                count += 1

            j += 1
            if count == 66:
                break
        j=0
        i=0
        for index,row in self.neutralComments.iterrows():
            if j == i:
                if row["Text Length"]>100:
                    continue
                i += 5
                df.append(
                    [row.ID, row.Text, row.Upvotes, row.Depth, row["Created Timestamp(UTC)"], row.Replies, row.Author,
                     row["Post ID"], row["Parrant Comment ID"], row["Text Length"], row["Edited"], row["Is Submitter"],
                     row["Subreddit Name"], row["seethal positive"], row["seethal nagative"], row["seethal neutral"],
                     row["twitter positive"], row["twitter nagative"], row["twitter neutral"],
                     row["finiteautomata positive"], row["finiteautomata nagative"], row["finiteautomata neutral"],
                     row["seethal label"], row["twitter label"], row["finiteautomata label"], row["final label"]])
                count += 1
            j += 1

            if count == 100:
                break

        df = pd.DataFrame(df,columns=['ID', 'Text', 'Upvotes', 'Depth', 'Created Timestamp(UTC)', 'Replies',
                                           'Author', 'Post ID', 'Parrant Comment ID', 'Text Length', 'Edited',
                                           'Is Submitter', 'Subreddit Name','seethal positive','seethal nagative','seethal neutral','twitter positive','twitter nagative','twitter neutral','finiteautomata positive','finiteautomata nagative','finiteautomata neutral','seethal label','twitter label','finiteautomata label','final label'])
        df.to_csv(os.path.join(os.getcwd(), f'Submission\\hundred_comments_with_ans.csv'),index=False)
        df.drop("seethal positive",axis=1,inplace=True)
        df.drop("seethal nagative",axis=1,inplace=True)
        df.drop("seethal neutral",axis=1,inplace=True)
        df.drop("twitter positive",axis=1,inplace=True)
        df.drop("twitter nagative",axis=1,inplace=True)
        df.drop("twitter neutral",axis=1,inplace=True)
        df.drop("finiteautomata positive",axis=1,inplace=True)
        df.drop("finiteautomata nagative", axis=1, inplace=True)
        df.drop("finiteautomata neutral", axis=1, inplace=True)
        df.drop("seethal label", axis=1, inplace=True)
        df.drop("twitter label", axis=1, inplace=True)

        df.drop("finiteautomata label", axis=1, inplace=True)
        df.drop("final label", axis=1, inplace=True)


        df["Student_1"]=np.NAN
        df["Student_2"]=np.NAN
        df["Student_3"]=np.NAN

        df.to_csv(os.path.join(os.getcwd(), f'Submission\\hundred_comments.csv'),index=False)

labelComments=LabelComments()
labelComments.generateLabel()
labelComments.extractComments()







