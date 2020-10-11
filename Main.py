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

whale_belly = Material(diffuse= color(0.887, 0.973, 1), spec = 128)
whale_skin = Material(diffuse=color(1, 1, 1), spec = 32)
whale_eye = Material(diffuse=color(0.3, 0.3, 0.3), spec=256)

boxMat = Material(texture = Texture('box.bmp'))

earthMat = Material(texture = Texture('earthDay.bmp'))


width = 128
height = 128
r = Raytracer(width,height)
# r.glClearColor(0.2, 0.6, 0.8)
r.glClear()

# r.envmap = Envmap('starSky.bmp')

# Lights
#r.pointLights.append( PointLight(position = V3(-4,4,0), intensity = 0.5))
#r.pointLights.append( PointLight(position = V3( 4,0,0), intensity = 0.5))
r.dirLight = DirectionalLight(direction = V3(1, -1, -2), intensity = 0.5)
r.ambientLight = AmbientLight(strength = 0.2)

# Objects
#r.scene.append( Sphere(V3( 0, 0, -8), 2, brick) )
#r.scene.append( Sphere(V3( -0.5, 0.5, -5), 0.25, stone))
#r.scene.append( Sphere(V3( 0.25, 0.5, -5), 0.25, stone))

#Moby Dick
r.scene.append( AABB(V3( 0,-3,-14), V3(4, 8, 1), whale_belly)) # belly
r.scene.append( AABB(V3( 0,-3,-16), V3(6, 12, 1), whale_skin)) # body
r.scene.append( AABB(V3(-3,-3,-15), V3(1, 2, 1), whale_skin)) # left flipper
r.scene.append( AABB(V3( 3,-3,-15), V3(1, 2, 1), whale_skin)) # right flipper
r.scene.append( AABB(V3(-3, 0,-16), V3(1, 1, 1), whale_eye)) #left eye
r.scene.append( AABB(V3( 3, 0,-16), V3(1, 1, 1), whale_eye)) # right eye


#Perquod
# r.scene.append( AABB(V3(0, -3, -10), V3(5, 0.1, 5) , boxMat ) )

# r.scene.append( Sphere(V3( 0, 0, -8), 2, earthMat))



r.rtRender()

r.glFinish('output.bmp')
