#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from data_provider import load_rep_data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(False)
ax.set_frame_on(False)


def graph_present():
    data = load_rep_data()
    df = pd.DataFrame(data)
    sub = df[['name', 'present', 'yea', 'nay', 'absent']].sort_values(by='yea', ascending=False)
    sns.barplot(x="yea", y="name", data=sub, label='small')
    plt.show()
    return


def graph_present_by_party():
    data = load_rep_data()
    df = pd.DataFrame(data)
    sub = df[['name', 'present', 'party', 'yea', 'nay']]
    group = sub.groupby(['party']).sum().sort_values(by='present', ascending=True)
    group.plot(kind='barh', ax=ax)
    plt.show()
    return


def show_votes():
    data = load_rep_data()
    mat = []
    labels = []
    for d in data:
        mat.append(d['votes'][:100])
        labels.append(d['name'])
    mat = np.array(mat)
    ax.matshow(mat, cmap=plt.cm.get_cmap('coolwarm'), aspect='auto')
    ax.set_yticklabels(['']+labels)
    plt.show()
    return


def plot_solidarity_index():
    data = load_rep_data()
    mat = []
    for d in data:
        mat.append(d['votes'])
    line = np.sum(mat, axis=0)
    plt.matshow(line)
    print line.shape
    plt.show()
    return


plot_solidarity_index()


