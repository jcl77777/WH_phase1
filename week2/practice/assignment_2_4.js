/*def get_number(index):
your code here
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70
*/

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