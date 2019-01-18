import os
import SimpleITK as sitk
import cv2
import constant_model

def normalize(image):
    MIN_BOUND = constant_model.normalization_min_bound
    MAX_BOUND = constant_model.normalization_max_bound
    image = (image - MIN_BOUND) / (MAX_BOUND - MIN_BOUND)
    image[image > 1] = 1.
    image[image < 0] = 0.
    return image

def get_image(from_path, save_path, save_id):
    image = sitk.ReadImage(from_path)
    image_array = sitk.GetArrayFromImage(image)
    for current_image in image_array:
        normalize_image = normalize(current_image)
        save_name = os.path.join(save_path, 'test_image_'+str(save_id)+'.png')
        cv2.imwrite(save_name, normalize_image*255)
        save_id += 1
        print(save_id)

def get_image_dir(from_path, save_path):
    count = 1
    for f_name in [f for f in os.listdir(from_path) if f.endswith('image.nii.gz')]:
        get_image(os.path.join(from_path, f_name), save_path, count*10000)
        count += 1

if __name__ == '__main__':
    from_path = constant_model.get_test_from_path
    save_path = constant_model.get_test_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_image_dir(from_path, save_path)
