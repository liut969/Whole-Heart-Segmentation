import os
import SimpleITK as sitk
import cv2
from PIL import Image
import numpy as np
import constant_model

def normalize(image, num_of_heart):
    max_pixel_values = constant_model.max_pixel_values
    min_pixel_values = constant_model.min_pixel_values
    MIN_BOUND = min_pixel_values[num_of_heart]
    MAX_BOUND = max_pixel_values[num_of_heart]
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image

def get_image(from_path, save_path, path_first_inference, save_id, num_of_heart):
    image = sitk.ReadImage(from_path)
    image_array = sitk.GetArrayFromImage(image)
    for current_image in image_array:
        normalize_image = normalize(current_image, num_of_heart)
        first_inference_image_name = os.path.join(path_first_inference, str(save_id)+'_niftynet_out.png')
        save_name = os.path.join(save_path, 'image_'+str(save_id)+'.png')
        image_first_inference = Image.open(first_inference_image_name)
        im_rotate = image_first_inference.rotate(90)
        im_transpose = im_rotate.transpose(Image.FLIP_TOP_BOTTOM)
        image_first_inference = np.array(im_transpose)
        image_after_first_inference = normalize_image

        # kernel = np.ones((5, 5), np.uint8)
        # image_first_inference_closing = cv2.morphologyEx(image_first_inference, cv2.MORPH_CLOSE, kernel)
        # image_bin = image_first_inference_closing > 0
        image_bin = image_first_inference > 0
        image_after_first_inference[image_bin == 0] = 0
        cv2.imwrite(save_name, image_after_first_inference*255)
        save_id += 1
        print(save_id)

def get_image_dir(from_path, save_path, first_inference_path):
    for i in range(7):
        count = 1
        current_path = save_path+'/'+str(i)
        if not os.path.isdir(current_path):
            os.makedirs(current_path)
        for f_name in [f for f in os.listdir(from_path) if f.endswith('image.nii.gz')]:
            get_image(os.path.join(from_path, f_name), current_path, first_inference_path, count*10000, i)
            count += 1

if __name__ == '__main__':
    from_path = constant_model.get_test_from_path
    first_inference_path = constant_model.get_test_first_inference_path
    save_path = constant_model.get_test_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_image_dir(from_path, save_path, first_inference_path)
