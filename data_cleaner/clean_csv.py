### Databasing ###
import pandas as pd
import numpy as np


### Cleaning Functions ###
import dateparser
from datetime import datetime
def clean_ratings(col):
    ''' Clean Ratings from reviews '''
    ''' if string characters appears, than user did not give a ratings breakdown. so clear the line. '''
    r = re.compile('characters')
    ratings = col
    ratings = ['' if r.search(rating) else rating for rating in ratings]
    r = re.compile('look|smell|taste|feel|overall|: ')
    ratings = [r.sub('',rating).split(' | ') for rating in ratings]
    ratings = [ra if ra == [''] else list(map(float, ra)) for ra in ratings]
    return ratings

def clean_dates(col):
    ### Clean posted date from reviews
    posted = col
    def parse_dates(text, origin):
        #Parses absolute and relative dates    
        try:
            date = datetime.strptime(text, '%b %d, %Y')
        except ValueError:
            date = dateparser.parse(text, settings={'RELATIVE_BASE': origin})
        return date
    scraping_date = dateparser.parse('Jul 3, 2019')
    post_cleaned = [parse_dates(post, scraping_date) for post in posted]
    return post_cleaned
