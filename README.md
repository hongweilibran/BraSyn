
-----------------------------------------

This is a tutorial about BraSyn challenge's setup and specific implementations during the validation and test stages. 

### Data format of the test set
Each patient in the test set has the **same** naming format as the ones in the training and validation sets.  
However, one modality will be randomly dropped during the test stage. 

We provide a Python script named _dropout_modality.py_ to show how it works on the validation set. 

Please note that your container will only take on one folder as the input and be iterated on the whole test set. You will expect the format like this: 
 

       BraTS-GLI-99999-000

        |  BraTS-GLI-99999-000-t1c.nii.gz

        |  BraTS-GLI-99999-000-t1n.nii.gz

        |  BraTS-GLI-99999-000-t2f.nii.gz
   
In this case, t2w (T2-weighted) is missing   

### Detecting missing modality during inference 
When presenting three image files in each test folder, if you wish to automatically figure out which one is missing, we provide a script to do it. Please check _detect_missing_modality.py_. 

Please note that after synthesizing the missing one, you **DO NOT need to copy** the other three files to the output folder. Please check the end of the Python script. This is because we will do automated segmentation based on the four modalities afterward.

### Performing segmentation using the synthetic image as a part of the input
After generating the missing image, segmentation can be performed by taking three real modalities + the missing modality as the input. 
We use the **[FeTS Consensus Models](https://github.com/FeTS-AI/Front-End/releases/tag/1.0.1 )** for image segmentation, the command is:  

```ruby
${fets_root_dir}/bin/FeTS_CLI_Segment -d /path/to/output/DataForFeTS \ # data directory after invoking ${fets_root_dir}/bin/PrepareDataset

  -a fets_singlet,fets_triplet \ # can be used with all pre-trained models currently available in FeTS

  -lF STAPLE,ITKVoting,SIMPLE,MajorityVoting \ # if a single architecture is used, this parameter is ignored

  -g 1 \ # '0': cpu, '1': request gpu

  -t 0 # '0': inference mode, '1': training mode
```
