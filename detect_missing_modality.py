## This script is an example on how to detect one missing modality given one patient folder, \
## synthesize the missing one with a toy algorithm, and generate the output 

import os
import SimpleITK as sitk 
import shutil

val_folder = '/hdd3/bran/data/pseudo_val_set/BraTS-GLI-00001-000' # only one folder is tested for your container! 
output_folder = '/hdd3/bran/data/output'  #

if not os.path.exists(output_folder):
    os.mkdir(output_folder)

def syntheize_missing_modality(input_path_1, input_path_2, input_path_3, output_path):
    ## this is a toy example to syntheize a missing image by weightedly averaging the intensities of three inputs
    # please define your own algorithm for the BraSyn challenge  

    array_1 = sitk.GetArrayFromImage(sitk.ReadImage(input_path_1))
    array_2 = sitk.GetArrayFromImage(sitk.ReadImage(input_path_2))
    array_3 = sitk.GetArrayFromImage(sitk.ReadImage(input_path_3))
    
    output_array = 0.5*array_1 + 0.3*array_2 + 0.2*array_3
    output_img = sitk.GetImageFromArray(output_array)
    output_img.CopyInformation(sitk.ReadImage(input_path_1))  # so that the output would have the same meta data
    sitk.WriteImage(output_img, output_path)  # please make sure the filename ends with '.nii.gz'
    return 0


file_list = os.listdir(val_folder)
file_list.sort()
full_modality_list = ['t1c', 't1n', 't2f', 't2w']  # the list of four modalities
modality_list = [file_list[0][-10:-7], file_list[1][-10:-7], file_list[2][-10:-7]]
# print(modality_list)
miss_one = list(set(full_modality_list) - set(modality_list))[0]
print('the missing modality is: '+miss_one)

in_path_1 = os.path.join(val_folder, file_list[0])
in_path_2 = os.path.join(val_folder, file_list[1])
in_path_3 = os.path.join(val_folder, file_list[2])
out_path = os.path.join(output_folder, file_list[2][:-10]+miss_one+file_list[2][-7:])
syntheize_missing_modality(in_path_1, in_path_2, in_path_3, out_path)

## now we have generated a fake 3d mri scan 
## please copy the other three files to the output foler!!!!! 
shutil.copyfile(in_path_1, os.path.join(output_folder, file_list[0]))
shutil.copyfile(in_path_2, os.path.join(output_folder, file_list[1]))
shutil.copyfile(in_path_3, os.path.join(output_folder, file_list[2]))





    





    
