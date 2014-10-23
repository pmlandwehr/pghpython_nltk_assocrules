__author__ = 'pmlandwehr'

import nltk
import pandas as pd


data = pd.read_pickle('all_narrative_cleanup.csv')

print('total length %d' % data.shape[0])

tagged_narrative = data.apply(nltk.pos_tag)

pickle.dump(tagged_narrative, open('all_narrative_tagged.txt', 'wb'))