import os
import SimpleITK as sitk
import cv2
import constant_model

def get_label(from_path, save_path, save_id, num_of_heart):
    values_of_label = constant_model.values_of_label
    current_label_value = values_of_label[num_of_heart]
    label = sitk.ReadImage(from_path)
    label_array = sitk.GetArrayFromImage(label)
    for current_label in label_array:
        save_binary_label_name = os.path.join(save_path, 'label_bin_'+str(save_id)+'.png')
        save_image = current_label == current_label_value
        save_image = save_image.astype(int)
        cv2.imwrite(save_binary_label_name, save_image)
        save_id += 1
        print(save_id)

def get_label_dir(from_path, save_path):
    for i in range(7):
        count = 1
        current_path = save_path+'/'+str(i)
        if not os.path.isdir(current_path):
            os.makedirs(current_path)
        for f_name in [f for f in os.listdir(from_path) if f.endswith('label.nii.gz')]:
            get_label(os.path.join(from_path, f_name), current_path, count*10000, i)
            count += 1

if __name__ == '__main__':
    from_path = constant_model.get_label_from_path
    save_path = constant_model.get_label_save_path
    if not os.path.isdir(save_path):
        os.makedirs(save_path)
    get_label_dir(from_path, save_path)
