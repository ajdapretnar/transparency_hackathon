import time, calendar, re, string, nltk
import lxml,urllib2
import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import pickle
import random
import datetime
from datetime import timedelta
import sys, traceback
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
import numpy as np


def get_rep_names():
    result = list()
    r = requests.get('http://integriteta.evennode.com/api/poslanci/vsi')
    reps = r.json()
    for r in reps:
        result.append(r['properties']['name'])
    return result


def get_rep_votes(name):
    r = requests.get('http://localhost:3000/api/poslanci/en/' + name)
    votes = r.json()['votes']
    result = [float(x['vote']) for x in votes]
    return result


def get_rep_data():
    names = get_rep_names()
    data = [get_rep_votes(name) for name in names]
    with open('data/rep_votes.pickle', 'wb') as handle:
        pickle.dump(data, handle)
    return data


def make_stat_array():
    with open('data/rep_votes.pickle', 'rb') as handle:
        values = pickle.load(handle)
    authnames = get_rep_names()
    result = np.array(values)
    print result
    return {'mat': result, 'users': authnames}


def do_tsne(input, draw):
    pca = PCA(n_components=2)
    mat = input['mat']
    labels = input['users']
    Y = pca.fit_transform(mat)
    model = TSNE(n_components=2, init='random', n_iter=50000, random_state=0, verbose=1, learning_rate=10)
    #Y = model.fit_transform(mat)
    if draw:
        print "drawing ..."
        x_list = [x for [x, y] in Y]
        y_list = [y for [x, y] in Y]
        fig = plt.figure()
        ax = fig.add_subplot(111)

        plt.plot(x_list, y_list, "ro")
        idx = 0
        for xy in zip(x_list, y_list):
            ax.annotate('%s' % labels[idx], xy=xy, textcoords='offset points')
            idx += 1
        plt.show()
    return Y


#print get_rep_votes('VILFAN PETER')

#get_rep_data()

vectors = make_stat_array()
do_tsne(vectors, True)