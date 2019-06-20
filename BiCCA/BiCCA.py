#!/usr/bin/env python3
"""
Improving vector space word representations using multilingual correlation
"""
import numpy as np
import click
import os
import gzip
from sklearn import preprocessing
from sklearn.cross_decomposition import CCA


def reader(file_handle, size):
    X = []
    vocab = []
    for i in file_handle.readlines():
        items = i.strip().split()
        if len(items) == size + 1:
            vocab.append(items[0])
            X.append([float(i) for i in items[1:]])
    X = vec_norm(X)
    emb = {}
    for i, v in enumerate(vocab):
        emb[v] = X[i]
    return emb


def vec_norm(X):
    X = preprocessing.normalize(X)
    return X


def read_word_vectors(filename, vec_size=200):
    ''' Read all the word vectors and normalize them '''
    print('Loading word vector: {}'.format(filename))
    with open(filename, 'r') as f:
        if filename.endswith('.gz'):
            fileObject = gzip.open(filename, 'r')
        else:
            fileObject = open(filename, 'r')
        wordvec = reader(fileObject, vec_size)
    return wordvec


def get_aligned_vectors(wordAlignFile, basedWordVectors, testedWordVectors):
    print('Loading alignment file: {}'.format(wordAlignFile))
    alignedVectors = {}
    subsetTest = {}
    based_len = len(basedWordVectors[list(basedWordVectors.keys())[0]])
    with open(wordAlignFile, 'r') as f:
        for line in f.readlines():
            word_in_base, word_in_test = line.strip().split(" ||| ")
            if word_in_test not in testedWordVectors:
                continue
            if word_in_base not in basedWordVectors:
                continue
            alignedVectors[word_in_test] = np.zeros(based_len, dtype=float)
            alignedVectors[word_in_test] += basedWordVectors[word_in_base]
            subsetTest[word_in_test] = testedWordVectors[word_in_test]
    print("No. of aligned vectors found: "+str(len(alignedVectors))+'\n')
    return alignedVectors, subsetTest


def save_orig_subset_and_aligned(tmp_dir, lang1name, lang2name,
                                 lang2WordVectors, lang1AlignedVectors):
    lang1_to_lang2 = os.path.join(tmp_dir, lang1name + '2' + lang2name + '.vec')
    lang2_in_align = os.path.join(tmp_dir, lang2name + '.aligned.vec')
    print('writing the aligned {} part in file {}'.format(lang2name,
                                                          lang2_in_align))
    with open(lang2_in_align, 'w') as f:
        for word, vec in lang1AlignedVectors.items():
            f.write(word + ' ' + ' '.join(map(lambda X: str(X), vec)) + '\n')
    print('writing the {} in {} vector in file {}'.format(lang1name, lang2name,
                                                          lang1_to_lang2))
    with open(lang1_to_lang2, 'w') as f:
        for word, vec in lang1AlignedVectors.items():
            f.write(word + ' ' + ' '.join(map(lambda X: str(X), vec)) + '\n')


def align_vec(base, test, align, tmp_dir):
    basedWordVectors = read_word_vectors(base)
    testedWordVectors = read_word_vectors(test)
    '''align test to base vec'''
    alignedVectors, subsetTest = get_aligned_vectors(align, basedWordVectors,
                                                     testedWordVectors)
    save_orig_subset_and_aligned(tmp_dir, base, test, testedWordVectors,
                                 alignedVectors)
    return basedWordVectors, testedWordVectors, alignedVectors, subsetTest


def dict_to_matrix(dic):
    return np.matrix([dic[i] for i in sorted(dic.keys())])


def trans(origin, weight):
    avg = np.repeat(np.mean(origin, axis=1), origin.shape[1]).reshape(origin.shape)
    return np.dot(origin - avg, weight)


def output(outdir, lang, ccaed, origin):
    ccaed_test_out_file = os.path.join(outdir, lang + '.ccaed.vec')
    print('writing CCA modeled {} to {}'.format(lang, ccaed_test_out_file))
    with open(ccaed_test_out_file, 'w') as f:
        for i, v in enumerate(sorted(origin.keys())):
            f.write(v + ' ' + ' '.join(map(lambda X: str(X), ccaed[i])) + '\n')


@click.command()
@click.option('--test', help='tested language embedding vector')
@click.option('--base', help='based language embedding vector')
@click.option('--align', help='word alignment file. format: base ||| test')
@click.option('--project', help='project name')
@click.option('--r', type=float, default=1.0, help='the ratio of new and old '
                                                   'embedding vector size. [1]')
def main(test, base, align, project, r):
    outdir = os.path.join(os.getcwd(), project)
    tmp_dir = os.path.join(outdir, 'tmp.{}'.format(project))
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)
    print('temporary dir: {}'.format(tmp_dir))
    basedWordVectors, testedWordVectors, aligned_test, subsetTest = \
        align_vec(base, test, align, tmp_dir)
    test_cols = len(testedWordVectors)
    base_cols = len(basedWordVectors)
    print('normalizing matrix')
    baseX = preprocessing.normalize(dict_to_matrix(basedWordVectors))
    testX = preprocessing.normalize(dict_to_matrix(testedWordVectors))
    aligned_testX = preprocessing.normalize(dict_to_matrix(aligned_test))
    subtestX = preprocessing.normalize(dict_to_matrix(subsetTest))
    cca = CCA(n_components=200)
    print('computing CCA')
    cca.fit(subtestX, aligned_testX)
    ccaed_test = trans(testX, cca.x_weights_)
    ccaed_base = trans(baseX, cca.y_weights_)
    ccaed_test = preprocessing.normalize(ccaed_test)
    ccaed_base = preprocessing.normalize(ccaed_base)
    output(outdir, test, ccaed_test, testedWordVectors)
    output(outdir, base, ccaed_base, basedWordVectors)


if __name__ == '__main__':
    main()
