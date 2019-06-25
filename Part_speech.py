from datetime import datetime
import pandas as pd
from nltk.tokenize import  word_tokenize ,PunktSentenceTokenizer
import matplotlib.pyplot as plt
from scipy import stats
import nltk

startTime = datetime.now()

df=pd.read_excel("billboard_lyrics_1964-2015.xlsx",header=0,  encoding='latin-1')

## Exploration shows that some lyrics include \n character, as double spaces. This are replaces as simple space
df["Lyrics"]=df["Lyrics"].str.replace('\n'," ")
df["Lyrics"]=df["Lyrics"].str.replace('  '," ")

top_10=df[df["Rank"]<=10]
top_10["Words"]=top_10["Lyrics"].apply(lambda x: len(word_tokenize(x)))



## Let´s find differents parts of speach using nltk tools. 
def part_speech(Lyric):
    tokenizer = PunktSentenceTokenizer()  
    tokenized = tokenizer.tokenize(Lyric)
    all_words=list()
    n_verbs=0
    n_adjetives=0
    n_adverbs=0
    verbs=["VB","VBD","VBG","VBN","VBP","VBZ"]
    verbs_list=list()
    adjetives=["JJ","JJR","JJS"]
    adjetives_list=list()
    adverbs=["RB","RBR","RBS"]
    adverbs_list=list()
    for sentence in tokenized:
        words=word_tokenize(sentence)
        tagged=nltk.pos_tag(words)
        for tag in tagged:
            if tag[1] in verbs:
                n_verbs+=1
                if tag[0].lower() not in verbs_list:
                    verbs_list.append(tag[0])
            elif tag[1] in adjetives:
                n_adjetives+=1
                if tag[0].lower() not in adjetives_list:
                    adjetives_list.append(tag[0])
            elif tag[1] in adverbs:
                n_adverbs+=1
                if tag[0].lower() not in adverbs_list:
                    adverbs_list.append(tag[0])
    return (n_verbs,n_adjetives,n_adverbs,len(verbs_list),len(adjetives_list),len(adverbs_list))

part_speach=pd.Series(top_10["Lyrics"].apply(lambda x: part_speech(x)))

## Let´s find the use of this parts of speech in the total of the lyrics
top_part_speach=pd.DataFrame(part_speach.tolist(), index= part_speach.index,columns=["Verbs","Adjetives","Adverbs","Unique Verbs","Unique Adjetives","Unique Adverbs"])
top_10 = pd.merge(top_10, top_part_speach, right_index=True,left_index=True, how='outer')
top_10["%Verbs"]=top_10["Verbs"]/top_10["Words"]*100
top_10["%Adjetives"]=top_10["Adjetives"]/top_10["Words"]*100
top_10["%Adverbs"]=top_10["Adverbs"]/top_10["Words"]*100


top_10["%Unique Verbs"]=top_10["Unique Verbs"]/top_10["Words"]*100
top_10["%Unique Adjetives"]=top_10["Unique Adjetives"]/top_10["Words"]*100
top_10["%Unique Adverbs"]=top_10["Unique Adverbs"]/top_10["Words"]*100

evaluate_columns=["Words","%Unique Verbs","%Unique Adjetives","%Unique Adverbs"]

## Now let´s see the evolution of this parameters though time

evol_anual=pd.DataFrame()
for group,frame in top_10.groupby("Year"):
    for column in evaluate_columns:
        evol_anual.at[group,"Mean"+str(column)]=frame[column].mean()

fig = plt.figure(figsize=(18, 16),facecolor='w', edgecolor='k')
        
for column,num in zip(evol_anual.columns,range(1,len(evol_anual.columns)+1)):
    ax = fig.add_subplot(2,len(evol_anual.columns)/2,num)
##  Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(evol_anual.index,evol_anual[column])
    line = slope*evol_anual.index+intercept
    plt.plot(evol_anual.index,evol_anual[column],'o', evol_anual.index, line)
    plt.text(0, 0, "R^2 ="+str(r_value)+"\n "+str(slope) +"* X  + "+str(intercept))
    ax.set_title(column,fontsize=10)    

plt.xlabel("Years")

plt.show()
print("The script takes ", (datetime.now()- startTime).total_seconds()," sec" )    



