import homework8 as hw8
import unittest
import timeit
import random

class TestHW8(unittest.TestCase):

   # def test_load_corpus(self):
   #     r = hw8.load_corpus("brown_corpus.txt");
   #     self.assertEquals(r[1402], [('It', 'PRON'), ('made', 'VERB'),\
   #                      ('him', 'PRON'), ('human', 'NOUN'),\
   #                      ('.', '.')]);
   #     self.assertEquals(r[1799], [('The', 'DET'), ('prospects', 'NOUN'),\
   #                      ('look', 'VERB'), ('great', 'ADJ'),\
   #                      ('.', '.')]);

    def test_most_probable_tags(self):
        r =  hw8.load_corpus("brown_corpus.txt");
        t = hw8.Tagger(r);
        self.assertEquals(t.most_probable_tags(["The", "blue", "bird", "sings"]),\
                        ['DET', 'ADJ', 'NOUN', 'VERB']);

        self.assertEquals(t.most_probable_tags( ["The", "man", "walks", "."]),\
                        ['DET', 'NOUN', 'VERB', '.']);
        print t.most_probable_tags(["ihop"])

    def test_viterbi_tags(self):
        c = hw8.load_corpus("brown_corpus.txt");
        t = hw8.Tagger(c);
        s = "I am waiting to reply".split();
        self.assertEquals(t.viterbi_tags(s), ['PRON', 'VERB', 'VERB', 'PRT', 'VERB']);
        self.assertEquals(t.most_probable_tags(s), ['PRON', 'VERB', 'VERB', 'PRT', 'NOUN']);

        s = "I saw the play".split();
        self.assertEquals(t.most_probable_tags(s),['PRON', 'VERB', 'DET', 'VERB']);
        self.assertEquals(t.viterbi_tags(s), ['PRON', 'VERB', 'DET', 'NOUN']);

        
    def test_time(self):
        count = 10
        print ' '
        t = timeit.Timer("hw8.load_corpus(\"brown_corpus.txt\"); ", 'import homework8 as hw8')
        print 'avg time for loading corpus: {}'.format(t.timeit(count)/count)
        print ' '
        t = timeit.Timer("hw8.Tagger(c);", 'import homework8 as hw8; c = hw8.load_corpus(\"brown_corpus.txt\"); ')
        print 'avg time for init : {}'.format(t.timeit(count)/count)

if __name__ == '__main__':
    unittest.main()

