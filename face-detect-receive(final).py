import cv2
from aead import AEAD
import base64
import numpy as np
import pickle
from matplotlib import pyplot as plt
import time
import scpEg

associated_dataB = None
key = None
Camera = {'Camera1':'192.168.1.2','Camera2': '192.15.123.111'}
i = 0

def main():
  global associated_dataB
  global key
  global i
  print('Available Cameras')
  #Ensure the data is from the camera the user chooses
  for key in Camera:
    print (key)
  cameraNumber = input('Enter the Camera which you like to obtain data from:')
  #Check for any files in directory
  while(scpEg.fileCheck(i) == False):
    pass

  #key and associated are assume to be in the server already. 
  key = readFile('key{}'.format(i))
  associated_dataB = cameraNumber.encode()
  #read the files
  faceCountEncrypted = readFile('faceCount{}'.format(i))
  imageEncrypted = readFile('image{}'.format(i))
  #create AEAD object
  cryptor = AEAD(key)
  #if file name is random, then the one way to identifed which file is for faceCount which is image is through length.
  #FileName is random so that sniffer cannot associated name of file with the data it holds
  try:
    if(len(faceCountEncrypted) < len(imageEncrypted)):
      number = number_decryption(cryptor,faceCountEncrypted,associated_dataB)
      image = image_decryption(cryptor,imageEncrypted,associated_dataB)   
    else:
      number = number_decryption(cryptor,imageEncrypted,associated_dataB)
      image = image_decryption(cryptor,faceCountEncrypted,associated_dataB)  
    print(number)
    scpEg.fileRemove(number,i)
    i =i + 1
     # Convert RGB to BGR
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    display(image)
  except ValueError:
    print('This Data is not from ' + associated_dataB.decode())

def display(image):
  plt.imshow(image,interpolation = 'bicubic')
  plt.xticks([]),plt.yticks([])
  plt.show()
   
def readFile(filename):
  with open(filename,'rb') as BinaryFile:
    data = pickle.load(BinaryFile)
    return data

def image_decryption(cryptor,ct,associated_dataB):
  #decrypted data in bytes
  decodedImageBytes = cryptor.decrypt(ct,associated_dataB)
  #bytesString to bytes
  decodedImageBytesString = base64.b64decode(decodedImageBytes)
  #bytes to bytesArray
  decodedImageBytesArray = np.frombuffer(decodedImageBytesString,dtype=np.uint8)
  #reads an image from buffer memory
  img = cv2.imdecode(decodedImageBytesArray,1)
  return img

def number_decryption(cryptor,ct,associated_dataB):
  # Decrypt the file with the face count
  numberB = cryptor.decrypt(ct,associated_dataB)
  number = int.from_bytes(numberB,'little')
  return number

if __name__ == '__main__':
  main()
