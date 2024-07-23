operations = ['+', '-', '*', '/']
num_operations = len(operations)

minNum = 1
maxNum = 10

num_cards = 4

margin_error = 0.00001

# dad: 30%
# spencer: 45%

success = open("doable.txt", "w")
failed = open("notdoable.txt", "w")

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

def solvable (a,b,c,d): #Issue: only contains linearly built equations, but those with those with groupings don't work
	for perm in permutation([a,b,c,d]):
		for i in range(0, pow(num_operations, num_cards - 1)):
			temp = i
			iteration = 1
			todo_operations = [str(perm[0])]
			while iteration < num_cards:
				operation = temp % num_operations
				temp = int(temp / num_operations)
				todo_operations.append(operations[operation])
				todo_operations.append(str(perm[iteration]))
				iteration += 1

			straight = "((%s) %s) %s" % (" ".join(todo_operations[0:3]), " ".join(todo_operations[3:5]), " ".join(todo_operations[5:7]))
			join = "(%s) %s (%s)" % ((" ".join(todo_operations[0:3])), todo_operations[3], (" ".join(todo_operations[4:7])))
			
			valOne = eval(straight)
			try:
				valTwo = eval(join)
			except ZeroDivisionError:
				valTwo = 0

			if abs(valOne - 24) <= margin_error:
				success.write(str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + "\t" + straight + "\n")
				return True
			elif abs(valTwo - 24) <= margin_error:
				success.write(str(a) + ", " + str(b) + ", " + str(c) + ", " + str(d) + "\t" + join + "\n")
				return True
	return False



count = 0
total = 0


for i in range(minNum, maxNum + 1):
	for j in range(i, maxNum + 1):
		for k in range(j, maxNum + 1):
			for l in range(k, maxNum + 1):
				if solvable(i, j, k, l):
					count += 1
				else:
					failed.write(str(i) + ", " + str(j) + ", " + str(k) + ", " + str(l) + "\n")
				total += 1
				print("Completed " + str(total))
print("Total: %.2f%%" % (count / total * 100))

success.close()
failed.close()

