# Automatic Whole Heart Segmentation Using a Two-stage U-Net Framework and an Adaptive Threshold Window

If you find this code is useful for your research, please consider citing:
```
@ARTICLE{8737680, 
author={T. {Liu} and Y. {Tian} and S. {Zhao} and X. {Huang} and Q. {Wang}}, 
journal={IEEE Access}, 
title={Automatic Whole Heart Segmentation Using a Two-Stage U-Net Framework and an Adaptive Threshold Window}, 
year={2019}, 
volume={7}, 
number={}, 
pages={83628-83636}, 
keywords={Heart;Image segmentation;Training;Microsoft Windows;Task analysis;Medical diagnostic imaging;Whole heart segmentation;U-Net;adaptive threshold window;segmentation}, 
doi={10.1109/ACCESS.2019.2923318}, 
ISSN={2169-3536}, 
month={},}
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
