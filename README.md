Install all the requirements at first:

node
npm
ngrok

Also add the ngrok auth token using the following command:

ngrok config add-authtoken <<>>
raspberrypi.local

source /home/pi/py-venv/venv/bin/activate

Then run:

node server.js

It'll run the server on local host of 3000 port.


Then run the ngrok server on 3000 port using this command:

ngrok http --domain=killdeer-special-dogfish.ngrok-free.app 3000


Now, run the otp_gen.py

 and face_detect.py if needed.
