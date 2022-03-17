# PASSer2.0

Codes in /src are for the data processing and model training.

For 90 selected proteins, the orinigal files only have PDB IDs, so we use 1-findPDB.py and 2-downloadPDB.py to extract PDB IDs and download corresponding .pdb files.
3-findPockets.py is used with FPocket to identify pockets. 4-collectPocketFeatures.py is used to label the pockets as allosteric or not and save features and labels.

For proteins from ASBench, the original files have a summary .xls file and complex .pdb files. The .xls file was modified a little. asbench_label.py is used to extract the pocket features and label them (in the first run, uncomment the Fpocket command line).

5-autoML.py is the AutoGluon model training file, with several adjustable parameters. train_ak.py is the AutoKeras model training file. Pickle files from both protein lists should be merged together first.
