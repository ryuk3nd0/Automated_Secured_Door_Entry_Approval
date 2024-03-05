const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
app.use(express.static(__dirname)); // Serve static files from the current directory
app.use(express.json());

const csvFilePath = path.join(__dirname, 'guest_requests.csv');
let canCheckOTP = true; // Variable to control OTP checking

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
      res.status(200).send('Your request has been accepted. You will be notified with OTP if verified.');

      canCheckOTP = false; // Disable OTP checking after a successful submission

      // Enable OTP checking after 2 seconds
      setTimeout(() => {
        canCheckOTP = true;
      }, 2000);
    }
  });
});

app.get('/checkOTP', (req, res) => {
  if (!canCheckOTP) {
    res.status(403).send('Please wait for a moment before checking for OTP again');
    return;
  }

  fs.readFile(csvFilePath, 'utf8', (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).send('Error reading data');
    } else {
      const lines = data.trim().split('\n').filter(line => line.trim() !== ''); // Remove empty lines
      let latestOTP = '';
      let latestPhoneNumber = '';
      let latestVerified = '';

      // Find the latest non-empty entry and its associated OTP
      for (let i = lines.length - 1; i >= 0; i--) {
        const line = lines[i].trim();
        if (line !== '') {
          const columns = line.split(',');
          latestOTP = columns[columns.length - 2].trim(); //OTP is the second last column
          latestPhoneNumber = columns[2].trim(); //Phone number is the third column
          latestVerified = columns[columns.length - 1].trim(); //Verified is the last column
          if(!latestOTP) console.log(`Latest OTP found: ${latestOTP}`);
          break;
        }
      }

      if (latestOTP && latestPhoneNumber === req.query.phoneNumber && latestVerified === '1') {
        res.status(200).json({ otp: latestOTP, 
          phoneNumber: latestPhoneNumber, 
          verified: latestVerified,
          message: '🎉 Congratulations 🎉Your request has been approved. Use this OTP: ' + latestOTP + ' to unlock the door.'});
      } else if(latestVerified === '0') {
        res.status(200).json({ otp: latestOTP, 
          phoneNumber: latestPhoneNumber, 
          verified: latestVerified,
          message: '❌ Sorry ❌ Your request has been declined.'});
      } else {
        res.status(404).send('No valid OTP available');
      }
    }
  });
});

app.listen(3000, () => {
  console.log('Server is running on port 3000');
});