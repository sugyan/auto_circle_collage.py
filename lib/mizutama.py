import cv2
import random
import numpy as np
from os import path

class Mizutama:
    def __init__(self, img):
        rows, cols, _ = img.shape
        if max(rows, cols) > 1024:
            l = max(rows, cols)
            img = cv2.resize(img, (cols * 1024 / l, rows * 1024 / l))
        self.img = img
        self.mizutama = []

    def detect_mizugi(self):
        self.mizugi_areas = []
        mzg = cv2.inRange(cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV), np.array([0, 180, 8]), np.array([360, 255, 247]))
        mzg = cv2.erode(mzg, np.ones((1, 1), np.uint8))  # kernel size?
        mzg = cv2.dilate(mzg, np.ones((1, 1), np.uint8)) # kernel size?
        _, contours, _ = cv2.findContours(mzg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            if contour.size > 25:
                self.mizugi_areas.append(contour)

    def detect_faces(self):
        cascades_dir = path.normpath(path.join(cv2.__file__, '..', '..', '..', '..', 'share', 'OpenCV', 'haarcascades'))
        cascade = cv2.CascadeClassifier(path.join(cascades_dir, 'haarcascade_frontalface_alt2.xml'))
        gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        self.faces = cascade.detectMultiScale(gray)
        print self.faces

    def create_mizutama(self):
        for x, y, w, h in self.faces:
            c = self.create_circle(x + w / 2, y + h / 2, max(h / 2, w / 2))
            if c is not None:
                self.mizutama.append(c)
        for verts in ([0, 0], [0, self.img.shape[0]], [self.img.shape[1], 0], [self.img.shape[1], self.img.shape[0]]):
            c = self.create_circle(verts[0], verts[1])
            if c is not None:
                self.mizutama.append(c)
        for i in range(0, 150):
            c = self.create_circle(random.randrange(self.img.shape[1]), random.randrange(self.img.shape[0]))
            if c is not None:
                self.mizutama.append(c)

    def create_circle(self, x, y, m = None):
        r = min(self.img.shape[0], self.img.shape[1])
        while self.detect_mizugi_collision(x, y, r):
            r -= 5
            if m is not None and r < m:
                return (x, y, r)
            if r < 20:
                return
        return (x, y, r)

    def detect_mizugi_collision(self, x, y, r):
        for mizugi_area in self.mizugi_areas:
            rect = cv2.boundingRect(mizugi_area)
            if self.check_rect_collision(rect, (x, y, r)):
                hull = cv2.convexHull(mizugi_area)
                if self.check_convex_hull_collision(hull, (x, y, r)):
                    return True
        for c in self.mizutama:
            if self.detect_mizutama_collision(c, (x, y, r)):
                return True
        return False

    def detect_mizutama_collision(self, c1, c2):
        # return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 < (c1[2] + c2[2]) ** 2
        return (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 < (c1[2] * 0.9 + c2[2] * 0.9) ** 2

    def check_rect_collision(self, rect, circle):
        rx, ry, rw, rh = rect
        cx, cy, cr = circle
        lr = rx - cr <= cx <= rx + rw + cr and ry <= cy <= ry + rh
        tb = ry - cr <= cy <= ry + rh + cr and rx <= cx <= rx + rw
        tl = (rx - cx) ** 2 + (ry - cy) ** 2 < cr ** 2
        tr = (rx + rw - cx) ** 2 + (ry - cy) ** 2 < cr ** 2
        bl = (rx - cx) ** 2 + (ry + rh - cy) ** 2 < cr ** 2
        br = (rx + rw - cx) ** 2 + (ry + rh - cy) ** 2 < cr ** 2
        return lr or tb or tl or tr or bl or br

    def check_convex_hull_collision(self, hull, circle):
        cx, cy, cr = circle
        if cv2.pointPolygonTest(hull, (cx, cy), False) >= 0.0:
            return True
        for i in range(len(hull)):
            a = hull[i][0]
            b = hull[i + 1][0] if i < len(hull) - 1 else hull[0][0]
            pa = a - (np.array([cx, cy]))
            ab = b - a
            mag = np.linalg.norm(ab)
            if mag < 5:
                continue
            if abs(np.cross(pa, ab) / mag) < cr:
                return True
        return False

    def collage(self):
        self.detect_faces()
        self.detect_mizugi()
        self.create_mizutama()

        # mizutama mask
        mask = np.zeros((self.img.shape[0], self.img.shape[1]), np.uint8)
        for mztm in self.mizutama:
            cv2.circle(mask, (mztm[0], mztm[1]), mztm[2], 255, -1)
        img1 = cv2.bitwise_and(self.img, self.img, mask = mask)

        # inpaint and blur
        blur = cv2.blur(cv2.inpaint(self.img, 255 - mask, 10, cv2.INPAINT_TELEA), (50, 50))
        img2 = cv2.bitwise_and(blur, blur, mask = 255 - mask)

        return cv2.add(img1, img2)
