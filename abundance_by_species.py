from __future__ import division #float stuff

import sys
read_type = sys.argv[1] # is it 1, 2 or joined

file_list =[]

file_numbers= ["ERR031017", "ERR031018", "ERR031019", "ERR031022", "ERR031023", "ERR031024", "ERR031025", "ERR031026", "ERR031027", "ERR031028", "ERR031029", "ERR031030", "ERR031031", "ERR031032", "ERR031033", "ERR031035", "ERR031038", "ERR031039", "ERR031040", "ERR031041", "ERR031042", "ERR031043", "ERR031044", "ERR299295", "ERR299296", "ERR299297", "ERR299298", "ERR299299"]
for file_number in file_numbers:
	file_name = file_number + "_" + read_type + "_centrifuge_report.tsv"
	file_list.append(file_name)

print(file_list)


entries = [] # a list
seen_list = [] # a list
number = len(file_list) 
count = 0 #keep track of what iteration of the loop we're on
tapeh = [] #total abundance for species exclude human, append this list as you go, each entry in the list is the tapeh for each file
# need to come back to that

def fill_in_line(abundance,count):
	start = "0\t"*(count)
	end = "0\t" * (number - count) #number - count is the number of entries to the right of the one we've just put in
	end = end[:-2] #don't want that tab at the end
	output = start + abundance + "\t" + end #+ "\n" #writes output as a string
	return(output)

for file_name in file_list:
	input_file_handle = open(file_name)
	input_file = input_file_handle.read()
	input_file_handle.close()
	#input_file = input_file.strip(" ")
	input_file = input_file.split("\n") # split on new lines
	# now input_file is a list made up of the lines of the input file
	input_file.pop() #removes the empty cell the above splitting creates
	#print(input_file)
	for file_line in input_file: #loop over that list
		file_line = file_line.split("\t") #split the lines of the file into LISTS

		if file_line[2] == "species": #ignore all lines that don't pass this
			abundance = file_line[6] #the abundance figure for this species
			taxid = file_line[1] # taxid for this line
			species_name = file_line[0].strip("\n") #phyla name for this line
			if taxid in seen_list: # if it's in seen list, it means we've seen it before, and the info from this file_line needs to be ammended to a line we've already made
				entry_line_count = 0 # for the upcoming search of entries, which line are we on?
				#entries_split = entries.split("\n") #if something's in the seen list, then there should be something here from the else loop below #don't want to mess with entries. No longer needed, entries is a list now
				entry_line_new = "" #initialise this variable
				for entry_line in entries: #begin searching through entries
					entry_line_split = entry_line.split("\t") #leave entry_lines untouched
					#entry_line_split.pop()
					if len(entry_line_split) != 31:
						print ("error at count " + str(count))
						print(len(entry_line_split))
					entry_line_new = "" #initialise this variable
					#print(entry_line_split)
					if taxid == entry_line_split[1]: #entry_line[1] should be taxid in the entries list:
						temp_count = count + 2 #two columns of boilerplate (phyla, taxid)
						#temp_count is used to "position" the read info into the new line
						entry_line_split[temp_count] = abundance
						entry_line_new = "\t".join(entry_line_split) #the new version of that line
						# print(entry_line_new)
						break #call off the search
					entry_line_count = entry_line_count + 1
				entries[entry_line_count] = entry_line_new
			else: #if it is not seen in the list. #This is the step that will happen first
				#free to tack it on a new line
				new_entry = species_name + "\t" + taxid + "\t" + fill_in_line(abundance,count)
				entries.append(new_entry) #append this string to the list
				seen_list.append(taxid) #in future, all lines with this taxid will go to the "if" level of this conditional
	count = count + 1 #keeps track of which file we're on. #This is the right level of indentation
	#print(entries)
#	print(count)
#	print(seen_list)
		#print(seen_list)

#print(entries)

# I can make full lines easily enough, need to split entries (have it in a list) such that I can replace certain lines with new lines based on the ones they are replacing

#what I want to do
# go through each file
# get every phyla
# but you need to have empty spaces for everything as well
# so at the start, somehow set every line to be a tab separated sequence of zeros
# but that'll wipe all the info
# so if it isn't in the list, (seen_list) do the zero thing, if it is in the list, it's been seen before, so search through the entries list to find the right entry, then use index to make the relevant changes to that line (in entries) and then stop the search
# break apparently does that



##Make some new variables to store stuff
#probably don't need this stuff
apeh_list = []
header = ""
for file_name in file_list:
	err = file_name[4:9] #this actually cuts off the first number, but we don't need it and including those zeroes is a nuisance in Excel/libra
	header = header + "\t" + err
	apeh_list.append(0) #we'll replace these zeroes soon
#print(apeh_list) #nailed it
#for apeh in apeh_list:

nonnorm_output_filename = "stamp_input_multiple_files_abundances_species_nonnorm_" + read_type + ".tsv"

program_nonnorm_output = open(nonnorm_output_filename,"w")
program_nonnorm_output.write("\n".join(entries))
program_nonnorm_output.close()

#entry_line_new = "\t".join(entry_line_split)


for entry in entries:
	entry = entry.split("\t")
	if str(entry[1]) != "9606" and str(entry[1]) != "32630": #not homo sapiens or synthetic contruct
		apeh_count = 0 #which apeh are we on in the following loop
		for apeh in apeh_list:
			entry[apeh_count + 2] = entry[apeh_count + 2].replace("e","E") #the file uses both for some reason
			apeh_list[apeh_count] = apeh = float(apeh) + float(entry[apeh_count + 2])
			#print(entry[apeh_count + 2]) #apeh_count + 2 should be the relevant abundance column
			apeh_count = apeh_count + 1
#print(apeh_list)


norm_entries = "species" + header + "\n"
for entry in entries:
	entry = entry.split("\t")
	if str(entry[1]) != "9606" and str(entry[1]) != "32630":
		#print ("now on " + str(entry))
		apeh_count = 0 # this count is our way of moving "across" the eventual file
		for apeh in apeh_list:
			abundance_norm = float(float(entry[apeh_count + 2])/float(apeh)) #divide the read count by the total read count for that sample
# depending on if it is the start or the end of the line, this bit will have to be different
			if apeh_count == 0: #ie we're at the start
				norm_entries = norm_entries + entry[0] + "\t" + str(abundance_norm) + "\t" #entry[0] should be the phylum name
			elif apeh_count == number - 1: #-1 because of the start at zero thing #ie we're on the last one here
				norm_entries = norm_entries + str(abundance_norm) + "\n"
			else: # the in between columns
				norm_entries = norm_entries  + str(abundance_norm) + "\t"
			apeh_count = apeh_count + 1

# ok, so that's the total without chordata

print(norm_entries)

norm_output_filename = "stamp_input_multiple_files_abundances_species_" + read_type + ".tsv"

program_output = open(norm_output_filename,"w") #that won't get confusing...
program_output.write(norm_entries)
program_output.close()
