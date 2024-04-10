#Task1
def find_and_print(messages, current_station):
    #set the min_distance as the default value: inf (set to infinity). This allows to easily compare the current minimum (or maximum) value with the new values encountered.
    min_distance = float('inf')
    #set the nearest_friend to the default value: None
    nearest_friend = None

    #check each message and loops for each friend in the messages dictionary
    for friend, message in messages.items():
        #loop for station and pair number in the station dictionary
        for station, station_number in songshan_xindian_line_stations.items():
            #check if a station name is in message
            #and check first if the Xiaobitan station in the message
            if station in message and station == "Xiaobitan":
                #calculate the distance using abs function - absolute value of this difference between the current station in the message and the station number
                distance = abs(int(songshan_xindian_line_stations[current_station]) - int(station_number))
                #check if the distance is smaller than the min_distance
                if distance < min_distance:
                    #set the min_distance = distance
                    min_distance = distance
                    #declare the nearfriend from the message
                    nearest_friend = friend
                    #if found, no need to loop the next round
                    break
            #if not Xiaobitan station, then check other stations in message
            elif station in message and station != "Xiaobitan":
                distance = abs(int(songshan_xindian_line_stations[current_station]) - int(station_number))
                if distance < min_distance:
                    min_distance = distance
                    nearest_friend = friend
                    break

    #if nearest_friend is found, print
    if nearest_friend:
        print(nearest_friend)
    else:
        print("No friend found.")

songshan_xindian_line_stations = {
    "Songshan": "1", 
    "Nanjing Sanmin": "2", 
    "Taipei Arena": "3",
    "Nanjing Fuxing": "4", 
    "Songjiang Nanjing": "5", 
    "Zhongshan": "6", 
    "Beimen": "7", 
    "Ximen": "8", 
    "Xiaonamen": "9", 
    "Chiang Kai-Shek Memorial Hall":"10",
    "Guting":"11", 
    "Taipwower Building": "12", 
    "Gongguan":"13", 
    "Wanlong":"14", 
    "Jingmei": "15", 
    "Dapinglin":"16", 
    "Qizhang": "17",
    "Xindian City Hall":"18", 
    "Xiaobitan":"18",
    "Xindian":"19"
}

messages={
    "Leslie":"I'm at home near Xiaobitan station.",
    "Bob":"I'm at Ximen MRT station.",
    "Mary":"I have a drink near Jingmei MRT station.",
    "Copper":"I just saw a concert at Taipei Arena.",
    "Vivian":"I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie

#Task2
#check the time input from the user (hour, duration) against whatever exist in the booking dictionary
def overlap(start1, duration1, start2, duration2):
    #Checks if two time slots overlap.
    #check if user input hour >= existing booked hour and user input hour < existing booked hour + existing booked duration 
    #OR check if user input hour + duration > existing booked hour and user input hour + duration <= existing booked hour + existing booked duration
    return (start1 >= start2 and start1 < start2 + duration2) or (start1 + duration1 > start2 and start1 + duration1 <= start2 + duration2)
    #example
    #print(book(consultants, 11, 2, "price")) Jenny got booked at 11-13pm for 2 hours
    #print(book(consultants, 10, 2, "price")) then Jenny cannot be booked at 10-12pm for 2 hours, instead John can be booked. 
    #print(book(consultants, 11, 1, "rate"))  then Jenny and John cannot be booked at 11-12pm for 1 hour, instead Bob can be booked. 
    #print(book(consultants, 11, 2, "rate"))  all three are booked at 11am. No service is available for the requested time.

def book(consultants, hour, duration, criteria):
    #create a list to store the available consultants against user input
    available_consultants = []
    #create a dictionary (key value pair) to store hour, duration
    booking = {}
    #loop through each consultant to check the availabilitiy
    for consultant in consultants:
        is_available = True
        #loop through each booking of the consultant to check the overlap
        # Accessing an existing key - booking. If the key pair value does not exist, the default value [] will be returned
        for booking in consultant.get("bookings", []):
            if overlap(hour, duration, booking["start"], booking["duration"]):
                #check the hour and duration is not overlap with the existing booking
                #if overlap, then the consultant is not available, then is_available will be False
                is_available = False
                break  # Stop checking bookings for this consultant if already unavailable

        if is_available:  # Check availability after checking all bookings
            available_consultants.append(consultant)

    if not available_consultants:
        return "No Service"    

    # Sort the available consultants based on the given criteria
    if criteria == "price":
        #.sort(key=None, reverse=False) sorts the list in place
        # sort the consultant based on the input of critieria (price or rate) using lambda function
        available_consultants.sort(key=lambda x: x["price"])
    elif criteria == "rate":
        #sort reverse = True to sort the list in descending order (highest to lowest)
        available_consultants.sort(key=lambda x: x["rate"], reverse=True)
    # if the criteria is not price or rate, return an error message
    else:
      return "Invalid criteria. Choose 'price' or 'rate'."

    # Book the first available consultant
    booked_consultant = available_consultants[0] #take the index = 0 consultant in the list
    # Add booking to the booked consultant
    if "bookings" not in booked_consultant:
        booked_consultant["bookings"] = []  # Create bookings list if it doesn't exist
    booked_consultant["bookings"].append({"start": hour, "duration": duration})  # Append booking
    return booked_consultant["name"]


consultants = [
    {"name": "John", "rate": 4.5, "price": 1000},
    {"name": "Bob", "rate": 3, "price": 1200},
    {"name": "Jenny", "rate": 3.8, "price": 800}
]
print(book(consultants, 15, 1, "price"))  # Output: Jenny
print(book(consultants, 11, 2, "price"))  # Output: Jenny
print(book(consultants, 10, 2, "price"))  # Output: John
print(book(consultants, 20, 2, "rate"))   # Output: John
print(book(consultants, 11, 1, "rate"))   # Output: Bob
print(book(consultants, 11, 2, "rate"))   # Output: No Service
print(book(consultants, 14, 3, "price"))  # Output: John

#Task3
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

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

#Task4
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