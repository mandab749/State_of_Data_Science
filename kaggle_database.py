# Python program to generate WordCloud 

# importing all necessery modules 
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt 
import pandas as pd 

# Reads file 
df = pd.read_csv(r"other_text_responses.csv", encoding ="latin-1")
print(len(df.columns)) 

comment_words = ' '
stopwords = list(STOPWORDS) + ["NaN"]

# iterate through the csv file 
for val in df.Q13_OTHER_TEXT:	
    # typecaste each val to string 
    val = str(val) 

	# split the value 
    tokens = val.split() 
	
	# Converts each token into lowercase 
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
		
    for words in tokens: 
        comment_words = comment_words + words + ' '


wordcloud = WordCloud(width = 800, height = 800, 
				background_color ='white', 
				stopwords = stopwords, 
				min_font_size = 10).generate(comment_words) 

# plot the WordCloud image					 
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0) 

plt.show() 



