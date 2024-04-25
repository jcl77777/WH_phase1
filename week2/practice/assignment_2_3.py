'''
def func(*data):
# your code here
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
'''

def func(*names):
  #put middle names in the dictinonary (name, count pair)
  middle_names = {}
  
  #loop through each name to figure out its length
  for name in names:
    length = len(name)

  #middle name logic below 
  #If there are 2 or 3 words in a name, the middle name is defined as the second word
    if length == 2 or length == 3:
      middle_name = name[1]
    #If there are more than 4 words in a name, the middle name is defined as the third word
    elif length >= 4:
      middle_name = name[2]
    else:
      continue

    #count the middle names shown in the dictionary
    #If the middle name is in the dictionary, add the count
    if middle_name in middle_names:
      #add 1 to the count
      middle_names[middle_name] += 1
    else:
      middle_names[middle_name] = 1

    '''#print the count
    print("\nMiddle Name Counts:")
    for middle_name, count in middle_names.items():
        print(f"{middle_name}: {count}")'''
    
  #check the unqiue count among all middlenames shown
  #set a list to store the unique middle name is the count = 1
  unique_middle_names = [name for name, count in middle_names.items() if count == 1]
  #check by the length if the length is 0 then no unique middle names
  if len(unique_middle_names) == 0:
    print("No unique middle name found.")
  #if there is only one unique middle name, print the name
  elif len(unique_middle_names) == 1:
    #check all the names which fits to the unique middle name we found and print the name
    for name in names:
            middle_name = name[1] if len(name) == 2 or len(name) == 3 else name[2]
            if middle_name == unique_middle_names[0]:
                print(name)
  #if there are more than one middle names in the list, then print no unique middle name
  elif len(unique_middle_names) > 1:
    print("No unique middle name found.")

#print middle name
def print_middle_name(*names):
  for name in names:
    length = len(name)

    #If there are 2 or 3 words in a name, the middle name is defined as the second word
    if length == 2 or length == 3:
      #middle_name = name[1]
      print(name[1])
    #If there are more than 4 words in a name, the middle name is defined as the third word
    elif length == 4 or length == 5:
      #middle_name = name[2]
      print(name[2])
    else:
      print(f"The middle name of {name} cannot be defined.")

#spilit names into parts
def split_name(*names):
  for name in names:
    print(name[1])

# Example usage
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
