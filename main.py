import time

from src.object_tracking_and_processing import ObjectTrackingAndProcessing

def main() -> None:
    time.sleep(1)
    
    ObjectTrackingAndProcessing().process_video_stream()


if __name__ == '__main__':
    main()
