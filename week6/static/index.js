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
