import cv2
import face_recognition
from aead import AEAD
import base64
import numpy as np
import pickle
from matplotlib import pyplot as plt
import os
from picamera import PiCamera
from time import sleep
import shutil

face_count = 0
adjustment = 60
associated_data = "Camera1"
image = None
i = 0

def main():
    global image
    global i
    j=0
    ## still_image is for the camera module. Uncomment only if u have an camera module
    #still_image()
    file_list = os.listdir()
    for i in range(len(file_list)):
        if('.jpg' in file_list[i]):
            filename = file_list[i]
            #Load the photo into the face recognition algorithm and obtain face_locations
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            #Mask the face with random image
            image = masking(face_locations)
            SaveBlurring()
            #Generate key
            key = AEAD.generate_key()
            #Encrypt image and face count
            faceCountEncrypted = number_encryption(key)
            imageEncrypted = image_encryption(key)
            writeBinaryFile(faceCountEncrypted,'faceCount{}'.format(j))
            writeBinaryFile(imageEncrypted,'image{}'.format(j))
            # Assume key and assoicated_data already known at the server side
            writeBinaryFile(key,'key{}'.format(j))
            writeBinaryFile(associated_data.encode(),'associated_data{}'.format(j))
            j = j + 1

def masking(face_locations):
    global face_count
    img11 = cv2.imread("smiley.png")
    img1 = cv2.cvtColor(img11, cv2.COLOR_RGB2BGR)
    #getting wdith and height of image
    window_height,window_width = image.shape[:2]

    for face_location in face_locations:
        face_count = face_count + 1

        # Print the location of each face in this image
        top, right, bottom, left = face_location
        top = top - adjustment
        bottom = bottom + adjustment
        left = left - (int)(adjustment/2)
        right = right + (int)(adjustment/2)
        if(top < 0):
           top = 0
        if(left < 0):
            left = 0
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

        # You can access the actual face itself like this:
        #gettin roi
        face_image = image[top:bottom, left:right]
        #saving the face image
        cv2.imwrite('face'+str(face_count)+'.png',cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))
        cv2.imwrite('Converted/face'+str(face_count)+'.png',cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR))

        #resize img1 to become img2
        height,width = face_image.shape[:2]
        img2 = cv2.resize(img1,(width,height))

        #create mask
        img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
        ret,mask = cv2.threshold(img2gray, 245, 255, cv2.THRESH_BINARY_INV)

        #create inverse mask
        mask_inv = cv2.bitwise_not(mask)

        # Now black-out the area of logo in ROI
        img1_bg = cv2.bitwise_and(face_image,face_image,mask = mask_inv)
        #cv2.imshow("img1_bg",img1_bg)

        # Take only region of logo from logo image.
        img2_fg = cv2.bitwise_and(img2,img2,mask = mask)
        
        # Put logo in ROI and modify the main image
        dst = cv2.add(img1_bg,img2_fg)

        #modify main image
        image[top:bottom, left:right] = dst

    print("Faces found: ", face_count)
    return image

    #save no of faces
    with open("noOfFaces.txt", "w") as f: 
        f.write(str(face_count)) 

def SaveBlurring():
    global image

    #convert final image to BGR
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    #Saving the faceless image
    cv2.imwrite('final.jpg',image)

def writeBinaryFile(dataB,filename):
    with open(filename,'wb') as f:
        pickle.dump(dataB,f)
    #Make another copy as backup
    shutil.copy(filename,'Converted/' + filename)
        
def generate_key():
    #generate key
    key = AEAD.generate_key()
    return key


def image_encryption(key):
    cryptor =  AEAD(key)
    #convert image to memory buffer
    imageBytesArray = cv2.imencode('.jpg',image)[1]
    #convert bytesArray to bytesString
    imageBytes = base64.b64encode(imageBytesArray)
    #encrypted data
    ct = cryptor.encrypt(imageBytes,associated_data.encode())
    return ct

def number_encryption(key):
    cryptor = AEAD(key)
    #convert int to bytes
    face_countB = face_count.to_bytes(2,'little')
    ct = cryptor.encrypt(face_countB, associated_data.encode())
    return ct
    
def decryption():
    #decrypted data in bytes
    decodedImageBytes = cryptor.decrypt(ct,associated_data.encode())
    #bytesString to bytes
    decodedImageBytesString = base64.b64decode(decodedImageBytes)
    #bytes to bytesArray
    decodedImageBytesArray = np.frombuffer(decodedImageBytesString,dtype=np.uint8)
    #reads an image from buffer memory
    img = cv2.imdecode(decodedImageBytesArray,0)
    return img
def still_image():
    global i
    camera = PiCamera()
    #Rotate the camera to an upright position
    camera.rotation = 270
    camera.start_preview()
    sleep(5)
    camera.capture('image{}.jpg'.format(i))
    camera.stop_preview()


if __name__ == '__main__':
		main()
