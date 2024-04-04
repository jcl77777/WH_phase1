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