
from torchmetrics.image import StructuralSimilarityIndexMeasure
import torch
import numpy as np
import SimpleITK as sitk 

# Define evaluation Metrics
ssim = StructuralSimilarityIndexMeasure(return_full_image=True)

def __percentile_clip(input_tensor, reference_tensor=None, p_min=0.5, p_max=99.5, strictlyPositive=True):
    """Normalizes a tensor based on percentiles. Clips values below and above the percentile.
    Percentiles for normalization can come from another tensor.

    Args:
        input_tensor (torch.Tensor): Tensor to be normalized based on the data from the reference_tensor.
            If reference_tensor is None, the percentiles from this tensor will be used.
        reference_tensor (torch.Tensor, optional): The tensor used for obtaining the percentiles.
        p_min (float, optional): Lower end percentile. Defaults to 0.5.
        p_max (float, optional): Upper end percentile. Defaults to 99.5.
        strictlyPositive (bool, optional): Ensures that really all values are above 0 before normalization. Defaults to True.

    Returns:
        torch.Tensor: The input_tensor normalized based on the percentiles of the reference tensor.
    """
    if(reference_tensor == None):
        reference_tensor = input_tensor
    v_min, v_max = np.percentile(reference_tensor, [p_min,p_max]) #get p_min percentile and p_max percentile

    if( v_min < 0 and strictlyPositive): #set lower bound to be 0 if it would be below
        v_min = 0
    output_tensor = np.clip(input_tensor,v_min,v_max) #clip values to percentiles from reference_tensor
    output_tensor = (output_tensor - v_min)/(v_max-v_min) #normalizes values to [0;1]

    return output_tensor

            

def compute_metrics(gt_image: torch.Tensor, prediction: torch.Tensor, mask: torch.Tensor, normalize=True):
    """Computes MSE, PSNR and SSIM between two images only in the masked region.

    Normalizes the two images to [0;1] based on the gt_image 0.5 and 99.5 percentile in the non-masked region.
    Requires input to have shape (1,1, X,Y,Z), meaning only one sample and one channel.
    For SSIM, we first separate the input volume to be tumor region and non-tumor region, then we apply regular SSIM on the complete volume. In the end we take
    the two volumes.

    Args:
        gt_image (torch.Tensor): The ground truth image (***.nii.gz)
        prediction (torch.Tensor): The inferred/predicted image
        mask (torch.Tensor): The segmentation mask (seg.nii.gz)
        normalize (bool): Normalizes the input by dividing trough the maximal value of the gt_image in the masked
            region. Defaults to True

    Raises:
        UserWarning: If you dimensions do not match the (torchmetrics) requirements: 1,1,X,Y,Z

    Returns:
        float: (SSIM_tumor, SSIM_non_tumor)
    """

    if not (prediction.shape[0] == 1 and prediction.shape[1] == 1):
        raise UserWarning(f"All inputs have to be 5D with the first two dimensions being 1. Your prediction dimension: {prediction.shape}")
    
    # Normalize to [0;1] individually after intensity clipping
    if normalize:
        gt_image = __percentile_clip(gt_image, p_min=0.5, p_max=99.5, strictlyPositive=True)
        prediction = __percentile_clip(prediction, p_min=0.5, p_max=99.5, strictlyPositive=True)

    mask[mask>0] = 1
    mask = mask.type(torch.int64)
    # Get Infill region (we really are only interested in the infill region)
    prediction_tumor = prediction * mask
    gt_image_tumor = gt_image * mask

    prediction_non_tumor = prediction * (1-mask)
    gt_image_non_tumor = gt_image * (1-mask)

 
    # SSIM - apply on complete masked image but only take values from masked region
    ssim_idx_full_image = ssim(preds=prediction_tumor, target=gt_image_tumor)
    ssim_idx = ssim_idx_full_image[mask]
    SSIM_tumor = ssim_idx.mean()

    ssim_idx_full_image = ssim(preds=prediction_non_tumor, target=gt_image_non_tumor)
    ssim_idx = ssim_idx_full_image[1 - mask]
    SSIM_non_tumor = ssim_idx.mean()

    return float(SSIM_tumor), float(SSIM_non_tumor)




real_path = 'data/reference/BraTS-GLI-00000-000/BraTS-GLI-00000-000-t1n.nii.gz'
syn_path = 'data/output/BraTS-GLI-00000-000/BraTS-GLI-00000-000-t1n.nii.gz'
seg_path = 'data/reference/BraTS-GLI-00000-000/BraTS-GLI-00000-000-seg.nii.gz'

array_real = sitk.GetArrayFromImage(sitk.ReadImage(real_path))
array_syn = sitk.GetArrayFromImage(sitk.ReadImage(syn_path))
array_seg = sitk.GetArrayFromImage(sitk.ReadImage(seg_path))

array_real = array_real[np.newaxis, np.newaxis, ...]
array_syn = array_syn[np.newaxis, np.newaxis, ...]
array_seg = array_seg[np.newaxis, np.newaxis, ...]

print(np.shape(array_real))

array_real = torch.tensor(array_real)
array_syn = torch.tensor(array_syn)
array_seg = torch.tensor(array_seg)


SSIM_tumor, SSIM_non_tumor = compute_metrics(array_real, array_syn,array_seg, normalize=True)

print(SSIM_tumor)
print(SSIM_non_tumor)


