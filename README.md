# Automatic Whole Heart Segmentation Using a Two-stage U-Net Framework and an Adaptive Threshold Window

If you find this code is useful for your research, please consider citing:
```
@article{liu2019automatic,
  title={Automatic Whole Heart Segmentation Using a Two-stage U-Net Framework and an Adaptive Threshold Window},
  author={Liu, Tao and Tian, Yun and Zhao, Shifeng and Huang, Xiaoying and Wang, Qingjun},
  journal={IEEE Access},
  year={2019},
  publisher={IEEE}
}
```

## Installation
```
python 3.5
tensorflow-gpu	1.12.0
NiftyNet	0.4.0
```
[download the data set](http://www.sdspeople.fudan.edu.cn/zhuangxiahai/0/mmwhs17/data1.html) to ``` ./data ```

![](https://github.com/liut969/Whole-Heart-Segmentation/blob/master/data/temp/result.gif?raw=true)

## Step one
1. Get train image：```python step_one/get_image.py```  
2. Get label image：```python step_one/get_label.py```  
3. Get weight map：```python step_one/heatmap.py```
4. Get test image: ```python step_one/get_test.py``` 
5. Run the configuration file for training: ```python net_segment.py train -c ini/train_whole_heart.ini```
6. Run the configuration for inference：```python net_segment.py inference -c ini/inference_whole_heart.ini```
7. Display results：```python step_one/show_result.py```
8. View score：```python step_one/score_of_whole_heart.py```  
## Step two
1. Get train image：```python step_two/get_image.py```  
2. Get label image：```python step_two/get_label.py```  
3. Get weight map：```python step_two/heatmap,py```
4. Get test image: ```python step_two/get_test.py``` 
5. Run the configuration file for training:
- ```python net_segment.py train -c ini/train_0.ini```
- ```python net_segment.py train -c ini/train_1.ini```
- ```python net_segment.py train -c ini/train_2.ini```
- ```python net_segment.py train -c ini/train_3.ini```
- ```python net_segment.py train -c ini/train_4.ini```
- ```python net_segment.py train -c ini/train_5.ini```
- ```python net_segment.py train -c ini/train_6.ini```
6. Run the configuration for inference：
- ```python net_segment.py nference -c ini/inference_0.ini```
- ```python net_segment.py inference -c ini/inference_1.ini```
- ```python net_segment.py inference -c ini/inference_2.ini```
- ```python net_segment.py inference -c ini/inference_3.ini```
- ```python net_segment.py inference -c ini/inference_4.ini```
- ```python net_segment.py inference -c ini/inference_5.ini```
- ```python net_segment.py inference -c ini/inference_6.ini```
7. Display results：```python step_two/show_result.py```
8. View score：```python step_two/score_of_ever_part.py```  
