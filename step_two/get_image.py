import os
import SimpleITK as sitk
import cv2
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

def get_image(from_path, save_path, save_id, num_of_heart):
    image = sitk.ReadImage(from_path)
    image_array = sitk.GetArrayFromImage(image)
    label_path = from_path.replace('image', 'label')
    label = sitk.ReadImage(label_path)
    label_array = sitk.GetArrayFromImage(label)

    for i, current_image in enumerate(image_array):
        current_label = label_array[i]
        normalize_image = normalize(current_image, num_of_heart)
        save_name = os.path.join(save_path, 'image_'+str(save_id)+'.png')
        label_bin = current_label > 0
        normalize_image[label_bin == 0] = 0
        cv2.imwrite(save_name, normalize_image*255)
        save_id += 1
        print(save_id)

def get_image_dir(from_path, save_path):
    for i in range(7):
        count = 1
        current_path = save_path+'/'+str(i)
        if not os.path.isdir(current_path):
            os.makedirs(current_path)
        for f_name in [f for f in os.listdir(from_path) if f.endswith('image.nii.gz')]:
            get_image(os.path.join(from_path, f_name), current_path, count*10000, i)
            count += 1

if __name__ == '__main__':
    from_path = constant_model.get_image_from_path
    save_path = constant_model.get_image_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_image_dir(from_path, save_path)
