import cv2
import mediapipe as mp
import time


class poseDetector():
    def __init__(self ,  mode = False , upBody = False , smooth  = True ,  dectionCon = 0.5 , trackCon = 0.5):
        self.mode = mode 
        self.upBody = upBody
        self.smooth = smooth
        self.dectionCon = dectionCon
        self.trackCon = trackCon
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode  ,self.upBody , self.smooth,self.dectionCon ,self.trackCon)

    def getPose(self ,  frame ,  draw=True):
        imgRGB= cv2.cvtColor(frame , cv2.COLOR_BGR2RGB)
        self.result = self.pose.process(imgRGB)
        if self.result.pose_landmarks :
            if draw :
                self.mpDraw.draw_landmarks(frame , self.result.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return frame
    
    def getlandmark(self,  frame , draw = True) :
        marklist = []
        if self.result.pose_landmarks:
          for id , lm  in enumerate(self.result.pose_landmarks.landmark) :
            h , w , c = frame.shape
            cx  ,  cy = int(lm.x*w) , int(lm.y*h)
            marklist.append([id, cx, cy])
            if draw:
                cv2.circle(frame,  (cx,cy) ,  5 , (255 ,255, 0)  , cv2.FILLED)
        return marklist        

            
       
        

   
 




  


# ---------------------------- |Test code| ------------------------------------------------------

def main():
    cam =cv2.VideoCapture(0)
    pTime = 0
    detector = poseDetector() # object creat 

    while True :
      sucess, frame = cam.read()
      img = detector.getPose(frame , False)
      marklist = detector.getlandmark(img, False)
      try :
        # print(marklist[14])
        cv2.circle(frame,  (marklist[14][1] , marklist[14][2]) ,  5 , (255 ,255, 0)  , cv2.FILLED)
      except IndexError :
          print("Not found")
     

      cTime = time.time()
      fps = 1/(cTime-pTime)
      pTime = cTime
      cv2.putText(frame , str(int(fps)) , (70, 50) , cv2.FONT_HERSHEY_PLAIN , 3 , (255, 0, 255) , 3)
      cv2.imshow("Image" , frame)
      if cv2.waitKey(30) & 0xff == ord('q'):
              break
                                  




if __name__ == "__main__" :
    main()
