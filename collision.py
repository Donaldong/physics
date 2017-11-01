"""
    File name: collision.py
    Author: Donald Dong
    Date created: 10/30/2017
    Reference: https://en.wikipedia.org/wiki/Elastic_collision
"""

from vpython import *
import numpy as np


def vec(arr):
    """
    Convert ndarray into a vpython vector
    :type arr: numpy.ndarray
    """
    return vector(arr[0], arr[1], arr[2])


class Object:
    def __init__(self, pos, mass):
        """
        Initialize an object with mass
        :type pos: numpy.ndarray
        :type mass: double
        """
        self.p = np.asarray(pos)
        self.m = mass
        self.v = np.zeros(3).astype(float)    # velocity
        self.a = np.zeros(3).astype(float)    # acceleration
        self.f = np.zeros(3).astype(float)    # net force

    def add_force(self, f):
        """
        Add a force vector
        """
        self.f += np.asarray(f)

    def step(self, dt):
        """
        Step based on elapsed time
        :type dt: double
        """
        self.a = self.f / self.m
        self.v += self.a * dt
        self.p += self.v * dt
        self.f = np.zeros(3).astype(float)


class Sphere(Object):
    # Define the border
    BOARDER_X = 5
    BOARDER_Y = -3
    # How many times the balls collide into each other?
    COUNT = 0

    def __init__(self, pos, mass, r):
        Object.__init__(self, pos, mass)
        self.r = r
        self.s = sphere(pos=vec(self.p), radius=r)

    def step(self, dt):
        if self.p[1] - self.r > Sphere.BOARDER_Y + 2 * Sphere.BOARDER_X:
            self.p[1] = Sphere.BOARDER_Y + 2 * Sphere.BOARDER_X - self.r
            self.v[1] *= -1.0
        if self.p[1] - self.r < Sphere.BOARDER_Y:
            self.p[1] = Sphere.BOARDER_Y + self.r
            self.v[1] *= -1.0
        if self.p[0] - self.r < -Sphere.BOARDER_X:
            self.p[0] = -Sphere.BOARDER_X + self.r
            self.v[0] *= -1.0
        if self.p[0] + self.r > Sphere.BOARDER_X:
            self.p[0] = Sphere.BOARDER_X - self.r
            self.v[0] *= -1.0
        if self.p[2] - self.r < -Sphere.BOARDER_X:
            self.p[2] = -Sphere.BOARDER_X + self.r
            self.v[2] *= -1.0
        if self.p[2] + self.r > Sphere.BOARDER_X:
            self.p[2] = Sphere.BOARDER_X - self.r
            self.v[2] *= -1.0
        Object.step(self, dt)
        self.s.pos = vec(self.p)

    def is_colliding(self, sphere):
        n = np.linalg.norm(sphere.p - self.p)
        if n <= self.r + sphere.r:
            Sphere.COUNT += 1
            n = (sphere.p - self.p) / n
            v1 = self.v
            v2 = sphere.v
            self.v = -n * np.linalg.norm(((self.m - sphere.m) * v1 + 2 * sphere.m * v2) / (self.m + sphere.m))
            sphere.v = n * np.linalg.norm(((sphere.m - self.m) * v2 + 2 * self.m * v1) / (self.m + sphere.m))
            return True
        return False

c = "Collision - Physics 3D\nAuthor: Donald Dong\nLeft click to toggle Gravity."
ground = box(pos=vector(0, 2, 0), length=10, height=10, width=10, color=color.gray(0.9), opacity=0.2)
g = 9.81
g_enable = True


def handle_click():
    global g_enable
    g_enable = not g_enable

scene.bind("mousedown", handle_click)
spheres_m = [
    50.0,
    25.0
]
spheres = [
    Sphere(np.zeros(3), spheres_m[1], 0.5),
    Sphere([0.5, 5, 0], spheres_m[0], 0.15),
    Sphere([0.5, 2, 0.5], spheres_m[0], 0.2),
    Sphere([0.5, 3, -0.5], spheres_m[0], 0.3),
    Sphere([-0.5, 4, 0.5], spheres_m[0], 0.4),
    Sphere([0.5, 5, -0.5], spheres_m[0], 0.1),
]

track = int(input())
spheres[track].s.color = color.red
f1 = gcurve(color=color.red)
dt = 0.01
t = 0
while True:
    scene.caption = "{}\nCollision Count: {}\n".format(c, Sphere.COUNT)
    f1.plot(pos=(t, np.linalg.norm(spheres[track].v)))  # curve
    rate(1.0/dt)
    if g_enable:
        spheres[0].add_force([0, -spheres_m[0] * g, 0])
        for i in range(len(spheres)-1):
            spheres[i+1].add_force([0, -spheres_m[1] * g, 0])
    for i in range(len(spheres)):
        for j in range(i+1, len(spheres)):
            spheres[i].is_colliding(spheres[j])
    for sphere in spheres:
        sphere.step(dt)
    t += dt
