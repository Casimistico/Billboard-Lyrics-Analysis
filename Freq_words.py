import pandas as pd
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize ,PunktSentenceTokenizer
from nltk.corpus import stopwords
import nltk
from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from nltk.stem import WordNetLemmatizer 
startTime = datetime.now()

df=pd.read_excel("billboard_lyrics_1964-2015.xlsx",header=0,  encoding='latin-1')

df["Decade"]=df["Year"]//10*10

## Exploration shows that some lyrics include \n character, as double spaces. This are replaces as simple space
df["Lyrics"]=df["Lyrics"].str.replace('\n'," ")
df["Lyrics"]=df["Lyrics"].str.replace('  '," ")


def count_words(Series):
    lemmatizer = WordNetLemmatizer()
    total_words=list()
    stop_words = set(stopwords.words('english'))
    for i in Series.index:
        try:
            song = word_tokenize(Series["Lyrics"][i])
            for word in song:
                if word not in stop_words:
                    total_words.append(word.lower())
        except:
            continue

    return " ".join([lemmatizer.lemmatize(w) for w in total_words])

df_freq=df[["Lyrics","Decade"]]


evaluate_freq=pd.DataFrame()
lemmatizer = WordNetLemmatizer()
for group,frame in df_freq.groupby("Decade"):
    
    words=count_words(frame)
    evaluate_freq.at[group,"Words"]=words
    evaluate_freq.at[group,"Total Words"]=len(words)

## Let´s see difference between top 50 common words in 1960 and 2015, which are lost since 1960 and which are appear in 2015
freq_1960=nltk.FreqDist(word_tokenize(evaluate_freq.loc[1960][0])).most_common(50)
freq_2015=nltk.FreqDist(word_tokenize(evaluate_freq.loc[2010][0])).most_common(50)
freq_1960=list(zip(*freq_1960))[0]
freq_2015=list(zip(*freq_2015))[0]

not_2015=list()
not_1965=list()

for i in freq_1960:
    if i not in freq_2015:
        not_2015.append(i)

for i in freq_2015:
    if i not in freq_1960:
        not_1965.append(i)

print("New since 1965", not_1965)
print("Lost in 2015", not_2015)

## This words are new in 2015 compared to 1960, so let´s see the evolution through time
words_eval=['money', 'fuck','night',  'bitch']




fig = plt.figure(figsize=(18, 16),facecolor='w', edgecolor='k')
fig.suptitle("Word evoulution through decades",fontsize=12)

for word in words_eval:
    ## This words appear are normalized, as is important to compare their intrincic evolution
    plt.plot(evaluate_freq["Words"].str.count(word)/evaluate_freq["Words"].str.count(word).sum(),label=word)
    plt.legend(loc='upper left')
    plt.xlabel("Years")
    plt.ylabel("Normalized freq")
plt.show()
             
fig = plt.figure(figsize=(18, 16),facecolor='w', edgecolor='k')
fig.suptitle("Word frequency in songs through decades",fontsize=12) 


x, y = np.ogrid[:300, :300]
mask = (x - 150) ** 2 + (y - 150) ** 2 > 130 ** 2
mask = 255 * mask.astype(int)

wordcloud = WordCloud(background_color="white", repeat=True, mask=mask)

for axis,num in zip(evaluate_freq.index,range(1,len(evaluate_freq.index)+1)):
    ax = fig.add_subplot(2,3,num)
    wordcloud.generate_from_frequencies(nltk.FreqDist(word_tokenize(evaluate_freq.loc[axis][0])))
    plt.axis("off")
    plt.imshow(wordcloud, interpolation="bilinear")
    ax.set_title("The '"+str(axis)[-2:],fontsize=10, loc='right',)



print("The script takes ", (datetime.now()- startTime).total_seconds()," sec" )    


plt.show()
