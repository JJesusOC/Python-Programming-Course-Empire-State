#global variable
count = 0


#will try to convert input into number. if can't, error will occur. *input validation*
def number_converter (text):
    return float(text)


#add
def add(x, y):
    return x + y

#subtract
def subtract(x, y):
    return x - y

#multiply
def multiply(x, y=1):
    return x * y

#divide
def division (x, y):
    if y == 0:
        return "Uh ohh! Cannot divide by zero :( "

    return x / y


# local variable and comparing between local and global variables 
def variable_comparision():
    count = 99999999
    return count


# working with only the division on the try. Dealing with the variable changing into float 
# as part of the exception, which the code crashes and says it cannot convert.
# deal with also the diving by zero as the other exception. 

try:
    x = number_converter(input("Enter the first number: "))
    y = number_converter(input("Enter the second number: "))
    print("Dividing results: ", division(x,y))

except InputError:
    print("Invalid input. Enter numbers only. ")

except OutputError:
    print("Error! Undefined!")