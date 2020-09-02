import caffeine
from gl import Render, color, V2, V3
from obj import Obj, Texture
from shaders import *

width = 1920
height = 1080

# width = 800
# height = 500

print("Inicio")
r = Render(width,height)

# CHARACTER
r.active_texture = Texture('./models/model.bmp')
r.active_normalMap = Texture('./models/model_normal.bmp')

r.active_shader = normalMap
r.loadModel('./models/model.obj', V3(1.5,-1,-2), V3(1,1,1), V3(0,190,0))

# GOLEMS
r.active_texture = Texture('./models/Stone/rough.bmp')

r.active_shader = toon
r.loadModel('./models/Stone/Stone.obj', V3(-2,0,-5), V3(0.2,0.2,0.2), V3(0,0,0))

r.active_shader = colorful
r.loadModel('./models/Stone/Stone.obj', V3(2,0,-5), V3(0.2,0.2,0.2), V3(0,0,0))

# ROCKS
r.active_texture = Texture('./models/Rock/rock_texture.bmp')
r.active_normalMap = Texture('./models/Rock/rock_normal.bmp')

r.active_shader = colorful
r.loadModel('./models/Rock/rock.obj', V3(-4,0,-7), V3(0.007,0.007,0.007), V3(0,0,0))

r.active_shader = normalMap
r.loadModel('./models/Rock/rock.obj', V3(4,0,-7), V3(0.007,0.007,0.007), V3(0,0,0))

# GOLD BAG
r.active_texture = Texture('./models/GoldBag/gold_bag_textures.bmp')

r.active_shader = phong
r.loadModel('./models/GoldBag/gold_bag.obj', V3(0,1,-8), V3(0.08,0.08,0.08), V3(0,0,90))

r.active_shader = toon
r.loadModel('./models/GoldBag/gold_bag.obj', V3(1,1,-10), V3(0.08,0.08,0.08), V3(-50,0,0))

# MOON
r.active_texture = Texture('./models/Moon/moon.bmp')

r.active_shader = toon
r.loadModel('./models/Moon/Moon_2K.obj', V3(-10,6,-15), V3(1,1,1), V3(0,0,0))

r.glFinish('output.bmp')

print("Fin")