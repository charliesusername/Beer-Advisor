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


### EDA Visualization ###
def poly_fit_line(x, y):
    z = np.polyfit(x, y, 3)
    f = np.poly1d(z)
    #f_text = ' + '.join(['{:0.3e}X^{}'.format(f[x],x) for x in range(len(f)+1)])
    return pd.DataFrame({'x_fit': np.linspace(x[0], x[-1], 50),'y_fit', f(x_fit)})#, f_text

### NLP functions ###
import re,  math, csv
import nltk, gensim, spacy
from nltk import FreqDist
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from gensim import corpora
def stemmer(text):
    ## takes a string and returns a PorterStemmed string
    text = re.sub('[^a-zA-Z]',' ',text).lower().split()    
    ps = PorterStemmer()
    text = [ps.stem(word) for word in text if not word in set(stopwords.words('english'))]
    text = ' '.join(text)
    return text

def make_corpus(cat):
    ## takes a dataframe and returns the corpus of stemmed text data
    l = len(cat.text)
    corpus = l*[None]
    rl = math.floor(l / 100.0) * 100    
    print("%complete: ",end="\t")
    for i in range(l):
        if i / rl % 0.25 == 0:
            out = int(i / rl * 100)
            print(out,end='\t')
        corpus[i] = stemmer(cat.text.iloc[i])
    return corpus

def textlist_to_csv(list_,name):
    ## takes a list of strings and writes to csv delimited by newlines
    fname = '../data/cleaned/' + name + '.csv'
    with open(fname, 'w', newline="\n") as f:
        wr = csv.writer(f,delimiter="\n")
        wr.writerow(list_)

def csv_to_textlist(name):
    result = []
    fname = '../data/cleaned/' + name + '.csv'
    with open(fname) as csvfile:
        spamreader = csv.reader(csvfile,delimiter='\n')
        for row in spamreader:
            result.append(', '.join(row))
    return result

def freq_words(x, terms = 30):
    all_words = ' '.join([text for text in x])
    all_words = all_words.split()
    
    fdist = FreqDist(all_words)
    words_df = pd.DataFrame({'word':list(fdist.keys()), 
                             'count':list(fdist.values())})
    # selecting top 20 most frequent words
    d = words_df.nlargest(columns='count', n=terms)
    plt.figure(figsize=(20,5))
    ax = sns.barplot(data=d, x="word", y="count")
    ax.set(ylabel='Count')
    plt.show()
    
def lemmatization(texts, tags=['NOUN', 'ADJ']): 
    # filter noun and adjective
    output = []
    for sent in texts:
        doc = nlp(" ".join(sent)) 
        output.append([token.lemma_ for token in doc 
                       if token.pos_ in tags])
        return output


### ML/LDA MODELLING ###
from sklearn.feature_extraction.text import CountVectorizer 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from gensim.models.ldamodel import LdaModel
from gensim.corpora.dictionary import Dictionary
from gensim.models.coherencemodel import CoherenceModel

def gen_doc_matrix(series):
    #nlp = spacy.load('en', disable=['parser', 'ner'])
    tokenized_reviews = pd.Series(series).apply(lambda x: x.split())
    reviews_2 = lemmatization(tokenized_reviews)    
    reviews_3 = []
    for i in range(len(reviews_2)):
        reviews_3.append(' '.join(reviews_2[i]))
    lza_revs['text'] = reviews_3
    freq_words(lza_revs.text, 20)
    dictionary = corpora.Dictionary(reviews_2)
    doc_term_matrix = [dictionary.doc2bow(rev) for rev in reviews_2]

def LDAmodel(dict_):
    # Creating the object for LDA model using gensim library
    LDA = gensim.models.ldamodel.LdaModel

    # Build LDA model
    lda_model = LDA(corpus=doc_term_matrix, id2word=dictionary, num_topics=7,
                   random_state=100, chunksize=1000, passes=50)

def compute_coherence_values(dictionary, corpus, texts, limit=40, start=2, step=6):
    """
    Compute c_v coherence for various number of topics

    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        print(num_topics)
        model=LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics)
        print(num_topics)
        model_list.append(model)
        print(num_topics)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        print(coherencemodel)
        coherence_values.append(coherencemodel.get_coherence())
        print(num_topics)

    return model_list, coherence_values


### Visualizations ###
import pyLDAvis
import pyLDAvis.gensim
#%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
