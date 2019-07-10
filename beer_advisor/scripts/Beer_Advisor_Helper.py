## Helper file of all function, widgets and code to display Beer Advisor's
## Beer Recommender App 

print('importing...')


import ipywidgets as widgets
import pandas as pd
import numpy as np
import datetime as dt
from scipy import stats
import re, warnings 
from tabulate import tabulate
import ipywidgets as widgets
from IPython.display import display, clear_output, HTML, Markdown, Latex
from ipywidgets import Layout, interact, interact_manual



########## DATA GRAB ##########
beers = pd.read_csv('data/beer_info.csv')#.drop('Unnamed: 0',axis=1)
reviews = pd.read_csv('data/beer_ratings.csv').drop('Unnamed: 0',axis=1)
#breweries = beers.sort_values('brewery').brewery.unique()
family_lookup = pd.read_csv('data/beer_family_lookup.csv').drop('idx',axis=1)
family_lookup.rename(columns={'style':'beer_style'},inplace=True)

beers = pd.merge(beers,family_lookup,on='beer_style')

my_beers = [977,982,8980,9653,2678,4146,4143]
my_rates = [3.2,4.1,2.7,3.4,3.1,4.5,4.2]

########## HELPFUL FUNCTIONS ##########

def pandas_df_to_markdown_table(df):
    from IPython.display import Markdown, display
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.to_csv(sep="|", index=False)))


########## PRESENTATION UI AND FUNCTIONS ##########

show_overview_btn = widgets.Button(
    description="Let's get started!",
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show Overview Block',
    icon=''
)
show_webscraping_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show Webscraping Block',
    icon=''
)
show_EDA_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show EDA Block',
    icon=''
)
show_superuserplot_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show superuser plot',
    icon=''
)
show_boxplot_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show boxplot plot',
    icon=''
)

show_boxhist_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show boxplot and histogram',
    icon=''
)

show_correlation_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show correlational plot',
    icon=''
)

show_beeradvisor1_btn = widgets.Button(
    description='',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beeradvisor section 1',
    icon=''
)

show_beeradvisor2_btn = widgets.Button(
    description='Your Preferences?',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beeradvisor section 2',
    icon=''
)

show_beeradvisor3_btn = widgets.Button(
    description='Group Em Up',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beeradvisor section 3',
    icon=''
)

show_beeradvisor4_btn = widgets.Button(
    description='Calculate Correlation',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beeradvisor section 4',
    icon=''
)

show_beeradvisor5_btn = widgets.Button(
    description='Try these Beers!',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beeradvisor section 5',
    icon=''
)

show_beerrecs_btn = widgets.Button(
    description='Closer Look',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beer recommendations',
    icon=''
)

show_shameless_plug_btn = widgets.Button(
    description='Author Desc.',
    disabled=False,
    button_style='primary', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Show beer recommendations',
    icon=''
)


def show_overview_text(b):
    clear_output()
    show_overview_btn.close()
    display(Markdown(overview_text))
    display(show_webscraping_btn)
    
def show_webscraping_text(b):
    show_webscraping_btn.close()
    display(Markdown(webscraping_text))
    display(show_EDA_btn)

def show_EDA1_text(b):
    show_EDA_btn.close()
    display(Markdown(EDA1_text))
    display(show_boxhist_btn)
    
def goplot_super_user(b):
    show_superuserplot_btn.close()
    plot_super_user2()
    display(Markdown(show_boxplot_intro_text))
    display(show_correlation_btn)    

def goplot_boxplot(b):
    boxplot_family()

def goplot_boxhist(b):
    show_boxhist_btn.close()
    plot_boxhist()
    display(Markdown(EDA2_text))
    display(show_superuserplot_btn)
    
def goplot_correlation(b):
    show_correlation_btn.close()
    plot_correlation2()
    display(Markdown(EDA3_text))
    display(show_beeradvisor1_btn)
    
def show_beeradvisor1_text(b):
    show_beeradvisor1_btn.close()
    display(Markdown(beeradvisor1_text))
    display(show_beeradvisor2_btn)

def show_beeradvisor2_text(b):
    show_beeradvisor2_btn.close()
    display(Markdown(beeradvisor2_text))
    display(show_beeradvisor3_btn)
    
def show_beeradvisor3_text(b):
    show_beeradvisor3_btn.close()
    display(Markdown(beeradvisor3_text))
    display(show_beeradvisor4_btn)

def show_beeradvisor4_text(b):
    show_beeradvisor4_btn.close()
    display(Markdown(beeradvisor4_text))
    display(show_beeradvisor5_btn)

def show_beeradvisor5_text(b):
    show_beeradvisor5_btn.close()
    display(Markdown(beeradvisor5_text))
    display(show_beerrecs_btn)

def show_beerrecs(b):
    show_beerrecs_btn.close()
    [display_beer(recs_df.iloc[i,:].to_frame().values.tolist())
     for i in range(4)]
    display(show_shameless_plug_btn)
    
def show_shameless_plug(b):
    show_shameless_plug_btn.close()
    display(Markdown(shameless_plug_text))
  


recs_df = beers[beers.beer_id.isin([1944,7635,8959,483,8096])]
def display_beer(r):    
    print("Name: ", r[4][0])
    print("Brewery: ", r[6][0])
    print("Family: ",r[10][0])
    print('ABV: ',r[1][0],'\t BA Score: ',r[0][0])
    print("Description: ", r[7][0])
    display(Markdown('![No Image Available]({})'.format(r[3][0])))
    print('*.*'*35)
    pass


########## PLOT GENERATION ##########

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.plotly
import plotly.io as pio
init_notebook_mode(connected=True)

### Show timeseries of supersuser
def plot_super_user():
    def find_user_aggregate(u):
        df = reviews[reviews.username == u].posted.value_counts()
        df = df.reset_index().rename(columns = {'index':'date'})
        df = (
                df.
                groupby(by=[pd.to_datetime(df.date.rename(columns={'date':'year'})).dt.year,
                            pd.to_datetime(df.date.rename(columns={'date':'month'})).dt.month])
                .agg('count')
            )
        df = df.reset_index().rename(columns = {'level_0':'year','level_1':'month'})[['year','month','posted']]
        df['dates'] = [dt.datetime.strptime('-'.join([str(df['month'][i]),str(df['year'][i])]),'%m-%Y') for i in range(df.shape[0])]
        return df[['dates','posted']]

    top10_users = list(reviews.groupby('username').agg('count').sort_values('posted',ascending=False).index[:10])
    
    data = [find_user_aggregate(user) for user in top10_users]
    traces=[]
    for i in range(len(top10_users[:])):
        df = data[i]
        xU = df.dates
        yU = df.posted.values

        trace = dict(
            x=xU,
            y=yU,
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name = top10_users[i]
        )
        traces.append(trace)
    review_counts_by_time = traces


    layout = dict(title = 'Montly Aggregate of Super-User Activity',
                  yaxis = dict(
                      title = 'Per Month Count'),
                  xaxis = dict(
                      title = 'Date'
                  )
                 )
    fig = dict(data = review_counts_by_time, layout = layout)
    #pio.write_image(fig, 'img/super_user_lifetime.png', width=600, height= 600,scale = 1)
    return plotly.offline.iplot(fig)

def plot_super_user2():
    def find_user_aggregate(u):
        df = reviews[reviews.username == u].posted.value_counts()
        df = df.reset_index().rename(columns = {'index':'date'})
        df = (
                df.
                groupby(by=[pd.to_datetime(df.date.rename(columns={'date':'year'})).dt.year,
                            pd.to_datetime(df.date.rename(columns={'date':'month'})).dt.month])
                .agg('count')
            )
        df = df.reset_index().rename(columns = {'level_0':'year','level_1':'month'})[['year','month','posted']]
        df['dates'] = [dt.datetime.strptime('-'.join([str(df['month'][i]),str(df['year'][i])]),'%m-%Y') for i in range(df.shape[0])]
        return df[df.dates < '2019-06-01'][['dates','posted']]
    
    def find_all_aggregate(users):
        df = reviews[~reviews.username.isin(users)].posted.value_counts()
        df = df.reset_index().rename(columns = {'index':'date'})
        df = (
                df.
                groupby(by=[pd.to_datetime(df.date.rename(columns={'date':'year'})).dt.year,
                            pd.to_datetime(df.date.rename(columns={'date':'month'})).dt.month])
                .agg('count')
            )
        df = df.reset_index().rename(columns = {'level_0':'year','level_1':'month'})[['year','month','posted']]
        df['dates'] = [dt.datetime.strptime('-'.join([str(df['month'][i]),str(df['year'][i])]),'%m-%Y') for i in range(df.shape[0])]
        return df[df.dates < '2019-06-01'][['dates','posted']]
    

    top10_users = list(reviews.groupby('username').agg('count').sort_values('posted',ascending=False).index[:10])
    
    data = [find_user_aggregate(user) for user in top10_users]
    data.append(find_all_aggregate(top10_users))
    traces=[]
    for i in range(len(top10_users[:])+1):
        df = data[i]
        xU = df.dates
        yU = df.posted.values
        if i < 10: 
            name = top10_users[i]
        else:
            name = 'Everyone Else'
        trace = dict(
            x=xU,
            y=yU,
            hoverinfo='x+y',
            mode='lines',
            line=dict(width=0.5),
            stackgroup='one',
            name = name
        )
        traces.append(trace)
        
    
    
        
        

    review_counts_by_time = traces


    layout = dict(title = 'Montly Aggregate of Super-User Activity',
                  yaxis = dict(
                      title = 'Per Month Count'),
                  xaxis = dict(
                      title = 'Date'
                  )
                 )
    fig = dict(data = review_counts_by_time, layout = layout)
    #pio.write_image(fig, 'img/super_user_lifetime.png', width=600, height= 600,scale = 1)
    return plotly.offline.iplot(fig)

### Show boxplots of the percentage of beers rated in each family by the top 10 reviewers
def boxplot_family():
    top10 = reviews.groupby('username').agg('count').sort_values('posted',ascending=False).index[:10].values
    df = reviews[reviews.username.isin(top10)].join(beers[['family','BAscore']],on='beer_id',how='left')
    df = df.groupby(by=['family','username']).agg({'posted':'count','score':'mean'})
    families = df.reset_index().family.unique()    
    data = []
    i=0
    for family in families[:10]:
        num_beers = len(beers.reset_index()[beers.family == family].index.values)
        trace1 = go.Box(
            y=df.loc[family]['posted'] / num_beers,
            name=family,
            xaxis='x1',
            yaxis='y1'
            
        )
        trace2 = go.Box(
            y=df.loc[family]['score'],
            name=family,
            xaxis='x1',
            yaxis='y2'
        )
        data.append(trace1)
        data.append(trace2)
        i=i+1
            
    layout = go.Layout(
        xaxis = dict(            
            anchor='x1',
            title='Beer Family',
            linewidth = 2,
            mirror = True
        ),
        yaxis1 = dict(
            domain=[0, 0.5],
            anchor='y1',
            title = 'Number of Reviews'
        ),
        
        yaxis2 = dict(
            domain=[0.5, 1],
            anchor='y2',
            title = 'Ratings'
        ),
        showlegend = False
        
    )
    fig = go.Figure(data=data,layout=layout)
    
    return plotly.offline.iplot(fig)

## Show distribution of Users Review Numbers
def plot_boxhist():
    y0 = (reviews.groupby('username').agg('count').sort_values('posted',ascending=False).posted.values)
    z = np.abs(stats.zscore(y0))

    trace0 = go.Box(y=y0[z>3],xaxis = 'x1',yaxis='y1',name='')
    trace1 = go.Histogram(x=y0[z>3],xaxis = 'x2',yaxis='y2',name='')
    layout = go.Layout(
        xaxis1 = dict(anchor='x1',domain=[0,0.5]),
        xaxis2 = dict(anchor='x2',domain=[0.6,1],title='Number of Reviews'),
        yaxis1 = dict(anchor='x1',domain=[0,1],title='Number of Reviews'),
        yaxis2 = dict(anchor='x2',domain=[0,1],title='Unique Users'),
        title = 'Distribution of Review per User',
        showlegend=False
    )
    data = [trace0, trace1]
    fig = go.Figure(data=data,layout=layout)
    return plotly.offline.iplot(fig)

# Show Correlation between
def plot_correlation():
    df = beers[['num_reviews','BAscore','beer_name','family']].sort_values('num_reviews')
    x = df['num_reviews'].values
    y = df['BAscore'].values
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    x_fit = np.linspace(x[0], x[-1], 50)
    y_fit = f(x_fit)

    trace1 = go.Scatter(x = x,y = y,mode='markers',name=list(df['family'].values),hovertext=df['beer_name'].values,
                        marker=dict(size=5))
    trace2 = go.Scatter(x = x_fit, y = y_fit, mode = 'lines',name='2d Polyfit')
    layout = go.Layout(title='BA Score by Number of Reviews')
    data = [trace1,trace2]
    fig = go.Figure(data,layout)
    return plotly.offline.iplot(fig)

def plot_correlation2():
    df = beers[['num_reviews','BAscore','beer_name','family']].sort_values('num_reviews')
    families = list(beers['family'].unique())
    x = df['num_reviews'].values
    y = df['BAscore'].values
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    x_fit = np.linspace(x[0], x[-1], 50)
    y_fit = f(x_fit)
    traces = []
    for family in families:
        df0 = (
            beers[beers.family == family]
            [['num_reviews','BAscore','beer_name','family']]
        )
        trace = go.Scatter(x = df0['num_reviews'].values,
                           y = df0['BAscore'].values,
                           mode='markers',name=family,
                           hovertext=df['beer_name'].values,
                           marker=dict(size=5))
        traces.append(trace)
    
    trace_fit = go.Scatter(x = x_fit, y = y_fit, mode = 'lines',name='2d Polyfit')
    traces.append(trace_fit)
    layout = go.Layout(title='BA Score by Number of Reviews')
    fig = go.Figure(data = traces, layout = layout)
    return plotly.offline.iplot(fig)

########## COLLABORATIVE FILTERING ##########
from scipy.stats.stats import pearsonr

def run_generate(b):
    print('Finding Recommendations...')
    recommendations = generate_recommendations(user_prefs.beers.values,user_prefs.rates.values,beers,reviews)
    
    print('Recommendations Found!!!')
    display(recommendations)


def user_item_review_matrix(beers_,beers,reviews):    
    
    '''Generates a user_item_review matrix provided a list of beers.'''
    '''Used in collaborative filtering'''
    beer_tdf = (
        beers[['beer_name','beer_style','beer_id']]
        [beers.index.isin(beers_)]
    )
    
    return (        
        reviews[reviews.beer_id.isin(beer_tdf.index)]
        .merge(beer_tdf,how='left',on='beer_id')
        [['username','score','beer_id','posted']]
        .drop_duplicates(subset=['beer_id','username'],keep='first')
        .pivot(index='username',columns='beer_id',values='score')
    )

def corr(X, Y):
    r = np.corrcoef(X,Y)[0,1]
    f = 0.5 * np.log((1+r)/(1-r))
    se=1/np.sqrt(len(X)-3)
    ucl=f+2*se
    lcl=f-2*se
    lcl=(np.exp(2*lcl)-1) / (np.exp(2*lcl)+1)
    ucl=(np.exp(2*ucl)-1) / (np.exp(2*ucl)+1)
    return r,lcl,ucl

def generate_recommendations(list_,scores_,beersdf,reviewsdf):
    beers = beersdf
    reviews = reviewsdf
    '''Takes a list of beer_ids and personal scores, and generates a list of beer_ids to try.
    Uses Pearson Coefficient Method '''
    # Create a DataFrame to store users products and ratings
    user_reviews = (
        pd.DataFrame({'username':'user','score':scores_,'beer_id':list_})
        .pivot(index='username',columns='beer_id',values='score')        
    )
    
    #Generate a User-Item-Review matrix
    uirm = user_item_review_matrix(list(user_reviews.columns),beers,reviews)
    uirm_df = pd.concat([user_reviews, uirm])
    
    
    # Calculate the Pearson Correlation to user ratings
    rankings = {'user':[],'corr':[],'pairs':[]}    
    for i in range(1,len(uirm_df)):
        new_df = uirm_df.iloc[[0,i],:]
        new_df = new_df.dropna(axis=1, how='any')    
        if new_df.shape[1] >= 2:
            val = list(new_df.values)
            corr(val[0],val[1])[0]            
            rankings['user'].append(new_df.index[1])
            rankings['corr'].append(corr(val[0],val[1])[0])
            rankings['pairs'].append(new_df.shape[1])    
    ranking_df = pd.DataFrame(rankings)
    ranking_df.set_index('user',inplace=True)   
    
    recommender = (
        pd.merge(ranking_df,uirm,how='left',left_index=True,right_index=True)
        .dropna(axis=1,how='all')
    )

    similar_beers = (
        reviews[reviews['username'].isin(list(recommender.index))]
        .merge(beers,how='left',on='beer_id')
        [['username','score','beer_name','beer_id']]    
        .drop_duplicates(subset=['beer_id','username'],keep='first')
        .pivot(index='username',columns='beer_id',values='score')
    )
   
    try_these = pd.concat([recommender,similar_beers],axis=1, 
                          join_axes=[recommender.index]).drop(list(recommender.columns)[2:],axis=1)
   
    try_these.loc['total'] = try_these.sum(axis=0)
    try_these.loc['sim.sum'] = try_these.mul(try_these['corr'],axis=0).sum()    
    try_these.loc['total/sim.sum'] = try_these.loc['total'] / try_these.loc['sim.sum']     
    top_5 = list(try_these.T['total/sim.sum'].sort_values(ascending=False).head(5).index)
    return beers[beers.index.isin(top_5)][['beer_name','brewery','beer_style','BAscore']]









########## PRESENTATION TEXT ##########

overview_text = """ 
# Beer Advisor Overview

Hello, and welcome to Beer Advisor.

This project had three steps:
1. This project aimed to scrape as much data as possible from [BeerAdvocate.com](https://www.beeradvocate.com)
2. Peform Numerical Analysis on user reviews.
3. Develop a recommender system to suggest beers to new users based on the data scraped from previous reviews.
"""

webscraping_text = """
### 1. Webscraping

__Beer Advocate__ is online community where users can rate and review all beers, craft to mainstream. This website was scraped using a _scrapy spider_. Information on the general product page and each individual review was pulled by the spider.

    
    Beer Advocate boasts a database of nearly 300,000 beers (probably more at this point).

    Only looked at beers with more than 100 user ratings. (conveniently listed on the beer list page)

    3 hours later and we have nearly 10,000 individual beers and 1.7 million individual reviews!!
    

Based on the origin of the data, the information was piped into one of two csv files and generated tables of information similar to this:

#### Beers DataFrame

|   beer_id | beer_name                        | brewery                            | beer_style                 |   abv |   num_reviews |   ranking |
|----------:|:---------------------------------|:-----------------------------------|:---------------------------|------:|--------------:|----------:|
|      9128 | Motor City Brewing Ghettoblaster | Motor City Brewing Works           | English Dark Mild Ale      |   4.2 |            64 |     44196 |
|       205 | Spellbound IPA                   | Spellbound Brewing                 | American IPA               |   6.5 |            35 |     13651 |
|      9358 | Red Nose Winter Ale              | Natty Greene's Pub & Brewing Co.   | Winter Warmer              |   6.8 |            51 |     38773 |
|      6646 | Hunter Vanilla                   | 18th Street Brewery - Gary Taproom | English Sweet / Milk Stout |   8.5 |            61 |      1391 |
|      3753 | Bière De Miel Biologique         | Brasserie Dupont sprl              | Belgian Saison             |   8   |           184 |     16355 |

#### Reviews DataFrame
  
|   review_id |   beer_id | posted              | ratings                     |   score | username        |
|------------:|----------:|:--------------------|:----------------------------|--------:|:----------------|
|      675575 |      4399 | 2012-04-26 00:00:00 | [4.5, 4.5, 3.5, 4.0, 4.0]   |    3.95 | Rutager         |
|     1270933 |      7509 | 2016-04-19 00:00:00 | [4.0, 4.25, 4.0, 4.25, 4.0] |    4.09 | stortore        |
|      686394 |      4481 | 2009-10-21 00:00:00 | [4.0, 4.0, 4.5, 4.5, 4.5]   |    4.35 | Josievan        |
|     1347362 |      7959 | 2009-11-13 00:00:00 | [4.0, 3.0, 3.0, 2.5, 2.0]   |    2.81 | civilizedpsycho |
|     1119392 |      6675 | 2010-02-17 00:00:00 | [4.0, 4.5, 4.0, 4.0, 4.0]   |    4.12 | drizzam         |


Due to the enormity of reviews scraped from this website, text content was omitted from this notebook to save on data limits. Some _post-processed text_ will be discussed later.

Lets look a little more closely at the data...

"""

EDA1_text = """
### 2. Numerical Analysis

In our dataset we have reviews from 57,023 individual users.

|   EDA  |   count |    mean |     std |   min |   25% |   50% |   75% |   __max__ |
|-------:|--------:|:-------:|:-------:|:-----:|:-----:|:-----:|:-----:|:-----:|
| summary|   57023 | 30.8128 | 133.207 |     1 |     1 |     2 |     9 |  __4175__ |

"""



EDA2_text = """


We can see that the vast majority of reviews are supplied by __less than 25%__ of the population ==> The dataset is _heavily skewed_ to a set of __super users__

Lets try to find some of our __super users__. Here are the Top 10


|  user  |   StonedTrippin |   metter98 |   superspak |   brentk56 |   BEERchitect |   UCLABrewN84 |   zeff80 |   woodychandler |   jlindros |   NeroFiddled |
|:-------|----------------:|-----------:|------------:|-----------:|--------------:|--------------:|---------:|----------------:|-----------:|--------------:|
| posted |            4175 |       4056 |        3855 |       3753 |          3682 |          3581 |     3015 |            2959 |       2957 |          2834 |

"""



show_boxplot_intro_text = """




What's the impact of all these reviews? Do more reviews for a given product impact its favorability?


"""

EDA3_text = """

Notice how as the number of reviewsfor a given beer gets larger the score stabilizes.

Does that imply that beers with thousands of reviews are more accurately scored?

    Perhaps its simple a popularity bias
   
Regardless, the more reviews a beer has, the higher its score.

And the higher its score, the higher it's visibility.
"""



beeradvisor1_text = """
### 3. Beer Advisor Recommender

With all of our data, we can actually approach the building of a Recommender System.

- Not at all like Netflix or Facebooks. Beer Advisor is a _baby recommender_

We employ a __User-Item Collaborative Filter__:
1. You input a series of Beers that you like _(or don't like)_ 

"""
beeradvisor2_text = """


| Beers |   Lagunitas IPA |   Two Hearted Ale |   Sweet Action |   Hoegaarden Original White Ale |   Blue Moon Belgian White |   Club De Stella Artois |   Yuengling Traditional Lager |
|:------|----------------:|------------------:|---------------:|--------------------------------:|--------------------------:|------------------------:|------------------------------:|
| Scores |             3.2 |               4.1 |            2.7 |                             3.4 |                       3.1 |                     4.5 |                           4.2 |


2. We find other users who have rated those same beers!!
"""


beeradvisor3_text = """



| index| username     |   Lagunitas IPA |   Two Hearted Ale |   Sweet Action |   Hoegaarden Original White Ale |   Blue Moon Belgian White |   Club De Stella Artois |   Yuengling Traditional Lager |
|:-----|:-------------|----------------:|------------------:|---------------:|--------------------------------:|--------------------------:|------------------------:|------------------------------:|
| 0    | KidDoc       |          nan    |              4.18 |            nan |                          nan    |                    nan    |                     nan |                           nan |
| 1    | NCSUdo       |            4.38 |              4.44 |            nan |                          nan    |                      3.57 |                     nan |                           nan |
| 2    | ThreePistols |          nan    |            nan    |            nan |                            4    |                    nan    |                     nan |                             4 |
| 3    | appenzeller  |            4.08 |            nan    |            nan |                            3.73 |                    nan    |                     nan |                           nan |
| -    | -            |               - |            -      |            -   |                            -    |                    -    |                     - |                           - |
| 6930 | FireorHigher |            nan  |            nan    |            nan |                            nan  |                    3.51    |                     nan |                           3.18 |

3. Measure the correlation between the two
"""
beeradvisor4_text = """



| user       |       corr |    Lagunitas IPA |   Two Hearted Ale |   Sweet Action |   Hoegaarden Original White Ale |   Blue Moon Belgian White |   Club De Stella Artois |   Yuengling Traditional Lager |
|:-----------|-----------:|-------:|------:|-------:|-------:|-------:|-------:|-------:|
| TheSarge   | -0.042 |   3.86 |  3.68 |    nan |   3.76 |   2.88 |    nan |   2.56 |
| SkunkWorks |  0.300  |   3.82 |  4.32 |    nan |   3.4  | nan    |    nan |   3    |
| HotHands   |  0.923  | nan    |  4.15 |    nan |   3.95 | nan    |    nan |   3.45 |
| jsprain1   |  0.136  |   3.65 |  4.5  |    nan |   3.66 |   3.59 |    nan |   3.73 |
| Tom_Banjo |  0.995 |   3    |   3.46 |   3    |   3.46 | nan    |    nan | nan    |
| beergoot  |  0.876 |   3.66 |   4.45 | nan    | nan    | nan    |    nan |   3.33 |


4. Mutliplies across the rows and then sums down the columns
5. Outputs the 5 most highly scored beers weighted by my closest users (_in terms of preference_)
"""
beeradvisor5_text = """




|    beer  | Turbo Nerd XIPA |       Vanilla Joe |       Innis & Gunn Lager Beer |        Filthy Dirty IPA |       Brunch Money |
|:---------|-----------:|-----------:|-----------:|-----------:|-----------:|
| corr.sum | 0.00584292 | 0.00584274 | 0.00584233 | 0.00584223 | 0.00584183 |

Let's take a look at the top two beers and see why we might like them so much...
"""

shameless_plug_text = """

I hope you enjoyed this presentation.

* Check out my [github](https://github.com/charliesusername/Beer-Advisor) to view the code behind this project and my other projects. 

* Or my [LinkedIn](https://www.linkedin.com/in/charles-cohen-999782119/) if your _hiring_!!


    A Data Science Project by Charles Cohen

"""


clear_output()
print('All Scripts Imported!!!')