"""main_lstm.py
Oops did RNN by accident
"""

import os
import utils

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from PIL import Image

symbols = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
NULL_CHAR = '`'
SYMBOLS = NULL_CHAR + symbols

class LSTMTagger(nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super(LSTMTagger, self).__init__()
    self.hidden_size = hidden_size

    self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
    self.i2o = nn.Linear(input_size + hidden_size, output_size)
    self.o2o = nn.Linear(hidden_size + output_size, output_size)
    self.dropout = nn.Dropout(0.1)
    self.softmax = nn.LogSoftmax(dim=1)

  def forward(self, input, hidden):
    input_combined = torch.cat((input, hidden), 1)
    hidden = self.i2h(input_combined)
    output = self.i2o(input_combined)
    output_combined = torch.cat((hidden, output),1)
    output = self.o2o(output_combined)
    output = self.dropout(output)
    output = self.softmax(output)
    return output, hidden

  def initHidden(self):
    return torch.zeros(1, self.hidden_size)


def prepare_sequence(seq, to_ix):
  idxs = torch.zeros((len(seq), len(to_ix)))
  for i, w in enumerate(seq):
    idxs[i, to_ix[w]] = 1
  return idxs


training_data = []

folder_name = "2cameras_1file/"
file_names = os.listdir(folder_name)
txts = [x for x in file_names if x[-4:] == ".txt"]
for txt in txts:
  f = open(folder_name + txt, "r")
  content = f.read()
  content = utils.normal_shift(content, NULL_CHAR)
  lines = content.split("\n")[:-1]
  truth = txt[:-4]
  n_chars = len(lines[0])-1
  for char_i in range(n_chars):
    char_lines = [x[char_i] for x in lines]
    char_truth = truth[char_i]
    training_data.append((char_lines, char_truth))

word_to_ix = {}
for i, s in enumerate(SYMBOLS):
  word_to_ix[s] = i

model = LSTMTagger(len(SYMBOLS), len(SYMBOLS), len(SYMBOLS))
loss_function = nn.NLLLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)
criterion = nn.NLLLoss()


#Overfit this thing
for _ in range(200):
  loss = 0
  for q, a in training_data:
    inputs = prepare_sequence(q, word_to_ix)
    hidden = model.initHidden()
    model.zero_grad()
    for i in range(inputs.size(0)):
      output, hidden = model(torch.unsqueeze(inputs[i],0), hidden)
    a_onehot = prepare_sequence(a, word_to_ix)
    target = utils.log_softmax(a_onehot)
    l = criterion(output[0], torch.tensor(word_to_ix[a]))
    loss += l
  print(loss)
  loss.backward()
  optimizer.step()

#Let's try some of the unlabeled suckers.

folder_name = "unlabeled/"
file_names = os.listdir(folder_name)
txts = [x for x in file_names if x[-4:] == ".txt"]

for txt in txts:
  f = open(folder_name + txt, "r")
  content = f.read()
  content = utils.normal_shift(content, NULL_CHAR)
  lines = content.split("\n")[:-1]
  linelens = [len(x) for x in lines]
  n_chars = max(linelens)
  predicted_plate = ''
  for char_i in range(n_chars):
    char_lines = [x[char_i] for x in lines]
    char_truth = truth[char_i]
    inputs = prepare_sequence(char_lines, word_to_ix)
    hidden = model.initHidden()
    for i in range(inputs.size(0)):
      output, hidden = model(torch.unsqueeze(inputs[i],0), hidden)
    index = torch.argmax(output)
    symbol = SYMBOLS[index]
    predicted_plate += symbol
  im = Image.open(folder_name + txt[:-4])
  print(predicted_plate)
  im.show()
  input()
