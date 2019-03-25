# SQL output is imported as a pandas dataframe variable called "df"
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

df['first_name'] = df['first_name'].apply(str)
terms = ','.join(list(df['first_name']))
wordcloud = WordCloud(max_font_size=100, width=1100, height=900, min_font_size=12, background_color="rgba(255, 255, 255, 0)", mode="RGBA", collocations=False, colormap="Purples").generate(terms)
fig = plt.figure(figsize=(24,20))
fig.subplots_adjust(left=0.01, bottom=0, right=1, top=1, wspace=0, hspace=0)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
fig.tight_layout()

periscope.output(plt)
