
'''
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
    
'''