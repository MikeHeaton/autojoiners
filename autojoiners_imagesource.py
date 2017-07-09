import cv2
import numpy as np

FRONT_CASCADE_PATH = "haarcascade_frontalface_default.xml"
SIDE_CASCADE_PATH = "haarcascade_profileface.xml"

# FACE DETECT PARAMS
SCALEFACTOR = 1.1
MINNEIGHBORS = 10
MINSIZE = (30, 30)


class CascadeWrapper():
    def __init__(self, cascadesource, flip=False):
        self.cascade = cv2.CascadeClassifier(cascadesource)
        self.flip = flip


class ImageSource():
    def get_image(self):
        raise NotImplementedError

    def stop(self):
        # Use, if needed, to close down input streams
        pass


class FacesFromVideo(ImageSource):
    def __init__(self, frame_source, pertubation=0, border=[0,0],
                 cascades=[CascadeWrapper(FRONT_CASCADE_PATH, flip=False),
                           CascadeWrapper(SIDE_CASCADE_PATH, flip=False),
                           CascadeWrapper(SIDE_CASCADE_PATH, flip=True)]):
        self.frame_source = frame_source
        self.variance = pertubation
        self.cascades = cascades
        if type(self.cascades) is not list:
            self.cascades = [self.cascades]
        self.all_faces = []
        self.border_size = border

    def get_image(self):
        while True:
            frame = self.frame_source.get_frame()
            faces = self._all_faces_in_frame(frame)
            if len(faces) > 0:
                biggest_face_in_frame = max(faces, key=lambda im: im.size)
                self.all_faces += [biggest_face_in_frame]
                return biggest_face_in_frame

    def stop(self):
        self.frame_source.stop()

    def _all_faces_in_frame(self, frame):
        face_locations = self._face_locations(frame)
        return [self._extract_region_from_image(face_loc, frame)
                for face_loc in face_locations]

    def _face_locations(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = [i for cascade in self.cascades
                 for i in self._run_cascade(cascade, gray_image)]

        return faces

    def _run_cascade(self, cascade, gray_image):
        if cascade.flip:
            oriented_gray_image = cv2.flip(gray_image, 1)
        else:
            oriented_gray_image = gray_image
        detected_faces = cascade.cascade.detectMultiScale(
                                                oriented_gray_image,
                                                scaleFactor=SCALEFACTOR,
                                                minNeighbors=MINNEIGHBORS,
                                                minSize=MINSIZE)

        return [f for f in detected_faces]
        # Just using 'detected_faces' doesn't work
        # because detectMultiScale returns different types
        # for zero and nonzero results.

    def _extract_region_from_image(self, region, image):
        x, y, w, h = region
        x, y, w, h = (int(x + np.random.randn() * self.variance),
                      int(y + np.random.randn() * self.variance),
                      w, #int(w + np.random.randn() * self.variance),
                      h) #int(h + np.random.randn() * self.variance))
        face = image[max(0, y - self.border_size[0]): min(y + h + self.border_size[0], image.shape[0]),
                     max(0, x - self.border_size[1]): min(x + w + self.border_size[1], image.shape[1]),
                     :]
        return face


class RawImages(ImageSource):
    def __init__(self, frame_source):
        self.frame_source = frame_source

    def get_image(self):
        frame = self.frame_source.get_frame()
        return frame
