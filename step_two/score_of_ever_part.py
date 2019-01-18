import SimpleITK as sitk
from PIL import Image
import numpy as np
import cv2
import csv
import constant_model


def score_of_one_part(path_nii, path_png, nii_id, part_id):
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
        kernel = np.ones((5, 5), np.uint8)
        image_png = cv2.morphologyEx(image_png, cv2.MORPH_CLOSE, kernel)

        bin_current_image = current_image == constant_model.values_of_label[part_id]
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
    scores = np.zeros([5, 8])
    for i in range(7):
        average = 0
        print('current_patt: ', i)
        for j in range(1, 5):
            print(j)
            label_path = constant_model.score_of_ever_part_label_path+str(1000+j)+'_label.nii.gz'
            inference_path = constant_model.score_of_ever_part_inference_path+str(i)
            M, S, M_and_S = score_of_one_part(label_path, inference_path, j, i)
            current_score = (2*M_and_S)/(M+S)
            print(M, S, M_and_S, current_score)
            average += current_score
            scores[j-1, i] = round(current_score, 3)
        average /= 4.0
        print('average is:', average)
        scores[4, i] = round(average, 3)

    for i in range(5):
        scores[i, 7] = round(np.sum(scores[i, ...])/7.0, 3)

    headers = ['LV', 'Myo', 'RV', 'LA', 'RA', 'aorta', 'PA', 'WHS']
    with open(constant_model.score_of_ever_part_save_csv_name, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(scores)
