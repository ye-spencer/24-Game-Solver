# 24 Game Solver

Thie project was originally created to calculate the percentage of hands that are solvable in the card game *24*. It has since progressed into a bot that can play the game on 4nums.com.

To learn how to the rules of 24 [Click Here](https://www.spencerye.com/blogs/How%20To%20Play%2024.html)


# How to use

## Initial download

1. Download the code an unzip it anywhere

## Running the bot

1. Run `python bot.py`
2. Wait for the window to load, and click the "Against the clock" option
3. Within 3 seconds, place your mouse slightly above and to the right of the top corner of the canvas (does not need to be exact)

> [!IMPORTANT]
> Program can't be left alone, if you don't see and click the coffee breaks fast enough the program will crash

4. Once you are satisfied with your score. Open another window using your keyboard to intentionally crash the system.
 - Windows + i works well for this purpose

## Running the analysis
1. Select the test you want by uncommenting the proper test in the `main()` function in `solver.py`.
2. Run `python solver.py`

# Example

I recorded the beginning of a run using the `bot.py` below


https://github.com/user-attachments/assets/a0a4b9a3-b67f-4758-8956-06d0e01cf65e

# Process & Challenges

The project was created to solve the long standing dispute in my family about how many playing hands were solvable in the game 24. Developing an algorithm to solve each hand was straightforward: all I had to do was build each possible tree of operations for each hand, and evaluate it to see if it equaled 24.

However, deciding what hands were to be included proved to be a much more challnging task. The problem of permuations, duplicates, and probability of each combination all had to be factored in. In the end there are three different methods:  iterating through each possible combination (715 combinations in total), iterating through each possible hand counting order (10,000 permutations in total), and simulating 10,000 rounds of the game (100,000 sampled rounds in total). Their respective answers are 76.5%, 83.5%, and ~85.72%.

I was able to reuse the solving function to assist in the creation of the bot. The bot would connect to 4nums using a chromedriver and a recent version of Chrome. Then I collected the contents of the website using Selenium. However, the website uses a canvas, which I assume is easier to draw on, but it also prevents me from using Selenium to collect the numbers on screen.

As a result, I resorted to transfering the entire canvas image to use OpenCV and Tesseract to read the text from each box. I would crop part of the image, filter and apply a binary threshold to increase contrast in the image. I struggled to find the right PSM to use, but eventaully settled on 7 once it consistently returned the best results. Then we calculate the operations and order of the numbers necessary to equal 24. 

Since the operation buttons are always in the same location, the script just needed calibration on the offsets to move to the correct location after parsing the operation list.

## Interesting Features & Discussion

4nums.com implements coffee breaks to allow mere humans to have a chance to recover while going for high scores. However, this is an issue as they come randomly, and mess with the parsing of the images. Ideally, the script will be able to detect these coffee breaks, but for now it waits a moment after every solve to let the user to click off. This soluation took 2 seconds to implement.
