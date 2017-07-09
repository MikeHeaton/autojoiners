import scipy.misc
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as ptch
from tqdm import tqdm


class JoinerCanvas():
    def __init__(self, canvas_shape, shatter_source,
                 image_source, output_path):
        self.canvas_shape = canvas_shape
        self.shatter_source = shatter_source
        self.image_source = image_source
        self.output_path = output_path

    def create_canvas(self):
        for polygon in tqdm(self.shatter_source.shatter()):
            image = self.image_source.get_image()
            image = scipy.misc.imresize(image, self.canvas_shape)

            self._add_clipped_image(polygon, image)

        self.image_source.stop()

    def show_save_canvas(self):
        plt.axis('off')
        plt.savefig(self.output_path, bbox_inches='tight')
        plt.show()

    def _add_clipped_image(self, polygon, image):
        patch = ptch.Polygon(polygon, fill=False, edgecolor='none')

        im = plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax = plt.gca()
        ax.add_patch(patch)
        im.set_clip_path(patch)
