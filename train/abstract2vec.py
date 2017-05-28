import os, nltk, csv, re 
from os.path import isfile, join
from random import shuffle
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec

#TO DO: remove stop words?????
#TO DO: make sure input docs are formatted correctly

#TODO: Keep this file in the train folder!

class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources
        
        flipped = {}
        
        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')
    
    def __iter__(self):
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    yield LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no])
    
    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            with utils.smart_open(source) as fin:
                for item_no, line in enumerate(fin):
                    self.sentences.append(LabeledSentence(utils.to_unicode(line).split(), [prefix + '_%s' % item_no]))
        return self.sentences
    
    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences



def train_d2v():
    #Obtain txt abstracts and txt patents 
    filedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    files = os.listdir(filedir)

    #Doc2Vec takes [['a', 'sentence'], 'and label']
    docLabels = [f for f in files if f.endswith('.txt')]

    sources = {}  #{'2_139.txt': '2_139.txt'}
    for lable in docLabels:
        sources[lable] = lable
    sentences = LabeledLineSentence(sources)

    
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=8)
    model.build_vocab(sentences.to_array())
    for epoch in range(10):
        model.train(sentences.sentences_perm())

    model.save('./a2v.d2v')


def load_model():
    model = Doc2Vec.load('a2v.d2v')
    return model
    # print (model.most_similar('invention'))
    # print(model.docvecs[11])


#TODO: also get authors and stuff
def get_data():
    #Obtain txt abstracts and txt patents 
    filedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    files = os.listdir(filedir)

    #Doc2Vec takes [['a', 'sentence'], 'and label']
    docLabels = [f for f in files if f.endswith('.txt')]

    abstracts = [] #list of dicts with {"abstract": 2_23, "data": [['list', 'of', 'lists', 'with', 'strings'], [], .. [] ]}
    patents = [] #list of dicts with {"patent": 2_US123, "data": [['list', 'of', 'lists', 'with', 'strings'], [], .. [] ]}
    for doc in docLabels:

        list_of_sents = []

        if re.match(".*US.*", doc): #documents with "US" in it are patents 
            patentloc = os.path.join( filedir, doc)
            patent = open(patentloc, 'r')
            patent_text = patent.read()
            patent_sents = nltk.sent_tokenize(patent_text) #requires nltk.data()
            for sent in patent_sents:
                word_list = sent.split()
                list_of_sents.append(word_list)
            
            pDict = {"patent": doc, "data": list_of_sents}
            patents.append(pDict)
        
        else: 
            abstractloc = os.path.join( filedir, doc)
            abstract = open(abstractloc, 'r')
            abstract_text = abstract.read()
            abstract_sents = nltk.sent_tokenize(abstract_text) #requires nltk.data()
            for sent in abstract_sents:
                word_list = sent.split()
                list_of_sents.append(word_list)

            aDict = {"abstract": doc, "data": list_of_sents}
            abstracts.append(aDict)

    return abstracts, patents



# def compare_patents_to_abstracts():
#     model = load_model()
#     abstracts, patents = get_data()

#     for p in patents:
#         p_id = p["patent"]
#         p_number = re.sub("(\_US.*\.txt)", '', p_id)
#         p_data = p["data"]
#         for a in abstracts:
#             if a["abstract"].startswith(p_number):
                # sim = model.similarity([p_id], [a["abstract"]])
                # print(sim)
                ##### ##### get the cosine similarit
        




# compare_patents_to_abstracts()

model = load_model()
print(model.docvecs['4_99.txt_7'])
#print(model.docvecs.doctags)