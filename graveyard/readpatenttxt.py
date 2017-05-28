import re, sys, os

#Input: Name of txt that you want to read as a Python string
#Output: Clean txt

def retrieve_patent():
	all_patents_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Patent_Literature_Search_Pairs'))
	patent_dirs = os.listdir(all_patents_dir)
	for pd in patent_dirs: #E.g. #2 US200500blahblah-Description 
		try:
			pd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Patent_Literature_Search_Pairs', pd))
			pd_files = os.listdir(pd_path)
			for f in pd_files:
				if f.startswith('US') and f.endswith('.txt'):
					filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'Patent_Literature_Search_Pairs', pd, f))
					print(filename)
					fulltext = open(filename, 'r')
					print(fulltext)
					readtext = fulltext.read()
					print(readtext)
					# recordtext = re.split('\_+', readtext) #s
		except Exception as e:
			pass #probably a .DS_Store file


retrieve_patent()