import logging, os, sys
from readabstracttxt import retrieve_text_files
scriptpath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'train'))
sys.path.append(scriptpath)
from abstract2vec import train_d2v

#Step 0: Init log log
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='.pypatent.log')
#Step 1: Extract abstracts, then save as txt files in /train
#Step 2: If there is not a trained model, train the doc2vec model. Otherwise, load the doc2vec model
#Step 3: Create csv output document with patent-abstract comparisons  

#Run project
def run_pypatent():
	#Step 1: Extract abstracts from literature searches 
	logging.info("* BEGIN RETRIEVING ABSTRACTS ... ")
	retrieve_text_files()
	logging.info("* FINISHED RETRIEVING ABSTRACTS !!! ")
	#Step 2: Train doc2vec 
	path_to_model = os.path.abspath(os.path.join(os.path.dirname(__file__), 'train', './a2v.d2v'))
	if os.path.isfile(path_to_model):
		logging.info("* A TRAINED MODEL ALREADY EXISTS !!!")
		pass
	elif: 
		logging.info("* TRAINED MODEL NOT FOUND. TRAINING MODEL ... ")
		train_d2v()
		logging.info("* FINISHED TRAINING MODEL !!! ")
	# Step 3: Get results





run_pypatent()