# Description: This is the main file that will be used to run the tracking algorithm.
from utils import read_video, save_video
from Tracking import Tracker


def main():
    # The mainFrame like LAINe
    frames = read_video('Input_videos/samajeClips.mov')
    tracker = Tracker('models/best.pt')
    print('Tracking...')
    tracks = tracker.addTracker(frames, readFromSave=True, stubPath='stubs/track_stubs.pkl')
    print('Drawing Annotations...')
    TrackedVideo = tracker.drawAnnotatiomns(frames,tracks)
    save_video(TrackedVideo, 'Output_videos/samajeClips.avi')
    print('Completed :)')



if __name__ == "__main__":
    main()