import cv2.cv2 as cv2

# prints the bgr values when clicked on the image.

img = cv2.imread('screenshot.png')

def nothing(x):
    pass
def callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.putText(img, str(img[y,x]), (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0) )
        print(img[y,x])

cv2.namedWindow('image')
cv2.setMouseCallback('image', callback)
while True:
    cv2.imshow('image', img)
    if cv2.waitKey(1) == 27:
        break
cv2.destroyAllWindows()
