// Initial state of the side menu, assuming it starts closed
var isSideMenuOpen = false;

function toggleMenu() {
  var sideMenu = document.getElementById("side-menu");

  if (isSideMenuOpen) {
    // If the menu is open, close it
    sideMenu.classList.remove('open');
    isSideMenuOpen = false;
  } else {
    // If the menu is closed, open it
    sideMenu.classList.add('open');
    isSideMenuOpen = true;
  }
}

//render render the image
function renderImg(urlImg, imgTitle) {
  let newImg = document.createElement("img");
  newImg.classList.add('spot-img');
  newImg.src = urlImg;
  newImg.alt = imgTitle;
  //console.log(newImg);
  return newImg
}

//render render the title
function renderTitle(title) {
  let newText = document.createElement('p');
  newText.classList.add('p');
  newText.textContent = title;  // Set text content directly
  return newText;
}

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
      let targetImgUrl = "https://"+imgs.split("https://")[1];
      // console.log(targetImgUrl);
      //add to list
      urlImgs.push(targetImgUrl);
      //console.log(targetImgUrl)

      // process the spot title
      let title = target[i].stitle;
      //console.log(title);
      //add to list
      titles.push(title);
      }
    })
    .catch(error => console.error('Error fetching data:', error));


//small box rendering
const smallboxes = document.querySelectorAll(".small-box");

for (let i = 0; i < smallboxes.length; i++) {
    const smallBox = smallboxes[i];
    const imageElement = smallBox.querySelector("img");
    const titleElement = smallBox.querySelector("p");
    
    // Update the image source 
    imageElement.src = urlImgs[i];
    //imageElement.alt = "spot-img"; 
        
    // Update the title text
    titleElement.textContent = titles[i];
}

//big box rendering
const bigboxes = document.querySelectorAll(".big-box");

for (let i = 0; i < bigboxes.length; i++) {
      const bigBox = bigboxes[i];
      const imageElement = bigBox.querySelector("img");
      const titleElement = bigBox.querySelector(".big-box-content");
/*
      bigboxes[i].appendChild(newStar);
      bigboxes[i].appendChild(imageElement);
      bigboxes[i].appendChild(titleElement);
*/
      // Update the image source 
      imageElement.src = urlImgs[i];
      //imageElement.alt = "spot-img"; 
    
      // Update the title text
      titleElement.textContent = titles[i];
}