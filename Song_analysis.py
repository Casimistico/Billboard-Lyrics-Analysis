from nltk.tokenize import  word_tokenize
from nltk.corpus import stopwords
from nltk import FreqDist
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from Explore_dataframe import explorar_dataframe
from datetime import datetime
import matplotlib.pyplot as plt


startTime = datetime.now()

df=pd.read_excel("billboard_lyrics_1964-2015.xlsx",header=0,  encoding='latin-1')

##  First let´s explore the Dataset. First exploration shows  187 rows with nan values, both in "Lyrics" as in "Sources"

#explorar_dataframe(df)

mis_lic=df[df["Lyrics"].isnull()]
mis_source=df[df["Lyrics"].isnull()]

#print(mis_lic[mis_lic["Rank"]<=10]["Song"])

## For this proyect purposes,  top 10 ranked lyrics are complete for each year

## More exploration shows that some lyrics include \n character, as double spaces. This are replaces as simple space
df["Lyrics"]=df["Lyrics"].str.replace('\n'," ")
df["Lyrics"]=df["Lyrics"].str.replace('  '," ")

axis_drop=mis_lic.index
df=df.drop(axis_drop,axis=0)

##-------------
## Let´s start working with top 10 ranked songs for each year, this dataset has 510 entries. 

top_10=df[df["Rank"]<=10]

## Let´s defined some parameters to analyze the richness of the lyricis, such as number of words and number of unique words

top_10["Words"]=top_10["Lyrics"].apply(lambda x: len(word_tokenize(x)))
top_10["Unique Words"]=df["Lyrics"].apply(lambda x: len(FreqDist(word_tokenize(x))))

## Richness is defined as % of unique words in a song lyric.  Ej: if a all words in a lyric are different: Richness= 100% 
top_10["Richness"]=round(top_10["Unique Words"]/top_10["Words"]*100,2)

## It is interesting to find how many repetitions has the most common word of the lyric
top_10["Word Repetition"]=top_10["Lyrics"].apply(lambda x: FreqDist(word_tokenize(x)).most_common(1)[0][1])
top_10["%Rep"]=top_10["Word Repetition"]/top_10["Words"]*100

## Also is interesting to determine mean word lenght for each song, as the leaght of the longest word.
top_10["Word Length"]=df["Lyrics"].apply(lambda x: len(x)/len(x.split(" ")))
top_10["Longest word"]=df["Lyrics"].apply(lambda x: len(max(x.split(" "), key=len)))

## Another interesting feature is to determine how many meanfulness words (known as "stop words") are in each lyric. Nltk includes a set of stop words
stop_words = set(stopwords.words('english'))
top_10["Stop Words"]=df["Lyrics"].apply(lambda x: len([w for w in word_tokenize(x) if not w in stop_words]))
top_10["%Stop Words"]=top_10["Stop Words"]/top_10["Words"]*100





## ----- Graph of features-------

evaluate_columns=["Words","Unique Words","Richness","Word Length","Word Repetition","%Rep"]

## Lets see the evolution of each parameter through time. First let´s create a dataframe with the mean value for each year.                               
evol_anual=pd.DataFrame()
for group,frame in top_10.groupby("Year"):
    for column in evaluate_columns:
        evol_anual.at[group,"Mean"+str(column)]=frame[column].mean()


## And then let´s plot
    
fig = plt.figure(figsize=(18, 16),facecolor='w', edgecolor='k')
for column,num in zip(evol_anual.columns,range(1,len(evol_anual.columns)+1)):
    ax = fig.add_subplot(2,len(evol_anual.columns)/2,num)
##  Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(evol_anual.index,evol_anual[column])
    line = slope*evol_anual.index+intercept
    plt.plot(evol_anual.index,evol_anual[column],'o', evol_anual.index, line)
    plt.text(0, 0, "R^2 ="+str(r_value)+"\n "+str(slope) +"* X  + "+str(intercept))
    ax.set_title(column,fontsize=12)    

plt.xlabel("Years")


plt.show()
    

    

print("The script takes ", (datetime.now()- startTime).total_seconds()," sec" )    

