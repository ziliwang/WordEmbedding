#!/usr/bin/env python3
"""
Cross-Lingual Semantic Similarity ofWords as the Similarity of Their
SemanticWord Responses"""
import click
import multiprocessing
import time
from scipy import spatial
import functools
import numpy as np
from sklearn import preprocessing
from collections import defaultdict
import gzip
import os
import queue


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc


def computeDistance(word1, word2, emb1, emb2):
    try:
        w1 = emb1[word1]
        w2 = emb2[word2]
    except KeyError:
        return float(0.0)
    return w1.dot(w2)


def get_top_k(word1, emb1, emb2):
    bestw = [''] * 10
    bestd = [float(0)] * 10
    for j in emb2.keys():
        dist = computeDistance(word1, j, emb1, emb2)
        if dist > bestd[-1]:
            for i, a in enumerate(bestd):
                if dist > a:
                    bestw = bestw[:i] + [j] + bestw[i:9]
                    bestd = bestd[:i] + [dist] + bestd[i:9]
                    break
    return bestw, bestd


def sub_computeDist(emb1, emb2, inqueue, outqueue):
    while not inqueue.empty():
        try:
            lin1, lin2s = inqueue.get(timeout=2)
        except queue.Empty:
            os._exit(0)
        top, topd = get_top_k(lin1, emb1, emb2)
        for i, v in enumerate(top):
            if v in lin2s:
                outqueue.put(float(1/(i+1)))
                break
        print("remind {:5}".format(inqueue.qsize()), end='\r')
    os._exit(0)


@timeit
def computeDistMatrices(emb1, emb2, gold):
    correct = 0
    MRR = float(0.0)
    inqueue = multiprocessing.Queue()
    outqueue = multiprocessing.Queue()
    for w in gold.keys():
        inqueue.put((w, gold[w]))
    pool = []
    for i in range(10):
        p = multiprocessing.Process(target=sub_computeDist,
                                    args=(emb1, emb2, inqueue, outqueue, ))
        p.start()
        pool.append(p)
    for i in pool:
        i.join()
    print('\nfinished!\n')
    while not outqueue.empty():
        i = outqueue.get()
        correct += 1
        MRR += i
    print('{}/{} % age {}'.format(correct, len(gold.keys()),
          float(correct/len(gold.keys()))))
    print('{}/{} MRR {}'.format(MRR, len(gold.keys()),
          float(MRR/len(gold.keys()))))
    print("dist matrix done!")


def read_emb(_file, size):
    vocab = []
    X = []
    if _file.endswith('.gz'):
        with gzip.open(_file, 'r') as f:
            for i in f.readlines():
                items = i.strip().split()
                if len(items) == size + 1:
                    vocab.append(items[0])
                    X.append([float(i) for i in items[1:]])
                else:
                    pass
    else:
        with open(_file, 'r') as f:
            for i in f.readlines():
                items = i.strip().split()
                if len(items) == size + 1:
                    vocab.append(items[0])
                    X.append([float(i) for i in items[1:]])
                else:
                    pass
    X = norm(X)
    emb = {}
    for i, v in enumerate(vocab):
        emb[v] = X[i]
    return emb


def norm(X):
    X = preprocessing.normalize(X)
    """
    x_mean = X.mean(axis=0)
    X -= x_mean
    """
    return X


@click.command()
@click.option('--one', help='fisrt language')
@click.option('--two', help='second language')
@click.option('--pair', help='gold rule dict')
def main(one, two, pair):
    emb1 = read_emb(one, 200)
    print('{} loaded'.format(one))
    emb2 = read_emb(two, 200)
    print('{} loaded'.format(two))
    gold = defaultdict(set)
    with open(pair, 'r') as f:
        for i in f.readlines():
            lin1s, lin2s = i.strip().split('\t')
            for lin1 in lin1s.split():
                if lin1:
                    gold[lin1] = gold[lin1].union(set([i for i in lin2s.split() if i]))
    print(len([j for i in gold.keys() for j in gold[i]]))
    print('{} loaded'.format(pair))
    print('computing...\n')
    computeDistMatrices(emb1, emb2, gold)


if __name__ == '__main__':
    main()
