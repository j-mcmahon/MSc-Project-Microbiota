from __future__ import division #float stuff

import sys
read_type = sys.argv[1] # is it 1, 2 or joined
path_to_cent_report = sys.argv[2]
path_to_kreport = sys.argv[3]

file_numbers= ["ERR031017", "ERR031018", "ERR031019", "ERR031022", "ERR031023", "ERR031024", "ERR031025", "ERR031026", "ERR031027", "ERR031028", "ERR031029", "ERR031030", "ERR031031", "ERR031032", "ERR031033", "ERR031035", "ERR031038", "ERR031039", "ERR031040", "ERR031041", "ERR031042", "ERR031043", "ERR031044", "ERR299295", "ERR299296", "ERR299297", "ERR299298", "ERR299299"]
# these values were the SRA accesion numbers for my data

cent_report_files = []

for file_number in file_numbers:
	file_name = path_to_cent_report + file_number + "_" + read_type + "_centrifuge_report.tsv"
	cent_report_files.append(file_name)

kreport_files = []

for file_number in file_numbers:
	file_name = path_to_kreport + file_number + "_" + read_type + "_kreport_output.csv"
	kreport_files.append(file_name)

#print(kreport_files)

# use a dictionary approach where keys are genus taxids, the first value is the genus name and the values after that are the species that are in the genus, according to the kreports
genera = {} # This is the dictionary we will add our info to

seen_genera = [] # normal list
stopped_looking = 0

for file_name in kreport_files:
	kreport_file_handle = open(file_name)
	kreport_file = kreport_file_handle.read()
	kreport_file_handle.close()
	#print(file_name)
	kreport_file = kreport_file.split("\n") # split on new lines
	# now input_file is a list made up of the lines of the input file
	kreport_file.pop() #removes the empty cell the above splitting creates
	print("This is the start of the loop for a new file")
	current_genus = ""
	genus_name = "PLACEHOLDER_FOR_GENUS_NAME"
	stop_looking = 0 #establish/reset this
	skips = 0
	for file_line in kreport_file:
		file_line = file_line.split("\t")
		if file_line[4] == "28384": #other sequences, stop looking at this point
			stop_looking  = 1
			stopped_looking = stopped_looking + 1 #how many times did this happen (should be 28)
		#if stop_looking == 1:
			#print("should stop")
		if file_line[4] == 10239: #this is viruses, we still want those
			stop_looking = 0 #it's ok to look now, the bad stuff is gone
		if file_line[3] == "G" and stop_looking == 0: # if/when we hit a genus
			current_genus = file_line[4] #record the current_genus as the taxid
			genus_name = [file_line[5].strip("\n")]
# need to know if the genus has been stared already, and act accordingly
			if current_genus in seen_genera: #we've seen it in at least one other file prior to this one, so we're appending to an existing key
				#print("take a day off, Mr Python Script")
				skips = skips + 1
			elif current_genus not in seen_genera: # if we're seeing this genus for the first time ever and so need to establish the key
				genera[current_genus] = genus_name #this should be the genus name
				seen_genera.append(current_genus)
		elif file_line[3] == "S" and stop_looking == 0: #if/when we see a species
		# this has to happen after we've seen a genus
			species_taxid = file_line[4]
			if species_taxid not in genera[current_genus]:
				#print ("appending")
				genera[current_genus].append(species_taxid) #append species taxid to the entry in the dictionary that corresponds to the genus we're in
	print (skips)


print(str(stopped_looking) + " <- get concerned if this number isn't the number of files")

# output the dictionary to a file
dictionary_output_name = "dictionary_abundance_calculation_" + read_type + ".txt"
dictionary_output = open(dictionary_output_name,"w")
dictionary_output.write(str(genera))
dictionary_output.close()

		# that covers if we see a genus and if we see a species. Those are, I think, the only scenarios of interest.
# As far as I can see, the k-reports are reliably ordered
# This code is all part of the big loop, so the resulting dictionary should be pretty comprehensive
	#print("This is the end of the iteration for that file, this is current status of citrobacter ->" + str(genera["544"]))# A test! Citrobacter

# go through each centrifuge file, line by line
# for each taxid, start a for loop of through genera, check the values of every key for that taxid
# if that taxid is in the list, locate the previous instance, in that file, of that the taxid for that genus showing up. Add the new abundance value to that old abundance values

# scenario one. Hit on taxid. No genus level entry with that taxid exists in the file. Create it, using the abundance observed. Give both a taxid and the genus name. Everything else gets a zero.

# scenario two. Hit on taxid. A genus level entry with that taxid exists in the file. Locate the line for that taxid, and in the column corresponding to this file, change the zero to the abundance currently under examination.

number = len(cent_report_files)

def fill_in_line(reads,count): # function for filling in the blanks with the right amount of zeroes
	start = "0\t"*(count)
	end = "0\t" * (number - count) #number - count is the number of entries to the right of the one we've just put in
	end = end[:-2] #don't want that tab at the end
	output = start + reads + "\t" + end #+ "\n" #writes output as a string
	return(output)

genus_taxid_seen_list = []
genus_level_abundance = []
count = 0 #which file are we on in the upcoming loop?

for file_name in cent_report_files:
	cent_file_handle = open(file_name)
	cent_file = cent_file_handle.read()
	cent_file_handle.close()
	cent_file = cent_file.split("\n") # split on new lines
	# now input_file is a list made up of the lines of the input file
	cent_file.pop() #removes the empty cell the above splitting creates
	for file_line in cent_file:
		file_line = file_line.split("\t") #split the lines of the file into LISTS
		if file_line[2] == "species": # is it a species?
			abundance = file_line[6].strip("\n")
			if abundance != 0: #don't bother with the zero ones
				species_taxid = file_line[1]
				species_name = file_line[0]
				for genus_taxid in genera:
					#print ("the genus taxid under investigation is " + str(genus_taxid) + " which is " + str(genera[genus_taxid][0]))
					if species_taxid in genera[genus_taxid]: #if the taxid we're currently looking at is in the list of values for the genus taxid that we're currently looking at
						genus_name = str(genera[genus_taxid][0])
						if genus_taxid in genus_taxid_seen_list: # if we've seen this genus_taxid before, ie scenario two.
							entry_line_count = 0 #for the upcoming search of entries, which line are we on?
							entry_line_new = "" #intialise this variable

							for entry_line in genus_level_abundance:
								entry_line_split = entry_line.split("\t")
								if len(entry_line_split) != 31:
									print ("error at count " + str(count))
									print(len(entry_line_split))
								entry_line_new = "" #intialise this variable
								if genus_taxid==entry_line_split[1]: # should be the genus taxid in the entry_line_split version of genus_level_abundance
									temp_count = count + 2 #to account for the two columns of boilerplate (genus name, taxid). temp_count is used to "position" the abundance data into the right place
									#print(entry_line_split)
									#print ("temp_count = " + str(temp_count))
									entry_line_split[temp_count] = str(float(abundance) + float(entry_line_split[temp_count]))
									entry_line_new = "\t".join(entry_line_split) #the new, ammended version of that line
									break #call of the search
								entry_line_count = entry_line_count + 1 
							genus_level_abundance[entry_line_count] = entry_line_new
						else: #if genus_taxid isn't on the list. This step will take place first. In this scenario, we're free to take the data onto a new line
							#print(genus_name)
							new_entry = str(genus_name) + "\t" + str(genus_taxid) + "\t" + fill_in_line(abundance, count)
							genus_level_abundance.append(new_entry)
						genus_taxid_seen_list.append(genus_taxid)
	count = count + 1 #keep track of which file we're on

# output the non normalised data to a file, so it can be manually checked to see if it worked right
nonnorm_output_filename = "abundances_genus_level_nonnorm_"+ read_type +".tsv"
program_nonnorm_output = open(nonnorm_output_filename,"w")
program_nonnorm_output.write("\n".join(genus_level_abundance))
program_nonnorm_output.close()

ageh_list = [] # where we will the total abundances for each genus, excluding the genus homo
header = ""

for file_number in file_numbers:
	err = file_number[4:9] #this actually cuts off the first number, but we don't need it and including those zeroes is a nuisance in Excel/libra
	header = header + "\t" + err
	ageh_list.append(0) #we'll replace these zeroes soon


for entry in genus_level_abundance:
	entry = entry.split("\t")
	if str(entry[1]) != "9605" and str(entry[1]) != "32630": #not homo or synthetic contruct
		ageh_count = 0 #which ageh are we on in the following loop
		for ageh in ageh_list:
			entry[ageh_count + 2] = entry[ageh_count + 2].replace("e","E") #the file uses both for some reason
			ageh_list[ageh_count] = ageh = float(ageh) + float(entry[ageh_count + 2])
			#print(entry[ageh_count + 2]) #ageh_count + 2 should be the relevant abundance column
			ageh_count = ageh_count + 1
#print(ageh_list)


norm_genus_level_abundance = "species\ttaxid" + header + "\n"
for entry in genus_level_abundance:
	entry = entry.split("\t")
	if str(entry[1]) != "9605" and str(entry[1]) != "32630":
		#print ("now on " + str(entry))
		ageh_count = 0 # this count is our way of moving "across" the eventual file
		for ageh in ageh_list:
			abundance_norm = float(float(entry[ageh_count + 2])/float(ageh)) #divide the read count by the total read count for that sample
# depending on if it is the start or the end of the line, this bit will have to be different
			if ageh_count == 0: #ie we're at the start
				norm_genus_level_abundance = norm_genus_level_abundance + entry[0] + "\t" + entry[1] + "\t" + str(abundance_norm) + "\t" #entry[0] should be the species name, entry[1] should be taxids
			elif ageh_count == number - 1: #-1 because of the start at zero thing #ie we're on the last one here
				norm_genus_level_abundance = norm_genus_level_abundance + str(abundance_norm) + "\n"
			else: # the in between columns
				norm_genus_level_abundance = norm_genus_level_abundance  + str(abundance_norm) + "\t"
			ageh_count = ageh_count + 1

# ok, so that's the total without chordata

norm_output_filename = "abundances_genus_level_norm_with_taxids_" + read_type + ".tsv"

program_output = open(norm_output_filename,"w") 
program_output.write(norm_genus_level_abundance)
program_output.close()

norm_genus_level_abundance = "species" + header + "\n"
for entry in genus_level_abundance:
	entry = entry.split("\t")
	if str(entry[1]) != "9605" and str(entry[1]) != "32630":
		#print ("now on " + str(entry))
		ageh_count = 0 # this count is our way of moving "across" the eventual file
		for ageh in ageh_list:
			abundance_norm = float(float(entry[ageh_count + 2])/float(ageh)) #divide the read count by the total read count for that sample
# depending on if it is the start or the end of the line, this bit will have to be different
			if ageh_count == 0: #ie we're at the start
				norm_genus_level_abundance = norm_genus_level_abundance + entry[0] + "\t" + str(abundance_norm) + "\t" #entry[0] should be the species name, entry[1] should be taxids
			elif ageh_count == number - 1: #-1 because of the start at zero thing #ie we're on the last one here
				norm_genus_level_abundance = norm_genus_level_abundance + str(abundance_norm) + "\n"
			else: # the in between columns
				norm_genus_level_abundance = norm_genus_level_abundance  + str(abundance_norm) + "\t"
			ageh_count = ageh_count + 1

norm_output_filename = "abundances_genus_level_norm_without_taxids_" + read_type + ".tsv"

program_output = open(norm_output_filename,"w") 
program_output.write(norm_genus_level_abundance)
program_output.close()

#And we're done
