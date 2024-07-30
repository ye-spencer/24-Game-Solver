# bot.py
# Author: Spencer Ye
# Last Revised: July 30th, 2024
# Version: 0.5.4

from selenium import webdriver
import time
import pyautogui
import cv2
import base64
import numpy as np
from pytesseract import image_to_string
from solver import solvable
from collections import deque 


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

    # Executes the text as a JavaScript function, which turns the element into a DataURL (a URL that contains data inline) and removes the metadata
    canvas_base64 = driver.execute_script("return arguments[0].toDataURL('image/png').substring(21);", a)

    # Convert the DataURL away from b64 format
    cap = base64.b64decode(canvas_base64)

    # Convert the byte array into a image array
    image = cv2.imdecode(np.frombuffer(cap, np.uint8), 1)

    # # Testing by writing the result down
    # cv2.imwrite("result.jpg", image) 

    return image


# Parameters:
#   image: A image of the playing canvas
# Returns:
#   nums: The four numbers currently on the screen
def extract_numbers(image):
    nums = []

    # Convert the image into gray scale
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

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
#   operations: A list of symbols relating to the button that we need to click to solve the question correctly
def calculate_moves(nums):
    
    # Solve the set of numbers and split to get each operator
    operators = solvable(nums).split(" ")

    # Convert the numbers into a string so we can index it later
    nums_str = [str(i) for i in nums]

    # Replace each number with the box number
    operators = [str(nums_str.index(ch)) if ch.isdigit() else ch for ch in operators]
    

    moves = []
    operation_deque = deque()

    # For each symbol
    for operator in operators:
        if operator == '(': # Ignore if it is an opening bracket
            continue
        elif operator == ')': # If it is a closing bracket
            # Pop the last three symbols, which should be two numbers and a operation, and append them to the moves we need to make
            op_two = operation_deque.pop()
            op = operation_deque.pop()
            op_one = operation_deque.pop()
            moves.append(op_one)
            moves.append(op)
            moves.append(op_two)

            # Append the last box, since the new value is now held in that box
            operation_deque.append(op_two)
        else: # If it is an operator, append it to the operation queue
            operation_deque.append(operator)
    return moves

# Moves the mouse automatically to the correct places based on the operations
# Parameters:
#   operations: Numbers relating to the button that we need to click to solve the question correctly
# Returns:
#   None
def move_mouse(operations):
    for operation in operations:
        if operation == '0':
            continue
        elif operation == '1':
            continue
        elif operation == '2':
            continue
        elif operation == '3':
            continue
        elif operation == '+':
            continue
        elif operation == '-':
            continue
        elif operation == '*':
            continue
        elif operation == '/':
            continue
        else:
            print("ERROR UNRECOGNIZED OPERATION IN MOVE MOUSE")
    # Click submit button


def main():
    
    # Find the size of your current computer screen
    screen_size = pyautogui.size()
    screen_height = screen_size.height
    screen_width = screen_size.width

    # Instantiate the Chrome Driver
    driver = webdriver.Chrome('drivers/chromedriver.exe')

    driver.maximize_window()
    window_size = driver.get_window_size()
    window_height = window_size["height"]
    window_width = window_size["width"]

    print(screen_width)
    print(screen_height)
    print(window_width)
    print(window_height)

    # Open the website
    driver.get('http://4nums.com/')

    # Wait three seconds to click start and put mouse in proper position (slightly above and to the left of the top-left corner of canvas)
    time.sleep(3)

    CANVAS_SIDE_AVG = (screen_width + screen_height) / (window_width + window_height) * 400

    print("ASSUMED CANVAS SIZE")
    print(CANVAS_SIDE_AVG)

    standard_x = pyautogui.position().x
    standard_y = pyautogui.position().y

    while True:
        pyautogui.moveRel(CANVAS_SIDE_AVG, 0)
        time.sleep(0.2)
        pyautogui.moveRel(-1 * CANVAS_SIDE_AVG, 0)
        time.sleep(0.2)


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