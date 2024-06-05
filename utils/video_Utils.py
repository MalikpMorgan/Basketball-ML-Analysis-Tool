import cv2

# Take in a video using the path name check ret value 
# if so add the frames to the array
def read_video(videoPath):
    video = cv2.VideoCapture(videoPath)
    frames = []
    print('Reading video...')
    while True:
        ret, frame = video.read()
        if not ret:
            break
        frames.append(frame)
    return frames
    
 #    
def save_video(frames, videoPath):
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(videoPath, fourcc, 24 , (frames[0].shape[1], frames[0].shape[0]))
    print('Saving video...')
    for frame in frames:
        out.write(frame)
    out.release()