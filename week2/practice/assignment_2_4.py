'''def get_number(index):
your code here
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70
'''

def get_number(index):
  # Base cases for the first 4 terms
  if index == 0:
    return 0
  elif index == 1:
    return 4
  elif index == 2:
    return 8
  elif index == 3:
    return 7
  else:
    # Logic for calculating other terms based on 3的倍數
    if index % 3 == 0:  # index 3的倍數 
        return get_number(index - 1) - 1
    elif index % 3 == 1:  # index 餘數=1
        return get_number(index - 1) + 4
    elif index % 3 == 2:  # index 餘數=2
        return get_number(index - 1) + 4 
  return 0

# Print results for sample test cases
print(get_number(1))  # Output: 4
print(get_number(5))  # Output: 15
print(get_number(10)) # Output: 25
print(get_number(30)) # Output: 70
