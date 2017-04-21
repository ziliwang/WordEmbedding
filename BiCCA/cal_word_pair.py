#!/usr/bin/env python3
import click
from collections import defaultdict
import re


def align_reader(align_file):
    print('reading align file {}'.format(align_file))
    output = []
    with open(align_file, 'r') as f:
        for i in f.readlines():
            output.append([list(map(lambda X: int(X), i.split('-')))
                           for i in i.strip().split()])
    return output


def pair_lang_reader(pair_file):
    lang = []
    with open(pair_file, 'r') as f:
        for i in f.readlines():
            lang.append(i.strip().split(' ||| '))
    return lang


def cal_word_pair(lang_list, align_list, reverse):
    pairdict = defaultdict(lambda: defaultdict(int))
    if len(lang_list) != len(align_list):
        raise ValueError('different size')
    print('computing paired dict')
    for i, v in enumerate(lang_list):
        lang1, lang2 = v
        lang1_wds = lang1.split()
        lang2_wds = lang2.split()
        for lang1_index, lang2_index in align_list[i]:
            if reverse:
                pairdict[lang2_wds[lang2_index]][lang1_wds[lang1_index]] += 1
            else:
                pairdict[lang1_wds[lang1_index]][lang2_wds[lang2_index]] += 1
    return pairdict


def clean_rules(i, j):
    if re.search('[\W, 0-9]', i) or re.search('[\W, 0-9]', j):
        if i == j:
            return True
        return False
    return True


@click.command()
@click.option('--pair', help='paired file, fast align input file')
@click.option('--align', help='align file, fast align out file')
@click.option('--reverse', default=0, help='if reverse the langue pair of the output')
@click.option('--c', default=10, help='count lower limit')
def main(pair, align, reverse, c):
    align_ls = align_reader(align)
    langpir = pair_lang_reader(pair)
    pdict = cal_word_pair(langpir, align_ls, reverse)
    outfile = pair + '.wordpair'
    print('writing to {}'.format(outfile))
    with open(outfile, 'w') as f:
        for i in pdict.keys():
            _max = (None, 0)
            for j in pdict[i].keys():
                if not clean_rules(i, j):
                    continue
                if pdict[i][j] < c:
                    continue
                if pdict[i][j] > _max[1]:
                    _max = (j, pdict[i][j])
            if _max[0]:
                f.write('{} ||| {}\n'.format(i, _max[0]))


if __name__ == '__main__':
    main()
