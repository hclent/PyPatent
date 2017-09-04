import re, sys, os, fnmatch, logging

'''
Input: Null
Output: Takes each .txt file from patent directories for every
	patent, and prints each abstract* to its own .txt file.
	* Line 0 of the output file is the author, Line 1 is the title, and Line2 is the abstract 
	These will be used for training doc2vec, as well as comparing each abstract 
	to the primarty patent in question 
'''
#init logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='.pypatent.log')


def retrieve_text_files():
	logging.info("* Beginning retrieve_text_files(). Abstracts --> txt files ... ")
	all_patents_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'TEXT_Files')) 
	patent_dirs = os.listdir(all_patents_dir)

	for pd in patent_dirs: #E.g. #2 US200500blahblah-Description
		#Check to see if 'WOS Literature search' dir exists 
		pd_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'TEXT_Files', pd))
		dir_exists = os.path.isdir(pd_path)
		if dir_exists is True:
			logging.info("Directory " + str(pd)+ " exists!")
		if dir_exists is False:
			logging.info("Missing a directory")
			#If it doesn't exist, just look in the patent directory (pd)

		#Init empty lists to append info to 
		authors = []
		titles = []
		abstracts = []
		
		traindir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'train')) #/PyPatent/train
		
		patent_association = pd[:5] #grab first 5 chars to get patent number
		patent_number = re.sub('[^\d]','', patent_association) #just keep number
		logging.info("* Pattent "+ str(patent_number))

		try:
			search_docs = os.listdir(pd_path)
			for txtfile in search_docs:
				#the files for #128 are incorrect but files starting with just 128 are fine
				if txtfile.startswith("#128") or txtfile.startswith("#17") or txtfile.startswith("#46"):
					'''
					Missing ---------- dividers between search records:
					#17 Records Search parts 1-10
					#46 Records Search 
					'''
					logging.info("SKIPPING: " + str(txtfile))
					logging.info("its not formatted correctly...")
					pass
				
				elif fnmatch.fnmatch(txtfile, '*.txt'): #this ignores _DS_Store files 
					f =  os.path.abspath(os.path.join(pd_path, txtfile))
					#print(f)
					logging.info("reading file: " + str(f))
					fulltext = open(f, 'r', encoding="ISO-8859-1")
					readtext = fulltext.read()
					recordtext = re.split('\_+', readtext) #split on "______" type things

					#print(str(len(recordtext)) + " RECORDS IN " + str(f))

					for record in recordtext:
						if (len(record)) < 100: #if its too short, its probably empty
							logging.info("Empty record. Skip.")
							pass
						
						else:
							#initialize empty lists to check that the record has author, title, abstract
							current_author = []
							current_title = []
							current_abstract = [] 
							running_abstract = [] #for multi-line abstracts 

							text_lines = record.splitlines()

							for i, line in enumerate(text_lines):
								#print(str(i)+": " + str(line[:20]))
								
								#Get Author
								if re.match("^(\t*By\:)", line):
									current_author.append(line)
									logging.info(line)
								elif re.match("^(\t*Author\(s\))", line):
									current_author.append(line)
									logging.info(line)
								
								#Get Title
								if re.match("^(\t*Title\:)", line):
									current_title.append(line)
									logging.info(line)
								
								#Get Abstract
								if re.match("^(\t*Abstract\:)", line):
									running_abstract.append(line)
									#print(line)
									logging.info(line)
									#TODO: get the next line

								#if the previous line was Abstract:
								if re.match("^(\t*Abstract\:)",text_lines[i-1]):
									#and if this current line is longer than 100
									if len(line) >= 50:
										if not re.match("^\t*(Title\:|Source|By|Author|Conference)", line):
											#print(line)
											running_abstract.append(line)

								#if there was "Abstract:" header two lines ago, 
								# it may still be part of the abstract 
								if re.match("^(\t*Abstract\:)",text_lines[i-2]):
									#and if this current line is longer than 100
									if len(line) >= 50:
										if not re.match("^\t*(Title\:|Source|By|Author|Conference)", line):
											#print(line)
											running_abstract.append(line)

								
								if line == text_lines[-1]: #if its the last line
									#print(len(running_abstract))
									if len(running_abstract) >= 1:
										joined_text = (" ").join(running_abstract)
										#print(joined_text)
										current_abstract.append(joined_text)

							#Make sure this abstract has Author, Title, Abstract
							if (len(current_author)) == 0: #no author
								empty_author = 'Null Author'
								logging.info("Null Author")
								authors.append(empty_author)
							else:
								authors.append(current_author[0])

							if (len(current_title)) == 0: #no title
								empty_title = 'Null Title'
								logging.info("Null Title")
								titles.append(empty_title)
							else:
								titles.append(current_title[0])

							if (len(current_abstract)) == 0: #no abstract
								empty_abstract = 'Null Abstract'
								logging.info("Null Abstract")
								abstracts.append(empty_abstract)
							else:
								abstracts.append(current_abstract[0])

			#NB: this is on the level of 1 patent (multiple lit search files )
			# logging.info("* Done extracting abstracts from this file... ")
			# logging.info(str(len(authors)) + " authors")
			# logging.info(str(len(titles)) + " titles")
			# print(str(len(abstracts)) + " abstracts")

			'''
			The only lit searches showing up with repeats are Patents 2, 17, 46
			17 and 46 were excluded for bad formatting
			2 ... will need to investivate. 
			'''
			# unique_authors = list(set(authors))
			# unique_titles = list(set(titles))
			# unique_abstracts = list(set(abstracts))

			# print("* KEEPING ONLY UNIQUE ABSTRACTS ... ")
			# print(str(len(unique_authors)) + " unique authors")
			# print(str(len(unique_titles)) + " unique titles")
			# print(str(len(unique_abstracts)) + " unique abstracts")
			# print("#" * 20)

			#Print abstracts to 'train' folder
			#only grab the first thing from abstracts where there might be duplicates?

			print_info = list(zip(authors, titles, abstracts))
			logging.info("* printing abstracts to txt")
			for i in range(0, len(print_info)):
				abstract_name = str(patent_number) + '_' +str(i) + '.txt'
				completeName = os.path.join(traindir, abstract_name)
				logging.info(completeName)
				sys.stdout = open(completeName, "w")
				print(print_info[i][0]) #line 0 will be author
				print('\n')
				print(print_info[i][1]) #line 1 will be title
				print('\n')
				print(print_info[i][2]) #line 2 will be abstract
				print('\n')

		except Exception as e: #probably a .DS_Store file
			logging.info(e)


retrieve_text_files()

