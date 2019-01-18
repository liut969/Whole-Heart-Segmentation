import SimpleITK as sitk
import numpy as np
import cv2
import os
import constant_model


def nii_gz_to_png(path_nii, path_png):
    image = sitk.ReadImage(path_nii)
    image_array = np.squeeze(sitk.GetArrayFromImage(image))
    cv2.imwrite(path_png, image_array*255)

if __name__ == '__main__':
    for i in range(7):
        path_from = constant_model.show_result_from_path+str(i)+'/output'
        path_to = constant_model.show_result_save_path+str(i)
        if not os.path.isdir(path_to):
            os.makedirs(path_to)
        for f_name in [f for f in os.listdir(path_from) if f.endswith('.nii.gz')]:
            count = f_name.replace('.nii.gz', '')
            path_nii = os.path.join(path_from, f_name)
            path_png = os.path.join(path_to, count + '.png')
            nii_gz_to_png(path_nii, path_png)
            print(path_nii)
