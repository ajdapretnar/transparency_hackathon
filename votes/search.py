
from __future__ import print_function
import pickle, requests
from EventRegistry import *
from calendar import monthrange


def get_rep_names():
    result = list()
    r = requests.get('http://integriteta.evennode.com/api/poslanci/vsi')
    reps = r.json()
    for r in reps:
        result.append(r['properties']['name'])
    return result


def get_law_names():
    result = list()
    r = requests.get('http://www.zakonodajni-monitor.si/api/zakoni/vsi')
    reps = r.json()
    for r in reps:
        result.append(r['sessions'][0]['title'])
    with open('data/laws.pickle', 'wb') as handle:
        pickle.dump(result, handle)
    return result


def load_law_names():
    with open('data/laws.pickle', 'rb') as handle:
        return pickle.load(handle)


er = EventRegistry(host="http://eventregistry.org", logging = True)
f = open('results_zakoni.txt', 'w')


def get_person_articles(name):
    result = []
    for year in range(2013, 2016):
        for month in xrange(1, 13, 2):
            print (year, month, month + 3, monthrange(year, month))
            if month < 10:
                q = QueryArticles()     # we want to make a search for articles
                q.setDateLimit(datetime.date(year, month, 1), datetime.date(year, month + 2, monthrange(year, month + 2)[1]))      # articles should be in particular date range
                q.addKeyword(name.lower())       # article should contain word apple
                q.addRequestedResult(RequestArticlesInfo(page=0, count=199, IncludeArticleLocation=True))  # get 30 articles that match the criteria
                res = er.execQuery(q)       # execute the query
                if 'articles' in res:
                    result.extend(res['articles']['results'])
    return result


def write_titles_to_file(name, res, f):
    f.write(name.encode('utf-8') + '\n')
    for r in res:
        if r['lang'] == 'slv':
            f.write(r['date'].encode('utf-8') + '\t' + r['title'].encode('utf-8') + '\n')
    f.write('----------------\n\n')
    return

laws = load_law_names()
for n in laws:
    print (n)
    articles = get_person_articles(n)
    write_titles_to_file(n, articles, f)

#q = get_person_articles('cerar miro')
#print (q, len(q))

f.close()
