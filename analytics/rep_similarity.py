from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from data_provider import load_rep_data, colors, party_colors, stop_words, vocabulary
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from scipy.interpolate import interp1d
import numpy as np


def make_stat_array_votes():
    data = load_rep_data()
    votes = [x['votes'] for x in data]
    names = [x['name'] + ' (' + x['party'] + ')' for x in data]
    sizes = [x['present'] for x in data]
    parties = [x['party'] for x in data]
    result = np.array(votes)
    return {'mat': votes, 'names': names, 'sizes': sizes, 'parties': parties}


def text_to_vectors():
    data = load_rep_data()#[:40]
    names = [x['name'] + ' (' + x['party'] + ')' for x in data]
    quotes = [x['quotes'].lower() for x in data]
    sizes = [x['present'] for x in data]
    parties = [x['party'] for x in data]
    vectorizer = TfidfVectorizer\
        (min_df=25, stop_words=stop_words,
         strip_accents='unicode', lowercase=True, ngram_range=(1, 2),
         norm='l2', smooth_idf=True, sublinear_tf=False, use_idf=True,
         analyzer='word'
         )
    print 'vectorizing ...'
    X = vectorizer.fit_transform(quotes)
    D = -(X * X.T).todense()
    return {'mat': D, 'names': names, 'sizes': sizes, 'parties': parties}


def do_tsne(data_in, draw=True, do_pca=False, coloring='party'):
    pca = PCA(n_components=2)
    mat = data_in['mat']
    labels = data_in['names']
    sizes = data_in['sizes']
    parties = data_in['parties']
    min_size = min(sizes)
    max_size = max(sizes)
    m = interp1d([min_size, max_size], [7, 15])
    sizes = [int(m(x)) for x in sizes]
    kmeans_model = KMeans(n_clusters=10)
    if do_pca:
        Y = pca.fit_transform(mat)
    else:
        model = TSNE(n_components=2, init='random', n_iter=1000000,
                     random_state=0, verbose=1, learning_rate=20, perplexity=50)
        Y = model.fit_transform(mat)
    kmeans_model.fit(Y)
    if coloring != 'party':
        color_list = [colors[x] for x in kmeans_model.labels_]
    else:
        color_list = [party_colors[x.lower()] for x in parties]
    if draw:
        x_list = [x for [x, y] in Y]
        y_list = [y for [x, y] in Y]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.patch.set_facecolor('black')
        ax.grid(False)
        plt.plot(x_list, y_list, marker='o', markersize=1, linewidth=0, color='r')
        idx = 0
        for xy in zip(x_list, y_list):
            ax.text(xy[0], xy[1], labels[idx], color=color_list[idx], fontsize=sizes[idx]) #size_list[idx]
            idx += 1
        plt.show()
    return Y


#vectors = make_stat_array_votes()
vectors = text_to_vectors()
do_tsne(vectors, draw=True, do_pca=False, coloring='party')
