import SimpleITK as sitk
from PIL import Image
import numpy as np
import constant_model

def score_of_one_part(path_nii, path_png, nii_id):
    image = sitk.ReadImage(path_nii)
    image_array = np.squeeze(sitk.GetArrayFromImage(image))
    sum_M = 0
    sum_S = 0
    sum_M_and_S = 0
    for image_id in range(len(image_array)):
        current_image = image_array[image_id]
        path_test = path_png+'/'+str(10000*nii_id+image_id)+'_niftynet_out.png'
        image_png = Image.open(path_test)
        im_rotate = image_png.rotate(90)
        im_transpose = im_rotate.transpose(Image.FLIP_TOP_BOTTOM)
        image_png = np.array(im_transpose)

        bin_current_image = current_image > 0
        bin_image_png = image_png > 0
        comment_image = (bin_current_image & bin_image_png)
        M = np.sum(bin_current_image)
        S = np.sum(bin_image_png)
        M_and_S = np.sum(comment_image)
        sum_M += M
        sum_S += S
        sum_M_and_S += M_and_S
    return sum_M, sum_S, sum_M_and_S

if __name__ == '__main__':
    average = 0
    for i in range(1, 5):
        print(i)
        label_path = constant_model.score_of_whole_heart_label_path+str(1000+i)+'_label.nii.gz'
        inference_path = constant_model.score_of_whole_heart_inference_path
        M, S, M_and_S = score_of_one_part(label_path, inference_path, i)
        print(M, S, M_and_S, (2*M_and_S)/(M+S))
        average += (2*M_and_S)/(M+S)
    print('average is:', average/4.0)

