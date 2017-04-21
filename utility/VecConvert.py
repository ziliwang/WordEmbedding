#!/usr/bin/env python3
import re
import click


@click.command()
@click.option('--bicvm', help='bicvm model')
@click.option('--wordvec_size', type=int, help='word vector size')
def main(bicvm, wordvec_size):
    with open(bicvm, 'r') as f:
        a = f.readline().split()
    for i, v in enumerate(a):
        if v == '_UNK_':
            wd_start = i
    wdlist = []
    for i, v in [(i, a[i:i+3]) for i in range(wd_start + 1, len(a), 3)]:
        if not re.match(r'\d+$', v[0]):
            vec_start = i
            break
        else:
            wdlist.append(v[1])
    vec = [a[i:i + wordvec_size] for i in range(vec_start, len(a), wordvec_size)]
    if len(wdlist) == len(vec):
        for i, v in enumerate(wdlist):
            if not i == 0:
                print(' '.join([v] + vec[i]))
    else:
        raise ValueError('non-except')


if __name__ == '__main__':
    main()
