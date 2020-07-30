import numpy as np

def detect_face(preds, image):
    width = image.shape[1]
    height = image.shape[0]
    cube_crop = image[preds[1]:preds[3], preds[0]:preds[2]]
    #cv2.imshow('my_img', cube_crop)

    def detect_color(bgr_pixel):
        colors = {
            "green": [40,150,85],
            "blue": [220,75,40],
            "red": [50,37,125],
            "yellow": [50,140,130],
            "white": [130, 150, 140],
            "orange": [50,70,150]
        }
        score = {"green": 0, "blue": 0, "red": 0, "yellow": 0, "white": 0, "orange": 0}

        for k, v in colors.items():
            color_score = 0

            for i in range(3):
                color_score += abs(v[i] - bgr_pixel[i])
            score[k] = color_score

        return min(score, key=score.get)

    def calculate_most_common_color(colors):
        color_dict = {}
        for color in set(colors):
            color_dict[color] = colors.count(color)
        return max(color_dict, key=color_dict.get)

    def extract_color_info_from_cube_face(cropped_image):
        h, w, c = cropped_image.shape
        patch_height = np.ceil(h / 3).astype(int)
        patch_width = np.ceil(w / 3).astype(int)

        face_info = [[None, None, None], [None, None, None], [None, None, None]]
        i = 0
        for x in range(0, w, patch_width):
            j = 0
            for y in range(0, h, patch_height):

                # Sample 9 pixels for colors and vote
                color_vote = []
                quarter_patch_height = np.ceil(patch_height / 4).astype(int)
                quarter_patch_width = np.ceil(patch_width / 4).astype(int)
                half_patch_height = (np.ceil(patch_height)/2).astype(int)
                half_patch_width = (np.ceil(patch_width)/2).astype(int)

                pixels_to_sample = [
                    cropped_image[y + quarter_patch_height][x + quarter_patch_width],
                    cropped_image[y + (patch_height - quarter_patch_height)][x + quarter_patch_width],
                    cropped_image[y + quarter_patch_height][x + (patch_width - quarter_patch_width)],
                    cropped_image[y + (patch_height - quarter_patch_height)][x + (patch_width - quarter_patch_width)],
                    cropped_image[y + half_patch_height][x + half_patch_width],
                    cropped_image[y + quarter_patch_height][x + half_patch_width],
                    cropped_image[y + half_patch_height][x + quarter_patch_width],
                    cropped_image[y + (patch_height - quarter_patch_height)][x + half_patch_width],
                    cropped_image[y + half_patch_height][x + (patch_width - quarter_patch_width)],
                ]

                for pixel in pixels_to_sample:
                    color_vote.append(detect_color(pixel))

                face_info[j][i] = calculate_most_common_color(color_vote)
                j += 1
            i += 1

        return face_info

    face_info = extract_color_info_from_cube_face(cube_crop)

    return face_info

