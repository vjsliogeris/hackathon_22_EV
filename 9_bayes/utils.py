"""utils.py
Used by all methods.
"""

from itertools import combinations, product

import numpy as np
import torch

def hamming_dist(
    s1: str,
    s2: str) -> int:
  """Return hamming distance between two words
  """
  if len(s1) != len(s2):
    raise Exception('Unequal lengths')
  n_chars = len(s1)
  dist = 0
  for i in range(n_chars):
    if s1[i] != s2[i]:
      dist += 1
  return dist


def log_softmax(x):
  e = torch.exp(x)
  softmax = e / torch.sum(e)
  lsm = torch.log(softmax)
  return lsm


def construct_probs(
    possibilities: list,
    probabilities: list):
  """Construct possible combinations of number plates and their probabilities
  """
  output = []
  n_chars = len(possibilities)
  combos = product(*possibilities)
  for combo in combos:
    plat = ""
    prob = 1
    for i, letter in enumerate(combo):
      plat += letter
      prob_i = possibilities[i].index(letter)
      prob *= probabilities[i][prob_i]
    output.append((plat, prob))
  output.sort(reverse = True, key = lambda x: x[1])
  return output


def normal_shift(
    s: str,
    null_char = '`') -> str:
  """Shift strings so they're aligned

  Append null characters to words that lack them so it matches with
  most full strings the most.
  """
  guesses = s.split("\n")[:-1]
  n_chars = [len(x) for x in guesses]
  max_len = max(n_chars)
  full_guesses = [x for x in guesses if len(x) == max_len]
  for i, guess_i in enumerate(guesses):
    if len(guess_i) < max_len:
      to_add = max_len - len(guess_i)
      index_combos = combinations(range(max_len), to_add)
      best_version = None
      best_error = np.inf
      for index_combo in index_combos:
        mean_val = 0
        version = guess_i
        for null_i in index_combo:
          version = version[:null_i] + null_char + version[null_i:]
        for full_g in full_guesses:
          mean_val += hamming_dist(full_g, version)
        mean_val = mean_val / len(full_guesses)
        if mean_val < best_error:
          best_error = mean_val
          best_version = version
        guesses[i] = best_version
  output = ''
  for g in guesses:
    output += g + "\n"
  return output
