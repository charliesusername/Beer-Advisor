import pandas as pd
import numpy as np
import datetime as dt
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import plotly.plotly
init_notebook_mode(connected=True)
reviews = pd.read_csv('data/beer_ratings.csv').drop('Unnamed: 0',axis=1)

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
    super_user_fig = dict(data = review_counts_by_time, layout = layout)
    return plotly.offline.iplot(super_user_fig)