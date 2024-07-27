# bot.py
# Author: Spencer Ye
# Last Revised: July 25th, 2024
# Version: 0.2.1

from selenium import webdriver
import time
import pyautogui
import cv2
import base64
import numpy as np

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

    # # Testing by writing the result down
    # cv2.imwrite("result.jpg", image) 

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


    # While (true):
    #   Get numbers from screen
    #   Deduce the solution
    #   Move the mouse to all of the correct locations and click



if __name__ == "__main__":
    main()