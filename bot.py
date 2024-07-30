# bot.py
# Author: Spencer Ye
# Last Revised: July 30th, 2024
# Version: 1.0.1

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
EST_CANVAS_PIXELS = 400
BLOCK_0_OFFSET_X = 50
BLOCK_0_OFFSET_Y = 50
BLOCK_1_OFFSET_X = 210
BLOCK_1_OFFSET_Y = 50
BLOCK_2_OFFSET_X = 50
BLOCK_2_OFFSET_Y = 210
BLOCK_3_OFFSET_X = 210
BLOCK_3_OFFSET_Y = 210
BLOCK_PLUS_OFFSET_X = 50
BLOCK_PLUS_OFFSET_Y = 300
BLOCK_SUB_OFFSET_X = 110
BLOCK_SUB_OFFSET_Y = 300
BLOCK_MULT_OFFSET_X = 170
BLOCK_MULT_OFFSET_Y = 300
BLOCK_DIV_OFFSET_X = 240
BLOCK_DIV_OFFSET_Y = 300
BLOCK_SUBMIT_OFFSET_X = 355
BLOCK_SUBMIT_OFFSET_Y = 370
BLOCK_SKIP_OFFSET_X = 350
BLOCK_SKIP_OFFSET_Y = 310

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

    # Get the solution from the solver
    solution = solvable(nums)

    # If the solution is None, escape (All are solvable, but there are a few bugs still)
    if solution == None:
        return ["skip"]

    # Solve the set of numbers and split to get each operator
    operators = solvable(nums).split(" ")

    # Convert the numbers into a string so we can index it later
    nums_str = [str(i) for i in nums]
    box_nums = ["0", "2", "1", "3"]
    
    # Replace each number with the box number
    temp = []
    for ch in operators:
        if ch.isdigit():
            i = nums_str.index(ch)
            temp.append(box_nums[i])
            del nums_str[i]
            del box_nums[i]
        else:
            temp.append(ch)

    operators = temp 

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
#   old_x: The original x position of the mouse
#   old_y: The original x position of the mouse
#   ratio: The estimated ratio between pixels on the window and screen resolution
# Returns:
#   None
def move_mouse(operations, old_x, old_y, ratio):

    # For each operation, move to the correct offset, click, and then return
    for operation in operations:
        if operation == '0':
            pyautogui.moveRel(BLOCK_0_OFFSET_X * ratio, BLOCK_0_OFFSET_Y * ratio, duration=0.1)
        elif operation == '1':
            pyautogui.moveRel(BLOCK_1_OFFSET_X * ratio, BLOCK_1_OFFSET_Y * ratio, duration=0.1)
        elif operation == '2':
            pyautogui.moveRel(BLOCK_2_OFFSET_X * ratio, BLOCK_2_OFFSET_Y * ratio, duration=0.1)
        elif operation == '3':
            pyautogui.moveRel(BLOCK_3_OFFSET_X * ratio, BLOCK_3_OFFSET_Y * ratio, duration=0.1)
        elif operation == '+':
            pyautogui.moveRel(BLOCK_PLUS_OFFSET_X * ratio, BLOCK_PLUS_OFFSET_Y * ratio, duration=0.1)
        elif operation == '-':
            pyautogui.moveRel(BLOCK_SUB_OFFSET_X * ratio, BLOCK_SUB_OFFSET_Y * ratio, duration=0.1)
        elif operation == '*':
            pyautogui.moveRel(BLOCK_MULT_OFFSET_X * ratio, BLOCK_MULT_OFFSET_Y * ratio, duration=0.1)
        elif operation == '/':
            pyautogui.moveRel(BLOCK_DIV_OFFSET_X * ratio, BLOCK_DIV_OFFSET_Y * ratio, duration=0.1)
        elif operation == 'skip':
            pyautogui.moveRel(BLOCK_SKIP_OFFSET_X * ratio, BLOCK_SKIP_OFFSET_Y * ratio, duration=0.1)
            pyautogui.click()
            pyautogui.moveTo(old_x, old_y)
            time.sleep(7) # Wait for the instruction to get off the screen
            return
        else:
            print("ERROR UNRECOGNIZED OPERATION IN MOVE MOUSE") # Click SKIP After
            pyautogui.moveRel(BLOCK_SKIP_OFFSET_X * ratio, BLOCK_SKIP_OFFSET_Y * ratio, duration=0.1)
            pyautogui.click()
            pyautogui.moveTo(old_x, old_y)
            time.sleep(7) # Wait for the instruction to get off the screen
            return

        pyautogui.click()
        pyautogui.moveTo(old_x, old_y)
    
    # Click submit button
    pyautogui.moveRel(BLOCK_SUBMIT_OFFSET_X * ratio, BLOCK_SUBMIT_OFFSET_Y * ratio, duration=0.15)
    pyautogui.click()
    pyautogui.moveTo(old_x, old_y)

def main():
    
    # Find the size of the current computer screen
    screen_size = pyautogui.size()
    screen_height = screen_size.height
    screen_width = screen_size.width

    # Instantiate the Chrome Driver
    driver = webdriver.Chrome('drivers/chromedriver.exe')

    # Find the size of the maximized window screen
    driver.maximize_window()
    window_size = driver.get_window_size()
    window_height = window_size["height"]
    window_width = window_size["width"]

    # Calculate the resolution of the canvas by estimating with the window and screen ratios
    CANVAS_SIDE_RATIO = (screen_width + screen_height) / (window_width + window_height)

    # Open the website
    driver.get('http://4nums.com/')

    # Wait three seconds to click start and put mouse in proper position (slightly above and to the left of the top-left corner of canvas)
    time.sleep(3)

    # Assuming the mouse position is correct, record the spot
    standard_x = pyautogui.position().x
    standard_y = pyautogui.position().y

    cont = True

    while cont:
        
        # Get the drawing on the canvas
        try:
            img = get_driver_image(driver)

            # Extract the numbers from the canvas
            nums = extract_numbers(img)

            # Calculate what buttons we have to click to get to 24
            operations = calculate_moves(nums)

            # Move the mouse to click the buttons according to what we have found
            move_mouse(operations, standard_x, standard_y, CANVAS_SIDE_RATIO)
        except ValueError: # Reading is closed, assumed to be intentional
            cont = False
        except Exception:
            print("Unknown Error")

    # Wait to allow user to interact with the end screen
    time.sleep(30)

    driver.quit()



if __name__ == "__main__":
    main()