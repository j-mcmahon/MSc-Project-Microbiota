from __future__ import division #float stuff

file_list = ["ERR031017_1_kreport_output.csv", "ERR031018_1_kreport_output.csv", "ERR031019_1_kreport_output.csv", "ERR031022_1_kreport_output.csv", "ERR031023_1_kreport_output.csv", "ERR031024_1_kreport_output.csv", "ERR031025_1_kreport_output.csv", "ERR031026_1_kreport_output.csv", "ERR031027_1_kreport_output.csv", "ERR031028_1_kreport_output.csv", "ERR031029_1_kreport_output.csv", "ERR031030_1_kreport_output.csv", "ERR031031_1_kreport_output.csv", "ERR031032_1_kreport_output.csv", "ERR031033_1_kreport_output.csv", "ERR031035_1_kreport_output.csv", "ERR031038_1_kreport_output.csv", "ERR031039_1_kreport_output.csv", "ERR031040_1_kreport_output.csv", "ERR031041_1_kreport_output.csv", "ERR031042_1_kreport_output.csv", "ERR031043_1_kreport_output.csv", "ERR031044_1_kreport_output.csv", "ERR299295_1_kreport_output.csv", "ERR299296_1_kreport_output.csv", "ERR299297_1_kreport_output.csv", "ERR299298_1_kreport_output.csv", "ERR299299_1_kreport_output.csv"]


entries = [] # a list
seen_list = [] # a list
number = len(file_list) 
count = 0 #keep track of what iteration of the loop we're on
trpeh = [] #total reads genus exclude human, append this list as you go, each entry in the list is the trpeh for each file

def fill_in_line(reads,count):
	start = "0\t"*(count)
	end = "0\t" * (number - count) #number - count is the number of entries to the right of the one we've just put in
	end = end[:-2] #don't want that tab at the end
	output = start + reads + "\t" + end #+ "\n" #writes output as a string
	return(output)

for file_name in file_list:
	input_file_handle = open(file_name)
	input_file = input_file_handle.read()
	input_file_handle.close()
	input_file = input_file.split("\n") # split on new lines
	# now input_file is a list made up of the lines of the input file
	input_file.pop() #removes the empty cell the above splitting creates
	#print(input_file)
	for file_line in input_file: #loop over that list
		file_line = file_line.split("\t") #split the lines of the file into LISTS

		if file_line[3] == "G": #ignore all lines that don't pass this
			reads = file_line[1] #reads from this sample
			taxid = file_line[4] # taxid for this line
			genus_name = file_line[5].strip("\n") #genus name for this line
			if taxid in seen_list: # if it's in seen list, it means we've seen it before, and the info from this file_line needs to be ammended to a line we've already made
				entry_line_count = 0 # for the upcoming search of entries, which line are we on?
				entry_line_new = "" #initialise this variable
				for entry_line in entries: #begin searching through entries
					entry_line_split = entry_line.split("\t") #leave entry_lines untouched
					if len(entry_line_split) != 31:
						print ("error at count " + str(count))
						print(len(entry_line_split))
					entry_line_new = "" #initialise this variable
					if taxid == entry_line_split[1]: #entry_line[1] should be taxid in the entries list:
						temp_count = count + 2 #two columns of boilerplate (genus, taxid)
						entry_line_split[temp_count] = reads
						entry_line_new = "\t".join(entry_line_split) #the new version of that line
						# print(entry_line_new)
						break #call off the search
					entry_line_count = entry_line_count + 1
				entries[entry_line_count] = entry_line_new
			else: #if it is not seen in the list. #This is the step that will happen first
				#free to tack it on a new line
				new_entry = genus_name + "\t" + taxid + "\t" + fill_in_line(reads,count)
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




#entries = entries.split("\n")
#entries.pop()
#print(entries)

##Make some new variables to store stuff
#probably don't need this stuff
rpeh_list = []
header = ""
for file_name in file_list:
	err = file_name[4:9] #this actually cuts off the first number, but we don't need it and including those zeroes is a nuisance in Excel/libra
	header = header + "\t" + err
	rpeh_list.append(0) #we'll replace these zeroes soon
#print(rpeh_list) #nailed it
#for rpeh in rpeh_list:

program_nonnorm_output = open("stamp_input_multiple_files_genus_nonnorm.tsv","w") #that won't get confusing...
program_nonnorm_output.write("\n".join(entries))
program_nonnorm_output.close()

#entry_line_new = "\t".join(entry_line_split)

for entry in entries:
	entry = entry.split("\t")
	if str(entry[1]) != "9605": #not homo
		rpeh_count = 0 #which rpeh are we on in the following loop
		for rpeh in rpeh_list:
			rpeh_list[rpeh_count] = rpeh = int(rpeh) + int(entry[rpeh_count + 2])
			#print(entry[rpeh_count + 2]) #rpeh_count + 2 should be the relevant reads column
			rpeh_count = rpeh_count + 1
#print(rpeh_list)


norm_entries = "genus" + header + "\n"
for entry in entries:
	entry = entry.split("\t")
	if str(entry[1]) != "9605":
		#print ("now on " + str(entry))
		rpeh_count = 0 # this count is our way of moving "across" the eventual file
		for rpeh in rpeh_list:
			reads_norm = float(float(entry[rpeh_count + 2])/float(rpeh)) #divide the read count by the total read count for that sample
# depending on if it is the start or the end of the line, this bit will have to be different
			if rpeh_count == 0: #ie we're at the start
				norm_entries = norm_entries + entry[0] + "\t" + str(reads_norm) + "\t" #entry[0] should be the phylum name
			elif rpeh_count == number - 1: #-1 because of the start at zero thing #ie we're on the last one here
				norm_entries = norm_entries + str(reads_norm) + "\n"
			else: # the in between columns
				norm_entries = norm_entries  + str(reads_norm) + "\t"
			rpeh_count = rpeh_count + 1

# ok, so that's the total without the genus homo

print(norm_entries)

program_output = open("stamp_input_multiple_files_genus.tsv","w") #that won't get confusing...
program_output.write(norm_entries)
program_output.close()
