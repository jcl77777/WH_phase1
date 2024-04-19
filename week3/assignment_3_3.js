function renderBox(boxElement, urlImg, title) {
    const imageElement = boxElement.querySelector("img");
    const titleElement = boxElement.querySelector("p") || boxElement.querySelector(".big-box-content"); // Handle both small and big box content classes

    //update the image
    if (imageElement) {
      imageElement.src = urlImg;
      imageElement.alt = title; 
    } else {
      console.error("Missing image element in box:", boxElement); // Handle missing image element
    }
    //update the title
    if (titleElement) {
      titleElement.textContent = title;
    } else {
      console.error("Missing title element in box:", boxElement); // Handle missing title element
    }
  }

//the most important!!! Asynchronous Issue!!!
//the html renders the images and titles is executing before the data is fetched from the API
//ensures that the rendering happens only after the data has been fetched successfully.
document.addEventListener('DOMContentLoaded', () => {
    const smallboxes = document.querySelectorAll(".small-box");
    const bigboxes = document.querySelectorAll(".big-box");
    
    // fetch data
    const url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
    const urlImgs = [];
    const titles = [];
    
    fetch(url)
    .then(response => response.json()) // Parse JSON response
    .then(data => {
        const target = data.data.results;
    
        for(let i=0;i<target.length;i++){
        //console.log(target[i].filelist);
        let imgs = target[i].filelist;
        let targetImg = "https://"+imgs.split("https://")[1];
        // console.log(targetImg);
        //add to list
        urlImgs.push(targetImg);
        //console.log(targetImg)

        // process the spot title
        let title = target[i].stitle;
        //console.log(title);
        //add to list
        titles.push(title);
        }
        
        for (let i = 0; i < Math.min(smallboxes.length, urlImgs.length, titles.length); i++) { // Handle potential array size mismatches
            renderBox(smallboxes[i], urlImgs[i], titles[i]);
        }
            // delete the img and title from the list
            for(let i=0;i<smallboxes.length;i++){
            titles.shift();
            urlImgs.shift();
            }
        
        for (let i = 0; i < Math.min(bigboxes.length, urlImgs.length, titles.length); i++) { // Handle potential array size mismatches
            renderBox(bigboxes[i], urlImgs[i], titles[i]);
        }
            // delete the img and title from the list
            for(let i=0;i<bigboxes.length;i++){
                titles.shift();
                urlImgs.shift();
        }   
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        // Display user-friendly message
        const container = document.getElementById('data-container'); // Replace with your element ID
        container.textContent = 'An error occurred while fetching data. Please try again later.';
    });
});
