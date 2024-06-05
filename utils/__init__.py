from utils.video_Utils import read_video, save_video
from utils.boundaryBox import getCenterOfBoundaryBox, getBoundaryBoxWidth

def main():
        # expose code here
    frames = read_video('Input_videos/samajeClips.mov')
    save_video(frames, 'Output_videos/samajeClips.avi')

if __name__ == "__main__":
    main()