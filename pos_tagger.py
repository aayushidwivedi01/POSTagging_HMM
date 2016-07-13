############################################################
# CIS 521: Homework 8
############################################################

student_name = "Aayushi Dwivedi"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import defaultdict
from math import log
import operator
############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    fp = open(path, 'r');
    return [[tuple(word.split("=")) for word in line.split()] for line in fp.readlines()]
class Tagger(object):

    def __init__(self, sentences):
        smoothing = 1e-10;
        tag_count = defaultdict(int);
        a_count = defaultdict(lambda:defaultdict(float));
        count_t_i = defaultdict(int);
        b_count = defaultdict(lambda:defaultdict(float));
        count_w = defaultdict(int);
        vocab = set();
       
        for sentence in sentences:
            tag_count[sentence[0][1]] += 1;
            for i in xrange(0, len(sentence) -1):
                a_count[sentence[i][1]][sentence[i+1][1]] += 1;
                count_t_i[sentence[i][1]] += 1;
                b_count[sentence[i][1]][sentence[i][0]] += 1;
                count_w[sentence[i][1]] += 1;
                vocab.add(sentence[i][0])   
            b_count[sentence[-1][1]][sentence[-1][0]] += 1;
            count_w[sentence[-1][1]] += 1;

        num_sentences = len(sentences);
        pi_tag = defaultdict(float, dict((tag,log(count)-log(num_sentences)) for tag, count in tag_count.iteritems()));
        
        total_count = len(count_t_i);
        for t_i, values in a_count.iteritems():
            for t_j, count in values.iteritems():
                a_count[t_i][t_j] = log(count ) - log((count_t_i[t_i] ));
        
        total_count = len(count_w);
        vocab_len = len(vocab);
        for tag, words in b_count.iteritems():
            for word, count in words.iteritems():
                b_count[tag][word] = log(b_count[tag][word] + smoothing) - log(count_w[tag] + smoothing * (vocab_len + 1));
            b_count[tag]["<UNK>"] = log(smoothing) - log( count_w[tag] + smoothing * (vocab_len +1))
        
        self.pi = pi_tag;
        self.a = a_count;
        self.b = b_count;

        
                
    def most_probable_tags(self, tokens):
        result = []
        arg_max = "";
        for token in tokens:
            max_prob = -10000
            for tag, words in self.b.iteritems():
                if token in words and self.b[tag][token] > max_prob:
                    max_prob = self.b[tag][token]
                    arg_max = tag;
                elif self.b[tag]["<UNK>"] > max_prob:
                    max_prob = self.b[tag]["<UNK>"];
                    arg_max = tag;
            result.append(arg_max);
        return result;

    def viterbi_tags(self, tokens):
        d_1 = {tag : prob + self.b[tag][tokens[0]] if tokens[0] in self.b[tag]\
             else  prob + self.b[tag]["<UNK>"] for tag, prob in self.pi.iteritems()}
        delta = [d_1];
        psi = [];
        for token in tokens[1:]:
            transition_probs = []
            d_t = dict();
            psi_t = dict();
            for t_j, words in self.b.iteritems():
                max_prob = -10000;
                arg_max = "";
                for t_i, prob in delta[-1].iteritems():                    
                    if (prob + self.a[t_i][t_j]) > max_prob:
                        max_prob = (prob + self.a[t_i][t_j])
                        arg_max = t_i;
                d_t[t_j] = max_prob + self.b[t_j][token] if token in words \
                        else max_prob + self.b[t_j]["<UNK>"]; 
                psi_t[t_j] = arg_max;
            delta.append(d_t);
            psi.append(psi_t);

        final_state = max(delta[-1].iteritems(), key=operator.itemgetter(1))[0]
        
        result = [final_state];
        for i in xrange(len(psi)-1, -1, -1):
            prev_state = psi[i][result[0]];
            result.insert(0, prev_state);
        return result
            
        


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
7
"""

feedback_question_2 = """
Implementing viterbi_tags.
None
"""

feedback_question_3 = """
Helped in visualizing the viterbi algorithm.
No.
"""
