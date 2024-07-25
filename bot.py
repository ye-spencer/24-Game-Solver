# bot.py
# Author: Spencer Ye
# Last Revised: July 25th, 2024
# Version: 0.1.0

from selenium import webdriver
import time
import pyautogui

def main():
    print("Working")
    
    driver = webdriver.Chrome('drivers/chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get('http://4nums.com/')
    time.sleep(5) # Let the user actually see something!
    time.sleep(5) # Let the user actually see something!
    driver.quit()



if __name__ == "__main__":
    main()