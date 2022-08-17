import os

def trim_predictions(predictions: list):
  lens = {}
  for p in predictions:
    p_len = len(p)
    if p_len in lens.keys():
      lens[p_len]+=1
    else:
      lens[p_len] = 1
  max_len = max(lens.items())[0]
  predictions = [p for p in predictions if len(p) == max_len]
  return predictions, max_len

def appearances(predictions: list):
  distinct = list(set(predictions))
  appearances = {}
  for lp in distinct:
    appearances[lp] = predictions.count(lp)
  return appearances

def compare_chars(idx: int, predictions:list):
  chars = [c[idx] for c in predictions]
  number_appear = appearances(chars)
  if len(number_appear) == 1:
    return list(number_appear.keys())[0], 100
  else:
    total = 0
    for item in number_appear.items():
      total += int(item[1])
    for key in number_appear:
      number_appear[key] = int(number_appear[key])/total*100
    char = max(number_appear, key=number_appear.get)
    return char, number_appear[char]


def predict(predictions: list):
  #1. trim too long or too short suggestions
  predictions, max_len = trim_predictions(predictions)
  #2. get distinct values and number of it appearances
  number_appearances = appearances(predictions)
  print(f"distinct values with no. of appearances \n{number_appearances} \n")
  # if only one suggestion per all frames - return instantly
  if len(number_appearances) == 1:
    return list(number_appearances)[0]
  else:
    #3. iterate through characters
    lp_num = ""
    for i in range(max_len):
      char, probability = compare_chars(i, predictions)
      lp_num = lp_num + char
    ####
    return lp_num

def main():
  cwd = os.getcwd()
  data_path = cwd+"/data"
  os.chdir(data_path)
  files = os.listdir()
  files = [f for f in files if '.txt' in f]

  all_files = {}
  temp = []
  for f in files:
    file = open(f, "r")
    while file:
      line = file.readline()
      line = line[:-1]
      if line == "":
        break
      else:
        temp.append(line)
    all_files[f] = temp
    temp = []

  for f in all_files:
    lp_num = ""
    print(f"reading file \n{f}\n")
    lp_num = lp_num + predict(all_files[f])
    print(lp_num)
    input("press enter for the next prediction\n\n\n")


if __name__ == "__main__":
  main()
