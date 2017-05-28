import os, sys
from readabstract import pdf_to_text

#Input: None, but you must be in the directory of the files you want to read.
#Middle step: pdf files containing abstracts are converted to .txt first
#Output: All abstracts printed to txt in /train folder

filedir = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(filedir)
for f in files:
	if '.pdf' in f:
		pdf_to_text(f) #convert pdf to text


def extract_abstracts():
	filedir = os.path.abspath(os.path.dirname(__file__))
	files = os.listdir(filedir)

	for f in files:
		if 'search' in f and '.txt' in f:
			fulltext = open(f, 'r')
			readtext = fulltext.read()
			text_lines = readtext.splitlines()
			for line in text_lines:
				if 'Abstract' in line or 'abstract' in line:
					traindir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'train'))
					clean_name = (f.strip('.txt'))
					new_name = (clean_name.strip('htm')) + 'txt'  
					completeName = os.path.join( traindir, new_name) #save abstracts in train folder
					sys.stdout = open(completeName, "w")
					print(line)
		


					
extract_abstracts()
