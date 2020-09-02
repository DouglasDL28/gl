from gl import *
import glMath

def flat(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx,ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    
    normal = glMath.cross_product(glMath.substract(B, A), glMath.substract(C, A))
    normal = glMath.normalize(normal)
    intensity = glMath.dot_product(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0 :
        return r, g, b
    else:
        return 0,0,0

def unlit(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255
    
    tx = ta.x * u + tb.x * v + tc.x * w
    ty = ta.y * u + tb.y * v + tc.y * w

    if render.active_texture:
        texColor = render.active_texture.getColor(tx,ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    return r, g, b

def gourad(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    intensityA = glMath.dot_product(na, render.light)
    intensityB = glMath.dot_product(nb, render.light)
    intensityC = glMath.dot_product(nc, render.light)

    colorA = (r * intensityA, g * intensityA, b * intensityA)
    colorB = (r * intensityB, g * intensityB, b * intensityB)
    colorC = (r * intensityC, g * intensityC, b * intensityC)

    b = colorA[2] * u + colorB[2] * v + colorC[2] * w
    g = colorA[1] * u + colorB[1] * v + colorC[1] * w
    r = colorA[0] * u + colorB[0] * v + colorC[0] * w

    r = 0 if r < 0 else r
    g = 0 if g < 0 else g
    b = 0 if b < 0 else b

    return r, g, b

def phong(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    tx = ta.x * u + tb.x * v + tc.x * w
    ty = ta.y * u + tb.y * v + tc.y * w
    if render.active_texture:
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = glMath.dot_product(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def cool(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = glMath.dot_product(normal, render.light)
    if intensity < 0:
        intensity = 0

    b *= intensity
    g *= intensity
    r *= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)

        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)


    return r, g, b

def toon(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    if render.active_texture:
        tx = ta.x * u + tb.x * v + tc.x * w
        ty = ta.y * u + tb.y * v + tc.y * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = glMath.dot_product(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return round(r, 1), round(g, 1), round(b, 1)
    else:
        return 0,0,0

def normalMap(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    tx = ta.x * u + tb.x * v + tc.x * w
    ty = ta.y * u + tb.y * v + tc.y * w

    if render.active_texture:
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w
    normal = V3(nx, ny, nz)

    if render.active_normalMap:
        texNormal = render.active_normalMap.getColor(tx, ty)
        texNormal = [ (texNormal[2] / 255) * 2 - 1,
                      (texNormal[1] / 255) * 2 - 1,
                      (texNormal[0] / 255) * 2 - 1]

        texNormal =glMath.normalize(texNormal)

        edge1 = glMath.substract(B,A)
        edge2 = glMath.substract(C,A)
        deltaUV1 = glMath.substract(tb, ta)
        deltaUV2 = glMath.substract(tc, ta)
        tangent = [0,0,0]
        f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])
        tangent[0] = f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0])
        tangent[1] = f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1])
        tangent[2] = f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])
        tangent = glMath.normalize(tangent)
        tangent = glMath.substract(tangent, glMath.multiply(glMath.dot_product(tangent, normal), normal))
        tangent = glMath.normalize(tangent)

        bitangent = glMath.cross_product(normal, tangent)
        bitangent = glMath.normalize(bitangent)

        #para convertir de espacio global a espacio tangente
        tangentMatrix = [[tangent[0],bitangent[0],normal[0]],
                        [tangent[1],bitangent[1],normal[1]],
                        [tangent[2],bitangent[2],normal[2]]]

        light = render.light
        light = glMath.multiply(tangentMatrix,light)
        light = glMath.normalize(light)

        intensity = glMath.dot_product(texNormal, light)
    else:
        intensity = glMath.dot_product(normal, render.light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def colorful(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    ta, tb, tc = kwargs['texCoords']
    na, nb, nc = kwargs['normals']
    b, g, r = kwargs['color']

    b /= 255
    g /= 255
    r /= 255

    tx = ta.x * u + tb.x * v + tc.x * w
    ty = ta.y * u + tb.y * v + tc.y * w

    if render.active_texture:
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nx = na[0] * u + nb[0] * v + nc[0] * w
    ny = na[1] * u + nb[1] * v + nc[1] * w
    nz = na[2] * u + nb[2] * v + nc[2] * w

    normal = V3(nx, ny, nz)

    intensity = glMath.dot_product(normal, render.light)

    rand = random.randint(0, 2)
    
    b *= intensity if rand == 0 else 0
    g *= intensity if rand == 1 else 0
    r *= intensity if rand == 2 else 0

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0
