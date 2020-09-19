from gl import Raytracer, color, V2, V3
from obj import Obj, Texture
from sphere import Sphere, Material, PointLight, AmbientLight
import random


# Snowman
snow = Material(diffuse=color(0.9,0.9,0.9), spec=32)
eyes = Material(diffuse=color(1,1,1), spec=64)
button = Material(diffuse=color(0.1,0.1,0.1), spec=16)
carrot = Material(diffuse=color(0.85,0.25,0.25), spec=32)

width = 240
height = 400

r = Raytracer(width,height)

r.pointLight = PointLight(position = V3(-2,2,0), intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)

#CUERPO
r.scene.append(Sphere(V3(0, -1, -5), 1, snow))
r.scene.append(Sphere(V3(0, 0.4, -5), 0.7, snow))
r.scene.append(Sphere(V3(0, 1.4, -5), 0.5, snow))

# BOTONES
r.scene.append(Sphere(V3(0, 0.4, -3), 0.08, button))
r.scene.append(Sphere(V3(0, 0, -3), 0.09, button))
r.scene.append(Sphere(V3(0, -.5, -3), 0.1, button))

#BOCA
r.scene.append(Sphere(V3(-0.14, 0.8, -3), 0.03, button))
r.scene.append(Sphere(V3(-0.06, 0.7, -3), 0.03, button))
r.scene.append(Sphere(V3(0.06, 0.7, -3), 0.03, button))
r.scene.append(Sphere(V3(0.14, 0.8, -3), 0.03, button))

#NARIZ
r.scene.append(Sphere(V3(0, 0.85, -3), 0.06, carrot))

#OJOS
r.scene.append(Sphere(V3(-0.1, 0.95, -3), 0.05, eyes))
r.scene.append(Sphere(V3(-0.1, 0.9505, -2.9), 0.03, button))

r.scene.append(Sphere(V3(0.1, 0.95, -3), 0.05, eyes))
r.scene.append(Sphere(V3(0.1, 0.9505, -2.9), 0.03, button))


r.rtRender()

r.glFinish('output.bmp')
