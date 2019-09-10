### Will look at UM vs OSU football programs for last 2 decades. 
## Look at W/L, direct W/L, Recruiting class rankings (not doing this), # of NFL players drafted, #Bowls/bowl wins

import pandas as pd
import numpy as np

UMrecord = pd.read_csv('Michigan.csv')
UMdraft = pd.read_csv('MichiganDraft.csv')
OSUrecord = pd.read_csv('OSU.csv')
OSUdraft = pd.read_csv('OSUdraft.csv')

columnstokeep = ['Year', 'Pct', 'AP Post', 'Bowl', 'Coach(es)']

UMrecord = UMrecord[columnstokeep]
OSUrecord = OSUrecord[columnstokeep]

## Remove 2019 and 1998 from records
UMrecord = UMrecord.drop([0,21])
OSUrecord = OSUrecord.drop([0,21])

###Head to Head data, 1 = UM win, 0 = OSU win
wins = [1,1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0]

##List of years
years = list(range(1999,2019))

## Break down # of draft picks per year 
UM_by_year = list()
OSU_by_year = list()
[UM_by_year.append(int(UMdraft['Yr_draft'].iloc[i].split('-')[0])) for i in range(len(UMdraft['Yr_draft']))]
[OSU_by_year.append(int(OSUdraft['Yr_draft'].iloc[i].split('-')[0])) for i in range(len(OSUdraft['Yr_draft']))];

### Need to create col w/ # of draftees per year
from collections import Counter

UM_by_year = [Counter(UM_by_year)[i] for i in years]
OSU_by_year = [Counter(OSU_by_year)[i] for i in years]

## number of bowl appearances and wins Pct
UMbowls = UMrecord['Bowl'].dropna()
OSUbowls = OSUrecord['Bowl'].dropna()

UMbowlapps = len(UMbowls)
OSUbowlapps = len(OSUbowls)

UMBowlPct = round([name.split('-')[1] for name in UMbowls].count('W') / UMbowlapps,2)
OSUBowlPct = round([name.split('-')[1] for name in OSUbowls].count('W') / OSUbowlapps,2)

## Label each df
UMrecord['Label'] = 'UM'
OSUrecord['Label'] = 'OSU'

UMrecord = UMrecord.set_index('Label')
OSUrecord = OSUrecord.set_index('Label')

##Adjusted from matplotlib barchart example API
def autolabel(rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width()/2., float(height),
                float(height),
                ha='center', va='bottom', fontsize=14)

## Plot bar graphs according to same style
def barplotstyle(UM,OSU,title,savefile):
    
    fig, ax = plt.subplots()
    
    barcall = [1,2]
    labels = ['Michigan', 'Ohio State']
    
    #Remove gridlines + background 
    plt.rcParams['axes.grid'] = False
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['figure.frameon'] = False
    
    rects1 = plt.bar(barcall, [UM, OSU], align='center', color = ['tab:blue', 'tab:red'])
    autolabel(rects1)
        
    plt.xticks(barcall, labels)
    plt.gca().set_title(title, fontsize=18)
    
    
    plt.gca().axes.get_yaxis().set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().set_xticklabels(labels, fontsize=14)
    
    fig.savefig(savefile)
    
    plt.show()


### Start graphics, W/L, Bowl appearances, bowl wins, direct W/L

import matplotlib.pyplot as plt
import matplotlib.ticker as tick
from matplotlib.cm import ScalarMappable 

get_ipython().magic('matplotlib notebook')
    
barplotstyle(UMbowlapps, OSUbowlapps, 'Bowl Appearances 1999-2018', 'BowlAppearances.png')

barplotstyle(UMBowlPct*100, OSUBowlPct*100, 'Bowl Win % 1999-2018','BowlPercent.png')

barplotstyle(sum(wins),len(wins)-sum(wins), 'Direct Wins 1999-2018', 'DirectWins.png')

### Record over time
import seaborn as sns

fig = plt.figure(figsize=(8,5))
ax = plt.gca()
sns.set_style("white")
plt.plot(UMrecord['Year'], UMrecord['Pct']*100, label = 'UM', color = 'tab:blue')
plt.plot(OSUrecord['Year'], OSUrecord['Pct']*100, color = 'tab:red', label ='OSU' )

#Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Set the x-axis to only show the year and y-axis to show win %
ax.xaxis.set_major_locator(plt.MaxNLocator(len(UMrecord['Year'])))
ax.xaxis.set_major_locator(tick.FixedLocator(years))

ax.set_title('UM and OSU Win %')
ax.set_ylabel('Win %')
ax.set_ylim(ymin=0)

plt.xticks(rotation=45)

plt.legend()

fig.savefig('WinPercent.png')

fig = plt.figure(figsize=(3,5))

ax = plt.gca()

swarmWins = (pd.concat([UMrecord['Pct']*100, OSUrecord['Pct']*100])
             .reset_index())
##Round win %
swarmWins['Win %'] = round(swarmWins['Pct'],1)

#create colors
colors = {'UM': 'tab:blue', 'OSU': 'tab:red'}

sns.swarmplot('Label' ,'Win %', palette= colors,data=swarmWins)
ax.set_xlabel('')
ax.get_yaxis().set_visible(False)
ax.set_ylim(ymin =0)

###Remove borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.show()

fig.savefig('WinSwarm.png')

### NFL players per year 

fig = plt.figure(figsize=(8,5))
ax = plt.gca()
sns.set_style("white")
plt.plot(UMrecord['Year'], UM_by_year, label = 'UM')
plt.plot(OSUrecord['Year'], OSU_by_year, color = 'red', label ='OSU')

#Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Set the x-axis to only show the year and y-axis to show win %
ax.xaxis.set_major_locator(plt.MaxNLocator(len(UMrecord['Year'])))
ax.xaxis.set_major_locator(tick.FixedLocator(years))

ax.set_title('NFL Draft Picks for UM vs. OSU')
ax.set_ylabel('# NFL Draft Picks')
ax.set_ylim(ymin=0)

plt.xticks(rotation=45)

plt.legend()

fig.savefig('Draft.png')


###Swarmplot

fig = plt.figure(figsize=(3,5))

ax = plt.gca()

draftlist1 = list()
draftlist2 = list()
for i in range(len(UM_by_year)):
    draftlist1.append('UM')
    draftlist2.append('OSU')
draft = pd.DataFrame([UM_by_year + OSU_by_year, draftlist1 + draftlist2]).T
draft.columns = ['picks', 'labels']

##convert picks form obj to int
draft.picks = draft.picks.astype(int)

sns.swarmplot('labels', 'picks', palette=colors, data=draft);

ax.set_xlabel('')
ax.get_yaxis().set_visible(False)
ax.set_ylim(ymin =0)

###Remove borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.show()

plt.legend()

fig.savefig('DraftSwarm.png')


### Plot the win pct by coach

from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm


UMrecord['Coach(es)'] = [name.split(' (')[0] for name in UMrecord['Coach(es)']]
OSUrecord['Coach(es)'] = [name.split(' (')[0] for name in OSUrecord['Coach(es)']]
OSUrecord['Coach(es)'].iloc[0] = 'Ryan Day / Urban Meyer'

##Get years with corresponding coaches

UMcoaches = (UMrecord.set_index('Coach(es)')
           .groupby(level=0)['Year']
           .agg({'min': min, 'max': max}))

OSUcoaches = (OSUrecord.set_index('Coach(es)')
           .groupby(level=0)['Year']
           .agg({'min': min, 'max': max}))

###Years
UMsegments = list()
OSUsegments = list()
[UMsegments.append([UMcoaches.iloc[i]['min'],UMcoaches.iloc[i]['max']]) for i in range(len(UMcoaches))]
[OSUsegments.append([OSUcoaches.iloc[i]['min'],OSUcoaches.iloc[i]['max']]) for i in range(len(OSUcoaches))]

###Make np array with pct and year

UM_PctYear = np.array(list((UMrecord['Year'], UMrecord['Pct'])))

##Create lists with Year and Win%
UMcoordinates = list()
OSUcoordinates = list()
[UMcoordinates.append([UMrecord['Year'].iloc[i], UMrecord['Pct'].iloc[i]]) for i in range(len(UMrecord['Year']))]
[OSUcoordinates.append([OSUrecord['Year'].iloc[i], OSUrecord['Pct'].iloc[i]]) for i in range(len(OSUrecord['Year']))];

import matplotlib.patches as mpatches

### UM coaches by color

## Create arrays for Linecolormap
UM_x = np.array(UMrecord['Year'])
UM_y = np.array(UMrecord['Pct']*100)
UMcoordinates = np.array([UM_x, UM_y]).T.reshape(-1,1,2)
segments = np.concatenate([UMcoordinates[:-1], UMcoordinates[1:]], axis=1)

## Set the boundaries for coaches
cmap = ListedColormap(['tab:blue', 'tab:red','tab:green','tab:orange'])
norm = BoundaryNorm([1999,2007,2011,2014,2018], cmap.N)

lc = LineCollection(segments, cmap=cmap, norm=norm)

## Feed the array of years to use as boundaries
lc.set_array((UM_x-1))

fig = plt.figure(figsize=(8,5))
ax=plt.gca()
ax.add_collection(lc)

##Configure axes 
plt.xlim(UM_x.min(), UM_x.max())
plt.ylim(UM_y.min(), 100)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Set the x-axis to only show the year and y-axis to show win %
ax.xaxis.set_major_locator(plt.MaxNLocator(len(UMrecord['Year'])))
ax.xaxis.set_major_locator(tick.FixedLocator(years))

ax.set_title('UM Win % by Coach')
ax.set_ylabel('Win %')
ax.set_ylim(ymin=0)


plt.xticks(rotation=45)

LloydCarr = mpatches.Patch(color='tab:blue', label='Lloyd Carr')
RichRodriguzz = mpatches.Patch(color='tab:red', label='Rich Rodriguez')
BradyHoke = mpatches.Patch(color='tab:green',label = 'Brady Hoke')
JimHarbaugh = mpatches.Patch(color='tab:orange', label='Jim Harbaugh')

plt.legend(handles=[LloydCarr, RichRodriguzz, BradyHoke, JimHarbaugh], loc = 'lower right')

fig.savefig('UMCoach.png')

### OSU coaches by color

## Create arrays for Linecolormap
OSU_x = np.array(OSUrecord['Year'])
OSU_y = np.array(OSUrecord['Pct']*100)
OSUcoordinates = np.array([OSU_x, OSU_y]).T.reshape(-1,1,2)
segments = np.concatenate([OSUcoordinates[:-1], OSUcoordinates[1:]], axis=1)

## Set the boundaries for coaches
cmap = ListedColormap(['tab:blue', 'tab:red','tab:green','tab:orange', 'tab:purple'])
norm = BoundaryNorm([1999,2000,2010,2011,2017,2018], cmap.N)

lc = LineCollection(segments, cmap=cmap, norm=norm)

## Feed the array of years to use as boundaries
lc.set_array((OSU_x-1))

fig = plt.figure(figsize=(8,5))
ax = plt.gca()
ax.add_collection(lc)

##Configure axes 
plt.xlim(OSU_x.min(), OSU_x.max())
plt.ylim(OSU_y.min(), 100)

#Remove top and right borders
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#Set the x-axis to only show the year and y-axis to show win %
ax.xaxis.set_major_locator(plt.MaxNLocator(len(UMrecord['Year'])))
ax.xaxis.set_major_locator(tick.FixedLocator(years))

ax.set_title('OSU Win % by Coach')
ax.set_ylabel('Win %')
ax.set_ylim(ymin=0)

plt.xticks(rotation=45)

JohnCooper = mpatches.Patch(color='tab:blue', label='John Cooper')
JimTressel = mpatches.Patch(color='tab:red', label='Jim Tressel')
LukeFikell = mpatches.Patch(color='tab:green', label='Luke Fikell')
UrbanMeyer = mpatches.Patch(color='tab:orange', label='Urban Meyer')
RyanDay_UrbanMeyer =mpatches.Patch(color='tab:purple', label='Ryan Day / Urban Meyer')

plt.legend(handles=[JohnCooper,JimTressel,LukeFikell, UrbanMeyer, RyanDay_UrbanMeyer], loc = 'lower right')

fig.savefig('OSUCoach.png')


