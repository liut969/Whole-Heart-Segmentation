import os
import numpy as np
from scipy.ndimage.morphology import distance_transform_edt
from skimage.io import imsave
from skimage.segmentation import find_boundaries
import SimpleITK as sitk
import constant_model


W_0, SIGMA = 10, 5
def construct_weights_and_mask(img):
    seg_boundaries = find_boundaries(img, mode='inner')
    bin_img = img > 0
    binary_with_borders = np.bitwise_xor(bin_img, seg_boundaries)
    foreground_weight = 1 - binary_with_borders.sum() / binary_with_borders.size
    background_weight = 1 - foreground_weight
    cell_ids = [x for x in np.unique(img)]
    distances = np.zeros((img.shape[0], img.shape[1], len(cell_ids)))
    for i, cell_id in enumerate(cell_ids):
        distances[..., i] = distance_transform_edt(img != cell_id)
    distances.sort(axis=-1)
    if len(distances[0][0]) >= 2:
        weight_map = W_0 * np.exp(-(1 / (2 * SIGMA ** 2)) * ((distances[..., 0] + distances[..., 1]) ** 2))
        weight_map[binary_with_borders] = foreground_weight
        weight_map[~binary_with_borders] += background_weight
    else:
        weight_map = img
    return weight_map

def get_image(from_path, save_path, save_id):
    image = sitk.ReadImage(from_path)
    image_array = sitk.GetArrayFromImage(image)
    for current_image in image_array:
        weight_map = construct_weights_and_mask(current_image)
        save_name_weight = os.path.join(save_path, 'weight_'+str(save_id)+'.tif')
        imsave(save_name_weight, weight_map)
        save_id += 1
        print(save_id)


def get_image_dir(from_path, save_path):
    count = 1
    for f_name in [f for f in os.listdir(from_path) if f.endswith('label.nii.gz')]:
        get_image(os.path.join(from_path, f_name), save_path, count*10000)
        count += 1

if __name__ == "__main__":
    from_path = constant_model.heatmap_from_path
    save_path = constant_model.heatmap_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_image_dir(from_path, save_path)
