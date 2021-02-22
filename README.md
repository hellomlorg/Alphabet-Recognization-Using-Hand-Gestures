# Alphabet-Recognisation-Using-Hand-Gesture

## Overview</br>
This is a simple app to predict the alphabet that is written on screen using an object-of-interest ( a red pen ). Screen act as if like a blackboard . Model is trained on the top of Keras API.  </br>
</br>
## Working Example </br>

![4hdhr3](https://user-images.githubusercontent.com/58811384/95072324-a39d1880-0728-11eb-9170-33855833d08b.gif)

## Technical Aspects</br>
The Project is divided into three parts:</br>
  1-> Make a model using EMNIST Alphabet dataset using Keras to predict the alphabet.</br>
  2-> Take the reference of red colour to draw on the screen . and using a deque to store the point of location where the red coloured object  is moving  and finally predict the alphabet .</br>
  3-> Adding a feature of sound ( to speak the predicted alphabet) . 
  
## YouTube Video (Explanation and demo)

[![Alphabet Recognition Using Hand Gestures](http://img.youtube.com/vi/7YDiblwu_qE/0.jpg)](http://www.youtube.com/watch?v=7YDiblwu_qE "Alphabet Recognition Using Hand Gestures")

## Code Requirements </br>
The code is written in python 3.7 .If you have a lower version of Python you can upgrade using the pip package , ensuring you have the latest version of pip . 
To install the required Packages and libraries , run the command in the project directory after cloning the repository.</br>

### pip install -r requirements.txt
</br>

## Data Description </br>
The "Extended Hello World" of object recognition for machine learning and deep learning is the EMNIST dataset for handwritten letters recognition. It is an extended version of the MNIST dataset.</br>


## Code Explanation </br>
 I have written a tutorial <a href=”#”>post on hello ML </a>explaining the code.</br> 


The small portion of the dataset is shown below.
</br>
![](pic1.jpg)




Each of the letters is stored as a numbered array(28 x 28) as shown below.
![](pic2.JPG)
</br>
 ## Code Execution </br>
 After following the above steps of installation . Open the terminal( cmd, powershell ) in the project directory and use the command </br> 
 ### python Hand Gesture Implementation.py </br>
