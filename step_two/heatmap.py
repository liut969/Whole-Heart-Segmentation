import os
import numpy as np
from scipy.ndimage.morphology import distance_transform_edt
from skimage.segmentation import find_boundaries
import SimpleITK as sitk
from skimage.io import imsave
import constant_model

W_0, SIGMA = 10, 5

def construct_heatmap_whole_heart(img):
    seg_boundaries = find_boundaries(img, mode='inner')
    bin_img = img > 0
    binary_with_borders = np.bitwise_xor(bin_img, seg_boundaries)
    foreground_weight = 1 - binary_with_borders.sum() / binary_with_borders.size
    background_weight = 1 - foreground_weight
    cell_ids = [x for x in np.unique(img) if x > 0]
    distances = np.zeros((img.shape[0], img.shape[1], len(cell_ids)))
    for i, cell_id in enumerate(cell_ids):
        distances[..., i] = distance_transform_edt(img != cell_id)
    distances.sort(axis=-1)
    if len(distances[0][0]) >= 2:
        weight_map = W_0 * np.exp(-(1 / (2 * SIGMA ** 2)) * ((distances[..., 0] + distances[..., 1]) ** 2))
        weight_map[binary_with_borders] = foreground_weight
        weight_map[~binary_with_borders] += background_weight
    else:
        weight_map = np.zeros(img.shape)
    return weight_map

def construct_heatmap_part(img, part_id):
    values_of_label = constant_model.values_of_label
    current_value_of_label = values_of_label[part_id]
    cell_ids = [x for x in np.unique(img)]
    if current_value_of_label in cell_ids:
        img = (img == current_value_of_label)
        seg_boundaries = find_boundaries(img, mode='inner')
        bin_img = img > 0
        binary_with_borders = np.bitwise_xor(bin_img, seg_boundaries)
        foreground_weight = 1 - binary_with_borders.sum() / binary_with_borders.size
        background_weight = 1 - foreground_weight
        img_background = ~img
        distances = np.zeros((img.shape[0], img.shape[1], 2))
        distances[..., 0] = distance_transform_edt(~img)
        distances[..., 1] = distance_transform_edt(~img_background)
        distances.sort(axis=-1)
        weight_map = W_0 * np.exp(-(1 / (2 * SIGMA ** 2)) * ((distances[..., 0] + distances[..., 1]) ** 2))
        weight_map[binary_with_borders] = foreground_weight
        weight_map[~binary_with_borders] += background_weight
    else:
        weight_map = np.zeros(img.shape)
    return weight_map

def get_image(from_path, save_path, save_id, part_id):
    image = sitk.ReadImage(from_path)
    image_array = sitk.GetArrayFromImage(image)
    for current_image in image_array:
        save_name_weight = os.path.join(save_path, 'weight_'+str(save_id)+'.tif')
        weight_map_part = construct_heatmap_part(current_image, part_id)
        weight_map_whole_heart = construct_heatmap_whole_heart(current_image)
        weight_map = weight_map_whole_heart + weight_map_part
        imsave(save_name_weight, weight_map)
        save_id += 1
        print(save_id)


def get_image_dir(from_path, save_path, part_id):
    count = 1
    for f_name in [f for f in os.listdir(from_path) if f.endswith('label.nii.gz')]:
        get_image(os.path.join(from_path, f_name), save_path, count*10000, part_id)
        count += 1

if __name__ == "__main__":
    from_path = constant_model.heatmap_from_path
    for i in range(7):
        save_path = constant_model.heatmap_save_path+'/'+str(i)
        if not os.path.isdir(save_path):
            os.makedirs(save_path)
        get_image_dir(from_path, save_path, i)
