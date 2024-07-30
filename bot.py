# bot.py
# Author: Spencer Ye
# Last Revised: July 30th, 2024
# Version: 0.4.3

from selenium import webdriver
import time
import pyautogui
import cv2
import base64
import numpy as np
from pytesseract import image_to_string
from solver import solvable


# CONSTANTS
SIZE_OF_BOX = 100
TOP_CORNER_ONE_X = 15
TOP_CORNER_ONE_Y = 15
TOP_CORNER_TWO_X = 15
TOP_CORNER_TWO_Y = 150
TOP_CORNER_THREE_X = 150
TOP_CORNER_THREE_Y = 15
TOP_CORNER_FOUR_X = 150
TOP_CORNER_FOUR_Y = 150

# Parameters:
#   driver: The web browsers driver
# Returns:
#   img: A image of the playing canvas
def get_driver_image(driver):
    # Identify the canvas
    a = driver.find_element_by_id("canvasID")
    print(type(a))

    # Executes the text as a JavaScript function, which turns the element into a DataURL (a URL that contains data inline) and removes the metadata
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", a)
    print(type(canvas_base64))

    # Convert the DataURL away from b64 format
    cap = base64.b64decode(canvas_base64)
    print(type(cap))

    # Convert the byte array into a image array
    image = cv2.imdecode(np.frombuffer(cap, np.uint8), 1)
    print(type(image))

    # Testing by writing the result down
    cv2.imwrite("result.jpg", image) 

    return image


# Parameters:
#   image: A image of the playing canvas
# Returns:
#   nums: The four numbers currently on the screen
def extract_numbers(image):
    nums = []

    # Crop the image to the proper box containing the first number
    crop_img = image[TOP_CORNER_ONE_Y:(TOP_CORNER_ONE_Y + SIZE_OF_BOX) , TOP_CORNER_ONE_X:(TOP_CORNER_ONE_X + SIZE_OF_BOX)]
   
    # Apply a OTSU binomial threshold to turn turn everything to black or white
    process_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Read the image, aiming to read the image as a line of text
    txt = image_to_string(process_img, config="--psm 7")

    # Strip the text and turn it into a number
    nums.append(int(txt.strip()))

    # Same steps as above for the second number
    crop_img = image[TOP_CORNER_TWO_Y:(TOP_CORNER_TWO_Y + SIZE_OF_BOX) , TOP_CORNER_TWO_X:(TOP_CORNER_TWO_X + SIZE_OF_BOX)]
    process_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    txt = image_to_string(process_img, config="--psm 7")
    nums.append(int(txt.strip()))

    # Same steps as above for the third number
    crop_img = image[TOP_CORNER_THREE_Y:(TOP_CORNER_THREE_Y + SIZE_OF_BOX) , TOP_CORNER_THREE_X:(TOP_CORNER_THREE_X + SIZE_OF_BOX)]
    process_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    txt = image_to_string(process_img, config="--psm 7")
    nums.append(int(txt.strip()))

    # Same steps as above for the fourth number
    crop_img = image[TOP_CORNER_FOUR_Y:(TOP_CORNER_FOUR_Y + SIZE_OF_BOX) , TOP_CORNER_FOUR_X:(TOP_CORNER_FOUR_X + SIZE_OF_BOX)]
    process_img = cv2.threshold(crop_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    txt = image_to_string(process_img, config="--psm 7")
    nums.append(int(txt.strip()))

    return nums

# Parameters:
#   nums: The four numbers currently on the screen
# Returns:
#   operations: Numbers relating to the button that we need to click to solve the question correctly
def calculate_moves(nums):
    print(solvable(nums))
    operators = solvable(nums).split(" ")[::-1]
    index = len(operators) - 1
    moves = []
    while (index >= 0):
        print(operators[index])
        index -= 1
    return operators

# Moves the mouse automatically to the correct places based on the operations
# Parameters:
#   operations: Numbers relating to the button that we need to click to solve the question correctly
# Returns:
#   None
def move_mouse(operations):
    print(operations)
    return


def main():
    # Find and print the size of your current computer screen
    print(pyautogui.size())


    # # Testing Code for Extract Numbers
    # img = cv2.imread('./numbers_test.jpg',0)
    # print(extract_numbers(img))
    # exit(0)

    # Testing Code for calculate moves
    nums = [8, 3, 2, 1]
    print(calculate_moves(nums))
    exit(0)


    # Instantiate the Chrome Driver
    driver = webdriver.Chrome('drivers/chromedriver.exe')

    # Open the website
    driver.get('http://4nums.com/')

    time.sleep(5)

    while(True):
        start_time = time.time()

        img = get_driver_image(driver)

        nums = extract_numbers(img)

        operations = calculate_moves(nums)

        move_mouse(operations)

        end_time = time.time()

        print(end_time - start_time)

    time.sleep(5)
    driver.quit()



if __name__ == "__main__":
    main()