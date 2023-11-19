import random
import zeep
import pickle
import _pickle as cPickle
import bz2
import hazm
from termcolor import colored
import networkx as nx

wsdl = 'http://nlp.sbu.ac.ir:8180/WebAPI/services/SynsetService?WSDL'
client_syn = zeep.Client(wsdl=wsdl)

wsdl_sense='http://nlp.sbu.ac.ir:8180/WebAPI/services/SenseService?WSDL'
client_sense=zeep.Client(wsdl=wsdl_sense)


def getSenseById(key, id):
    sense=client_sense.service.getSenseById(key, id)
    return sense


def getSynsetGlosses(key, id):
    synset_gloss=client_syn.service.getSynsetGlosses(key, id)
    return synset_gloss


def getSenseBySynset(key,id):
    senses = client_sense.service.getSensesBySynset(key, id)
    return senses


def synse_rel_by_id(key, rel_id):
    synset_rel = client_syn.service.getSynsetRelationsById(key, rel_id)
    return synset_rel


def getSynsetRelationsById(key, id):
    syns=client_syn.service.getSynsetExamples(key, id)
    return syns

def getSynsetExampleById(key, id):
    syns=client_syn.service.getSynsetExamples(key, id)
    return syns

def getSynsetById(key,id):
    syn=client_syn.service.getSynsetById(key, id)
    return syn

def getSynsetsByWord(key, search_word):
    syn=client_syn.service.getSynsetsByWord(key, 'LIKE', search_word)
    return syn

# key='d3f74809-3b91-11eb-8a1e-080027d731c1'
# "d404702b-3b91-11eb-8a1e-080027d731c1"
# for id in range(1,10):
#     print(getSynsetGlosses(key, id))


def gloss_getter(data, id):
    candids=[]
    chosen=[]
    gloss=data[id]['gloss'].replace('.','').replace('،','').split()
    trigrams=[]
    bigrams=[]
    for i in range(len(gloss)):
        try:
            trigrams.append(gloss[i]+' '+gloss[i+1]+' '+gloss[i+2])
        except:
            pass
        try:
            bigrams.append(gloss[i]+' '+gloss[i+1])
        except:
            pass
    for tri in trigrams:
        n=word_search2(data,tri)
        tri_words = tri.split()
        if len(n)==1:
            candids.append(tri)
            for word in tri_words:
                chosen.append(word)
    for bi in bigrams:
        in_the_list=False
        n=word_search2(data,bi)
        bi_wrods=bi.split()
        for bword in bi_wrods:
            if bword in chosen:
                in_the_list=True
        if len(n)==1 and not in_the_list:
            candids.append(bi)
            for word in bi_wrods:
                chosen.append(word)
    for mono_word in gloss:
        n=word_search2(data,mono_word)
        if len(n)>=1 and len(mono_word)>2:
            if mono_word not in chosen:
                candids.append(mono_word)
                chosen.append(mono_word)
    print(trigrams)
    print(bigrams)
    print(candids)
    return candids


def word_search(data,word):
    candids=[]
    for id in data.keys():
        if word in data[id]['syn_search'].split(','):
            candids.append(id)
    if candids!=[]:
        return candids
    else:
        print('No full matches found, searching for partial matches...')
        alternatives=[]
        for id in  data.keys():
            if word in data[id]['syn_search']:
                if id not in alternatives:
                    alternatives.append(id)
        return alternatives


def word_search2(data,word):
    candids=[]
    for id in data.keys():
        if word in data[id]['syn_search'].split(','):
            candids.append(id)
    return candids


def stop_finder(data):
    counter_dict={}
    for id in data.keys():
        print(id)
        print(data[id]['normal_tag'])
        if data[id]['normal_tag']==[]:
            pass
        pool=[]
        chosen=[]
        for tag in data[id]['normal_tag']:
            if tag not in pool:
                pool.append(tag)

        # for syn in data[id]['syn_search'].split(','):
        #     for id in data.keys():
        #         if syn in data[id]['gloss']:
        #             for tag in data[id]['normal_tag']:
        #                 if tag not in pool:
        #                     pool.append(tag)
        print('done')
        _new = []
        for t in pool:
            if t not in chosen:
                chosen.append(t)
                n = word_search2(data, hazm.Lemmatizer().lemmatize(t[0]))
                print(n)
                if len(n) == 1:
                    # try:
                    for t in data[n[0]]['normal_tag']:
                        if t not in _new:
                            _new.append(t)
                else:
                    for n_id in n:
                        if len(data[n_id]['senses']) == 1:
                            for t in data[n_id]['normal_tag']:
                                if t not in _new:
                                    _new.append(t)
        for gg in _new:
            if gg not in pool:
                pool.append(gg)
        #
        # _new = []
        # for t in pool:
        #     if t not in chosen:
        #         chosen.append(t)
        #         n = word_search2(data, hazm.Lemmatizer().lemmatize(t[0]))
        #         print(n)
        #         if len(n) == 1:
        #             # try:
        #             for t in data[n[0]]['normal_tag']:
        #                 if t not in _new:
        #                     _new.append(t)
        #         else:
        #             for n_id in n:
        #                 if len(data[n_id]['senses']) == 1:
        #                     for t in data[n_id]['normal_tag']:
        #                         if t not in _new:
        #                             _new.append(t)
        # for gg in _new:
        #     if gg not in pool:
        #         pool.append(gg)

        for p in pool:
            try:
                counter_dict[p]+=1
            except KeyError:
                counter_dict[p]=1
        print(counter_dict)
    return counter_dict


def path_finder(data, stops, word1, word2):
    pool1 = []
    pool2 = []
    n1 = word_search(data, word1)
    n2 = word_search(data, word2)
    print('First words:')
    for i in range(len(n1)):
        print(str(i + 1) + ' : ' + data[n1[i]]['syn_search'] + ' == ' + ' ' + data[n1[i]]['gloss'])
    index1 = input(colored('Please Enter Your 1st Choice:', 'red'))
    index1 = int(index1) - 1
    print(data[n1[index1]]['normal_tag'])

    print('\n')
    for i in range(len(n2)):
        print(str(i + 1) + ' : ' + data[n2[i]]['syn_search'] + ' == ' + ' ' + data[n2[i]]['gloss'])
    index2 = input(colored('Please Enter Your 2nd Choice:', 'red'))
    index2 = int(index2) - 1
    print(data[n2[index2]]['normal_tag'])


    for tag in data[n1[index1]]['normal_tag']:
        if tag[0] not in stops:
            pool1.append(tag)
    for syn in data[n1[index1]]['syn_search'].split(','):
        for id in data.keys():
            if syn in data[id]['gloss']:
                for tag in data[id]['normal_tag']:
                    if tag not in pool1 and tag[0] not in stops:
                        pool1.append(tag)




    for tag in data[n2[index2]]['normal_tag']:
        if tag[0] not in stops:
            pool2.append(tag)
    for syn in data[n2[index2]]['syn_search'].split(','):
        for id in data.keys():
            if syn in data[id]['gloss']:
                for tag in data[id]['normal_tag']:
                    if tag not in pool2 and tag[0] not in stops:
                        pool2.append(tag)


    shared = list(set(pool1).intersection(pool2))



    print(shared)
    print(len(pool1))
    print(len(pool2))
    print(len(shared))
    return n1[index1], n2[index2], pool1, pool2, shared

    # for j in range(t):
    #     _new=[]
    #     n1 = word_search2(data, hazm.Normalizer().normalize(pool1[j][0]))
    #     n2 = word_search2(data, hazm.Normalizer().normalize(pool2[j][0]))
    #     if len(n1)==1:
    #     # try:
    #         for t in data[n1[0]]['normal_tag']:
    #             if t[1]=='N':
    #                 _new.append(t)
    #         else:
    #             for n_id in n1:
    #                 if len(data[n_id]['senses'])==1:
    #                     for t in data[n_id]['normal_tag']:
    #                         if t[1] == 'N':
    #                             _new.append(t)
    #     print(counter)
    #     _new = []
    #
    #     for tag in pool1:
    #         print(len(pool1))
    #         n=word_search2(data,hazm.Normalizer().normalize(tag[0]))
    #         if len(n)==1:
    #         # try:
    #             for t in data[n[0]]['normal_tag']:
    #                 if t[1]=='N':
    #                     _new.append(t)
    #         else:
    #             for n_id in n:
    #                 if len(data[n_id]['senses'])==1:
    #                     for t in data[n_id]['normal_tag']:
    #                         if t[1] == 'N':
    #                             _new.append(t)
    #         # except:
    #         #     pass
    #     for t in _new:
    #         if t not in pool1:
    #             pool1.append(t)
    #
    #     _new = []
    #
    #     for tag in pool2:
    #         n=word_search2(data,hazm.Normalizer().normalize(tag[0]))
    #         if len(n)==1:
    #         # try:
    #             for t in data[n[0]]['normal_tag']:
    #                 if t[1] == 'N':
    #                     _new.append(t)
    #         else:
    #             for n_id in n:
    #                 if len(data[n_id]['senses']) == 1:
    #                     for t in data[n_id]['normal_tag']:
    #                         if t[1] == 'N':
    #                             _new.append(t)
    #         # except:
    #         #     pass
    #     for t in _new:
    #         if t not in pool2:
    #             pool2.append(t)
    #     counter+=1
    #     shared = list(set(pool1).intersection(pool2))
    #
    # print(len(pool1)+len(pool2))
    # print(shared)
    #
    #


def path_finder2(data, stops, graph, word1):
    pool1 = []
    pool2 = []
    neigh1=[]
    neigh2=[]
    my_list = list(data.keys())
    word2=int()
    while word2!=word1:
        word2=random.choice(my_list)



    for rel in data[word1]['relations']:
        if rel['synsetId2']!=word1:
            neigh1.append(rel['synsetId2'])
            pool1.append(rel['synsetId2'])
    for rel in data[word2]['relations']:
        if rel['synsetId2']!=word2:
            pool2.append(rel['synsetId2'])
            neigh2.append(rel['synsetId2'])


    for syn in data[word1]['syn_search'].split(','):
        i = 0
        while len(pool1) < 600:
            if syn in data[my_list[i]]['gloss']:
                if my_list[i] not in pool1:
                    pool1.append(my_list[i])

            i += 1
            if i == len(my_list) - 1:
                break

    for syn in data[word2]['syn_search'].split(','):
        i = 0
        while len(pool2) < 600:
            if syn in data[my_list[i]]['gloss']:
                if my_list[i] not in pool2:
                    pool2.append(my_list[i])

            i += 1
            if i == len(my_list) - 1:
                break

    if len(pool1) < 700:
        for tag in data[word1]['normal_tag']:
            n = word_search2(data, tag[0])
            if len(n) == 1:
                for syn in data[n[0]]['syn_search'].split(','):
                    for id in data.keys():
                        if syn in data[id]['gloss']:
                            if id not in pool1:
                                pool1.append(id)
        for id in neigh1:
            for tag in data[id]['normal_tag']:
                n = word_search2(data, tag[0])
                if len(n) == 1:
                    for syn in data[n[0]]['syn_search'].split(','):
                        for id in data.keys():
                            if syn in data[id]['gloss']:
                                if id not in pool1:
                                    pool1.append(id)

    if len(pool2) < 700:
        for tag in data[word2]['normal_tag']:
            n = word_search2(data, tag[0])
            if len(n) == 1:
                for syn in data[n[0]]['syn_search'].split(','):
                    for id in data.keys():
                        if syn in data[id]['gloss']:
                            if id not in pool2:
                                pool2.append(id)
        for id in neigh2:
            for tag in data[id]['normal_tag']:
                n = word_search2(data, tag[0])
                if len(n) == 1:
                    for syn in data[n[0]]['syn_search'].split(','):
                        for id in data.keys():
                            if syn in data[id]['gloss']:
                                if id not in pool2:
                                    pool2.append(id)


    shared = list(set(pool1).intersection(pool2))

    if len(shared) < 150:
        shortest = nx.shortest_path(graph, word1, word2)
        cutoff = len(shortest) - 1
        paths = list(nx.all_simple_paths(graph, word1, word2, cutoff=cutoff))
        for path in paths:
            for id in path:
                if id not in shared and id != word1 and id != word2:
                    shared.append(id)


    return word1, word2, pool1, pool2, shared

import numpy as np
import operator

def cosine(u,v):
    return np.dot(u,v)/(np.linalg.norm(u)*np.linalg.norm(v))
# #
def bechin(index1,index2,shared,encodings):
    chart={}
    for id in shared:
        chart[id]=abs(cosine(encodings[id],encodings[index1])-cosine(encodings[id],encodings[index2]))
    sorted_d = dict(sorted(chart.items(), key=operator.itemgetter(1), reverse=True))
    return sorted_d

# rels_raw=[]
# n=23
# for id in range(1,62000):
#     new_rels=synse_rel_by_id(keys[n], id)
#     print(id)
#     if new_rels==[]:
#         print('empty')
#         continue
#     elif new_rels[0]['id'] is not None:
#         rels_raw.append(new_rels)
#     elif new_rels[0]['id'] is None:
#         n+=1
#         print(n)
#         new_rels = synse_rel_by_id(keys[n], id)
#         rels_raw.append(new_rels)
#     if id%1111==0 or id%1112==0 or id%1113==0:
#         with open('save_{}'.format(id), 'wb') as checkp:
#             pickle.dump(rels_raw, checkp)
#             print('file saved {}'.format(id))
#             checkp.close()
#
#
#
#
# with open('raw_rels_fn3_complete', 'wb') as gold:
#     pickle.dump(rels_raw, gold)
#     gold.close()


# def get_synset_relation(word, key):
#     synsets = client.service.getSynsetsByWord(key,'EXACT',word)
#     synset_ids = [synset['id'] for synset in synsets]
#     for idx, synset_id in enumerate(synset_ids):
#         response = client.service.getSynsetGlosses(key,synset_id)
#         synsets[idx]['synsetglosses'] = response
#     return synsets
def bechin(index1,index2,shared,encodings):
    chart={}
    for id in shared:
        chart[id]=abs(cosine(encodings[id],encodings[index1])-cosine(encodings[id],encodings[index2]))
    sorted_d = dict(sorted(chart.items(), key=operator.itemgetter(1), reverse=True))

    print(sorted_d)
    return sorted_d

def _sort_euclidean(index1,index2,shared,encodings,data):
    chart={'index1':{},'index2':{}}
    for ids in shared:
        chart['index1'][data[ids]['syn_search']]=np.linalg.norm(encodings[ids]-encodings[index1])
        chart['index2'][data[ids]['syn_search']]=np.linalg.norm(encodings[ids]-encodings[index2])
    chart['index1']=dict(sorted(chart['index1'].items(), key=operator.itemgetter(1),reverse=True))
    chart['index2']=dict(sorted(chart['index2'].items(), key=operator.itemgetter(1),reverse=True))
    print(chart['index1'])
    print(chart['index2'])
    print(data[index1]['syn_search'])
    print(data[index2]['syn_search'])

    return chart


def daste_kon2(index1, index2, sorted_d, encodings, graph, data):
    all_seeds = {}
    for i in range(19):
        all_seeds[i]=[]






def daste_kon(index1,index2,sorted_d,encodings,graph,data):
    all_seeds={}

    for i in range(19):
        all_seeds[i]=[]

    all_seeds[0].append(index1)
    all_seeds[18].append(index2)
    chosen=[]
    chosen.append(index2)
    chosen.append(index1)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[1])<2:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[1].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[17])<2:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[17].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[1])==2 and len(all_seeds[17])==2:
                break

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[2])<3:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[2].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[16])<3:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[16].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[2])==3 and len(all_seeds[16])==3:
                all_seeds[16]=swapPositions(all_seeds[16], 0,  1)
                all_seeds[2]=swapPositions(all_seeds[2], 0,  1)
                break

    cos1=cosine(encodings[all_seeds[16][0]],encodings[all_seeds[17][0]])
    cos2=cosine(encodings[all_seeds[16][0]],encodings[all_seeds[17][-1]])

    cos3=cosine(encodings[all_seeds[16][-1]],encodings[all_seeds[17][0]])
    cos4=cosine(encodings[all_seeds[16][-1]],encodings[all_seeds[17][-1]])

    if cos1<cos2 and cos3>cos4:
        all_seeds[16] = swapPositions(all_seeds[16], 0, -1)

    cos1 = cosine(encodings[all_seeds[2][0]], encodings[all_seeds[1][0]])
    cos2 = cosine(encodings[all_seeds[2][0]], encodings[all_seeds[1][-1]])

    cos3 = cosine(encodings[all_seeds[2][-1]], encodings[all_seeds[1][0]])
    cos4 = cosine(encodings[all_seeds[2][-1]], encodings[all_seeds[1][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[2] = swapPositions(all_seeds[2], 0, -1)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[3])<4:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[3].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[15])<4:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[15].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[3])==4 and len(all_seeds[15])==4:
                all_seeds[3]=swapPositions(all_seeds[3],0,2)
                all_seeds[15]=swapPositions(all_seeds[15],0,2)
                break

    cos1=cosine(encodings[all_seeds[15][0]],encodings[all_seeds[16][0]])
    cos2=cosine(encodings[all_seeds[15][0]],encodings[all_seeds[16][-1]])

    cos3=cosine(encodings[all_seeds[15][-1]],encodings[all_seeds[16][0]])
    cos4=cosine(encodings[all_seeds[15][-1]],encodings[all_seeds[16][-1]])

    if cos1<cos2 and cos3>cos4:
        all_seeds[15]=swapPositions(all_seeds[15],0,-1)

    cos1 = cosine(encodings[all_seeds[3][0]], encodings[all_seeds[2][0]])
    cos2 = cosine(encodings[all_seeds[3][0]], encodings[all_seeds[2][-1]])

    cos3 = cosine(encodings[all_seeds[3][-1]], encodings[all_seeds[2][0]])
    cos4 = cosine(encodings[all_seeds[3][-1]], encodings[all_seeds[2][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[3] = swapPositions(all_seeds[3], 0, -1)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[4])<5:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[4].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[14])<5:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[14].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[4])==5 and len(all_seeds[14])==5:
                all_seeds[4]=swapPositions(all_seeds[4],0,2)
                all_seeds[14] = swapPositions(all_seeds[14], 0, 2)
                break

    cos1 = cosine(encodings[all_seeds[14][0]], encodings[all_seeds[15][0]])
    cos2 = cosine(encodings[all_seeds[14][0]], encodings[all_seeds[15][-1]])

    cos3 = cosine(encodings[all_seeds[14][-1]], encodings[all_seeds[15][0]])
    cos4 = cosine(encodings[all_seeds[14][-1]], encodings[all_seeds[15][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[14] = swapPositions(all_seeds[14], 0, -1)

    cos1 = cosine(encodings[all_seeds[4][0]], encodings[all_seeds[3][0]])
    cos2 = cosine(encodings[all_seeds[4][0]], encodings[all_seeds[3][-1]])

    cos3 = cosine(encodings[all_seeds[4][-1]], encodings[all_seeds[3][0]])
    cos4 = cosine(encodings[all_seeds[4][-1]], encodings[all_seeds[3][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[4] = swapPositions(all_seeds[4], 0, -1)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[5]) < 6:
                if cosine(encodings[_ids], encodings[index1]) > cosine(encodings[_ids], encodings[index2]):
                    all_seeds[5].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[13]) < 6:
                if cosine(encodings[_ids], encodings[index2]) > cosine(encodings[_ids], encodings[index1]):
                    all_seeds[13].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[5]) == 6 and len(all_seeds[13]) == 6:
                all_seeds[5] = swapPositions(all_seeds[5], 0, 2)
                all_seeds[5] = swapPositions(all_seeds[5], 1, 3)
                all_seeds[13] = swapPositions(all_seeds[13], 0, 2)
                all_seeds[13] = swapPositions(all_seeds[13], 1, 3)
                break

    cos1 = cosine(encodings[all_seeds[13][0]], encodings[all_seeds[14][0]])
    cos2 = cosine(encodings[all_seeds[13][0]], encodings[all_seeds[14][-1]])

    cos3 = cosine(encodings[all_seeds[13][-1]], encodings[all_seeds[14][0]])
    cos4 = cosine(encodings[all_seeds[13][-1]], encodings[all_seeds[14][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[13] = swapPositions(all_seeds[13], 0, -1)

    cos1 = cosine(encodings[all_seeds[5][0]], encodings[all_seeds[4][0]])
    cos2 = cosine(encodings[all_seeds[5][0]], encodings[all_seeds[4][-1]])

    cos3 = cosine(encodings[all_seeds[5][-1]], encodings[all_seeds[4][0]])
    cos4 = cosine(encodings[all_seeds[5][-1]], encodings[all_seeds[4][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[5] = swapPositions(all_seeds[5], 0, -1)

    cos1 = cosine(encodings[all_seeds[13][1]], encodings[all_seeds[14][1]])
    cos2 = cosine(encodings[all_seeds[13][1]], encodings[all_seeds[14][-2]])

    cos3 = cosine(encodings[all_seeds[13][-2]], encodings[all_seeds[14][1]])
    cos4 = cosine(encodings[all_seeds[13][-2]], encodings[all_seeds[14][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[13] = swapPositions(all_seeds[13], 1, -2)

    cos1 = cosine(encodings[all_seeds[5][1]], encodings[all_seeds[4][1]])
    cos2 = cosine(encodings[all_seeds[5][1]], encodings[all_seeds[4][-2]])

    cos3 = cosine(encodings[all_seeds[5][-2]], encodings[all_seeds[4][1]])
    cos4 = cosine(encodings[all_seeds[5][-2]], encodings[all_seeds[4][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[5] = swapPositions(all_seeds[5], 1, -2)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[6])<7:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[6].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[12])<7:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[12].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[6])==7 and len(all_seeds[12])==7:
                all_seeds[6]=swapPositions(all_seeds[6],0,3)
                all_seeds[6]=swapPositions(all_seeds[6],1,4)
                all_seeds[12]=swapPositions(all_seeds[12],0,3)
                all_seeds[12]=swapPositions(all_seeds[12],1,4)
                break

    cos1 = cosine(encodings[all_seeds[12][0]], encodings[all_seeds[13][0]])
    cos2 = cosine(encodings[all_seeds[12][0]], encodings[all_seeds[13][-1]])

    cos3 = cosine(encodings[all_seeds[12][-1]], encodings[all_seeds[13][0]])
    cos4 = cosine(encodings[all_seeds[12][-1]], encodings[all_seeds[13][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[12] = swapPositions(all_seeds[12], 0, -1)

    cos1 = cosine(encodings[all_seeds[6][0]], encodings[all_seeds[5][0]])
    cos2 = cosine(encodings[all_seeds[6][0]], encodings[all_seeds[5][-1]])

    cos3 = cosine(encodings[all_seeds[6][-1]], encodings[all_seeds[5][0]])
    cos4 = cosine(encodings[all_seeds[6][-1]], encodings[all_seeds[5][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[6] = swapPositions(all_seeds[6], 0, -1)

    cos1 = cosine(encodings[all_seeds[12][1]], encodings[all_seeds[13][1]])
    cos2 = cosine(encodings[all_seeds[12][1]], encodings[all_seeds[13][-2]])

    cos3 = cosine(encodings[all_seeds[12][-2]], encodings[all_seeds[13][1]])
    cos4 = cosine(encodings[all_seeds[12][-2]], encodings[all_seeds[13][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[12] = swapPositions(all_seeds[12], 1, -2)

    cos1 = cosine(encodings[all_seeds[6][1]], encodings[all_seeds[5][1]])
    cos2 = cosine(encodings[all_seeds[6][1]], encodings[all_seeds[5][-2]])

    cos3 = cosine(encodings[all_seeds[6][-2]], encodings[all_seeds[5][1]])
    cos4 = cosine(encodings[all_seeds[6][-2]], encodings[all_seeds[5][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[6] = swapPositions(all_seeds[6], 1, -2)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[7])<8:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[7].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[11])<8:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[11].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[7])==8 and len(all_seeds[11])==8:
                all_seeds[7]=swapPositions(all_seeds[7],0,3)
                all_seeds[7]=swapPositions(all_seeds[7],1,4)
                all_seeds[11]=swapPositions(all_seeds[11],0,3)
                all_seeds[11]=swapPositions(all_seeds[11],1,4)
                break

    cos1 = cosine(encodings[all_seeds[11][0]], encodings[all_seeds[12][0]])
    cos2 = cosine(encodings[all_seeds[11][0]], encodings[all_seeds[12][-1]])

    cos3 = cosine(encodings[all_seeds[11][-1]], encodings[all_seeds[12][0]])
    cos4 = cosine(encodings[all_seeds[11][-1]], encodings[all_seeds[12][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[11] = swapPositions(all_seeds[11], 0, -1)

    cos1 = cosine(encodings[all_seeds[7][0]], encodings[all_seeds[6][0]])
    cos2 = cosine(encodings[all_seeds[7][0]], encodings[all_seeds[6][-1]])

    cos3 = cosine(encodings[all_seeds[7][-1]], encodings[all_seeds[6][0]])
    cos4 = cosine(encodings[all_seeds[7][-1]], encodings[all_seeds[6][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[7] = swapPositions(all_seeds[7], 0, -1)

    cos1 = cosine(encodings[all_seeds[11][1]], encodings[all_seeds[12][1]])
    cos2 = cosine(encodings[all_seeds[11][1]], encodings[all_seeds[12][-2]])

    cos3 = cosine(encodings[all_seeds[11][-2]], encodings[all_seeds[12][1]])
    cos4 = cosine(encodings[all_seeds[11][-2]], encodings[all_seeds[12][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[11] = swapPositions(all_seeds[11], 1, -2)

    cos1 = cosine(encodings[all_seeds[7][1]], encodings[all_seeds[6][1]])
    cos2 = cosine(encodings[all_seeds[7][1]], encodings[all_seeds[6][-2]])

    cos3 = cosine(encodings[all_seeds[7][-2]], encodings[all_seeds[6][1]])
    cos4 = cosine(encodings[all_seeds[7][-2]], encodings[all_seeds[6][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[7] = swapPositions(all_seeds[7], 1, -2)

    for _ids in sorted_d.keys():
        if _ids not in chosen:
            if len(all_seeds[8])<9:
                if cosine(encodings[_ids],encodings[index1])>cosine(encodings[_ids],encodings[index2]):
                    all_seeds[8].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[10])<9:
                if cosine(encodings[_ids],encodings[index2])>cosine(encodings[_ids],encodings[index1]):
                    all_seeds[10].append(_ids)
                    chosen.append(_ids)
            if len(all_seeds[8])==9 and len(all_seeds[10])==9:
                all_seeds[8]=swapPositions(all_seeds[8],0,4)
                all_seeds[8]=swapPositions(all_seeds[8],1,5)
                all_seeds[8]=swapPositions(all_seeds[8],2,3)

                all_seeds[10]=swapPositions(all_seeds[10],0,4)
                all_seeds[10]=swapPositions(all_seeds[10],1,5)
                all_seeds[10]=swapPositions(all_seeds[10],2,3)
                break

    cos1 = cosine(encodings[all_seeds[10][0]], encodings[all_seeds[11][0]])
    cos2 = cosine(encodings[all_seeds[10][0]], encodings[all_seeds[11][-1]])

    cos3 = cosine(encodings[all_seeds[10][-1]], encodings[all_seeds[11][0]])
    cos4 = cosine(encodings[all_seeds[10][-1]], encodings[all_seeds[11][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[10] = swapPositions(all_seeds[10], 0, -1)

    cos1 = cosine(encodings[all_seeds[8][0]], encodings[all_seeds[7][0]])
    cos2 = cosine(encodings[all_seeds[8][0]], encodings[all_seeds[7][-1]])

    cos3 = cosine(encodings[all_seeds[8][-1]], encodings[all_seeds[7][0]])
    cos4 = cosine(encodings[all_seeds[8][-1]], encodings[all_seeds[7][-1]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[8] = swapPositions(all_seeds[8], 0, -1)

    cos1 = cosine(encodings[all_seeds[10][1]], encodings[all_seeds[11][1]])
    cos2 = cosine(encodings[all_seeds[10][1]], encodings[all_seeds[11][-2]])

    cos3 = cosine(encodings[all_seeds[10][-2]], encodings[all_seeds[11][1]])
    cos4 = cosine(encodings[all_seeds[10][-2]], encodings[all_seeds[11][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[10] = swapPositions(all_seeds[10], 1, -2)

    cos1 = cosine(encodings[all_seeds[8][1]], encodings[all_seeds[7][1]])
    cos2 = cosine(encodings[all_seeds[8][1]], encodings[all_seeds[7][-2]])

    cos3 = cosine(encodings[all_seeds[8][-2]], encodings[all_seeds[7][1]])
    cos4 = cosine(encodings[all_seeds[8][-2]], encodings[all_seeds[7][-2]])

    if cos1 < cos2 and cos3 > cos4:
        all_seeds[8] = swapPositions(all_seeds[8], 1, -2)

    for _ids in reversed(list(sorted_d.keys())):
        if _ids not in chosen:
            if len(all_seeds[9])<10 and cosine(encodings[_ids],encodings[index2])>.6:
                all_seeds[9].append(_ids)
                chosen.append(_ids)
            if len(all_seeds[9])==10:
                break

    if len(all_seeds[9]) < 10:
        for _ids in reversed(list(sorted_d.keys())):
            if _ids not in chosen:
                if len(all_seeds[9]) < 10:
                    all_seeds[9].append(_ids)
                    chosen.append(_ids)
                if len(all_seeds[9]) == 10:
                    break

    for i in range(len(all_seeds[9])):
        if i!=4 and i!=5:
            if cosine(encodings[index1],encodings[all_seeds[9][i]])>cosine(encodings[index1],encodings[all_seeds[9][5]]):
                all_seeds[9]=swapPositions(all_seeds[9],i,5)
    for i in range(len(all_seeds[9])):
        if i != 4 and i != 5:
            if cosine(encodings[index1], encodings[all_seeds[9][i]]) > cosine(encodings[index1], encodings[all_seeds[9][4]]):
                all_seeds[9] = swapPositions(all_seeds[9], i, 4)

    sum_cosine1=cosine(encodings[all_seeds[9][-1]],encodings[all_seeds[8][-1]])+cosine(encodings[all_seeds[9][-1]],encodings[all_seeds[10][-1]])
    sum_cosine2=cosine(encodings[all_seeds[9][-1]],encodings[all_seeds[8][0]])+cosine(encodings[all_seeds[9][-1]],encodings[all_seeds[10][0]])

    sum_cosine3=cosine(encodings[all_seeds[9][0]],encodings[all_seeds[8][0]])+cosine(encodings[all_seeds[9][0]],encodings[all_seeds[10][0]])
    sum_cosine4=cosine(encodings[all_seeds[9][0]],encodings[all_seeds[8][-1]])+cosine(encodings[all_seeds[9][0]],encodings[all_seeds[10][-1]])

    if sum_cosine1<sum_cosine2 and sum_cosine3<sum_cosine4:
        all_seeds[9]=swapPositions(all_seeds[9],0,-1)

    sum_cosine1 = cosine(encodings[all_seeds[9][-2]], encodings[all_seeds[8][-2]]) + cosine(encodings[all_seeds[9][-2]],
                                                                                        encodings[all_seeds[10][-2]])
    sum_cosine2 = cosine(encodings[all_seeds[9][-2]], encodings[all_seeds[8][1]]) + cosine(encodings[all_seeds[9][-2]],
                                                                                           encodings[all_seeds[10][1]])

    sum_cosine3 = cosine(encodings[all_seeds[9][1]], encodings[all_seeds[8][1]]) + cosine(encodings[all_seeds[9][1]],
                                                                                          encodings[all_seeds[10][1]])
    sum_cosine4 = cosine(encodings[all_seeds[9][1]], encodings[all_seeds[8][-2]]) + cosine(encodings[all_seeds[9][1]],
                                                                                       encodings[all_seeds[10][-2]])
    if sum_cosine1<sum_cosine2 and sum_cosine3<sum_cosine4:
        all_seeds[9]=swapPositions(all_seeds[9],1,-2)

    for j in all_seeds.keys():
        print(len(all_seeds[j]))
###########
    #################
        ###################
 #   FINALLLLLL
### yadet nare bayad line vasati ro bechini

    return all_seeds


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def path_finder3(data, graph, word1,word2,encodings):
    pool1 = []
    pool2 = []
    neigh1=[]
    neigh2=[]
    print(word1)
    my_list = list(data.keys())

    for rel in data[word1]['relations']:
        if rel['synsetId2'] != word1 and rel['type']!='Related-to':
            neigh1.append(rel['synsetId2'])
            pool1.append(rel['synsetId2'])
    for rel in data[word2]['relations']:
        if rel['synsetId2'] != word2 and rel['type']!='Related-to':
            pool2.append(rel['synsetId2'])
            neigh2.append(rel['synsetId2'])

    for syn in data[word1]['syn_search'].split(','):
        for id in data.keys():
            if syn in data[id]['gloss']:
                if id not in pool1:
                    pool1.append(id)

    for syn in data[word2]['syn_search'].split(','):
        for id in data.keys():
            if syn in data[id]['gloss']:
                if id not in pool2:
                    pool2.append(id)

    print('pool1: ' + str(len(pool1)))
    print('pool2: ' + str(len(pool2)))


    for id in neigh1:
        for syn in data[id]['syn_search'].split(','):
            for id in data.keys():
                if syn in data[id]['gloss']:
                    if id not in pool1:
                        pool1.append(id)

    for id in neigh2:
        for syn in data[id]['syn_search'].split(','):
            for id in data.keys():
                if syn in data[id]['gloss']:
                    if id not in pool2:
                        pool2.append(id)

    for syn in data[word1]['syn_search'].split(','):
        i = 0
        if syn in data[my_list[i]]['gloss']:
            if my_list[i] not in pool1 and np.linalg.norm(encodings[my_list[i]]-encodings[word1])<23:
                pool1.append(my_list[i])
        i += 1
        if i == len(my_list) - 1:
            break

    for syn in data[word2]['syn_search'].split(','):
        i = 0
        if syn in data[my_list[i]]['gloss'] and np.linalg.norm(encodings[my_list[i]]-encodings[word2])<23:
            if my_list[i] not in pool2:
                pool2.append(my_list[i])
            i += 1
            if i == len(my_list) - 1:
                break

    print('pool1: ' + str(len(pool1)))
    print('pool2: ' + str(len(pool2)))


    for tag in data[word1]['normal_tag']:
        n = word_search2(data, tag[0])
        if len(n) == 1:
            pool1.append(n[0])
        elif len(n)>1:
            min_index=0
            min_fasele=30
            for id_result in n:
                _x=np.linalg.norm(encodings[id_result]-encodings[word1])
                if _x<min_fasele:
                    min_index=id_result
                    min_fasele=_x
            if min_index!=0:
                pool1.append(min_index)

    for tag in data[word2]['normal_tag']:
        n = word_search2(data, tag[0])
        if len(n) == 1:
            pool2.append(n[0])
        elif len(n)>1:
            min_index = 0
            min_fasele = 30
            for id_result in n:
                _x = np.linalg.norm(encodings[id_result] - encodings[word2])
                if _x < min_fasele:
                    min_index = id_result
                    min_fasele = _x
            if min_index != 0:
                pool2.append(min_index)

    print('pool1: ' + str(len(pool1)))
    print('pool2: ' + str(len(pool2)))


    for id in neigh1:
        for tag in data[id]['normal_tag']:
            n = word_search2(data, tag[0])
            if len(n) == 1:
                pool1.append(n[0])
            elif len(n)>1:
                min_index = 0
                min_fasele = 30
                for id_result in n:
                    _x = np.linalg.norm(encodings[id_result] - encodings[word1])
                    if _x < min_fasele:
                        min_index = id_result
                        min_fasele = _x
                if min_index != 0:
                    pool1.append(min_index)


    for id in neigh2:
        for tag in data[id]['normal_tag']:
            n = word_search2(data, tag[0])
            if len(n) == 1:
                pool2.append(n[0])
            elif len(n) > 1:
                min_index = 0
                min_fasele = 30
                for id_result in n:
                    _x = np.linalg.norm(encodings[id_result] - encodings[word2])
                    if _x < min_fasele:
                        min_index = id_result
                        min_fasele = _x
                if min_index != 0:
                    pool2.append(min_index)

    _pos_for_del=['Adjective','Verb']
    for id in pool1:
        if data[id]['pos'] in _pos_for_del:
            pool1.remove(id)
        _two_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                print(data[id]['syn_search'])
                _two_part=True
        if _two_part==True and id in pool1:
            pool1.remove(id)

    for id in pool2:
        if data[id]['pos'] in _pos_for_del:
            pool2.remove(id)
        _one_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                _one_part=True
        if _one_part==True and id in pool2:
            pool2.remove(id)

    for id in pool1:
        if data[id]['pos'] in _pos_for_del:
            pool1.remove(id)
        _two_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                print(data[id]['syn_search'])
                _two_part=True
        if _two_part==True and id in pool1:
            pool1.remove(id)

    for id in pool2:
        if data[id]['pos'] in _pos_for_del:
            pool2.remove(id)
        _one_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                _one_part=True
        if _one_part==True and id in pool2:
            pool2.remove(id)

    for id in pool1:
        if data[id]['pos'] in _pos_for_del:
            pool1.remove(id)
        _two_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                print(data[id]['syn_search'])
                _two_part=True
        if _two_part==True and id in pool1:
            pool1.remove(id)

    for id in pool2:
        if data[id]['pos'] in _pos_for_del:
            pool2.remove(id)
        _one_part=False
        for syn in list(data[id]['syn_search'].split(',')):
            if len(list(syn.split()))>=2:
                _one_part=True
        if _one_part==True and id in pool2:
            pool2.remove(id)

    shared = list(set(pool1).intersection(pool2))
    print('pool1: ' + str(len(pool1)))
    print('pool2: ' + str(len(pool2)))
    print(len(shared))

    if len(shared) < 50:
        shortest = nx.shortest_path(graph, word1, word2)
        cutoff = len(shortest)
        paths = list(nx.all_simple_paths(graph, word1, word2, cutoff=cutoff))
        for path in paths:
            for id in path:
                if id not in shared and id != word1 and id != word2:
                    shared.append(id)

    return shared



data=pickle.load(open('final_data','rb'))
G=pickle.load(open('graph_normal','rb'))
examples=pickle.load(open('examples','rb'))
encodings=pickle.load(open('encodings','rb'))
stops=pickle.load(open('stop','rb'))
index1, index2, pool1, pool2,shared=path_finder2(data,stops,G,'هجوم','گرداب')
chart=bechin(index1,index2,shared,encodings)