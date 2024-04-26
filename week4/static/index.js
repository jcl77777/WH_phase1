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


/*JSONResponse
document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("loginForm");
  form.addEventListener("submit", function(event) {
      event.preventDefault();
      const formData = new FormData(form);
      const data = {
          username: formData.get('username'),
          password: formData.get('password')
      };
      fetch('/signin', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(data)
      })
      .then(response => response.json())
      .then(data => {
          if (data.redirect) {
              window.location.href = data.redirect;
          } else {
              // Handle errors or show messages here
              alert(data.error_message);
          }
      })
      .catch(error => console.error('Error:', error));
  });
});
*/