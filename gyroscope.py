from vpython import *


class Gyroscope:
    def __init__(self):
        self.ring_color = color.gray(0.8)
        self.flag1 = False
        self.flag2 = False
        rod_color = color.orange

        ring_thickness = 0.03
        rod_axis_length = 0.2
        radius_ring = [1.0, 0.9, 0.8]
        radius_disk = 0.5

        self.rings = [
            ring(pos=vector(0, 0, 0), axis=vector(0, 0, 1), radius=radius_ring[0],
                 thickness=ring_thickness, color=self.ring_color),
            ring(pos=vector(0, 0, 0), axis=vector(0, 1, 0), radius=radius_ring[1],
                 thickness=ring_thickness, color=self.ring_color),
            ring(pos=vector(0, 0, 0), axis=vector(1, 0, 0), radius=radius_ring[2],
                 thickness=ring_thickness, color=self.ring_color)
        ]

        self.rods = [
            cylinder(pos=vector(radius_ring[0] - rod_axis_length/2, 0, 0), axis=vector(1, 0, 0),
                     radius=ring_thickness/2, color=rod_color, length=rod_axis_length),
            cylinder(pos=vector(-radius_ring[0] + rod_axis_length/2, 0, 0), axis=vector(1, 0, 0),
                     radius=ring_thickness/2, color=rod_color, length=-rod_axis_length),
            cylinder(pos=vector(0, 0, radius_ring[1] - rod_axis_length / 2), axis=vector(0, 0, 1),
                     radius=ring_thickness / 2, color=rod_color, length=rod_axis_length),
            cylinder(pos=vector(0, 0, -radius_ring[1] + rod_axis_length / 2), axis=vector(0, 0, 1),
                     radius=ring_thickness / 2, color=rod_color, length=-rod_axis_length),
            cylinder(pos=vector(0, -0.65-rod_axis_length, 0), axis=vector(0, 1, 0), radius=ring_thickness / 2,
                     color=rod_color, length=1.3+2*rod_axis_length),
        ]

        self.disk = cylinder(pos=vector(0, -rod_axis_length/2, 0), axis=vector(0, 1, 0), radius=radius_disk,
                             color=color.yellow, length=rod_axis_length)

        self.box = box(pos=vector(0, 0, 0), length=2.2*radius_ring[0],
                       height=2.2*radius_ring[0], width=2.2*radius_ring[0], opacity=0.2)

        rho_rings = 2.0
        rho_disk = 4.0
        k = rho_rings*pi*ring_thickness ** 2 * 2 * pi
        self.m_rings = [k*radius_ring[0], k*radius_ring[1], k*radius_ring[2]]
        self.m_disk = rho_disk * pi * radius_disk ** 2 * rod_axis_length

        self.compounds = [
            compound([
                self.box, self.rings[0], self.rods[0], self.rods[1]
            ]),
            compound([
                self.rings[1], self.rods[2], self.rods[3]
            ]),
            compound([
                self.rings[2], self.rods[4], self.disk
            ])
        ]

    def step(self, elapsed, angle, axis=vector(0, 1, 0)):
        self.compounds[0].rotate(angle, axis)
        self.compounds[1].rotate(angle, axis)
        self.compounds[1].rotate(angle)
        self.compounds[2].rotate(angle, vector(0, 1, 0))

scene.caption = "Gyroscope Simulation\n\tDonald Dong & Reyna Ortiz"
ground = box(pos=vector(0, -3, 0), length=10, height=0.1, width=10, color=color.gray(0.9))
gyro = Gyroscope()


def handle_click():
    if scene.mouse.pick is gyro.compounds[0]:
        if gyro.flag1:
            scene.mouse.pick.color = color.gray(0.8)
            gyro.flag1 = False
        else:
            scene.mouse.pick.color = color.red
            gyro.flag1 = True
    if scene.mouse.pick is gyro.compounds[2]:
        if gyro.flag2:
            scene.mouse.pick.color = color.gray(0.8)
            gyro.flag2 = False
        else:
            scene.mouse.pick.color = color.green
            gyro.flag2 = True


scene.bind("mousedown", handle_click)


dt = 1e5
while True:
    # rate(200)
    rate(200)
    gyro.step(dt, 0.01, vector(0, 1, 0))
