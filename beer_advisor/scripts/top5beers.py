from scripts.helper import clean_ratings
import pandas as pd
import numpy as np
import re

### Collaborative Filtering
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
    
    
    
    
