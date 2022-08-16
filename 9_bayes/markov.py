"""markov.py
Markov chain implementation of guessing.
For now it only looks at the final value when testing.
May be possible to consider even prior occurrences.
Or not, it's a markov chain, it _may_ be priced in.
"""

import os

import numpy as np

import utils

symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NULL_CHAR = '`'
SYMBOLS = NULL_CHAR + symbols
PROB_RANGE = 0.01


def rid_entry(
    mc: np.ndarray,
    ridee: int) -> np.ndarray:
  """Rids the markov chain of an entry, passing off probabilities onwards
  """
  consider_indices = list(range(mc.shape[0]))
  consider_indices.remove(ridee)
  n_values = mc.shape[0]-1
  mc_new = np.empty((n_values, n_values))
  for i_old in consider_indices:
    for j_old in consider_indices:
      i_new = i_old
      j_new = j_old
      if i_old > ridee:
        i_new -= 1
      if j_old > ridee:
        j_new -= 1
      mc_new[i_new,j_new] = mc[i_old, j_old]\
          + (mc[i_old, ridee] * mc[ridee, j_old])
  return mc_new


n_symbols = len(SYMBOLS)
#Initialise markov chain with zeros
markov_chain = np.zeros((n_symbols, n_symbols))

folder_name = "unlabeled/"
file_names = os.listdir(folder_name)
txts = [x for x in file_names if x[-4:] == ".txt"]

for txt in txts:
  f = open(folder_name + txt, "r")
  content = f.read()
  content = utils.normal_shift(content, NULL_CHAR)
  lines = content.split("\n")[:-1]
  for i in range(len(lines)-1):
    j = i+1
    str_i = lines[i]
    str_j = lines[j]
    if len(str_i) != len(str_j):
      raise Exception('Unequal lengths')
    n_chars = len(str_i)
    for c_i in range(n_chars):
      char_i = str_i[c_i]
      char_j = str_j[c_i]
      index_i = SYMBOLS.index(char_i)
      index_j = SYMBOLS.index(char_j)
      markov_chain[index_i, index_j] += 1

#Normalising
for i in range(n_symbols):
  s = np.sum(markov_chain[i,:])
  markov_chain[i,:] = markov_chain[i,:] / s
#Get rid of the null_char entry
markov_chain = rid_entry(markov_chain, 0)

test_files = os.listdir("2cameras_1file/")
test_files = [x for x in test_files if x[-4:] == ".txt"]
for t_file in test_files:
  truth = t_file[:-4]
  f = open("2cameras_1file/"+t_file, "r")
  content = f.read()
  lines = content.split("\n")
  final_line = lines[-2]
  n_chars = len(final_line) 
  possibilities = [[] for _ in range(n_chars)]
  probabilities = [[] for _ in range(n_chars)]
  for chari, final_char in enumerate(final_line):
    final_char_i = symbols.index(final_char)
    probs = markov_chain[final_char_i,:]
    notable = np.nonzero(probs > PROB_RANGE)
    for n in notable[0]:
      possibilities[chari].append(symbols[n])
      probabilities[chari].append(probs[n])
  possible = utils.construct_probs(possibilities, probabilities)

  print("Line observed: "+final_line)
  for plate, prob in possible:
    print("{0}: {1}%".format(plate, prob*100))
  print("Actual line: "+truth)
  input("Enter to continue..")
