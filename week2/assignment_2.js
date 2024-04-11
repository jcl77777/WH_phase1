//Task1
function findAndPrint(messages, currentStation) {
    // Set the min_distance as the default value: inf (set to infinity).
    // This allows to easily compare the current minimum (or maximum) value with the new values encountered.
    let minDistance = Infinity;
    let nearestFriend = null;
  
    // Check each message and loops for each friend in the messages object
    for (let friend in messages) {
      // Loop for station and pair number in the station dictionary
      for (let station in songpanXindianLineStations) {
        // Check if a station name is in message
        // and check first if the Xiaobitan station in the message
        if (messages[friend].includes(station) && station === "Xiaobitan") {
          // Calculate the distance using Math.abs function - absolute value of this difference between the current station in the message and the station number
          let distance = Math.abs(
            parseFloat(songpanXindianLineStations[currentStation]) -
            parseFloat(songpanXindianLineStations[station])
          );
  
          // Check if the distance is smaller than the minDistance
          if (distance < minDistance) {
            // Set the minDistance = distance
            minDistance = distance;
            // Declare the nearFriend from the message
            nearestFriend = friend;
            // If found, no need to loop the next round
            break;
          }
        } // If not Xiaobitan station, then check other stations in message
        else if (messages[friend].includes(station) && station !== "Xiaobitan") {
          let distance = Math.abs(
            parseFloat(songpanXindianLineStations[currentStation]) -
            parseFloat(songpanXindianLineStations[station])
          );
          if (distance < minDistance) {
            minDistance = distance;
            nearestFriend = friend;
            break;
          }
        }
      }
    }
  
    // If nearestFriend is found, print
    if (nearestFriend) {
      console.log(nearestFriend);
    } else {
      console.log("No friend found.");
    }
  }
  
  const songpanXindianLineStations = {
    Songshan: "1",
    "Nanjing Sanmin": "2",
    "Taipei Arena": "3",
    "Nanjing Fuxing": "4",
    "Songjiang Nanjing": "5",
    Zhongshan: "6",
    Beimen: "7",
    Ximen: "8",
    Xiaonamen: "9",
    "Chiang Kai-Shek Memorial Hall": "10",
    Guting: "11",
    "Taipwower Building": "12",
    Gongguan: "13",
    Wanlong: "14",
    Jingmei: "15",
    Dapinglin: "16",
    Qizhang: "17",
    Xiaobitan: "17.1",
    "Xindian City Hall": "17.6",
    Xindian: "18"
  };

  
  const messages = {
    Leslie: "I'm at home near Xiaobitan station.",
    Bob: "I'm at Ximen MRT station.",
    Mary: "I have a drink near Jingmei MRT station.",
    Copper: "I just saw a concert at Taipei Arena.",
    Vivian: "I'm at Xindian station waiting for you."
  };
  
  findAndPrint(messages, "Wanlong"); // Output: Mary
  findAndPrint(messages, "Songshan"); // Output: Copper
  findAndPrint(messages, "Qizhang"); // Output: Leslie
  findAndPrint(messages, "Ximen"); // print Bob
  findAndPrint(messages, "Xindian City Hall"); // print Vivian

//Task2
// Helper function to check for overlapping time slots
function overlap(start1, duration1, start2, duration2) {
    const end1 = start1 + duration1;
    const end2 = start2 + duration2;
    return (start1 <= end2 && end1 >= start2);
  }
  
  // Main booking function
  function book(consultants, hour, duration, criteria) {
    // Create a list to store the available consultants
    const availableConsultants = [];
  
    // Loop through each consultant to check availability
    for (const consultant of consultants) {
      let isAvailable = true;
  
      // Check for overlapping bookings
      for (const booking of consultant.bookings || []) {
        if (overlap(hour, duration, booking.start, booking.duration)) {
          isAvailable = false;
          break;
        }
      }
  
      if (isAvailable) {
        availableConsultants.push(consultant);
      }
    }
  
    if (availableConsultants.length === 0) {
      return "No Service";
    }
  
    // Sort the available consultants based on the given criteria
    if (criteria === "price") {
      availableConsultants.sort((a, b) => a.price - b.price);
    } else if (criteria === "rate") {
      availableConsultants.sort((a, b) => b.rate - a.rate);
    } else {
      return "Invalid criteria. Choose 'price' or 'rate'.";
    }
  
    // Book the first available consultant
    const bookedConsultant = availableConsultants[0];
  
    // Add the booking to the consultant's bookings
    if (!bookedConsultant.bookings) {
      bookedConsultant.bookings = [];
    }
    bookedConsultant.bookings.push({ start: hour, duration: duration });
  
    return bookedConsultant.name;
  }
  
  const consultants = [
    { name: "John", rate: 4.5, price: 1000, bookings: [] },
    { name: "Bob", rate: 3, price: 1200, bookings: [] },
    { name: "Jenny", rate: 3.8, price: 800, bookings: [] }
  ];
  
  console.log(book(consultants, 15, 1, "price")); // Output: Jenny
  console.log(book(consultants, 11, 2, "price")); // Output: Jenny
  console.log(book(consultants, 10, 2, "price")); // Output: John
  console.log(book(consultants, 20, 2, "rate")); // Output: John
  console.log(book(consultants, 11, 1, "rate")); // Output: Bob
  console.log(book(consultants, 11, 2, "rate")); // Output: No Service
  console.log(book(consultants, 14, 3, "price")); // Output: John

  //Task3
  function func(...names) {
    // Put middle names in the dictionary (name, count pair)
    let middleNames = {};
  
    // Loop through each name to figure out its length
    for (let name of names) {
      let length = name.length;

      //Declare middleName variable
      let middleName;

      // If there are 2 or 3 words in a name, the middle name is defined as the second word
      if (length === 2 || length === 3) {
        middleName = name[1];
        // If there are more than 4 words in a name, the middle name is defined as the third word
      } else if (length === 4 || length === 5) {
        middleName = name[2];
      } else {
        continue;
    }
  
    // Count the middle names shown in the dictionary
    // If the middle name is in the dictionary, add the count
    if (middleName in middleNames) {
        middleNames[middleName] +=1;
    } else {
        middleNames[middleName] = 1;
    }
}

    // Check the unique count among all middle names shown
    //set an new empty array called uniqueMiddleNames to store unique middle names with specification
    let uniqueMiddleNames = [];
    // Loop through the middleNames object to filter by the count of 1
    for (const name of Object.keys(middleNames)) {
        if (middleNames[name] === 1) {
            // Push the name into the new array
            uniqueMiddleNames.push(name);
        }
    }

    // Check by the length if the length is 0 then no unique middle names
    if (uniqueMiddleNames.length === 0) {
      console.log("No unique middle name found.");
    } // If there is only one unique middle name, print the name
    else if (uniqueMiddleNames.length === 1) {
      for (let name of names) {
        let middleName =
          name.length === 2 || name.length === 3 ? name[1] : name[2];
        if (middleName === uniqueMiddleNames[0]) {
          console.log(name);
        }
      }
    } // If there are more than one middle names in the list, then print no unique middle name
    else {
      console.log("No unique middle name found.");
    }
  }
  
  func("彭大牆", "陳王明雅", "吳明"); // prints 彭大牆
  func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花"); // prints 林花花
  func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // prints 沒有
  func("郭宣雅", "夏曼藍波安", "郭宣恆"); // prints 夏曼藍波安


//Task4
function getNumber(index) {
    // Base cases for the first 4 terms
    if (index === 0) { // "=" = "===", ":" = "{}"
      return 0; // add ; to end of line to complete the statement
    } else if (index === 1) { //elif = else if 
      return 4; 
    } else if (index === 2) {
      return 8;
    } else if (index === 3) {
      return 7;
    } else {
      // Logic for calculating other terms based on 3的倍數
      if (index % 3 === 0) {
        // index 3的倍數 
        return getNumber(index - 1) - 1;
      } else if (index % 3 === 1) {
        // index 餘數=1
        return getNumber(index - 1) + 4;
      } else if (index % 3 ===2) {
        // index 餘數=2
        return getNumber(index - 1) + 4;
      }
    }
  }
  
  // Print results for sample test cases
  console.log(getNumber(1)); // Output: 4
  console.log(getNumber(5)); // Output: 15
  console.log(getNumber(10)); // Output: 25
  console.log(getNumber(30)); // Output: 70