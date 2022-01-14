from multipledispatch import dispatch


# passing one parameter
@dispatch(int, int)
def product(first, second):
    return first * second


# passing two parameters
@dispatch(int, int, int)
def product(first, second, third):
    return first * second * third


# you can also pass data type of any value as per requirement
@dispatch(float, float, float)
def product(first, second, third):
    return first * second * third


# calling product method with 2 arguments
print(product(2, 3, 2))  # this will give output of 12
print(product(2.2, 3.4, 2.3))  # this will give output of 17.985999999999997
print(product(2, 3))  # this will give output of 6
