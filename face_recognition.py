"""
Created on Sat Dec 16 19:40:42 2017

@author: vsnick
"""
import cv2
import os
import os.path
import numpy as np

subjects = ["", "Emma watson", "Disha patani"]

def detect_face(img):
 gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
 faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
 if (len(faces) == 0):
     return None, None
 x, y, w, h = faces[0]
 return gray[y:y+w, x:x+h], faces[0]

def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)    
    faces = []
    labels = []
    for dir_name in dirs:
        print dir_name
        if not dir_name.startswith("s"):
            continue;       
        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name 
        print subject_dir_path
        subject_images_names = os.listdir(subject_dir_path)
        #print subject_images_names
        i = 0
        for image_name in subject_images_names:
            print repr(i)+" "+image_name
            i = i + 1 
            if image_name.startswith("."):
                continue;        
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            #cv2.imshow("Training on image...", image)
            #cv2.waitKey(100)
            face, rect = detect_face(image)
            if face is not None:        
                faces.append(face)
                labels.append(label)
            #cv2.destroyAllWindows()
            #cv2.waitKey(1)
            #cv2.destroyAllWindows()
    return faces, labels

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
 
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img):
    img = test_img.copy()
    face, rect = detect_face(img)
    label= face_recognizer.predict(face)
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return img

#or use EigenFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.createEigenFaceRecognizer()
 
#or use FisherFaceRecognizer by replacing above line with 
#face_recognizer = cv2.face.createFisherFaceRecognizer()

face_recognizer = cv2.face.createLBPHFaceRecognizer()

if(os.path.exists('model.xml')):
    print("Trained Model Available..")
    face_recognizer.load("model.xml")
else:
    print("Preparing data...")
    faces, labels = prepare_training_data("training-data")
    print("Data prepared")
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    face_recognizer.train(faces, np.array(labels))
    face_recognizer.save("model.xml")

print("Predicting images...")

#load test images
test_img1 = cv2.imread("test-data/test1.jpg")
test_img2 = cv2.imread("test-data/test2.jpg")

#perform a prediction
predicted_img1 = predict(test_img1)
predicted_img2 = predict(test_img2)
print("Prediction complete")

#display both images
cv2.imshow(subjects[1], predicted_img1)
cv2.imshow(subjects[2], predicted_img2)
cv2.waitKey(0)
cv2.destroyAllWindows()