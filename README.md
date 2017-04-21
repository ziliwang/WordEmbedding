# word embedding
```
.
├── BiCCA	 		# BiCCA model
├── eval			# evaluation method
├── README.md
└── utiutility
```
## Bilingual Word Embedding
### BiCCA model
Faruqui M, Dyer C. Improving vector space word representations using multilingual correlation[C]. Association for Computational Linguistics, 2014.
open source: https://github.com/mfaruqui/eacl14-cca
###### file
  - cal_word_pair.py: computing the bilingual vocabulary.
  - BiCCA.py: BiCCA model
### translation evaluation
  - eval/words_sim.py: script
  - eval/bldict: blingual dictionary
evaluating the cross-lingual model
### utility
  - VecConvert.py: convert BiCVM output to Word2Vec output
