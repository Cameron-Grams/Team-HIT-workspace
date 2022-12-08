import nltk
import re
import string
import contractions
import collections
from collections import defaultdict
from sklearn import metrics
from time import time

#--------------------------------

# from our SOP
def preprocess_text(text, flg_stemm = True, flg_lemm = True, lst_stopwords=None):
    text_clean = re.sub(r'[^\w\s.,]', '', str(text).strip())
    lst_text = text_clean.split()
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]
    if flg_stemm == True:
        stemm = nltk.stem.porter.PorterStemmer()
        lst_text = [stemm.stem(word) for word in lst_text]
    if flg_lemm == True:
        lem=nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]

    text_clean = ' '.join(filter(None, lst_text))
    text_clean = text_clean.replace(" ,",",").replace(' .', '.')
    text_clean = contractions.fix(text_clean)
    return text_clean

#------------------------------------
# from: https://scikit-learn.org/stable/auto_examples/text/plot_document_clustering.html#quantifying-the-quality-of-clustering-results


