# Photo Encryption using Raspberry Pi 3
## Introduction
The image is first captured using the camera module of Raspberry Pi.
<img src="https://github.com/pinkai123/Photo-Encryption-in-Edge-Computing/blob/master/test1.jpg">
Faces are identified and mask with another image and the number of faces in the photo is obtained.
<img src="https://github.com/pinkai123/Photo-Encryption-in-Edge-Computing/blob/master/test.png">
The file with the number of face is encrypted and sent to the server.
For this experiment,the masked image is also encrypted using AEAD and sent to the server.
The files are decrypted to obtain the masked image and the number of faces.


## Technical Information
SSH needs to be setup first before running any of the code
There are 3 python scripts.
Please look at the comment in the scripts for the explanation of each part of the code

### 123.jpg 
example photo

### smiley.jpg 
image to mask the face

### face-detect-send(final).py 
	* Load the image into the face recognition algorithm
	* Mask the face with random images
	* Encrypt the file with AEAD
	* Run on Raspberry Pi

### face-detect-receive(final).py 
	*check and copy the file from the client into the server
 	*Decrypt and display the image and face count
	*Run on Windows Server

### scpEg.py 
	*Check the directory in the client for file and scp the file in
	*Remove any files in the client after the files are copied over
