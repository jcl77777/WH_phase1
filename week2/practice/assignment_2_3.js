/*
def func(*data):
# your code here
func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安
*/

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

    // Set a list to store the unique middle names where the count is 1
    /*let uniqueMiddleNames = Object.entries(middleNames)
      .filter(([name, count]) => count === 1) //.filter function filters the array to create a new array, keeping only entries where the count property is 1 in the new one.
      .map(([name]) => name);  //.map function extracting names into a new array*/
   
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