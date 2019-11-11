
# coding: utf-8

# In[2]:



import os
import pandas as pd
import re 

import matplotlib.pyplot as plt

# Load data
usecols = ['publication', 'title', 'date', 'content']
articles1 = pd.read_csv('articles1.csv', usecols=usecols)
articles2 = pd.read_csv('articles2.csv', usecols=usecols)
articles3 = pd.read_csv('articles3.csv', usecols=usecols)
articles = pd.concat([articles1, articles2, articles3])

# Expand contractions
#   These are from:
#    http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
#    all credits go to alko and arturomp @ stack overflow.

contractions_dict = {"ain't": "is not", "aren't": "are not","can't": "cannot", 
        "can't've": "cannot have", "'cause": "because", "could've": "could have", 
        "couldn't": "could not", "couldn't've": "could not have","didn't": "did not", 
        "doesn't": "does not", "don't": "do not", "hadn't": "had not", 
        "hadn't've": "had not have", "hasn't": "has not", "haven't": "have not", 
        "he'd": "he would", "he'd've": "he would have", "he'll": "he will", 
        "he'll've": "he he will have", "he's": "he is", "how'd": "how did", 
        "how'd'y": "how do you", "how'll": "how will", "how's": "how is", 
        "I'd": "I would", "I'd've": "I would have", "I'll": "I will", 
        "I'll've": "I will have","I'm": "I am", "I've": "I have", 
        "i'd": "i would", "i'd've": "i would have", "i'll": "i will", 
        "i'll've": "i will have","i'm": "i am", "i've": "i have", 
        "isn't": "is not", "it'd": "it would", "it'd've": "it would have", 
        "it'll": "it will", "it'll've": "it will have","it's": "it is", 
        "let's": "let us", "ma'am": "madam", "mayn't": "may not", 
        "might've": "might have","mightn't": "might not","mightn't've": "might not have", 
        "must've": "must have", "mustn't": "must not", "mustn't've": "must not have", 
        "needn't": "need not", "needn't've": "need not have","o'clock": "of the clock", 
        "oughtn't": "ought not", "oughtn't've": "ought not have", "shan't": "shall not",
        "sha'n't": "shall not", "shan't've": "shall not have", "she'd": "she would", 
        "she'd've": "she would have", "she'll": "she will", "she'll've": "she will have", 
        "she's": "she is", "should've": "should have", "shouldn't": "should not", 
        "shouldn't've": "should not have", "so've": "so have","so's": "so as", 
        "this's": "this is",
        "that'd": "that would", "that'd've": "that would have","that's": "that is", 
        "there'd": "there would", "there'd've": "there would have","there's": "there is", 
        "they'd": "they would", "they'd've": "they would have", "they'll": "they will", 
        "they'll've": "they will have", "they're": "they are", "they've": "they have", 
        "to've": "to have", "wasn't": "was not", "we'd": "we would", 
        "we'd've": "we would have", "we'll": "we will", "we'll've": "we will have", 
        "we're": "we are", "we've": "we have", "weren't": "were not", 
        "what'll": "what will", "what'll've": "what will have", "what're": "what are", 
        "what's": "what is", "what've": "what have", "when's": "when is", 
        "when've": "when have", "where'd": "where did", "where's": "where is", 
        "where've": "where have", "who'll": "who will", "who'll've": "who will have", 
        "who's": "who is", "who've": "who have", "why's": "why is", 
        "why've": "why have", "will've": "will have", "won't": "will not", 
        "won't've": "will not have", "would've": "would have", "wouldn't": "would not", 
        "wouldn't've": "would not have", "y'all": "you all", "y'all'd": "you all would",
        "y'all'd've": "you all would have","y'all're": "you all are","y'all've": "you all have",
        "you'd": "you would", "you'd've": "you would have", "you'll": "you will", 
        "you'll've": "you will have", "you're": "you are", "you've": "you have" } 

contractions_re = re.compile('(%s)' % '|'.join(contractions_dict.keys()))
def expand_contractions(s, contractions_dict=contractions_dict):
    def replace(match):
        return contractions_dict[match.group(0)]
    return contractions_re.sub(replace, s)

articles['content'] = articles['content'].apply(expand_contractions)

# Remove uppercase substrings that reappear in the body text unnaturally 
# (often re-appearing sources and reporting cities which are included in every article etc.) 
# and also remove all quotation marks in text content to clear the text.
pat = r'(^[A-Z]+\s+([A-Z]+\s+)*\—|^[a-zA-Z]+\s+\([a-zA-Z]+\))|\"|\”|FLASHBACK:'
articles['content'] = articles['content'].str.replace(pat, '')

# Remove some odd characters and change some characters like apostrophes to use 
# the same char encoding
pat = '\[|\]|\\xa0|\\n'
articles['content'] = articles['content'].str.replace(pat, ' ')

pat = r"‘|’|´|’|\xe2"
articles['content'] = articles['content'].str.replace(pat, "'")

pat = r"\\|“"
articles['content'] = articles['content'].str.replace(pat, '')

# Lowercase articles and content
articles['content'] = articles['content'].str.lower()
articles['title'] = articles['title'].str.lower()


# Print some info and get a list of publishers
vCounts = articles['publication'].value_counts().sort_index()
listPublishers = vCounts.index.tolist()
y = vCounts.values.tolist()

N = len(y)
width = 1/1.5
plt.bar(listPublishers, y, width, color="green")
plt.xlabel('Publisher', fontsize=10)
plt.ylabel('Number of articles', fontsize=10)
plt.xticks(range(N), listPublishers, fontsize=8, rotation=90)
plt.title('Number of articles by publisher')
plt.show()


# In[4]:



from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

articles = articles.set_index('publication')

for pub in listPublishers:
    data = articles.loc[pub]
    stopwords = set(STOPWORDS)
    words = pub.split()
    for word in words:
        stopwords.add(word)
    wordcloud = WordCloud(
                            background_color='black',
                            stopwords=stopwords,
                            max_words=250,
                            max_font_size=40,
                            width=800,
                            height=400
                             ).generate(str(data['title']))
    
    wordcloud2 = WordCloud(
                            background_color='black',
                            stopwords=stopwords,
                            max_words=250,
                            max_font_size=40,
                            width=800,
                            height=400
                             ).generate(str(data['content']))

    fig = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud)
    plt.title(pub + ' article title word cloud')
    plt.axis('off')
    plt.show()
    fig.savefig("word"+pub+"1.png")
    

    fig = plt.figure(figsize=(20,10))
    plt.imshow(wordcloud2)
    plt.title(pub + ' article content word cloud')
    plt.axis('off')
    plt.show()
    fig.savefig("word"+pub+"2.png")

