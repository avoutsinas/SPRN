import re

memory_stack = []

operators = ["+","-","*","^","/","%"]

r = ['1804289383','846930886','1681692777','1714636915','1957747793','424238335','719885386','1649760492','596516649','1189641421','1025202362','1350490027','783368690','1102520059','2044897763','1967513926','1365180540','1540383426','304089172','1303455736','35005211','521595368']

count = 0


#This function finds any non numerical characters in user_input and separates them with 'space' characters. 
#Special handling is required for "-", while pre-existing space characters are ignored.
def analyse_input(inpt):

  #To find non-digit characters, a regular expressions is used
  find_non_numbers = re.compile('\D')
  non_numbers_list = find_non_numbers.findall(inpt).copy()

  previous_char = "a"
  i=0
  
  for character in non_numbers_list:
    if character in inpt:
      if character == "-":
        inpt = inpt.replace(character," "+character)
      elif  character == " ":
        pass
      elif character == "=" and previous_char != " ":
        inpt = inpt.replace(character," "+"=="+" ")  
      else:  
        inpt = inpt.replace(character," "+character+" ")
    previous_char=non_numbers_list[i]
    i=i+1

  #This regular expression can find any entries in between "#" symbols, as they represent comments. 
  inpt = re.sub(r'#.+?#','', inpt)
  sort_input(inpt)


#This function is called upon to convert the analysed input to a list and further sort which elements of said list are passed to the process_input function
def sort_input(inpt):

  result = inpt.split()
  
  for i in range(len(result)):
    if result[i] in operators and len(memory_stack) == 0:
      print("Stack underflow")
      pass
    elif result[i] == "==" and len(memory_stack) != 0: 
      print(memory_stack[-1]) 
    else:
      process_input(result[i])


#This function returns True if the provided argument is an operator.
def check_for_operators(sign):
  i=0
  while i<len(operators):
    if operators[i] == sign:
      return True
    else:
      i=i+1  


#This function contains all the operations of the SRPN calculator. 
#It utilises a flag variable, for operations which need special handling (i.e zero division)
def execute_operation (x,y,op):

  flag = 0
  calculation = 0

  if op == "+":
    calculation = x+y
  elif op == "-":
      calculation = y-x
  elif op == "*":
    calculation = x*y
  elif op == "^":
    if x<0:
      print("Negative power.")
      flag = 1
    else:  
      calculation = pow(y,x) 
  elif op == "/":
    if x == 0:
      print("Divide by 0.")
      calculation = 0
      flag = 1
    else:  
      calculation = int(y/x)
  elif op == "%":
    if y==0:
      print("Divide by 0.")
      flag = 1
    else:
      calculation = modulo(x,y)
  else:
    pass 

  if flag == 1:
      return "null"  
  else:  
      return calculation
  
#This function determines whether the result of a calculation will be stored in the stack.
def register_result(inpt):
  try:
    x = memory_stack.pop()
    y = memory_stack.pop()
    result = execute_operation(x,y,inpt)
    if result == "null":
      push_stack(y)
      push_stack(x)
    else:  
      push_stack(result)
  except IndexError:  
    print("Stack underflow.")
    push_stack(x)


#This function ensures that modulo results are in line with the provided SRPN calculator.
#Note: the x=0 condition is not applied in the provided calculator, so it crashes. 
#Also for y=0 the program returns "Divide by 0".
def modulo(x,y):

  if y > 0:  
    return y%abs(x)
  elif y < 0:
    return -(y%(abs(x)))


#This function prints all of the stored numbers in a stack.
#In case of the stack being empty, the function prints a specific number.
def print_stack(stack):
  
  if len(stack) == 0:
    print ("-2147483648")
  else:  
    for j in range(len(stack)):
      print(stack[j])  
      

#This function stores numbers in the stack, taking into account the maximum allowed length of the stack and the highest and lowest values accepted by the calculator. For non numerical characters, a message is printed informing the user.
def push_stack(inpt):

  if len(memory_stack) >= 23 and inpt.replace('-','').isdigit():
    print ("Stack overflow.")  
  else:    
    try:
      if int(inpt) > 2147483647:
        memory_stack.append(2147483647)
      elif int(inpt) < -2147483648:  
        memory_stack.append(-2147483648)
      else:  
        memory_stack.append(int(inpt))
    except ValueError:
      print("Unrecognised operator or operand ", '"' + inpt + '".')


#This function contains a counter which is used by the process_input function, to generate the appropriate element of r.
#If the counter exceeds the length of array r (len(r)-1), its value is set back to "0"
def r_count():

  global count
  temp2 = count
  if count >= len(r)-1:
    count = 0
  else:  
    count = count + 1
  return temp2


#This function acts as the main processing hub for the calculator. It takes each element of the already analysed and sorted user input as an argument and calls different functions according to the input.
def process_input(inpt):

  if check_for_operators(inpt) == True:
    register_result(inpt)
  elif inpt == "=":
    if len(memory_stack) == 0:
      print("Stack empty.")
    else: 
      print(memory_stack[-1])
  elif inpt == "d":
    print_stack(memory_stack)
  elif inpt == "r":
    if len(memory_stack) >= 23:
      print ("Stack overflow.")
    else:
      temp1 = r_count() 
      push_stack(int(r[temp1]))
  else:
    push_stack(inpt)


#Main function
def main():
  print("You can now start interacting with the SRPN calculator")
  while True:
    user_input = input()
  
    analyse_input(user_input)
    
if __name__ == "__main__":
    main()
    