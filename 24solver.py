# 24solver.py
# Author: Spencer Ye
# Last Revised: July 27th, 2024
# Version: 1.3.1

# Constants to Change

possible_operations = ['+', '-', '*', '/']
num_operations = len(possible_operations)

min_num = 1
max_num = 10

num_cards = 4

margin_error = 0.00001


write_to_files = True

success_file_name = "doable.txt"
failed_file_name = "notdoable.txt"

# End Constants to Change

# Function taken from Geeksforgeeks.com to calculate the permuations
def permutation(lst):
 
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []
 
    # If there is only one element in lst then, only
    # one permutation is possible
    if len(lst) == 1:
        return [lst]
 
    # Find the permutations for lst if there are
    # more than 1 characters
 
    l = [] # empty list that will store current permutation
 
    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
       m = lst[i]
 
       # Extract lst[i] or m from the list.  remLst is
       # remaining list
       remLst = lst[:i] + lst[i+1:]

       # Generating all permutations where m is first
       # element
       for p in permutation(remLst):
           l.append([m] + p)
    return l

# Checks if a given set of 4 cards is solvable or not. If it is solvable, it writes the solution to the doable.txt file
# Parameters: 	cards: The card values
# 
# Returns: The operation string to get the answer if there is one; None otherwise
def solvable (cards):

	# Cycle through each permutation of the numbers
	for perm in permutation(cards):

		# Cycle through the number of possible combinations of operations. There are num_operations of possible operations, and we raise it to the power of the number of slots for operations (One less than the number of cards). Each number codes for a different combination of operations
		for i in range(0, pow(num_operations, num_cards - 1)):

			temp = i # Save i so we can do calculations with it

			# Represents our expression in list form
			equation = [str(perm[0])] # Add the first number, since all operations are binary.

			# For each possible operation, we decode the operation from i
			for iteration in range (1, num_cards):
				
				# Calculate the operation. 
				# Quick explanation of how this works: If there are n operations and m cards, we cycle through 0 to n ^ (m - 1). Each number decodes a set of operations, the first operation is i % n, the second is i % (n ^ 2) ... the last is i % (n ^ (m - 2)). The modulo operation results in a number between 0 and n - 1 inclusive, which is the index for an operation in our possible_operations array
				curr_operation = temp % num_operations
				temp = int(temp / num_operations)

				# Add the operation and next number to our equation
				equation.append(possible_operations[curr_operation])
				equation.append(str(perm[iteration]))

			# There are two unique order of operations for each permutation and operation set, which we calculate here
			straight = "((%s) %s) %s" % (" ".join(equation[0:3]), " ".join(equation[3:5]), " ".join(equation[5:7]))
			join = "(%s) %s (%s)" % ((" ".join(equation[0:3])), equation[3], (" ".join(equation[4:7])))
			
			# Use python's eval function to calculate the value of each expression
			try:
				valOne = eval(straight)
			except ZeroDivisionError:
				valOne = 0
			try:
				valTwo = eval(join)
			except ZeroDivisionError:
				valTwo = 0

			# If either value is 24 (or close enough to 24) we accept the number and return True
			if abs(valOne - 24) <= margin_error:
				return straight
			elif abs(valTwo - 24) <= margin_error:
				return join
	return None

def test_every_combination():
	count = 0 # The number of successful solves
	total = 0 # The total number of solves we attempted

	# Open files
	success = open(success_file_name, "w")
	failed = open(failed_file_name, "w")

	# Cycle through each possible set of numbers
	for i in range(min_num, max_num + 1):
		for j in range(i, max_num + 1):
			for k in range(j, max_num + 1):
				for l in range(k, max_num + 1):
					
					# Create array
					arr = [i, j, k, l]

					# If it is solvable, increment our count of solved
					solutions = solvable(arr)
					if solutions != None:
						count += 1
						if write_to_files:
							success.write("\t".join(str(x) for x in arr) + "\t" + solutions + "\n")
					else:
						if write_to_files:
							failed.write("\t".join(str(x) for x in arr) + "\n")
					
					total += 1 # This could be calculated by other means, but since the way we calculate might change, we are leaving this for now
			
					print("Completed " + str(total) + " sets")

	# Print the final percentage
	print("Total: %.2f%%" % (count / total * 100))

	# Close files
	success.close()
	failed.close()

def test_all_hands():
	count = 0 # The number of successful solves
	total = 0 # The total number of solves we attempted

	# Open files
	success = open(success_file_name, "w")
	failed = open(failed_file_name, "w")

	# Cycle through each possible set of numbers
	for i in range(min_num, max_num + 1):
		for j in range(min_num, max_num + 1):
			for k in range(min_num, max_num + 1):
				for l in range(min_num, max_num + 1):
					
					# Create array
					arr = [i, j, k, l]

					# If it is solvable, increment our count of solved
					solutions = solvable(arr)
					if solutions != None:
						count += 1
						if write_to_files:
							success.write("\t".join(str(x) for x in arr) + "\t" + solutions + "\n")
					else:
						if write_to_files:
							failed.write("\t".join(str(x) for x in arr) + "\n")
					
					total += 1 # This could be calculated by other means, but since the way we calculate might change, we are leaving this for now
			
					print("Completed " + str(total) + " sets")

	# Print the final percentage
	print("Total: %.2f%%" % (count / total * 100))

	# Close files
	success.close()
	failed.close()


# The main function
def main ():
	# test_every_combination()
	test_all_hands()
	return 0


if __name__ == "__main__":
	main()
