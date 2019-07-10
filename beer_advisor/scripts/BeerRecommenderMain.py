### Beer Recommender Sequence

from IPython.display import display, clear_output, HTML, Markdown, Latex
from ipywidgets import Layout, interact, interact_manual
import ipywidgets as widgets
import pandas as pd
import warnings


beers = pd.read_csv('data/beer_info.csv').drop('Unnamed: 0',axis=1)
breweries = beers.sort_values('brewery').brewery.unique()

user_prefs=pd.DataFrame({'beers':[],'rates':[]})


warnings.filterwarnings('ignore') 

def show_beer_info(b):
    print('this some fucking info be here b')

def remove_last_row(b):
    global user_prefs
    user_prefs.drop(user_prefs.tail(1).index,inplace=True)    

    clear_output()
    display(select_brewery)
    display(user_prefs)
    display(undo_last_beer_btn)   
    
def add_beer_to_list(b,r):
    global user_prefs       
    new_df = pd.DataFrame({'beers':[b],'rates':[r]},index=[b])
    user_prefs = user_prefs.append(new_df)
    user_prefs.drop_duplicates('beers',keep='last',inplace=True)
    


## Standalone Widgets

# Start Beer Selection Loop
begin_recommender_btn = widgets.Button(
    description='Begin Beer Recommender',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Begin Beer Recommender',
    icon='check'
)

# Select a brewery dropdown
select_brewery = widgets.Dropdown(
        options=breweries,
        value=breweries[0],
        description='Brewery:',
        disabled=False,
)

# Rate Slider for User Preference Selection
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

# Run Been Recommender Functions
gen_recs_btn = widgets.Button(
    description='Calculate Recommendations',
    disabled=False,
    button_style='info', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Calculate Recommendations',
    icon='check'
)

# Add currently selected beer to list
add_to_list = widgets.Button(
    description='Add Beer to List',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Add Beer to List',
    icon='check'
)

# Removes last added beer from list
undo_last_beer_btn = widgets.Button(
    description = 'Clear Last Beer',
    disabled=False,
    button_style='warning',
    tooltip='Remove the last rating from list',
    icon='check'
)

# Rate Slider for User Preference Selection
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

def beer_recommender(b):
    begin_recommender_btn.close()
    global user_prefs

    def get_brewery_selection(b):
        beer_list = beers[beers.brewery == select_brewery.value][['beer_id','beer_name']]
        beer_list = list(zip(beer_list.beer_name.values,beer_list.beer_id.values))
        select_beer = widgets.Dropdown(
            options=beer_list,
            value=beer_list[0][1],
            description='Select a Beer:',
            disabled=False,
        )
        display(select_beer, rate_slider, add_to_list)
        def go_to_add_beer_to_list(b):
            
            
            

            add_beer_to_list(select_beer.value,rate_slider.value)
            clear_output()

            display(select_brewery)
           
            display(user_prefs)
            display(undo_last_beer_btn)
            

        add_to_list.on_click(go_to_add_beer_to_list)

    

       
            


    display(select_brewery)
    display(user_prefs)
    select_brewery.observe(get_brewery_selection, names = 'value')
    undo_last_beer_btn.on_click(remove_last_row)








"""
### Main App Sequence

def add_beer(b):  
    
    #print(user_prefs)
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
            clear_output()
            display(new_beer_btn)
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

"""
### Generate Beer Recommender 

def run_generate(b):
    print('Finding Recommendations...')
    recommendations = generate_recommendations(user_prefs.beers.values,user_prefs.rates.values,beers,reviews)
    
    print('Recommendations Found!!!')
    display(recommendations)

### Collaborative Filtering for Beer Recommender App
from scipy.stats.stats import pearsonr


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