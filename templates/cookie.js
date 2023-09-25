// Function to extract cookies from document.cookie
function getCookies() {
  const cookies = {};
  document.cookie.split(';').forEach(cookie => {
    const [key, value] = cookie.trim().split('=');
    cookies[key] = value;
  });
  return cookies;
}

// Make a POST request to the login endpoint
fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    username: 'admin',
    password: 'admin',
  }),
  credentials: 'include', // Include cookies in the request
})
  .then(response => {
    // Log all response headers
    console.log('Response Headers:', response.headers);

    // You can access and use the cookies here
    const cookies = getCookies();
    console.log('Cookies Received:', cookies);

    // You can also access the response data if needed
    return response.json();
  })
  .then(data => {
    // Handle the response data here
    console.log('Response Data:', data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
