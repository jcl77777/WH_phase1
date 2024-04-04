// Initial state of the side menu, assuming it starts closed
var isSideMenuOpen = false;

function toggleMenu() {
  var sideMenu = document.getElementById("side-menu");
  
  if (isSideMenuOpen) {
    // If the menu is open, close it
    sideMenu.style.width = '0px';
    isSideMenuOpen = false;
  } else {
    // If the menu is closed, open it
    sideMenu.style.width = '250px';
    isSideMenuOpen = true;
  }
}

  
