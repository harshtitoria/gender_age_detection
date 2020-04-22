import numpy as np
import cv2
import pafy
"""
url = 'https://www.youtube.com/watch?v=c07IsbSNqfI&feature=youtu.be%27'
vpafy = pafy.new(url)
print (vpafy.title)
print (vpafy.rating)
print (vpafy.viewcount)
play = vpafy.getbest(preftype="mp4")
"""
cap = cv2.VideoCapture(play.url)
cap.set(3,480)
cap.set(4,640)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']


def load_caffe_models():
    age_net = cv2.dnn.readNetFromCaffe("deploy_age.prototxt","age_net.caffemodel")
    gender_net = cv2.dnn.readNetFromCaffe('deploy_gender.prototxt','gender_net.caffemodel')
    return(age_net, gender_net)


def video_detector(age_net,gender_net):
    font = cv2.FONT_HERSHEY_SIMPLEX


    while True:
        ret,image = cap.read()
        face_cascade = cv2.CascadeClassifier("harrcascade_frontalface_alt.xml")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)
   
        if len(faces)>0:
            print("Found{}faces".format(str(len(faces))))

        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x,y), (x+w,y+h),(255,255,0),2)
            #get a face
            face_image = image[y:y+h,x:x+w].copy()
            blob = cv2.dnn.blobFromImage(face_image, 1, (277,277), MODEL_MEAN_VALUES, swapRB=False)
            #prediction of gender
            gender_net.setInput(blob)
            gender_predictions = gender_net.forward()
            gender = gender_list[gender_predictions[0].argmax()]
            print("Gender : " + gender)
            #prediction of age
            age_net.setInput(blob)
            age_predictions = age_net.forward()
            age = age_list[age_predictions[0].argmax()]
            print("Age " + age)
            overlay_txt = "%s, %s"% (gender,age)
            cv2.putText(image, overlay_txt, (x,y), font, 2, (255,255,255), 2, cv2.LINE_AA)

        cv2.imshow("image", image)
        key = cv2.waitkey(1) & 0xFF
    
        if key == ord("q"):
            break

if __name__=="__main__":
    age_net,gender_net = load_caffe_models()
    video_detector(age_net,gender_net)





















