import numpy as np
import torch
import cv2
import time



# class Inference:
#     model = None
#     results = None
#     tag = None
#     datajumlahterdeteksi = [0,0,0]
#     def __init__(self):
#         self.model = torch.hub.load(r'../../yolo', 'custom', path='/home/alldone/Desktop/sawit-yolo/model/content/yolov5/runs/train/exp5/weights/best.pt', source='local',
#                        force_reload=True, device='cpu')
#         self.model.conf = 0.7
#         self.model.line_thickness = 1
#         # cam = cv2.VideoCapture(0) 
        
#     def detect(self,frame):
#         # cv2.resize(frame, (640, 480))
#         self.results = self.model(frame)
#         self.tag = self.results.names
#         if (len(self.results.xyxy[0]) != 0):
#             data_coor = self.results.xyxy[0].numpy()[0]
#             print("=====================================")
#             datajumlahterdeteksi = [0,0,0]
#             for i in self.results.xyxy[0]:
#                 datajumlahterdeteksi[int(i[5])] = datajumlahterdeteksi[int(i[5])] + 1
#             for number,i in enumerate(datajumlahterdeteksi):
#                 print(self.tag[number]+" : "+str(i))
#             print("=====================================")
#         frame = np.squeeze(self.results.render())
        
#         return frame
        


  
def readcamera():
    ret, frame = cam.read()
    cv2.resize(frame, (640, 480))
    return frame
def runned():
    
    while(True): 
        image = readcamera()
        
        fps_counter += 1
        if time.time() - fps_start_time >= 1.0:
            fps = fps_counter / (time.time() - fps_start_time)
            print(f"FPS: {fps:.2f}")
            
            fps_counter = 0
            fps_start_time = time.time()
    
        results = model(image)
        # print(dir(results.names))
        tag = results.names
        # print (tag)
        
        if (len(results.xyxy[0]) != 0):
            data_coor = results.xyxy[0].numpy()[0]
            print("=====================================")
            datajumlahterdeteksi = [0,0,0]
            for i in results.xyxy[0]:
                datajumlahterdeteksi[int(i[5])] = datajumlahterdeteksi[int(i[5])] + 1
            for number,i in enumerate(datajumlahterdeteksi):
                print(tag[number]+" : "+str(i))
            print("=====================================")
            
        cv_img = np.squeeze(results.render())
        
        
        cv2.imshow('frame', cv_img)
        coor = results.xyxy[0]
        i = 0
    
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    
    
    
    # After the loop release the cap object 
    cam.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 