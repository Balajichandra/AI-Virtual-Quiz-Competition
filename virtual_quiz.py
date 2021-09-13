## Note install --> pip install cvzone >= 1.5.1
import cv2
import csv
import time
from cvzone.HandTrackingModule import HandDetector
import cvzone
cap = cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.75)
class MCQ():
    def __init__(self,data):
        self.question = data[0]
        self.choice1  = data[1]
        self.choice2  = data[2]
        self.choice3  = data[3]
        self.choice4  = data[4]
        self.answer   = int(data[5])
        self.Usrans   = None
    def update(self,cursor,bboxs):
        for x,bbox in enumerate(bboxs):
            x1,y1,x2,y2 = bbox
            if x1<cursor[0]<x2 and y1<cursor[1]<y2:
                self.Usrans = x+1
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),cv2.FILLED)

pathCSV = "C:/Users/Balaji/Documents/Machine Learning/AI Virtual Mouse/mcqs.csv"
#print(pathCSV)
with open(pathCSV,newline='\n') as f:
    reader = csv.reader(f)
    dataAll = list(reader)[1:]
#print(dataAll)    
qNo = 0
qTotal = len(dataAll)

mcqList = []
for q in dataAll:
    mcqList.append(MCQ(q))
print(mcqList) 
print(len(mcqList))   
while True:
    success,img = cap.read()
    img = cv2.flip(img,1)
    Hands,img = detector.findHands(img,flipType=True)
    #mcq = mcqList[0]
    if qNo < qTotal:
        mcq = mcqList[qNo]
        img,bbox = cvzone.putTextRect(img,mcq.question,[100,100],2,2,offset=50,border=5)
        img,bbox1 = cvzone.putTextRect(img,mcq.choice1,[200,250],2,2,offset=50,border=5)
        img,bbox2 = cvzone.putTextRect(img,mcq.choice2,[500,250],2,2,offset=50,border=5)
        img,bbox3 = cvzone.putTextRect(img,mcq.choice3,[800,250],2,2,offset=50,border=5)
        img,bbox4 = cvzone.putTextRect(img,mcq.choice4,[1100,250],2,2,offset=50,border=5)

        if Hands:
            lmList = Hands[0]['lmList']
            cursor = lmList[8]
            length,info,img = detector.findDistance(lmList[8],lmList[12],img)
            if length < 60:
                mcq.update(cursor,[bbox1,bbox2,bbox3,bbox4])
                if mcq.Usrans is not None:
                    time.sleep(3)
                    qNo+=1
    else:
        score = 0
        for mcq in mcqList:
            if mcq.answer == mcq.Usrans:
                score+=1
        score = round((score/qTotal) * 100,2)
        img, _ = cvzone.putTextRect(img,"Quiz Completed",[250,300],2,2,offset=50,border=5)
        img, _ = cvzone.putTextRect(img,f'Your Score: {score}%',[700,300],2,2,offset=50,border=5)                        
    barValue = 150 + (950//qTotal)*qNo
    cv2.rectangle(img,(150,600),(barValue,650),(0,255,0),cv2.FILLED)
    cv2.rectangle(img,(150,600),(1100,650),(255,0,255),5)    
    img, _ = cvzone.putTextRect(img, f'{round((qNo / qTotal) * 100)}%', [1130, 635], 2, 2, offset=16)    
               

    cv2.imshow("img",img)
    cv2.waitKey(1)
    