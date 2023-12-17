import cv2
import numpy as np
import joblib
from tensorflow import keras
# import pytesseract
import matplotlib.pyplot as plt
# %matplotlib inline

def load_digit(digit):
    digit = cv2.resize(digit,(28,28))
    plt.imshow(digit,cmap='gray')
    digit =  digit.flatten()
    digit = np.expand_dims(digit,axis=0)
    digit = digit/ 255.0
    return digit

def load_model():
    return keras.models.load_model("digit_rec_2.h5")

def find_big_contour(contours):
    biggest_cntr = contours[0]
    bigt_area =50
    for i in contours:
        area = cv2.contourArea(i)
        if area > bigt_area :
            bigt_area = area
            biggest_cntr = i
            
    return biggest_cntr

def reorder_points(points):
    new_points = np.zeros((4,1,2))
    points = points.reshape(-1,2)
    new_points[0] = points[np.argmin(np.sum(points,axis=1))]
    new_points[3] = points[np.argmax(np.sum(points,axis=1))]
    new_points[1] = points[np.argmin(np.diff(points,axis=1))]
    new_points[2] = points[np.argmax(np.diff(points,axis=1))]
    return new_points

def segment_img(img):
    rows = np.vsplit(img,9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r,9)
        boxes.extend(iter(cols))
    
    return boxes
    
def extract_sudoku_blocks(image_path):
    sudoku = cv2.imread(image_path)
    gray = cv2.cvtColor(sudoku,cv2.COLOR_BGR2GRAY)
    blur = cv2.blur(gray,(3,3))
    thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    contours,h = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    biggest_cntr = find_big_contour(contours)
    points = reorder_points(biggest_cntr)
    pts1 = np.float32(points)
    pts2 = np.float32([[0,0],[450,0],[0,450],[450,450]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    warped_img = cv2.warpPerspective(sudoku,matrix,(450,450))
    boxes = segment_img(warped_img)
    # plt.imshow(boxes[0])
    recognize_digit(boxes)
    
def recognize_digit(boxes):
    model = load_model()
    sudoku = np.zeros((9,9),dtype=int)
    numbers = []
    for i,box in enumerate(boxes):
        digit = cv2.resize(box,(28,28))
        # digit = cv2.cvtColor(digit,cv2.COLOR_BGR2GRAY)
        _,digit = cv2.threshold(digit,120,255,cv2.THRESH_BINARY_INV)
        # imshow(cv2.resize(digit,(28,28)))
        # plt.imshow(digit,cmap='gray')
        # plt.show()
        digit = np.expand_dims(digit, 0)
        num = np.argmax(model.predict(digit))
        numbers.append(num)
        print(num)
        # print()
        row = i//9
        col = i%9
        sudoku[row,col] = num
    print(sudoku)
    
if __name__ == "__main__":
    image_path = "images\sudoku_2.jpg"  # Replace with the path to your grayscale Sudoku image
    numbers_with_blocks = extract_sudoku_blocks(image_path)

    # for number, block_number in numbers_with_blocks:
    #     print(f"Block {block_number}: {number}")


