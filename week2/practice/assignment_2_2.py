#check the time input from the user (hour, duration) against whatever exist in the booking dictionary
def overlap(start1, duration1, start2, duration2):
    """Checks if two time slots overlap."""
    end1 = start1 + duration1
    end2 = start2 + duration2
    return (start1 <= end2 and end1 >= start2)
    #calculate the end time for each time slot by adding the duration to the start time. 
    #check if the start time of the first time slot is less than or equal to the end time of the second time slot, and the end time of the first time slot is greater than or equal to the start time of the second time slot.
    #example
    #print(book(consultants, 11, 2, "price")) Jenny got booked at 11-13pm for 2 hours
    #print(book(consultants, 10, 2, "price")) then Jenny cannot be booked at 10-12pm for 2 hours, instead John can be booked. 
    #print(book(consultants, 11, 1, "rate"))  then Jenny and John cannot be booked at 11-12pm for 1 hour, instead Bob can be booked. 
    #print(book(consultants, 11, 2, "rate"))  all three are booked at 11am. No service is available for the requested time.

def book(consultants, hour, duration, criteria):
    #create a list to store the available consultants against user input
    available_consultants = []

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

    '''for consultant in available_consultants:
        if "bookings" not in consultant:
            consultant["bookings"] = []
        consultant["bookings"].append({"start": hour, "duration": duration})
        return consultant["name"]

    return "No Service"'''

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