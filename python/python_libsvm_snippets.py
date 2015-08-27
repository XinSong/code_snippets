#coding=gbk

import sys
sys.path.append('conf')
sys.path.append('lib')
import re

from collections import Counter
import liblinearutil as linear
import conf
import wordseg
import util

def get_word_dict(word_dict_file):
    word_dict = dict()
    for line in open(word_dict_file, 'r'):
        vec = line.strip().split('\t')
        word_dict[vec[0]] = int(vec[1])
    return word_dict

def generate_word_dict(train_file, word_dict_file=None):
    global word_segger
    word_count = dict()
    for line in open(train_file, 'r'):
        vec = line.strip().split('\t')
        y = vec[3]
        keywords = vec[4].split('<>|<>')
        for keyword in keywords:
            for word in word_segger.get_tokens(keyword):
                if not re.search('^\ *$', word):
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1
    word_count = sorted(word_count.iteritems(), key=lambda x: x[1], reverse=True)
    word_number = 1
    if word_dict_file:
        output = open(word_dict_file, 'w')
   
    for word, count in word_count:
        word_dict[word] = word_number
        word_number += 1
        if word_dict_file:
            output.write("%s\t%s\n" % (word, word_dict[word]))
    return word_dict

def get_feature(word_dict, raw_data_file, format_data_file):
    format_data = open(format_data_file, 'w')
    for line in open(raw_data_file, 'r'):
        vec = line.strip().split('\t')
        y = vec[3]
        keywords = vec[4].split('<>|<>')
        word_list = []
        for keyword in keywords:
            word_list.extend(word_segger.get_tokens(keyword))
        word_count = {word:count*1.0/len(word_list) for (word, count) in Counter(word_list).iteritems()}

        feature = ""
        for word, count in word_count.iteritems():
            if word not in word_dict:
                continue
            if feature == "":
                feature = "%s:%s" % (word_dict[word], count)
            else:
                feature = feature + " " + ("%s:%s" % (word_dict[word], count))
        format_data.write("%s\t%s\n" % (y, feature))

def train(word_dict):
    get_feature(word_dict, "data/train.dat", "data/train.format")
    get_feature(word_dict, "data/test.dat", "data/test.format")
    train_y, train_x = linear.svm_read_problem("data/train.format")
    model = linear.train(train_y, train_x) 
    linear.save_model("model.dat", model)
    
def evaluation(true_labels, pred_labels):
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0
    err_index = []
    for (index, label) in enumerate(pred_labels):
        if true_labels[index] == 1.0:
            if label == 1.0:
                tp += 1
            else:
                fn += 1
                err_index += [index]
        else:
            if label == 1.0:
                fp += 1
                err_index += [index]
            else:
                tn += 1
    err_output = open("err_index.txt", 'w')
    for err in err_index:
        err_output.write("%s\n" % err)

    print "ACC = ",(tp+tn)/(tp+tn+fp+fn)
    print "%s\t%s" % (tp, fn)
    print "%s\t%s" % (fp, tn)
    print "RECALL = ",tp/(tp+fn)
    print "PRECISION = ",tp/(tp+fp)

def main():
    util.WordSegger.init_conf(conf.SEGDICT_PATH, conf.TAGDICT_PATH, conf.STOPWORD_PATH)
    global word_segger
    word_segger = util.WordSegger.get_segger()
    generate_word_dict("data/train_dict", "data/word_dict")
    word_dict = get_word_dict("data/word_dict")
    train(word_dict)

    model = linear.load_model("model.dat")
    test_y, test_x = linear.svm_read_problem("data/test.format")
    test_y, test_x = linear.svm_read_problem("err.format")
    pred_labels, (ACC, MSE, SCC), pred_values = linear.predict(test_y, test_x, model)
    evaluation(test_y, pred_labels)
    pred_labels, , pred_values = linear.predict(test_y[7, test_x, model, "-q")

if __name__ == '__main__':
    main()
