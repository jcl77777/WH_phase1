const loginForm = document.getElementById('loginForm');
const termsCheckbox = document.getElementById('termsCheckbox');

loginForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Prevent the form without checking the box

  if (!termsCheckbox.checked) {
    alert('Please check the checkbox first');
  } else {
    // Submit the form
    loginForm.submit();
  }
});