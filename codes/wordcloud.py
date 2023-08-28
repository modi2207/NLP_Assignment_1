from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_csv(r"preprocessed_comments.csv")

comment_words = ''
stopwords = set(STOPWORDS)


for row in df.iterrows():

    comment = row[1].values
    # print(comment)

    val = str(comment)


    tokens = val.split()


    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()

    comment_words += " ".join(tokens) + " "

wordcloud = WordCloud(width=1200, height=1300,
                      min_word_length=3,
                      background_color='white',
                      stopwords=stopwords,
                      min_font_size=10).generate(comment_words)


plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

plt.show()