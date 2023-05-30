import os
import sys
from text import *
from utils import open_data
from tqdm import tqdm
from nltk.corpus import stopwords

pos = 0
neg = 0
dict = {}

def check_args():
    if len(sys.argv) != 2:
        print("Wrong command line arguments!")
        return 1
    elif not os.path.exists(sys.argv[1]):
        print(sys.argv[1] + "is not exist!")
        return 1
    else:
        print("Load data from " + sys.argv[1])
    
def print_help():
    print("Usage: python <project_name> <path_to_file>")

def add(sign, words):
    global pos, neg
    for word in words:
        if sign == '+':
            pos += 1
            if word in dict:
                dict[word]['+'] += 1
            else:
                dict[word] = {'+': 1, '-': 0 }
        elif sign == '-':
            neg += 1
            if word in dict:
                dict[word]['-'] += 1
            else:
                dict[word] = {'+': 0, '-': 1 }
        else:
            print("Unrecognized symbol " + sign)
            print("Program will terminate!")
            exit(1)

def count_unknown(words):
    cnt = 0
    for word in words:
        if word not in dict:
            cnt += 1
    return cnt

def count_distinct(sign):
    result = 0
    for word in dict:
        if dict[word][sign] != 0:
            result += 1
    return result

def bayes_classifier(sign, words):
    result = (pos if sign == '+' else neg) / (pos + neg)
    unknown = count_unknown(words)
    for word in words:
        result *= ((dict[word][sign] if word in dict else 0) + 1) / ((pos if sign == '+' else neg) + count_distinct(sign) + unknown)
    return result

if check_args() == 1:
    print("Function check_args() fail.")
    print_help()
    exit(1)

file = open_data(sys.argv[1])
lines = file.readlines()
stopwords = stopwords.words('english')

print("File parsing started!")
for line in tqdm(lines):
    words_line = [x for x in words(line) if x not in stopwords]
    add(line[0], words_line)

data = str(input())
test_data = [x for x in words(data) if x not in stopwords]
Ppos = bayes_classifier('+', test_data)
Pneg = bayes_classifier('-', test_data)

if (Ppos > Pneg):
    print('+')
else:
    print('-')