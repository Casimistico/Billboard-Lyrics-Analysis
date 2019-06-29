"""This module purpose is to extract relevant information about the richness of
lyrics in the billboard ranking through different years"""

from datetime import datetime
from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from explore_dataframe import explorar_dataframe

START_TIME = datetime.now()

DF = pd.read_excel("billboard_lyrics_1964-2015.xlsx", header=0, encoding='latin-1')






def dataframe_cleaning(dataframe, column):
    """Funtion for cleaning dataframe"""
    mis_lic = dataframe[dataframe[column].isnull()]
## More exploration shows that some lyrics include \n character, as double spaces.
## This are replaces as simple space
    dataframe[column] = dataframe[column].str.replace('\n', " ")
    dataframe[column] = dataframe[column].str.replace('  ', " ")
    axis_drop = mis_lic.index
    dataframe = dataframe.drop(axis_drop, axis=0)
    return dataframe

DF = dataframe_cleaning(DF, "Lyrics")

##-------------

def top_10_analysis(dataframe):
    """Let´s start working with top 10 ranked songs for each year"""
    top_10 = dataframe[dataframe["Rank"] <= 10]

## Let´s defined some parameters to analyze the richness lyricis
## such as number of words and number of unique words

    top_10["Words"] = top_10["Lyrics"].apply(lambda x:
                                             len(word_tokenize(x)))
    top_10["Unique Words"] = dataframe["Lyrics"].apply(lambda x: len(FreqDist(word_tokenize(x))))

##  Richness is defined as % of unique words in a song lyric.
##  Ej: if a all words in a lyric are different: Richness= 100%
    top_10["Richness"] = (round(top_10["Unique Words"]/top_10["Words"]*100
                                , 2))

## It is interesting to find how many repetitions has the most common word of the lyric
    top_10["Word Repetition"] = (top_10["Lyrics"].apply(lambda x:
                                                        FreqDist(word_tokenize(x))
                                                        .most_common(1)[0][1]))
    top_10["%Rep"] = top_10["Word Repetition"]/top_10["Words"]*100

## Also is interesting to determine mean word lenght for each song
    top_10["Word Length"] = dataframe["Lyrics"].apply(lambda x:
                                                      len(x)/len(x.split(" ")))
    top_10["Longest word"] = dataframe["Lyrics"].apply(lambda x:
                                                       len(max(x.split(" "),
                                                               key=len)))

##  Is interesting to determine how many meanfulness words ("stop words") are in each lyric.
##  Nltk includes a set of stop words
    stop_words = set(stopwords.words('english'))
    top_10["Stop Words"] = dataframe["Lyrics"].apply(lambda x:
                                                     len([w for w in word_tokenize(x)
                                                          if not w in stop_words]))
    top_10["%Stop Words"] = top_10["Stop Words"]/top_10["Words"]*100
    return top_10

## ----- Graph of features-------
def graphic_results(top_10):
    """This function graphs the dataframe that was analysed by top_10_analysis"""
    evaluate_columns = ["Words", "Unique Words", "Richness",
                        "Word Length", "Word Repetition", "%Rep"]
## Lets see the evolution of each parameter through time.
## First let´s create a dataframe with the mean value for each year.
    evol_anual = pd.DataFrame()
    for group, frame in top_10.groupby("Year"):
        for column in evaluate_columns:
            evol_anual.at[group, "Mean"+str(column)] = frame[column].mean()
## And then let´s plot
    fig = plt.figure(figsize=(18, 16), facecolor='w', edgecolor='k')
    for column, num in zip(evol_anual.columns, range(1, len(evol_anual.columns)+1)):
        axis = fig.add_subplot(2, len(evol_anual.columns)/2, num)
##  Linear regression
        slope, intercept, r_val, p_val, std = stats.linregress(evol_anual.index, evol_anual[column])
        line = slope*evol_anual.index + intercept
        plt.plot(evol_anual.index, evol_anual[column], 'o', evol_anual.index, line)
        axis.set_title(column, fontsize=12)
    plt.xlabel("Years")
    plt.show()

## ----- Let´s graph the results-------
if __name__ == "__main__":
    ##  First let´s explore the Dataset
    explorar_dataframe(DF)
    graphic_results(top_10_analysis(DF))
    print("The script takes ", (datetime.now()- START_TIME).total_seconds(), " sec")
