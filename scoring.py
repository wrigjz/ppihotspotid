#!/usr/bin/python3
###################################################################################################
## Karen Sarkisyan, IBMS, Academia Sinica, Taipei, 11529, Taiwan
## Modified by Jon Wright, ex-IBMS, Academia Sinica, Taipei, 11529, Taiwan to fit CR system
###################################################################################################
# Simple script to used a pretrained ML (Autogluon) model to predict critical residues
# This reads from the assemble.txt file and gives results to results_ambnum.txt file
# The location of the trained model is passed as the 1st command line argument to the script
# The predictions are made using Residue type, sasa, gas phase energy and conservation

import sys
import pandas as pd
from autogluon.tabular import TabularDataset, TabularPredictor

# set the location of the pretrained ML model
MODEL_FOLDER_PATH = sys.argv[1]

# Set the inputs to come from the the assemble.txt
ASSEMBLE_FILE_PATH = "./assemble.txt"

# Set the output location
CSV_PREDICTIONS_OUTPUT_PATH = "./results_ambnum.txt"

# Here we setup the inputs we need
INDATA = pd.read_csv(ASSEMBLE_FILE_PATH,delim_whitespace=True)
PRED_DATA = INDATA[['Ty','cons','sasa','gas_e']]

# Load the model and make the actual prediction
PREDICTOR = TabularPredictor.load(MODEL_FOLDER_PATH, require_py_version_match=False)
PREDICTIONS = PREDICTOR.predict(PRED_DATA)

# Write out the results
RESULT = INDATA[['Ty','Resi']].join(PREDICTIONS)
RESULT.set_axis(["Ty","Resi","Critical"], axis="columns", inplace=True)
POSITIVES = RESULT.loc[RESULT['Critical'] == 'P']
POSITIVES.to_csv(CSV_PREDICTIONS_OUTPUT_PATH,header=None, index=False)
