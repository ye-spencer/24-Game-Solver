# bot.py
# Author: Spencer Ye
# Last Revised: July 29th, 2024
# Version: 0.3.2

from selenium import webdriver
import time
import pyautogui
import cv2
import base64
import numpy as np
from pytesseract import image_to_string


# CONSTANTS
SIZE_OF_BOX = 107
TOP_CORNER_ONE_X = 13
TOP_CORNER_ONE_Y = 13
TOP_CORNER_TWO_X = 13
TOP_CORNER_TWO_Y = 147
TOP_CORNER_THREE_X = 147
TOP_CORNER_THREE_Y = 13
TOP_CORNER_FOUR_X = 147
TOP_CORNER_FOUR_Y = 147

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
    print(type(image))
    return []

# Parameters:
#   nums: The four numbers currently on the screen
# Returns:
#   operations: Numbers relating to the button that we need to click to solve the question correctly
def calculate_moves(nums):
    print(nums)
    return []

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



    img = cv2.imread('./numbers_test.jpg',0)
    cv2.imshow('image',img)
    cv2.waitKey(0)

    crop_img = img[TOP_CORNER_FOUR_Y:(TOP_CORNER_FOUR_Y + SIZE_OF_BOX) , TOP_CORNER_FOUR_X:(TOP_CORNER_FOUR_X + SIZE_OF_BOX)]
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)

    txt = image_to_string(crop_img, config="--psm 7")
    print(txt)

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