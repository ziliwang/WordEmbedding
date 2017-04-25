#!/usr/bin/env python3
"""
Cross-Lingual Semantic Similarity ofWords as the Similarity of Their
SemanticWord Responses.
version 1.1
similarity search algorithm:  brute-force search -> KDTree search speed up ~10x
remove multiprocessing
"""
import click
import time
from scipy import spatial
import functools
import numpy as np
from scipy.spatial import KDTree
from sklearn import preprocessing
from collections import defaultdict
import gzip
import os


def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc


@timeit
def computeDistMatrices(emb1, emb2, gold):
    correct = 0
    MRR = float(0.0)
    vob2 = []
    matrix2 = []
    for i in emb2.keys():
        vob2.append(i)
        matrix2.append(emb2[i])
    matrix2 = np.array(matrix2)

    kdtree = KDTree(matrix2, leafsize=100)
    for gold_en, gold_trans in gold.items():
        d, index = kdtree.query(emb1[gold_en], k=10)
        for i in index:
            if vob2[i] in gold_trans:
                correct += 1
                MRR += float(1/(i+1))
                break

    print('\nfinished!\n')
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
