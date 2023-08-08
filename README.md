
-----------------------------------------

This is a tutorial about BraSyn challenge's setup and specific implementations during the validation and test stages. 

### what is the data format of the test set?
Each patient of the test set has the **same** naming format as the ones in the training and validation sets.  
However, one modality will be randomly dropped during the test stage. 

We provide a python script named _dropout_modality.py_ to show how it works on the validation set. 

Please note that your container will only taking on one folder as the input. You will expect the format like this: 
 

       BraTS-GLI-99999-000

        |  BraTS-GLI-99999-000-t1c.nii.gz

        |  BraTS-GLI-99999-000-t1n.nii.gz

        |  BraTS-GLI-99999-000-t2f.nii.gz
   
In this case, t2w (T2-weighted) is missing   

### how to detect which modality is missing? 
When presenting three image files in each test folder, You will need t 
