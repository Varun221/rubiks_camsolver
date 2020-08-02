# Rubiks_Camsolver
A Rubiks Cube Solver that extracts colors on the face through webcam and prints out the solution moves ([working here](https://drive.google.com/file/d/14BqmjE04Cx_08AcqI3nNJ6N8w7c7IXnF/view?usp=sharing)).
The Algorithm used to solve the rubiks cube is Kociemba Algorithm ([read here](https://ruwix.com/the-rubiks-cube/herbert-kociemba-optimal-cube-solver-cube-explorer/)).

# Working
The Face of the cube is detected by Tiny YOLOv3 model trained on custom data prepared by Phone captures. The images were then labeled using [labelImg](https://github.com/tzutalin/labelImg) and the annotations were generated. \
A Tiny YOLOv3 model was then trained using this Awesome Repo, [TrainYourOwnYOLO](https://github.com/AntonMu/TrainYourOwnYOLO). The training process and explanation can be found in the [notebook](https://github.com/Varun221/rubiks_camsolver/blob/master/rubiks_camsolver_training.ipynb) given above. 
After the training the weights file was generated ([you can find it here](https://drive.google.com/file/d/1kFoPiE-IZl9eVfnV3zGOFlW5M3_sB6Rd/view?usp=sharing)), it was used along with the inference code in [this](https://github.com/AntonMu/TrainYourOwnYOLO) repo to detect the faces of the cube in a video.  \
Once the cube face is detected, the box image is cropped and the colors of the faces are found. The colors of the faces are then used to generate Cube string which denotes the positions of the pieces of the cube. \
To solve the cube, I used the library [rubiks_solver](https://github.com/Wiston999/python-rubik) which generates solutions for the cube in various methods.

# Detecting the Face colors
The bounding box generated from tiny YOLOv3 was cropped to get a tight crop of the cube face. The face was then divided into 9 patches. From each patch I generated 9 sample pixels, the color of these pixels was found using its "Distance" from the predefined colors of the cube. Once the colors of the Pixels are found, the final color of the patch is decided through voting. This same process is applied on the 9 patches of a face and the colors of the face are found.

# Usage
1. If you want to use this project. I recommend using a virtual environment. The process can be found [here](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/).
2. Once you have activated the virtual environment, Clone this repository, extract it if you downloaded a .zip or .tar file and cd into the cloned repository.
```bash
cd C:\rubiks_camsolver 
```
3. Install the Requirements file
```bash
pip install -r requirements.txt
```
4. Download the weights file from [here](https://drive.google.com/file/d/1kFoPiE-IZl9eVfnV3zGOFlW5M3_sB6Rd/view?usp=sharing) and put it inside " detect_data " folder.
5. Run the detector
```bash
python Detector.py
```
6. Ignore the Deprecation warnings. You may not find a good color detection because of lighting conditions. To tune the detection values, take a screenshot of the video feed containing your cube, name it "Screenshot". 
7. Then run the color_tuner.py script. This opens up your screenshot. Click on any one color of the cube for example, yellow, keep clicking on various points of the yellow color, you can see that various values are printed on the terminal. These are the BGR values of the yellow in the image.
8. Adjust the values in the face_detect.py script in the color dictionary. Do so for each color.
9. Once done, you will have a working Rubiks cube solver.

# References
### YOLO TRAINING
1. https://github.com/AntonMu/TrainYourOwnYOLO
2. https://github.com/zzh8829/yolov3-tf2 
### RUBIKS CUBE SOLVING
1. https://github.com/Wiston999/python-rubik
2. https://github.com/mazenkurdi/rubiks-cube-solver
3. https://github.com/pglass/cube
