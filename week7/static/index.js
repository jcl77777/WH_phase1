// function to delete message by clicking the button
async function confirmDeleteMessage(messageId) {
  if (confirm('Are you sure you want to delete this message?')) {
      try {
          const formData = new FormData();
          formData.append('message_id', messageId);

          const response = await fetch('/deleteMessage', {
              method: 'POST',
              body: formData,
          });

          if (response.redirected) {
              window.location.href = response.url; // Redirect to the new URL
          } else {
              console.error('Failed to delete message');
          }
      } catch (error) {
          console.error('Error deleting message:', error);
      }
  }
}

//search name and username in the DB if exists
document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('queryForm');
    if (queryForm) {
      queryForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const username = document.getElementById('username').value;
        console.log('Username:', username); 
        const resultDiv = document.getElementById('result');
        
        // Clear previous results
        resultDiv.innerHTML = '';
        console.log(resultDiv); 

        // Validate input
        if (!username) {
            resultDiv.innerHTML = 'Please enter a username.';
            return;
        }

        // Fetch member data
        fetch(`http://127.0.0.1:8000/api/member?username=${username}`)
            .then(response => {
                console.log('Response status:', response.status);
                console.log(response); // Log the response
                return response.json();
            })

            .then(data => {
                console.log('Data:', data); 
                if (data && data.username) { // Check for data and "username" property
                    const memberData = data; // Access member data
                    console.log('memberData:', memberData)
                    resultDiv.innerHTML = `
                        <p>${memberData.username} (${memberData.name})</p>
                    `;
                    } else {
                        resultDiv.innerHTML = 'No Data';
                    }          
                })
                .catch(error => {
                    console.error('Error:', error);
                    resultDiv.innerHTML = 'An error occurred while fetching data.';
                });
            });
        }  
    });

//update name 
const updateForm = document.getElementById('updateQueryForm');
const updateStatus = document.getElementById('update');
/*const requestBody = {
    id:1,
    name: 'new name'
};*/

updateForm.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent default form submission

    const newName = document.getElementById('updateName').value;
    console.log('new Name:', newName); 

    try {
        const response = await fetch('/api/member', {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({name: newName})
        });
    
    console.log('Request Body:', JSON.stringify({name: newName})); 
 
        if (!response.ok) {
          throw new Error('Failed to update name');
        }
      
        const data = await response.json();
        console.log('Success:', data);
        updateStatus.textContent = '更新成功';

    } catch (error) {
        console.error('Error:', error);
        updateStatus.textContent = 'Failed to Update';
      }
});