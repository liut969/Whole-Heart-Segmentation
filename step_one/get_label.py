import os
import SimpleITK as sitk
from skimage.io import imsave
import numpy as np
from skimage.segmentation import find_boundaries
import constant_model

def get_label(from_path, save_path, save_id):
    label = sitk.ReadImage(from_path)
    label_array = sitk.GetArrayFromImage(label)
    for current_image in label_array:
        save_name = os.path.join(save_path, 'train_label_'+str(save_id)+'.png')
        seg_bounderies = find_boundaries(current_image, mode='inner')
        bin_img = current_image > 0
        binary_with_borders = np.bitwise_xor(bin_img, seg_bounderies)
        imsave(save_name, binary_with_borders)
        save_id += 1
        print(save_id)


def get_label_dir(from_path, save_path):
    count = 1
    for f_name in [f for f in os.listdir(from_path) if f.endswith('label.nii.gz')]:
        get_label(os.path.join(from_path, f_name), save_path, count*10000)
        count += 1

if __name__ == '__main__':
    from_path = constant_model.get_label_from_path
    save_path = constant_model.get_label_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_label_dir(from_path, save_path)
