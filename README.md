# Determination of the Level or Volume of Sugarcane Bagasse using Image Processing

## :books: Libraries (requirements.txt)
- certifi==2020.6.20
- numpy==1.19.2
- opencv-contrib-python==4.4.0.44
- opencv-python==4.4.0.44
- wincertstore==0.2

Install the libraries needed for this work:

        { pip install -r requirements.txt }        

## :heavy_check_mark: Run First Steps

#### 1. Clone repository
Clone this repository from Github. 

#### 2. Detect level
##### 2.1 Command to detect coins Brazilian Real:
        { python main.py }

##### 2.2 Command to detect coins Dollar:
        { python main.py -o dollar }

#### 3. Result images above


#### Visor
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/visor.jpeg)

#### Camera installed
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/visorAcoplado.jpg)

Steps : a) BGR image. b) BGR to Gray. c) Detect circle with hough transform. d) Remove noises with medianBlur. e) Crop the center circle. f) Binary image. 
#### Result: 0% Level
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/level0.jpg)

#### Result: 50.65% Level
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/level50.jpg)

#### Result: 78.10% Level
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/level78.jpg)

#### Result: 100% Level
![alt text](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/level100.jpg)


See [the video no Youtube](https://www.youtube.com/watch?v=Rsdjpf3Vr3Q).
#### Result in real time:
![](https://github.com/eduardocarnunes/level-or-volume-sugarcane-bagasse/blob/master/images/video.gif)
