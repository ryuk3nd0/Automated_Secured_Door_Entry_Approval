function toggleMobileNumber() {
  const yesRadio = document.getElementById('yesRadio');
  const mobileNumberInput = document.getElementById('mobileNumberInput');

  if (yesRadio.checked) {
    mobileNumberInput.classList.remove('hidden');
  } else {
    mobileNumberInput.classList.add('hidden');
  }
}

function submitPhoneNumber() {
  const yesRadio = document.getElementById('yesRadio');
  const phoneNumberInput = document.getElementById('phoneNumber');
  const confirmationMessage = document.getElementById('confirmationMessage');

  if (yesRadio.checked && validatePhoneNumber(phoneNumberInput.value.trim())) {
    const phoneNumber = phoneNumberInput.value.trim();
    const dateTime = new Date().toLocaleString();
    const data = `${dateTime},${phoneNumber}\n`;

    // Send data to the server...
    fetch('/submitPhoneNumber', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ phoneNumber }),
    })
      .then(response => response.text())
      .then(data => {
        confirmationMessage.textContent = data;
        confirmationMessage.classList.remove('hidden');
        hideFormElements(); // Hide form elements on successful submission
      })
      .catch(error => console.error('Error:', error));
  } else {
    alert('Please enter a valid mobile number starting with "01" and having a total of 11 digits.');
  }
}

function validatePhoneNumber(phoneNumber) {
  const phoneNumberPattern = /^(01)\d{9}$/; // Regex pattern for "01" followed by 9 digits
  return phoneNumberPattern.test(phoneNumber);
}

function hideFormElements() {
  const yesNoQuestion = document.querySelectorAll('.container > label');
  const mobileNumberPrompt = document.getElementById('mobileNumberInput');
  const submitButton = document.querySelector('.container > button');

  yesNoQuestion.forEach(question => {
    question.classList.add('hidden');
  });

  mobileNumberPrompt.classList.add('hidden');
  submitButton.classList.add('hidden');
}

// Function to handle the keypress event in the mobile number input field
function handleKeyPress(event) {
  if (event.key === 'Enter') {
    submitPhoneNumber();
  }
}

document.addEventListener('DOMContentLoaded', function () {
  const phoneNumberInput = document.getElementById('phoneNumber');

  phoneNumberInput.addEventListener('keypress', handleKeyPress);
});
