## Helper file of all function, widgets and code to display Beer Advisor's
## Beer Recommender App 

import ipywidgets as widgets


### Standalone Widgets

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





import pandas as pd
import numpy as np
import re


    
    
    
    

### Functions 

def pandas_df_to_markdown_table(df):
    from IPython.display import Markdown, display
    fmt = ['---' for i in range(len(df.columns))]
    df_fmt = pd.DataFrame([fmt], columns=df.columns)
    df_formatted = pd.concat([df_fmt, df])
    display(Markdown(df_formatted.to_csv(sep="|", index=False)))





    




def show_beer_info(b):
    print('this some fucking info be here b')


