import caffeine
from gl import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
floor = Material(diffuse = color(0.75, 0.75, 0.75 ), spec = 64)
mirror = Material(spec = 64, matType = REFLECTIVE)

glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT) 


width = 256
height = 256
r = Raytracer(width,height)
r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

# r.envmap = Envmap('envmap.bmp')
r.pointLight = PointLight(position = V3(0,-1,2), intensity = 1)
r.ambientLight = AmbientLight(strength = 0.1)


r.scene.append(Plane( V3(2,0,-2), V3(-1,0,0), floor)) # derecha
r.scene.append(Plane( V3(-2,0,-2), V3(1,0,0), floor)) # izquierda
r.scene.append(Plane( V3(-1,1,-10), V3(0,0,1), floor)) # Centro
r.scene.append(Plane( V3(0,-2,-2), V3(0,1,0), floor)) # Piso
r.scene.append(Plane( V3(0,2,-2), V3(0,-1,0), floor)) # Techo

r.scene.append(AABB(V3(0.5, -1, -4), 0.5, brick))
r.scene.append(AABB(V3(-0.5, -1, -4), 0.5, stone))


r.rtRender()

r.glFinish('output.bmp')
