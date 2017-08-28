import os, nltk, csv, re, gensim, logging
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from os.path import isfile, join
from random import shuffle
from gensim import utils
from gensim.models.doc2vec import LabeledSentence
from gensim.models import Doc2Vec
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from operator import itemgetter


#TO DO: Don't train on docs with all "Null"s 

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='.pypatent.log')

tokenizer = RegexpTokenizer(r'\w+')
eng_stopwords = nltk.corpus.stopwords.words('english')
eng_stopwords.append('abstract')

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

'''
Pre-processes the text by tokenizing it and removing stopwords
'''
def clean_text(unprocessed_text):
    lower = unprocessed_text.lower()
    word_list = tokenizer.tokenize(lower)
    word_set = [w for w in word_list if w not in eng_stopwords]
    clean_string = (' ').join(word_set)
    return clean_string 

'''
Function called to actually train our doc2vec model.
'''
def train_d2v():
    filedir = os.path.abspath(os.path.join(os.path.dirname(__file__))) 
    files = os.listdir(filedir)
    print(len(files))

    docLabels = [f for f in files if f.endswith('.txt')]
    print(len(docLabels))

    keep_labels = [] #not going to keep labels for Null Text docs 
    data = []
    for doc in docLabels:
        #print(doc)
        source = os.path.abspath(os.path.join(os.path.dirname(__file__), doc))
        with open(source, "r") as f:
            
            if re.match(".*US.*", doc): #for patents 
                #print("PATENT: " + doc)
                the_text = f.read()
                keep_text = the_text.rstrip()
                clean_string = clean_text(keep_text)
                data.append(clean_string)
            
            if not re.match(".*US.*", doc): #for abstracts, only get the abstract parts
                #print("ABSTRACT: " + doc)
                try:
                    the_text = f.readlines() #all abstract files are at least 9 lines
                    authors = the_text[0] #don't train on author names or titles!
                    titles = the_text[3]
                    the_real_text = the_text[4:]
                    joined_text = (' ').join(the_real_text) #make it a string
                    keep_text1 = joined_text.rstrip() #remove \n\t\r etc. 
                    clean_string = clean_text(keep_text) #pre-process the text
                    # print(doc)
                    # print(clean_string)
                    # print("#" * 20)
                    #data.append(clean_string)

                    if re.match(".*Null\sText",clean_string):
                        print("skilling Null....")
                        pass
                    else:
                        data.append(clean_string)
                except Exception as e: #if a document is empty skip it 
                    logging.info(e)
            f.close()

    print(len(data))
    print(data[0])
    print("#"*20)
    print(data[50])
    print("#"*20)
    print(data[51])
    print("#"*20)
    print(data[100])
    print("#"*20)
    print(data[1000])


    # logging.info("* Creating LabeledLineSentence Class ...")
    # it = LabeledLineSentence(data, docLabels)
    # logging.info("* Created LabeledLineSentences!!! ")
   
    # logging.info("* Initializing Doc2Vec Model ... ")
    # model = gensim.models.Doc2Vec(size=300, window=10, min_count=5, workers=11,alpha=0.025, min_alpha=0.025) # use fixed learning rate
    
    # logging.info("* Training Doc2Vec Model ... ")
    # model.build_vocab(it)

    # for epoch in range(10):
    #    model.train(it)
    #    model.alpha -= 0.002 # decrease the learning rate
    #    model.min_alpha = model.alpha # fix the learning rate, no decay
    #    model.train(it)

    # model.save('./a2v.d2v')
    # logging.info("* Saving Doc2Vec Model !!!")


'''
Function to load our saved model 
'''
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

        if re.match(".*US.*", doc): #documents with "US" in it are patents
            label = doc
            pDict = {"label": label}
            patents.append(pDict)
        
        else: 
            abstractloc = os.path.join( filedir, doc)
            abstract = open(abstractloc, 'r')
            abstract_lines = abstract.readlines()
            authors = abstract_lines[0]
            titles = abstract_lines[3]
            label = doc
           

            aDict = {"label": label, "author": authors, "title": titles}
            abstracts.append(aDict)

    return abstracts, patents


#TODO: print to csv
def compare_patents_to_abstracts():
    results_list = []

    model = load_model()
    abstracts, patents = get_data()

    #sort patents
    sorted_patents = sorted(patents, key=itemgetter('label'))

    for p in sorted_patents:

        p_label = p["label"]
        p_number = re.sub("(\_US.*\.txt)", '', p_label)
        p_vec = model.docvecs[p_label] #Patent vector 
        P = sparse.csr_matrix(p_vec) #Sparse Patent Vector 
        
        for a in abstracts:
            if a["label"].startswith( str(p_number)+"_" ):
                a_label = a["label"]
                a_authors = (a["author"]).strip('\t\n\r')
                a_title = (a["title"]).strip('\t\n\r')
                if a_title is "Null Title" and a_authors is "Null Authors":
                    pass
                else:
                    a_vec = model.docvecs[a_label]
                    A = sparse.csr_matrix(a_vec)
                    sim = cosine_similarity(P, A) #cos(patent, abstract) #
                    percent = str((sim[0][0]) * 100) + "%"

                    # [patent_name, abstract_label, percent, abstract_title, abstract_authors ]
                    r_list = [p_label, a_label, percent, a_title]
                    results_list.append(r_list)
                
                #print(str(p_label) + " is " + str(sim) + " similar to " + str(a_label))
    
    with open('results.csv', 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['PatentName', 'AbstractFile', 'PercentSimilarity', 'AbstractTitle'])
        for row in results_list:
            filewriter.writerow(row)


        

train_d2v()
#compare_patents_to_abstracts()
#model = load_model()
#print(model.docvecs['98_US20050142162.txt'])
# print (model.most_similar('invention'))
# print(model.docvecs[11])
# print(model.docvecs.doctags)



