""" This module evaluates word frequencies in differents years
and plots them in differents styles"""
from datetime import datetime
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
from nltk.stem import WordNetLemmatizer
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
from song_analysis import dataframe_cleaning

START_TIME = datetime.now()

DF = pd.read_excel("billboard_lyrics_1964-2015.xlsx", header=0, encoding='latin-1')
## Let´s work with decades instead of years:
DF["Decade"] = DF["Year"]//10*10

DF = dataframe_cleaning(DF, "Lyrics")

def count_words(series):
    """This function counts the total o words in each lyric"""
    lemmatizer = WordNetLemmatizer()
    total_words = list()
    stop_words = set(stopwords.words('english'))
    for i in series.index:
        song = word_tokenize(series["Lyrics"][i])
        for word in song:
            if word not in stop_words:
                total_words.append(word.lower())


    return " ".join([lemmatizer.lemmatize(w) for w in total_words])



def freq_distrib_decade(dataframe):
    """This function finds the word frequency in each decade"""
    df_freq = dataframe[["Lyrics", "Decade"]]
    evaluate_freq = pd.DataFrame()
    for group, frame in df_freq.groupby("Decade"):
        words = count_words(frame)
        evaluate_freq.at[group, "Words"] = words
        evaluate_freq.at[group, "Total Words"] = len(words)
    return evaluate_freq

def missing_words_decade(dataframe, start_decade, end_decade):
    """This function finds which words disappear between to decades using evaluate_freq"""
    freq_start = FreqDist(word_tokenize(dataframe.loc[start_decade][0])).most_common(50)
    freq_start = list(zip(*freq_start))[0]
    freq_end = FreqDist(word_tokenize(dataframe.loc[end_decade][0])).most_common(50)
    freq_end = list(zip(*freq_end))[0]
    not_start = [w for w in freq_start if w not in freq_end]
    not_end = [w for w in freq_end if w not in freq_start]


    print("New since ", start_decade, not_start)
    print("Lost in ", end_decade, not_end)


## This words are new in 2015 compared to 1960, so let´s see the evolution through time

def word_evolution(dataframe, word_list):
    """Plots word evoulution through decades"""
    fig = plt.figure(figsize=(18, 16), facecolor='w', edgecolor='k')
    fig.suptitle("Word evoulution through decades", fontsize=12)

    for word in word_list:
## This words appear are normalized, as is important to compare their intrincic evolution
        plt.plot(dataframe["Words"].str.count(word)/dataframe["Words"]
                 .str.count(word).sum(), label=word)
        plt.legend(loc='upper left')
        plt.xlabel("Years")
        plt.ylabel("Normalized freq")
        plt.show()

def wordcloud_plot(dataframe):
    """This function plots the words distribution using wordcloud package"""
    fig = plt.figure(figsize=(18, 16), facecolor='w', edgecolor='k')
    fig.suptitle("Word frequency in songs through decades", fontsize=12)
    x_axis, y_axis = np.ogrid[:300, :300]
    mask = (x_axis - 150) ** 2 + (y_axis - 150) ** 2 > 130 ** 2
    mask = 255 * mask.astype(int)
    wordcloud = WordCloud(background_color="white", repeat=True, mask=mask)
    for axis, num in zip(dataframe.index, range(1, len(dataframe.index)+1)):
        plot = fig.add_subplot(2, 3, num)
        wordcloud.generate_from_frequencies(FreqDist(word_tokenize(dataframe.loc[axis][0])))
        plt.axis("off")
        plt.imshow(wordcloud, interpolation="bilinear")
        plot.set_title("The "+str(axis)[-2:]+ "'s", fontsize=10, loc='right',)
    plt.show()
##
if __name__ == "__main__":
## Let´s search, for example, missing/new words between 1960-200
    missing_words_decade(freq_distrib_decade(DF), 1960, 2000)
## Let´s plot the wordfrequency
    wordcloud_plot(freq_distrib_decade(DF))
    print("The script takes ", (datetime.now()- START_TIME).total_seconds(), " sec")
