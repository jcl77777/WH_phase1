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
                distance = abs(float(songshan_xindian_line_stations[current_station]) - float(station_number))
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
                distance = abs(float(songshan_xindian_line_stations[current_station]) - float(station_number))
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
    "Xiaobitan":"17.1",
    "Xindian City Hall":"17.6", 
    "Xindian":"18"
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
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian