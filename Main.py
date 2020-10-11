import caffeine
from gl import Raytracer, color, V2, V3
from obj import Obj, Texture, Envmap
from sphere import *
import random

brick = Material(diffuse = color(0.8, 0.25, 0.25 ), spec = 16)
stone = Material(diffuse = color(0.4, 0.4, 0.4 ), spec = 32)
floor = Material(diffuse = color(0.75, 0.75, 0.75 ), spec = 64)
water = Material(diffuse = color(0.137, 0.42, 0.48 ), spec = 64)
mirror = Material(spec = 64, matType = REFLECTIVE)
glass = Material(spec = 64, ior = 1.5, matType= TRANSPARENT)
water = Material(spec = 128, ior = 1.5, matType= TRANSPARENT)

whale_belly = Material(diffuse= color(0.887, 0.973, 1), spec = 128)
whale_skin = Material(diffuse=color(1, 1, 1), spec = 32)
whale_eye = Material(diffuse=color(0.3, 0.3, 0.3), spec=256)

boxMat = Material(texture = Texture('box.bmp'))

moonMat = Material(texture = Texture('moon.bmp'))


width = 256
height = 256
r = Raytracer(width,height)
# r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

r.envmap = Envmap('sky1.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
r.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.6)
r.ambientLight = AmbientLight(strength = 0.3)

# Objects
#r.scene.append( Sphere(V3( 0, 0, -8), 2, brick) )
#r.scene.append( Sphere(V3( -0.5, 0.5, -5), 0.25, stone))
#r.scene.append( Sphere(V3( 0.25, 0.5, -5), 0.25, stone))

#Water
r.scene.append(Plane(V3(0, -6, 1),V3(0, 1, 0), glass))
r.scene.append(Plane(V3(0, -7, 1),V3(0, 1, 0), water))

r.scene.append(Sphere(center=V3(-3, -5, -12), radius=0.2, material=water))
r.scene.append(Sphere(center=V3( 3, -5, -12), radius=0.2, material=water))
r.scene.append(Sphere(center=V3( 4, -4, -12.5), radius=0.1, material=water))
r.scene.append(Sphere(center=V3(-4, -4, -12.5), radius=0.1, material=water))
r.scene.append(Sphere(center=V3(-3.5, -4.5, -13), radius=0.15, material=water))
r.scene.append(Sphere(center=V3( 3.5, -4.5, -13), radius=0.15, material=water))

# #Moby Dick
r.scene.append( AABB(V3( 0,-4,-14), V3(4, 8, 1), whale_belly)) # belly
r.scene.append( AABB(V3( 0,-4,-16), V3(6, 12, 1), whale_skin)) # body
r.scene.append( AABB(V3(-3,-4,-15), V3(1, 2, 1), whale_skin)) # left flipper
r.scene.append( AABB(V3( 3,-4,-15), V3(1, 2, 1), whale_skin)) # right flipper
r.scene.append( AABB(V3(-3,-1,-16), V3(1, 1, 1), whale_eye)) #left eye
r.scene.append( AABB(V3( 3,-1,-16), V3(1, 1, 1), whale_eye)) # right eye


#Perquod
# r.scene.append( AABB(V3(0, -3, -10), V3(5, 0.1, 5) , boxMat ) )

r.scene.append( Sphere(V3( -5, 10, -20), 2, moonMat)) # moon



r.rtRender()

r.glFinish('output.bmp')
