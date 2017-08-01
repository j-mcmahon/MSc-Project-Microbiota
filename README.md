# MSc-Project-Microbiota

These scripts take multiple files corresponding to different samples and "join up" the information present, so for example all of the reads counts for a particular species will be on the same line in the output file.
The scripts then normalise the contents of each column of these new files.
Certain entries are also excluded, for example, with phyla data, we don't want "chordata" reads crowding out the bacterial reads.
The "group_abundance_by_phyla.py" and "group_abundaces_by_genus.py" perform an additional step. A dictionary is made of the taxonomy IDs for each phyla/genus found in the file to refer to later.
