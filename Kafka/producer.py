import sys
import time
import cv2
from kafka import KafkaProducer

topic = "video_stream_testing"

def stream_video(video_file):
    """
    Publish given video file to a specified Kafka topic. 
    This Kafka Server will be running on the localhost.
    
    :param video_file: path to video file <string>
    """
    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    video = cv2.VideoCapture(video_file)
    
    print('streaming video...')

    while(video.isOpened()):
        success, frame = video.read()

        if not success:
            print("bad read!")
            break
        
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send(topic, buffer.tobytes())

        time.sleep(0.2)
    video.release()
    print('stream/publish complete')

    
def publish_camera():
    """
    Publish camera video stream to specified Kafka topic.
    This Kafka Server will be running on the localhost.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
        
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())
            
            time.sleep(0.2)

    except:
        print("\nExiting.")
        sys.exit(1)

    camera.release()


if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg. 
    Otherwise it will default by streaming webcam feed.
    """
    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        stream_video(video_path)
    else:
        print("Straming of video has been completed!")
        publish_camera()