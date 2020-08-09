from gl import Render, color, V2, V3
from obj import Obj, Texture
import glMath

from shaders import *

import random

r = Render(1000,1000)

r.active_texture = Texture('./models/earthDay.bmp')
r.active_texture2 = Texture('./models/earthNight.bmp')

r.active_shader = toon

luz = V3(0,0,1)
r.light = glMath.normalize(luz)

r.loadModel('./models/earth.obj', V3(500,500,0), V3(1,1,1))

r.glFinish('toon.bmp')


