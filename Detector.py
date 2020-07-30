import os
from yolo import YOLO
from PIL import Image
import time
from face_detect import detect_face
import cv2.cv2 as cv2
import random
from cube_solve import solve_cube, generate_cube_string, verify_cube_string_is_valid


os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

Class_file = "detect_data/label.names"
Anchor_file = "detect_data/yolo_tiny_anchors.txt"
weights_file = "detect_data/trained_weights_final.h5"

# define YOLO detector
yolo = YOLO(
    **{
        "model_path": weights_file,
        "anchors_path": Anchor_file,
        "classes_path": Class_file,
        "score": 0.5,
        "gpu_num": 1,
        "model_image_size": (416, 416),
    }
)

# same colors as face_detect.py
colors = {
    "green": [35, 170, 80],
    "blue": [220, 75, 40],
    "red": [50, 37, 125],
    "yellow": [50, 140, 130],
    "white": [230, 150, 140],
    "orange": [50, 70, 150]
}
random_color = random.choice(list(colors.values()))

faces = {'up': None, 'left': None, 'front': None, 'right': None, 'back': None, 'down': None}

# ONE IMPORTANT THING TO REMEMBER IS OPENCV HAS BGR IMAGES AND PILLOW HAS RGB IMAGES
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
while(ret):
    ret, frame = cap.read()

    """ Detection of image"""
    # converting to pillow format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_pillow = Image.fromarray(frame_rgb)
    preds, det_frame_pillow = yolo.detect_image(frame_pillow, show_stats=False)
    #back to opencv
    #frame_rgb = np.asarray(det_frame_pillow)
    #det_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    frame[-100:, :] = [0,0,0]
    frame = cv2.putText(frame, "LETS SOLVE THE CUBE!", (0,410), cv2.FONT_HERSHEY_COMPLEX,
                        1, (0,255,0), thickness=2)


    for k,v in faces.items():
        if faces[k] == None:
            frame = cv2.putText(frame,
                                "Press {} to load up {} face".format(k[0], k.upper()),
                                (0,450), cv2.FONT_HERSHEY_COMPLEX,
                                 1, random_color, thickness=2)
            break

    if not len(preds):
        pane = frame[:90, -90:]
        pane[:,:] = [0,0,0]
        frame[:90, -90:] = pane
    else:
        face_info = detect_face(preds[0], frame)
        #print(face_info)

        # DISPLAYTING THE FACE BEING READ
        pane = frame[:90, -90:]
        pane[:,:] = [0,0,0]

        for i in range(3):
            for j in range(3):
                if (2-j):
                    pane[i*30 : (i+1)*30, -(3-j)*30:-(2-j)*30] = colors[face_info[i][j]]
                else:
                    pane[i*30 : (i+1)*30, -(3-j)*30:] = colors[face_info[i][j]]

        frame[:90, -90:] = pane

        fac_key = cv2.waitKey(1)
        if fac_key == ord('u'):
            faces['up'] = face_info
            print("Got up face - ", face_info)

            print("Want to reload? (y/n)")
            stat_u = cv2.waitKey()
            if stat_u == ord('y'):
                faces['up'] = None
                print("Let's load again then")
            else:
                print("Great! keep going!")

        if fac_key == ord('l'):
            faces['left'] = face_info
            print("Got left face - ", face_info)

            print("Want to reload? (y/n)")
            stat_l = cv2.waitKey()
            if stat_l == ord('y'):
                faces['left'] = None
                print("Let's load again then")
            else:
                print("Great! keep going!")

        if fac_key == ord('f'):
            faces['front'] = face_info
            print("Got front face - ", face_info)

            print("Want to reload? (y/n)")
            stat_f = cv2.waitKey()
            if stat_f == ord('y'):
                faces['front'] = None
                print("Let's load again then")
            else:
                print("Great! keep going!")

        if fac_key == ord('r'):
            faces['right'] = face_info
            print("Got right face - ", face_info)

            print("Want to reload? (y/n)")
            stat_r = cv2.waitKey()
            if stat_r == ord('y'):
                faces['right'] = None
                print("Let's load again then")
            else:
                print("Great! keep going!")

        if fac_key == ord('b'):
            faces['back'] = face_info
            print("Got back face - ", face_info)

            print("Want to reload? (y/n)")
            stat_b = cv2.waitKey()
            if stat_b == ord('y'):
                faces['back'] = None
                print("Let's load again then")
            else:
                print("Great! keep going!")

        if fac_key == ord('d'):
            faces['down'] = face_info
            print("Got down face - ", face_info)

            print("Want to reload? (y/n)")
            stat_d = cv2.waitKey()
            if stat_d == ord('y'):
                faces['down'] = None
                print("Let's load again then")
            else:
                print("Yay! YOU LOADED ALL THE FACES.\n\n PRESENTING YOU THE SOLUTION NOW - ")

        if list(faces.values()).count(None) == 0:
            cube_string = generate_cube_string(faces)
            validity = verify_cube_string_is_valid(cube_string)
            if not validity:
                break
            print("Faces recorded - \n", faces)
            moves = solve_cube(faces)
            print(f"Solution: \n{moves}\n")
            print("For notation reference, visit https://ruwix.com/the-rubiks-cube/notation/")
            time.sleep(2)
            break




    frame = cv2.putText(frame, "KEEP YOUR FRONT AS RED AND TOP AS YELLOW", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0,0,255), thickness=2)
    cv2.imshow('cube_detection', frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()

























