import cv2
import numpy as np
from threading import Thread

class FrameSource():
    def get_frame(self):
        raise NotImplementedError

    def stop(self):
        # Use, if needed, to close down input streams
        pass


class FramesFromWebcam(FrameSource):
    """def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.still_active, self.frame = self.webcam.read()
        self.webcam_stop = False
        Thread(target=self._update_camera, args=()).start()

    def _update_camera(self):
        while True:
            if self.webcam_stop or not self.still_active:
                print("Camera exiting.")
                self.webcam.release()
                return
            self.still_active, self.frame = self.webcam.read()

    def get_frame(self):
        return self.frame

    def stop(self):
        self.webcam_stop = True"""

    def __init__(self):
        self.webcam = cv2.VideoCapture(0)
        self.still_active, self.frame = self.webcam.read()

    def get_frame(self):
        self.still_active, self.frame = self.webcam.read()
        return self.frame

    def stop(self):
        self.webcam.release()


class FramesFromVideo(FrameSource):
    def __init__(self, input_filename):
        self.input_filename = cv2.VideoCapture(input_filename)

        self.video_frames = []
        self.video_has_been_read = False

    def get_frame(self):
        if not self.video_has_been_read:
            self._read_video_data()

        i = np.random.choice(len(self.video_frames))
        return self.video_frames[i]

    def _read_video_data(self):
        print("Reading video data... ")
        self.video_generator = self._video_frame_generator(self.input_filename)
        self.video_frames = [frame for frame in self.video_generator]
        self.video_has_been_read = True
        print("Finished reading {} frames.".format(len(self.video_frames)))

    def _video_frame_generator(self, video_capture):
        frame_exists, frame = video_capture.read()
        while frame_exists:
            yield frame
            frame_exists, frame = video_capture.read()
