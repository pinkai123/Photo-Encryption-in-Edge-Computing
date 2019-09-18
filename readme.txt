
<img src="https://github.com/pinkai123/Photo-Encryption-in-Edge-Computing/blob/master/test.jpg">
![test](https://github.com/pinkai123/Photo-Encryption-in-Edge-Computing/blob/master/test.jpg)

SSH needs to be setup first before running any of the code
There are 3 python scripts.

123.jpg - example photo

smiley.jpg - image to mask the face

face-detect-send(final).py - Load the image into the face recognition algorithm
			   - Mask the face with random images
			   - Encrypt the file with AEAD

face-detect-receive(final).py - check and copy the file from the client into the server
 			      - Decrypt and display the image and face count

scpEg.py - Check the directory in the client for file and scp the file in
	 - Remove any files in the client after the files are copied over

Please look at the comment in the scripts for the explanation of each part of the code
