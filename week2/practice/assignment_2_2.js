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
  
  // Example usage
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