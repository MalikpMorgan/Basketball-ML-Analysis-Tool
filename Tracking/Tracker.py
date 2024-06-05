from ultralytics import YOLO
import supervision as sv
import cv2
import os
import pickle
import sys
import copy
sys.path.append('../')
from utils import getBoundaryBoxWidth, getCenterOfBoundaryBox

class Tracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path) 
        self.trackers = sv.ByteTrack()

    def detectFrames(self, frames):
       batchSize = 20
       detections = []
       counter = 0
       for i in range(0, len(frames), batchSize):
            if counter == 2:
                break
            batchedDetections = self.model.predict(frames[i:i+batchSize], conf=0.2)
            detections += batchedDetections
            counter += 1
       return detections

    def addTracker(self, frames, readFromSave=False, stubPath = None): 
        
        if readFromSave and stubPath is not None and os.path.exists(stubPath):
            with open(readFromSave, 'rb') as f:
                return pickle.load(f)
        #initialize objects to track from the detections
        tracks = {
            "Player": [],
            "Ball": [],
            "Ref": [],
        }
        print('Detecting Frames...')
        detections = self.detectFrames(frames)
        print('Adding tracker...')
        for frameNum, detection in enumerate(detections):
            classNames = detection.names
            classNamesInv = {v: k for k, v in classNames.items()}
            print(classNames)
            print('======================')
            #supervision detection format?
            SupervisionDetections = sv.Detections.from_ultralytics(detection)
            print(SupervisionDetections)

            #Convert any  nodes to a track

            #add tracking by Id
            detectionsWithTracks = self.trackers.update_with_detections(SupervisionDetections)
            #initialize the tracks as an array of dictionaries
            tracks["Player"].append({})
            tracks["Ball"].append({})
            tracks["Ref"].append({})

            for detectionframes in detectionsWithTracks:
                bbox = detectionframes[0].tolist()
                classId = detectionframes[3]
                trackId = detectionframes[4]

                if classId == classNamesInv['Player']:
                    tracks["Player"][frameNum][trackId] = {"bbox": bbox}
                
                if classId == classNamesInv['Ref']:
                    tracks["Ref"][frameNum][trackId] = {"bbox": bbox}
                    
                if classId == classNamesInv['Ball']:
                    tracks["Ball"][frameNum][trackId] = {"bbox": bbox}

        print(detectionsWithTracks)

        if stubPath is not None:
            with open(stubPath,'wb') as f :
                pickle.dump(tracks, f)

        return tracks

    def drawElipse(self, frame, bbox, color, trackId = None):
        y2 = int(bbox[3])
        xCenter, _ = getCenterOfBoundaryBox(bbox)
        width = getBoundaryBoxWidth(bbox)

        cv2.ellipse(
            frame,
            center=(xCenter,y2),
            axes=(int(width), int(0.35*width)),
            angle=0.0,
            startAngle=-45,
            endAngle=235,
            color = color,
            thickness=2,
            lineType=cv2.LINE_4
        )

        return frame           

    def drawAnnotatiomns(self, frames, tracks):
        videoFrames = []
        counter = 0
        for frameNum, frame in enumerate(frames):
            if counter == 35:
                break
            frame = copy.deepcopy(frame)
            print(frameNum)
            playerDictonary = tracks["Player"][frameNum]
            refDictonary = tracks["Ref"][frameNum]
            ballDictonary = tracks["Ball"][frameNum]
            
            #draw the bounding boxes for the players
            for trackId, player in playerDictonary.items():
                boundarybox = player["bbox"]
                color = (131, 26, 174)
                frame = self.drawElipse(frame, boundarybox, color, trackId)

                videoFrames.append(frame)
            counter += 1      
        return videoFrames




            


