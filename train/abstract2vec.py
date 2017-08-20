import os, nltk, csv, re, gensim, logging
from os.path import isfile, join
from random import shuffle
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

#TO DO: remove stop words?????
#TO DO: make sure input docs are formatted correctly
#TO DO: Don't train on docs with all "Null"s 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='.pypatent.log')


'''
Modified LabeledLineSentence Class from 
https://medium.com/@klintcho/doc2vec-tutorial-using-gensim-ab3ac03d3a1

Results in 1 vec per 1 doc, rather than 1 vec for each sentence in a doc.
'''
class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
       self.labels_list = labels_list
       self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
            yield LabeledSentence(doc.split(), [self.labels_list[idx]])



def train_d2v():
    #Obtain txt abstracts and txt patents 
    filedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    files = os.listdir(filedir)

    docLabels = [f for f in files if f.endswith('.txt')]
    data = []
    for doc in docLabels:
        source = str("/Users/hclent/Desktop/PyPatent/train/" + doc)
        with open(source, "r") as f:
            the_text = f.read()
            data.append(the_text)
        # with utils.smart_open(source) as fin:
        #     data.append(io.BufferedReader.read(fin))

    logging.info("* Creating LabeledLineSentence Class ...")
    it = LabeledLineSentence(data, docLabels)
    logging.info("* Created LabeledLineSentences!!! ")
   
    logging.info("* Initializing Doc2Vec Model ... ")
    model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
    
    logging.info("* Training Doc2Vec Model ... ")
    model.build_vocab(it)

    for epoch in range(10):
       model.train(it)
       model.alpha -= 0.002 # decrease the learning rate
       model.min_alpha = model.alpha # fix the learning rate, no deca
       model.train(it)
    model.save('./a2v.d2v')
    logging.info("* Saving Doc2Vec Model !!!")


def load_model():
    logging.info("* Loading Doc2Vec Model ... ")
    model = Doc2Vec.load('a2v.d2v')
    logging.info("* Loaded Saved Doc2Vec Model !!!")
    return model


#TODO: also get authors and stuff
def get_data():
    #Obtain txt abstracts and txt patents 
    filedir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    files = os.listdir(filedir)

    docLabels = [f for f in files if f.endswith('.txt')]

    abstracts = [] 
    patents = [] 
    
    for doc in docLabels:

        list_of_sents = []

        if re.match(".*US.*", doc): #documents with "US" in it are patents 
            label = doc
            pDict = {"label": label}
            patents.append(pDict)
        
        else: 
            abstractloc = os.path.join( filedir, doc)
            abstract = open(abstractloc, 'r')
            abstract_lines = abstract.readlines()
            authors = abstract_lines[0]
            titles = abstract_lines[1]
            label = doc
           

            aDict = {"label": label, "author": authors, "title": titles}
            abstracts.append(aDict)

    return abstracts, patents


#TODO: print to csv
def compare_patents_to_abstracts():
    model = load_model()
    abstracts, patents = get_data()

    for p in patents:

        p_label = p["label"]
        p_number = re.sub("(\_US.*\.txt)", '', p_label)
        p_vec = model.docvecs[p_label] #Patent vector 
        P = sparse.csr_matrix(p_vec) #Sparse Patent Vector 
        for a in abstracts:
            if a["label"].startswith( str(p_number)+"_" ):
                a_label = a["label"]
                a_authors = a["author"]
                a_title = a["title"]

                a_vec = model.docvecs[a_label]
                A = sparse.csr_matrix(a_vec)
                sim = cosine_similarity(P, A) #cos(patent, abstract)
                print(str(p_label) + " is " + str(sim) + " similar to " + str(a_label))



        




compare_patents_to_abstracts()
# model = load_model()
# print(model.docvecs['4_99.txt_7'])
# print (model.most_similar('invention'))
# print(model.docvecs[11])
# print(model.docvecs.doctags)



