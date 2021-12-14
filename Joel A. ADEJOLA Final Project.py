#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install highlight-text


# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import highlight_text 


# In[3]:


# the famous import font code to use Andale Mono
import matplotlib.font_manager
from IPython.core.display import HTML

def make_html(fontname):
    return "<p>{font}: <span style='font-family:{font}; font-size: 24px;'>{font}</p>".format(font=fontname)

code = "\n".join([make_html(font) for font in sorted(set([f.name for f in matplotlib.font_manager.fontManager.ttflist]))])


# In[4]:


#Import CSV from FBref(from statbomb) from local

df = pd.read_csv('Shooting for Top 5 Leages - Sheet1.csv')


# In[5]:


df.head()


# In[6]:


#To create npxG/90
#Which measures sum of shot qualities per 90 minutes 

df['npxG/90'] = df['npxG']/df['90s']

#To drop the 'Rk' column
df.drop('Rk', axis = 1, inplace = True)

#To split player names
df['Player'] = df['Player'].str.split('\\', expand=True)[0]


# In[7]:


#To filter out players that have not played as often
df = df[df['90s']>=6.5]

#To get rid of goalkeepers and defenders and midfielders
df = df[df['Pos']!= 'GK']
df = df[df['Pos']!= 'MF']
df = df[df['Pos']!= 'DFMF']
df = df[df['Pos']!= 'MFDF']
df = df[df['Pos']!= 'DFFW']
df = df[df['Pos']!= 'DF'].reset_index()


# In[8]:


df.head(50)


# In[9]:


#To set color for background and color of text
background = '#313332'
text_color = 'white'

#To set the background and axis ticks to the colors above
fig, ax = plt.subplots(figsize=(10,5))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#To get rid of axis lines
spines = ['top', 'bottom', 'left', 'right']
for x in spines:
    if x in spines:
        ax.spines[x].set_visible(False)
        
sns.swarmplot(x='npxG/90', data = df, color = 'white',zorder=1)


#Plot Grealish
plt.scatter(0.326531,y=0,c='red',s=100,zorder=2)


# In[10]:


#To create list of metrics we are using
metrics = ['npxG/90', 'xG', 'Gls', 'npxG/Sh', 'Dist', 'np:G-xG']


# In[29]:


#Layout for the grid
fig,axes = plt.subplots(3,2,figsize=(20,10))
fig.set_facecolor(background)
ax.patch.set_facecolor(background)

#set up our base layer
mpl.rcParams['xtick.color'] = text_color
mpl.rcParams['ytick.color'] = text_color

#create a list of comparisons
counter=0
counter2=0
met_counter = 0

#Set up for-loop to plot layout of the metrics one by one
for i,ax in zip(df['Player'],axes.flatten()):
    ax.set_facecolor(background)
    ax.grid(ls='dotted',lw=.5,color='lightgrey',axis='y',zorder=1)
    
#To remove the spines of each plot again
    spines = ['top','bottom','left','right']
    for x in spines:
        if x in spines:
            ax.spines[x].set_visible(False)
            
#For loop to begin the plots for the first metric then end it after it completes the len of metrics          
    sns.swarmplot(x=metrics[met_counter],data=df,ax=axes[counter,counter2],zorder=1,color='white')
    ax.set_xlabel(f'{metrics[met_counter]}',c=text_color)
    
    for x in range(len(df['Player'])):
        if df['Player'][x] == 'Mohamed Salah':
            ax.scatter(x=df[metrics[met_counter]][x],y=0,s=200,c='red',zorder=2)
                        
    met_counter+=1
    if counter2 == 0:
        counter2 = 1
        continue
    if counter2 == 1:
        counter2 = 0
        counter+=1

s='<Mohamed Salah> Premier League Attacking Stats (2021/2022 Season)'
highlight_text.fig_text(s=s,
                x=.25, y=.88,
                #highlight_weights = ['bold'],
                fontsize=22,
                fontfamily = 'Andale Mono',
                color = text_color,
                #highlight_colours = ['#6CABDD'],
                va='center'
               )

fig.text(.12,.05,"Plot includes Forwards from Europe's Top 5 Leagues/ Goal Keepers, Defender, Midfielders and those with less than 6.5 90's played excluded",fontsize=11, fontfamily='Andale Mono',color=text_color)
fig.text(.12,.03,"@joeladejola / data via fbref.com + Statsbomb", fontstyle='italic',fontsize=11, fontfamily='Andale Mono',color=text_color)
fig.text(.12,.01,"inspired by @mckayjohns", fontstyle='italic',fontsize=11, fontfamily='Andale Mono',color=text_color)


plt.savefig('test.png',dpi=500,bbox_inches = 'tight',facecolor=background)


# In[ ]:




