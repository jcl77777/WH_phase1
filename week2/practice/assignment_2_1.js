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
            parseInt(songpanXindianLineStations[currentStation]) -
              parseInt(songpanXindianLineStations[station])
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
            parseInt(songpanXindianLineStations[currentStation]) -
              parseInt(songpanXindianLineStations[station])
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
    "Xindian City Hall": "18",
    Xiaobitan: "18",
    Xindian: "19"
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