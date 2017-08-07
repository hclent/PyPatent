import PyPDF2, re, sys, os, logging

#TODO: text could use more cleaning

#Input: Name of pdf that you want to read as a Python string
#Output: Text from pdf printed to a .txt file with same name as input file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='.pypatent.log')


def pdf_to_text(path_to_pdf, name_of_pdf, patent_number):
	#input document
	pdfFile = open(path_to_pdf, 'rb')
	#initialize pdf reader
	pdf = PyPDF2.PdfFileReader(pdfFile)
	#get number of pages
	num_pages = pdf.numPages

	#extract text from each page
	text_list = []
	for i in range(0, int(num_pages) ):
		pageObj = pdf.getPage(i)
		page_text = pageObj.extractText()
		page_lower = page_text.lower()
		text_list.append(page_lower)

	text_string = ''.join(text_list)


	#cleanText
	text_clean = re.sub('\(?\[?\d{2,}\)?\]?', '', text_string) #delete ()[]numbers
	text_cleaner = re.sub('[^\w\s\.]', '', text_clean) #delete punctuation
	text_cleanest = re.sub ('\.{2,}', '', text_cleaner) #delete repeated periods
	clean_text = re.sub('\s{1,}[^a]\s{1,}', ' ', text_cleanest) #delete alone letters/numbers

	#print to .txt
	traindir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'train')) #/PyPatent/train
	new_name = patent_number + '_' + (name_of_pdf.strip('pdf')) + 'txt'
	completeName = os.path.join(traindir, new_name)  #pmcid.txt #save to suffix path
	sys.stdout = open(completeName, "w")
	print(text_string)


def convertPdfs():
	all_patents_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'TEXT_Files')) 
	patent_dirs = os.listdir(all_patents_dir)
	for pd in patent_dirs: #E.g. #2 US200500blahblah-Description
		try:
			pd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TEXT_Files', pd))
		
			patent_association = pd[:5] #grab first 5 chars to get patent number
			patent_number = re.sub('[^\d]','', patent_association) #just keep #number

			files = os.listdir(pd_path)
			for f in files:
				if '.pdf' in f:
					logging.info("writing to txt: " + str(f))
					path_to_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TEXT_Files', pd, f))
					pdf_to_text(path_to_pdf, f, patent_number) #convert pdf to text
		except Exception as e:
			logging.info(e)

convertPdfs()