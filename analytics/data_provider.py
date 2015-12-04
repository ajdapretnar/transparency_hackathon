#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import pickle

colors = ['blueviolet','brown','cadetblue','chocolate','cornflowerblue','crimson','darkblue','darkcyan','darkgreen','darkmagenta','darkolivegreen','darkorange','darkorchid','darkred','darkseagreen','darkslateblue','darkslategray','darkviolet','deeppink','deepskyblue','dimgray']
party_colors = {
    'smc': 'cadetblue',
    'sds': 'orange',
    'desus': 'darkgreen',
    'nepovezan': 'white',
    'sd': 'red',
    'nsi': 'blueviolet',
    'zl': 'crimson',
    'pnsp': 'darkslategray',
    'imns': 'darkseagreen',
}
stop_words = ["a",  "ali",  "april",  "avgust",  "b",  "bi",  "bil",  "bila",  "bile",  "bili",  "bilo",  "biti",  "blizu",  "bo",  "bodo",  "bojo",  "bolj",  "bom",  "bomo",  "boste",  "boš",  "bova",  "brez",  "c",  "cel",  "cela",  "celi",  "celo",  "č",  "če",  "često",  "četrta",  "četrtek",  "četrti",  "četrto",  "čez",  "čigav",  "d",  "da",  "daleč",  "dan",  "danes",  "datum",  "december",  "deset",  "deseta",  "deseti",  "deseto",  "devet",  "deveta",  "deveti",  "deveto",  "do",  "dober",  "dobra",  "dobri",  "dobro",  "dokler",  "dol",  "dolg",  "dolga",  "dolgi",  "dovolj",  "drug",  "druga",  "drugi",  "drugo",  "dva",  "dve",  "e",  "eden",  "en",  "ena",  "ene",  "eni",  "enkrat",  "eno",  "etc.",  "f",  "februar",  "g",  "g.",  "ga",  "ga.",  "gor",  "gospa",  "gospod",  "h",  "halo",  "i",  "idr.",  "ii",  "iii",  "in",  "iv",  "ix",  "iz",  "j",  "januar",  "jaz",  "je",  "ji",  "jih",  "jim",  "jo",  "julij",  "junij",  "jutri",  "k",  "kadarkoli",  "kaj",  "kajti",  "kako",  "kakor",  "kamor",  "kamorkoli",  "kar",  "karkoli",  "katerikoli",  "kdaj",  "kdo",  "kdorkoli",  "ker",  "ki",  "kje",  "kjer",  "kjerkoli",  "ko",  "koder",  "koderkoli",  "koga",  "komu",  "kot",  "kratek",  "kratka",  "kratke",  "kratki",  "l",  "lahka",  "lahke",  "lahki",  "lahko",  "le",  "lep",  "lepa",  "lepe",  "lepi",  "lepo",  "leto",  "m",  "maj",  "majhen",  "majhna",  "majhni",  "malce",  "malo",  "manj",  "marec",  "me",  "med",  "medtem",  "mene",  "mesec",  "me",  "mi",  "midva",  "midve",  "mnogo",  "moj",  "moja",  "moje",  "mora",  "morajo",  "moram",  "moramo",  "moraš",  "morate",  "morem",  "mu",  "n",  "na",  "nad",  "naj",  "najina",  "najino",  "najmanj",  "naju",  "največ",  "nam",  "narobe",  "nas",  "naš",  "naša",  "naše",  "nato",  "nazaj",  "ne",  "nedavno",  "nedelja",  "nek",  "neka",  "nekaj",  "nekatere",  "nekateri",  "nekatero",  "nekdo",  "neke",  "nekega",  "neki",  "nekje",  "neko",  "nekoč",  "nekoga",  "ni",  "nič",  "nikamor",  "nikdar",  "nikjer",  "nikoli",  "nje",  "njega",  "njegov",  "njegova",  "njegovo",  "njej",  "njemu",  "njen",  "njena",  "njeno",  "nji",  "njih",  "njihov",  "njihova",  "njihovo",  "njiju",  "njim",  "njo",  "njo",  "njun",  "njuna",  "njuno",  "no",  "nocoj",  "november",  "npr.",  "o",  "ob",  "oba",  "obe",  "oboje",  "od",  "odprt",  "odprta",  "odprti",  "okoli",  "oktober",  "on",  "onadva",  "one",  "oni",  "onidve",  "osem",  "osma",  "osmi",  "osmo",  "oz.",  "p",  "pa",  "pet",  "peta",  "petek",  "peti",  "peto",  "po",  "pod",  "pogosto",  "poleg",  "poln",  "polna",  "polni",  "polno",  "ponavadi",  "ponedeljek",  "ponovno",  "potem",  "povsod",  "pozdravljen",  "pozdravljeni",  "prav",  "prava",  "prave",  "pravi",  "pravo",  "prazen",  "prazna",  "prazno",  "prbl.",  "pribl.",  "precej",  "pred",  "prej",  "preko",  "pri",  "približno",  "primer",  "pripravljen",  "pripravljena",  "pripravljeni",  "proti",  "prva",  "prvi",  "prvo",  "r",  "ravno",  "reč",  "redko",  "res",  "s",  "saj",  "sam",  "sama",  "same",  "sami",  "samo",  "se",  "sebe",  "sebi",  "sedaj",  "sedem",  "sedma",  "sedmi",  "sedmo",  "sem",  "september",  "seveda",  "si",  "sicer",  "skoraj",  "skozi",  "slab",  "smo",  "so",  "sobota",  "spet",  "sreda",  "srednja",  "srednji",  "sta",  "ste",  "stran",  "stvar",  "sva",  "š",  "šest",  "šesta",  "šesti",  "šesto",  "štiri",  "t",  "ta",  "tak",  "taka",  "take",  "taki",  "tako",  "takoj",  "tam",  "te",  "tebe",  "tebi",  "tega",  "težak",  "težka",  "težki",  "težko",  "ti",  "tista",  "tiste",  "tisti",  "tisto",  "tj.",  "tja",  "to",  "toda",  "torek",  "tretja",  "tretje",  "tretji",  "tri",  "tu",  "tudi",  "tukaj",  "tvoj",  "tvoja",  "tvoje",  "u",  "v",  "vaju",  "vam",  "vas",  "vaš",  "vaša",  "vaše",  "včasih",  "včeraj",  "ve",  "več",  "vedno",  "velik",  "velika",  "veliki",  "veliko",  "vendar",  "ves",  "vi",  "vidva",  "vii",  "viii",  "visok",  "visoka",  "visoke",  "visoki",  "vsa",  "vsaj",  "vsak",  "vsake",  "vsaka",  "vsakdo",  "vsaki",  "vsakomur",  "vse",  "vsega",  "vsi",  "vso",  "x",  "z",  "za",  "zadaj",  "zadnji",  "zakaj",  "zaprta",  "zaprti",  "zaprto",  "zdaj",  "zelo",  "zunaj",  "ž",  "že"]
vocabulary = ['varnost', 'vojska', 'begunci', 'migranti']

def request_rep_votes_stats(name):
    r = requests.get('http://www.zakonodajni-monitor.si/api/poslanci/en/' + name)
    votes = r.json()['votes']
    stats = r.json()['stats']
    result = [int(x['vote']) for x in votes]
    return result, stats


def request_rep_quotes(name):
    result = ''
    r = requests.get('http://www.zakonodajni-monitor.si/api/izjave/avtor/en/' + name + '/true')
    quotes = r.json()
    for r in quotes['docs']:
        result += r['text'] + ' '
    return result


def request_rep_data():
    result = list()
    r = requests.get('http://www.zakonodajni-monitor.si/api/poslanci/vsi')
    reps = r.json()
    for r in reps:
        name = r['properties']['name']#.replace('Č', 'C').replace('Š', 'S').replace('Ž', 'Z').replace('Đ', 'DZ')
        print name
        party = r['properties']['party']
        votes, stats = request_rep_votes_stats(name)
        quotes = request_rep_quotes(name)
        result.append({
            'name': name,
            'party': party,
            'votes': votes,
            'present': stats['present'],
            'absent': stats['absent'],
            'total': stats['total'],
            'abstained': stats['abstained'],
            'yea': stats['yea'],
            'nay': stats['nay'],
            'quotes': quotes
        })
    with open('data/poslanci_podatki.dat', 'wb') as handle:
        pickle.dump(result, handle)
    return result


def load_rep_data():
    with open('data/poslanci_podatki.dat', 'rb') as handle:
        result = pickle.load(handle)
    return result


def get_all():
    request_rep_data()
    return


#get_all()
