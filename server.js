const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.static(__dirname)); // Serve static files from the current directory
app.use(express.json());

const csvFilePath = path.join(__dirname, 'guest_requests.csv');

app.post('/submitPhoneNumber', (req, res) => {
  const phoneNumber = req.body.phoneNumber;
  const dateTime = new Date().toLocaleString();
  const data = `${dateTime},${phoneNumber}\n`;

  fs.appendFile(csvFilePath, data, { flag: 'a+' }, (err) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error saving data');
    } else {
      console.log('Data appended to file');
      // Change the message below to the desired message
      res.status(200).send('Your request has been accepted. You will be notified with an SMS if verified.');
    }
  });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});
