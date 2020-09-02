import struct
import random
import glMath
import math

from obj import Obj
from collections import namedtuple

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z','w'])

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b * 255), int(g * 255), int(r * 255)])

def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B.y - C.y)*(P.x - C.x) + (C.x - B.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        v = ( ((C.y - A.y)*(P.x - C.x) + (A.x - C.x)*(P.y - C.y) ) /
              ((B.y - C.y)*(A.x - C.x) + (C.x - B.x)*(A.y - C.y)) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w



BLACK = color(0,0,0)
WHITE = color(1,1,1)

class Render(object):
    """
    The Render class provides with atributes and methods to create a window, viewport and zbuffer to draw and then output into a .bmp file.
    """

    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

        self.light = V3(0,0,1)
        self.active_texture = None
        self.active_texture2 = None

        self.active_normalMap = None
        
        self.active_shader = None

        self.createViewMatrix()
        self.createProjectionMatrix()

    def createViewMatrix(self, camPosition = V3(0,0,0), camRotation = V3(0,0,0)):
        camMatrix = self.createObjectMatrix(translate=camPosition, rotate=camRotation)
        self.viewMatrix = glMath.inverse(camMatrix)


    def lookAt(self, eye, camPosition = V3(0,0,0)):

        forward = glMath.substract(camPosition, eye)
        forward = glMath.normalize(forward)

        right = glMath.cross_product(V3(0,1,0), forward)
        right = glMath.normalize(right)

        up = glMath.cross_product(forward, right)
        up = glMath.normalize(up)

        camMatrix = [[right[0], up[0], forward[0], camPosition.x],
                    [right[1], up[1], forward[1], camPosition.y],
                    [right[2], up[2], forward[2], camPosition.z],
                    [0,0,0,1]]

        self.viewMatrix = glMath.inverse(camMatrix)


    def createProjectionMatrix(self, n = 0.1, f = 1000, fov = 60):

        t = math.tan((fov * math.pi / 180) / 2) * n
        r = t * self.vpWidth / self.vpHeight

        self.projectionMatrix = [
            [n / r, 0, 0, 0],
            [0, n / t, 0, 0],
            [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
            [0, 0, -1, 0]
            ]

    def glCreateWindow(self, width, height):
        """
        Create window and viewport with input width and height.
        """
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0, 0, width, height)

    def glViewport(self, x, y, width, height):
        """
        Create viewport.
        """
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height

        self.viewportMatrix = [
            [width/2, 0, 0, x + width/2],
            [0, height/2, 0, y + height/2],
            [0, 0, 0.5, 0.5],
            [0, 0, 0, 1]
            ]

    def glClear(self):
        """
        Return window matrix and zbuffer matrix to default values.
        """
        self.pixels = [ [ self.clear_color for x in range(self.width)] for y in range(self.height) ]

        #Z - buffer, depthbuffer, buffer de profudidad
        self.zbuffer = [ [ float('inf') for x in range(self.width)] for y in range(self.height) ]

    def glVertex(self, x, y, color = None):
        """
        Draws point in window with NDC coordinates with input color or with current color.
        """
        pixelX = (x + 1) * (self.vpWidth / 2) + self.vpX
        pixelY = (y + 1) * (self.vpHeight / 2) + self.vpY

        if pixelX >= self.width or pixelX < 0 or pixelY >= self.height or pixelY < 0:
            return

        try:
            self.pixels[round(pixelY)][round(pixelX)] = color or self.curr_color
        except:
            pass

    def glVertex_coord(self, x, y, color = None):
        """
        Draws point with window coordinates with input color or with current color.
        """
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if x >= self.width or x < 0 or y >= self.height or y < 0:
            return

        try:
            self.pixels[y][x] = color or self.curr_color
        except:
            pass

    def glColor(self, r, g, b):
        """
        Changes current color to input color.
        """
        self.curr_color = color(r,g,b)

    def glClearColor(self, r, g, b):
        """
        Changes clear_color into input color.
        """
        self.clear_color = color(r,g,b)

    def glFinish(self, filename):
        """
        Writes window data into .bmp file.
        """
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Pixeles, 3 bytes cada uno
        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixels[x][y])

        archivo.close()

    def glZBuffer(self, filename):
        archivo = open(filename, 'wb')

        # File header 14 bytes
        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))
        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        # Image Header 40 bytes
        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        # Minimo y el maximo
        minZ = float('inf')
        maxZ = -float('inf')
        for x in range(self.height):
            for y in range(self.width):
                if self.zbuffer[x][y] != -float('inf'):
                    if self.zbuffer[x][y] < minZ:
                        minZ = self.zbuffer[x][y]

                    if self.zbuffer[x][y] > maxZ:
                        maxZ = self.zbuffer[x][y]

        for x in range(self.height):
            for y in range(self.width):
                depth = self.zbuffer[x][y]
                if depth == -float('inf'):
                    depth = minZ
                depth = (depth - minZ) / (maxZ - minZ)
                archivo.write(color(depth,depth,depth))

        archivo.close()

    def glLine(self, v0, v1, color = None):
        """
        Draws line with NDC coordinates.
        """
        x0 = round(( v0.x + 1) * (self.vpWidth  / 2 ) + self.vpX)
        x1 = round(( v1.x + 1) * (self.vpWidth  / 2 ) + self.vpX)
        y0 = round(( v0.y + 1) * (self.vpHeight / 2 ) + self.vpY)
        y1 = round(( v1.y + 1) * (self.vpHeight / 2 ) + self.vpY)

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glVertex_coord(y, x,color)
            else:
                self.glVertex_coord(x, y,color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLine_coord(self, v0, v1, color = None):
        """
        Draws line with window coordinates.
        """
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        
        try:
            m = dy/dx
        except ZeroDivisionError:
            pass
        else:
            y = y0

            for x in range(x0, x1 + 1):
                if steep:
                    self.glVertex_coord(y, x,color)
                else:
                    self.glVertex_coord(x, y,color)

                offset += m
                if offset >= limit:
                    y += 1 if y0 < y1 else -1
                    limit += 1

    def transform(self, vertex, vMatrix):
        """
        Translates and scales a vertex.
        """
        augVertex = V4( vertex[0], vertex[1], vertex[2], 1)
        transVertex = glMath.multiply(vMatrix, augVertex)

        transVertex = V3(transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])

        return transVertex

    def camTransform(self, vertex):
        augVertex = V4( vertex[0], vertex[1], vertex[2], 1)
        transVertex = glMath.multiply(glMath.multiply(glMath.multiply(self.viewportMatrix, self.projectionMatrix), self.viewMatrix), augVertex)

        transVertex = V3(transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])

        return transVertex

    def dirTransform(self, vertex, vMatrix):
        augVertex = V4( vertex[0], vertex[1], vertex[2], 0)
        transVertex = glMath.multiply(vMatrix, augVertex)

        transVertex = V3(transVertex[0],
                         transVertex[1],
                         transVertex[2])

        return transVertex

    def createObjectMatrix(self, translate = V3(0,0,0), scale = V3(1,1,1), rotate=V3(0,0,0)):

        translateMatrix = [
            [1, 0, 0, translate.x],
            [0, 1, 0, translate.y],
            [0, 0, 1, translate.z],
            [0, 0, 0, 1]
            ]

        scaleMatrix = [
            [scale.x, 0, 0, 0],
            [0, scale.y, 0, 0],
            [0, 0, scale.z, 0],
            [0, 0, 0, 1]
            ]

        rotationMatrix = self.createRotationMatrix(rotate)

        return glMath.multiply(glMath.multiply(translateMatrix, rotationMatrix), scaleMatrix)

    def createRotationMatrix(self, rotate=V3(0,0,0)):

        pitch = math.radians(rotate.x)
        yaw = math.radians(rotate.y)
        roll = math.radians(rotate.z)

        rotationX = [
            [1, 0, 0, 0],
            [0, math.cos(pitch),-math.sin(pitch), 0],
            [0, math.sin(pitch), math.cos(pitch), 0],
            [0, 0, 0, 1]
            ]

        rotationY = [
            [math.cos(yaw), 0, math.sin(yaw), 0],
            [0, 1, 0, 0],
            [-math.sin(yaw), 0, math.cos(yaw), 0],
            [0, 0, 0, 1]
            ]

        rotationZ = [
            [math.cos(roll),-math.sin(roll), 0, 0],
            [math.sin(roll), math.cos(roll), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
            ]

        return glMath.multiply(glMath.multiply(rotationX, rotationY), rotationZ)
    
    def loadModel(self, filename, translate = V3(0,0,0), scale = V3(1,1,1), rotate=V3(0,0,0), isWireframe = False):
        """
        Reads Obj file and draws it in window.
        Has wireframe flag.
        """
        model = Obj(filename)

        modelMatrix = self.createObjectMatrix(translate, scale, rotate)

        rotationMatrix = self.createRotationMatrix(rotate)

        for face in model.faces:

            vertCount = len(face)

            if isWireframe:
                for vert in range(vertCount):
                    v0 = model.vertices[ face[vert][0] - 1 ]
                    v1 = model.vertices[ face[(vert + 1) % vertCount][0] - 1]
                    v0 = V2(round(v0[0] * scale.x  + translate.x), round(v0[1] * scale.y  + translate.y))
                    v1 = V2(round(v1[0] * scale.x  + translate.x), round(v1[1] * scale.y  + translate.y))
                    self.glLine_coord(v0, v1)
            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]
                if vertCount > 3:
                    v3 = model.vertices[ face[3][0] - 1 ]

                v0 = self.transform(v0, modelMatrix)
                v1 = self.transform(v1, modelMatrix)
                v2 = self.transform(v2, modelMatrix)
                A = v0
                B = v1
                C = v2

                v0 = self.camTransform(v0)
                v1 = self.camTransform(v1)
                v2 = self.camTransform(v2)


                if vertCount > 3:
                    v3 = self.transform(v3, modelMatrix)
                    D = v3
                    v3 = self.camTransform(v3)

                vt0 = model.texcoords[face[0][1] - 1]
                vt1 = model.texcoords[face[1][1] - 1]
                vt2 = model.texcoords[face[2][1] - 1]
                vt0 = V2(vt0[0], vt0[1])
                vt1 = V2(vt1[0], vt1[1])
                vt2 = V2(vt2[0], vt2[1])
                if vertCount > 3:
                    vt3 = model.texcoords[face[3][1] - 1]
                    vt3 = V2(vt3[0], vt3[1])


                vn0 = model.normals[face[0][2] - 1]
                vn1 = model.normals[face[1][2] - 1]
                vn2 = model.normals[face[2][2] - 1]

                vn0 = self.dirTransform(vn0, rotationMatrix)
                vn1 = self.dirTransform(vn1, rotationMatrix)
                vn2 = self.dirTransform(vn2, rotationMatrix)
                if vertCount > 3:
                    vn3 = model.normals[face[3][2] - 1]
                    vn3 = self.dirTransform(vn3, rotationMatrix)


                self.triangle_bc(v0,v1,v2, texcoords = (vt0,vt1,vt2), normals = (vn0,vn1,vn2), verts = (A,B,C))
                if vertCount > 3: #asumamos que 4, un cuadrado
                    self.triangle_bc(v0,v2,v3, texcoords = (vt0,vt2,vt3), normals = (vn0,vn2,vn3), verts = (A,C,D))

    def drawPoly(self, points, color = None):
        """
        Draws polygon (w/o fill).
        """

        count = len(points)
        for i in range(count):
            v0 = points[i]
            v1 = points[(i + 1) % count]
            self.glLine_coord(v0, v1, color)

    def triangle(self, A, B, C, color = None):
        """
        Draws triangle (w/ fill).
        """
        
        def flatBottomTriangle(v1,v2,v3):
            #self.drawPoly([v1,v2,v3], color)
            for y in range(v1.y, v3.y + 1):
                xi = round( v1.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v1.y))
                xf = round( v2.x + (v3.x - v2.x)/(v3.y - v2.y) * (y - v2.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.glVertex_coord(x,y, color or self.curr_color)

        def flatTopTriangle(v1,v2,v3):
            for y in range(v1.y, v3.y + 1):
                xi = round( v2.x + (v2.x - v1.x)/(v2.y - v1.y) * (y - v2.y))
                xf = round( v3.x + (v3.x - v1.x)/(v3.y - v1.y) * (y - v3.y))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.glVertex_coord(x,y, color or self.curr_color)

        # A.y <= B.y <= Cy
        if A.y > B.y:
            A, B = B, A
        if A.y > C.y:
            A, C = C, A
        if B.y > C.y:
            B, C = C, B

        if A.y == C.y:
            return

        if A.y == B.y: #En caso de la parte de abajo sea plana
            flatBottomTriangle(A,B,C)
        elif B.y == C.y: #En caso de que la parte de arriba sea plana
            flatTopTriangle(A,B,C)
        else: #En cualquier otro caso
            # y - y1 = m * (x - x1)
            # B.y - A.y = (C.y - A.y)/(C.x - A.x) * (D.x - A.x)
            # Resolviendo para D.x
            x4 = A.x + (C.x - A.x)/(C.y - A.y) * (B.y - A.y)
            D = V2( round(x4), B.y)
            flatBottomTriangle(D,B,C)
            flatTopTriangle(A,B,D)

    def triangle_bc(self, A, B, C, texcoords = (), normals = (), verts = (), _color = None):
        """
        Draws triangle with barycentric coordinates (w/ fill).
        """
        #bounding box
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                if x >= self.width or x < 0 or y >= self.height or y < 0:
                    continue

                u, v, w = baryCoords(A, B, C, V2(x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w
                    if z < self.zbuffer[y][x] and z <= 1 and z >= -1:
                        
                        if self.active_shader:

                            r, g, b = self.active_shader(
                                self,
                                verts=verts,
                                baryCoords=(u,v,w),
                                texCoords=texcoords,
                                normals=normals,
                                color = _color or self.curr_color)
                        else: 
                            b, g, r = _color or self.curr_color

                        self.glVertex_coord(x, y, color(r,g,b))
                        self.zbuffer[y][x] = z















                











