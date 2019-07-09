

```python

```


      File "<ipython-input-7-8ac09e2f4545>", line 1
        $ jupyter nbconvert Beer_Advisor_Notebook.ipynb --to markdown --output output.md
        ^
    SyntaxError: invalid syntax
    



```python
### Imports
from scripts.top5beers import *
from IPython.display import display, clear_output, HTML
from ipywidgets import Layout, interact, interact_manual
import ipywidgets as widgets
import pandas as pd
import numpy as np
import warnings
from tabulate import tabulate
warnings.filterwarnings('ignore')

### Load Data
beers = pd.read_csv('data/beer_info.csv').drop('Unnamed: 0',axis=1)
reviews = pd.read_csv('data/beer_ratings.csv').drop('Unnamed: 0',axis=1)
breweries = beers.sort_values('brewery').brewery.unique()


### Widgets

add_beer = widgets.Button(
    description='Add Beer',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Add Beer',
    icon='check'
)
clear_list = widgets.Button(
    desccription='Clear List',
    disabled=False,
    button_style='danger',
    tooltip='Clears list of beers',
    icon='check'
)
brewery = widgets.Dropdown(
    options=breweries,
    value=breweries[0],
    description='Brewery:',
    disabled=False,
)

new_beer_btn = widgets.Button(
    description='Add a New Beer',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Add a New Beer',
    icon='check'
)

undo_last_beer_btn = widgets.Button(
    description = 'Clear user preferences',
    disabled=False,
    button_style='warning',
    tooltip='Remove the last rating from list',
    icon='check'
)

rate_slider = widgets.FloatSlider(
            value=3.5,
            min=1.0,
            max=5.0,
            step=0.1,
            description='Rate:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )
add_beer_btn = widgets.Button(
            description='Add Beer to List',
            disabled=False,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Add Beer',
            icon='check'
        )


### Functions 

def pandas_df_to_markdown_table(df):
    from IPython.display import Markdown, display
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.to_csv(sep="|", index=False)))

def on_add_beer_clicked(b):
    global user_prefs
    beer_ = select_beers.value
    rate_ = rate_slider.value
    user_prefs = user_prefs.append({'beers':int(beer_),'rates':rate_},ignore_index=True)
    


def remove_last_row(b):
    user_prefs.drop(user_prefs.tail(1).index,inplace=True)
    clear_output()
    display(new_beer_btn)
    print(user_prefs)
    display(undo_last_beer_btn)
    
gen_recs_btn = widgets.Button(
    description='Calculate Recommendations',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Calculate Recommendations',
    icon='check'
)
def run_generate(b):
    print('Finding Recommendations...')
    recommendations = generate_recommendations(user_prefs.beers.values,user_prefs.rates.values,beers,reviews)
    
    print('Recommendations Found!!!')
    display(recommendations)
    
    
def show_beer_info(b):
    print('this some fucking info be here b')
    
    
    
HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
The raw code for this IPython notebook is by default hidden for easier reading.
To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.''')

```




<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
The raw code for this IPython notebook is by default hidden for easier reading.
To toggle on/off the raw code, click <a href="javascript:code_toggle()">here</a>.



# Beer Advisor Overview

Hello, and welcome to Beer Advisor.

This project had three steps:
1. This project aimed to scrape as much data as possible from [BeerAdvocate.com](https://www.beeradvocate.com)
2. Peform Numerical Analysis on user reviews.
3. Develop a recommender system to suggest beers to new users based on the data scraped from previous reviews.
4. Analyze textual data from reviews to advisor brewers on new products.


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


### 2. Numerical Analysis

In our dataset we have reviews from 57,023 individual users.

|   EDA  |   count |    mean |     std |   min |   25% |   50% |   75% |   max |
|-------:|--------:|:-------:|:-------:|:-----:|:-----:|:-----:|:-----:|:-----:|
| summary|   57023 | 30.8128 | 133.207 |     1 |     1 |     2 |     9 |  4175 |

#########BOX PLOT#########


We can see that the vast majority of reviews are supplied by less than 25% of the population ==> The dataset is _heavily skewed_ to a set of __super users__

Lets try to find some of our __super users__. Here are the Top 10


|  user  |   StonedTrippin |   metter98 |   superspak |   brentk56 |   BEERchitect |   UCLABrewN84 |   zeff80 |   woodychandler |   jlindros |   NeroFiddled |
|:-------|----------------:|-----------:|------------:|-----------:|--------------:|--------------:|---------:|----------------:|-----------:|--------------:|
| posted |            4175 |       4056 |        3855 |       3753 |          3682 |          3581 |     3015 |            2959 |       2957 |          2834 |

#########Time Plot showing Users Lifetime Activity########

What's the impact of all these reviews? Do more reviews for a given product impact its favorability?


#########Rating V User Reviews#########




1. User Reviews Graphs
  1. User Reviews over time
  2. Rating v User Reviews
  3. Ratings v Styles of Beer
    1. Variance (Box-Plot), 

2. 


```python
summarized = reviews.groupby('username').agg({'posted':'count'})
tabulate(summarized.sort_values('posted',ascending=False).head(10).T,tablefmt='pipe',headers='keys')
```




    '|        |   StonedTrippin |   metter98 |   superspak |   brentk56 |   BEERchitect |   UCLABrewN84 |   zeff80 |   woodychandler |   jlindros |   NeroFiddled |\n|:-------|----------------:|-----------:|------------:|-----------:|--------------:|--------------:|---------:|----------------:|-----------:|--------------:|\n| posted |            4175 |       4056 |        3855 |       3753 |          3682 |          3581 |     3015 |            2959 |       2957 |          2834 |'




```python
summarized.sort_values('posted',ascending=False).head(10).T
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>username</th>
      <th>StonedTrippin</th>
      <th>metter98</th>
      <th>superspak</th>
      <th>brentk56</th>
      <th>BEERchitect</th>
      <th>UCLABrewN84</th>
      <th>zeff80</th>
      <th>woodychandler</th>
      <th>jlindros</th>
      <th>NeroFiddled</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>posted</th>
      <td>4175</td>
      <td>4056</td>
      <td>3855</td>
      <td>3753</td>
      <td>3682</td>
      <td>3581</td>
      <td>3015</td>
      <td>2959</td>
      <td>2957</td>
      <td>2834</td>
    </tr>
  </tbody>
</table>
</div>



### Beer Advisor Recommender
Using a collaborative recommender system, Beer Advisor can suggest a number of beers you may be interested in based on your preferences.

       --- The more ratings you have the more accurate Beer Advisor is. ---
       



```python
user_prefs=pd.DataFrame({'beers':[],'rates':[]})
warnings.filterwarnings('ignore')

def add_beer(b):    
    clear_output()
    display(new_beer_btn)
    #print(user_prefs)
    select_brewery = widgets.Dropdown(
        options=breweries,
        value=breweries[0],
        description='Select brewery:',
        disabled=False,
        button_style=''
    )
    def get_brewery(b):
        
        def add_rating(b):
            global user_prefs
            user_prefs = user_prefs.append({'beers':select_beer.value,'rates':rate_slider.value},ignore_index=True)
            user_prefs.drop_duplicates('beers',keep='last',inplace=True)
            #print(user_prefs)
            rate_slider.close()
            add_beer_btn.close()
            select_brewery.close()
            select_beer.close()
            display(undo_last_beer_btn)
            undo_last_beer_btn.on_click(remove_last_row)
            print(user_prefs)
            
            if user_prefs.shape[0] > 1:
                display(gen_recs_btn)                
                gen_recs_btn.on_click(run_generate)
                
            
        beer_list = beers[beers.brewery == select_brewery.value][['beer_id','beer_name']]
        beer_list = list(zip(beer_list.beer_name.values,beer_list.beer_id.values))
        select_beer = widgets.Dropdown(
            options=beer_list,
            value=beer_list[0][1],
            description='Select Beer:',
            disabled=False,
        )
        rate_slider = widgets.FloatSlider(
            value=3.5,
            min=1.0,
            max=5.0,
            step=0.1,
            description='Rate:',
            disabled=False,
            continuous_update=False,
            orientation='horizontal',
            readout=True,
            readout_format='.1f',
        )
        add_beer_btn = widgets.Button(
            description='Add Beer to List',
            disabled=False,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Add Beer',
            icon='check'
        )

        display(select_beer,rate_slider,add_beer_btn)
        select_beer.observe(show_beer_info, names = 'value')
        
        
        
        add_beer_btn.on_click(add_rating)
        



    display(select_brewery)
    select_brewery.observe(get_brewery, names = 'value')
    
    

display(new_beer_btn)
new_beer_btn.on_click(add_beer)



```


    Button(button_style='info', description='Add a New Beer', icon='check', style=ButtonStyle(), tooltip='Add a Ne…



```python

```
