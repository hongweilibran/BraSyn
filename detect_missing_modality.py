## This script is an example on how to detect missing modalities, \
## synthesize missing ones with a toy algorithm, and generate the outputs 

import os

val_set_missing = '/hdd3/bran/data/pseudo_val_set'
folder_list = os.listdir(val_set_missing)
modality_list = ['t1c', 't1n', 't2f', 't2w']  # the list of four modalities

def syntheize_missing_modality(input_1, input_2, input_3):
    ## this is a toy example to syntheize a missing image by linearly combinng the intensities of the three inputs
    # please define your own algorithm for the BraSyn challenge  
    output = 0.5*input_1 + 0.3*input_2 + 0.2*input_3
    
    return output


for ff in folder_list:
    print(ff)
