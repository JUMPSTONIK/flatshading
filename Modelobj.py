from SR1 import *
from collections import namedtuple
width = 800
height = 600
V2 = namedtuple('Vertex2', ['x', 'y'])
V3 = namedtuple('Vertex3', ['x', 'y', 'z'])
zbuffer = [[-99999999999 for x in range(1000)] for y in range(1000)]
class Modelobj(object):
	def __init__(self,filename):
		with open(filename) as f:
			self.lines = f.read().splitlines()
		self.vertices = []
		self.faces = []
		

	def read(self):
		for line in self.lines:
			if line:
				prefix, value = line.split(' ',1)

				if prefix == 'v':
					self.vertices.append(list(map(float,value.split(' '))))
				if prefix == 'f':
					self.faces.append([list(map(int, face.split('/'))) for face in value.split(' ')])
	def getverts(self):
		return self.vertices
	def getfaces(self):
		return self.faces
verts = []
def draw():
	verts_itter = iter(verts)
	try:
		while True:
			a = next(verts_itter)
			b = next(verts_itter)
			c = next(verts_itter)
			val.line_float(a[0],a[1],b[0],b[1])
			val.line_float(b[0],b[1],c[0],c[1])
			val.line_float(c[0],c[1],a[0],a[1])
	except StopIteration as e:
		print("f")
	

def load(filename,vertices,caras):
	var = Modelobj("BMONorm.obj")
	var.read()
	vertices = var.getverts()
	faces = var.getfaces()
	luz=V3(0,0,1)
	for face in faces:
	
		x1=round(0.8*(vertices[face[0][0]-1][0]+1)*(getwidth()/2))
		y1=round(0.8*(vertices[face[0][0]-1][1]+1)*(getwidth()/2))
		z1=round(0.8*(vertices[face[0][0]-1][2]+1)*(getwidth()/2))
		x2=round(0.8*(vertices[face[1][0]-1][0]+1)*(getwidth()/2))
		y2=round(0.8*(vertices[face[1][0]-1][1]+1)*(getwidth()/2))
		z2=round(0.8*(vertices[face[1][0]-1][2]+1)*(getwidth()/2))
		x3=round(0.8*(vertices[face[2][0]-1][0]+1)*(getwidth()/2))
		y3=round(0.8*(vertices[face[2][0]-1][1]+1)*(getwidth()/2))
		z3=round(0.8*(vertices[face[2][0]-1][2]+1)*(getwidth()/2))
		v1 = V3(x1,y1,z1)
		v2 = V3(x2,y2,z2)
		v3 = V3(x3,y3,z3)

		normal = normVec(prodx(restVec(v2,v1),restVec(v3,v1)))
		intens = prod(normal,luz)
		if intens<0:
			pass
		else:
			glColor(intens,intens,intens)
			triangle(v1,v2,v3)

def barycentric(A, B, C, P):
	cx, cy, cz = prodx(
		V3(B.x - A.x, C.x - A.x, A.x - P.x),
		V3(B.y - A.y, C.y - A.y, A.y - P.y)
	)

	if cz == 0:
		return -1, -1, -1
	# Coordenadas baricentricas
	u = cx/cz
	v = cy/cz
	w = 1 - (u + v)

	return w,v,u

def bbox(A, B, C):
	xs = sorted([A.x, B.x, C.x])
	ys = sorted([A.y, B.y, C.y])
	return V2(xs[0], ys[0]), V2(xs[2], ys[2])

def triangle(A, B, C):
	bbox_min, bbox_max = bbox(A, B, C)

	for x in range(bbox_min.x, bbox_max.x + 1):
		for y in range(bbox_min.y, bbox_max.y + 1):
			w, v, u = barycentric(A, B, C, V2(x, y))

			# Si estan fuera del triangulo, no pintar
			if w < 0 or v < 0 or u < 0:
				pass
			else:
				z = A.z * w + B.z * v + C.z * u
				# Si z es mayor que el z buffer, pintar y cambiar valor zbuffer
				if z > zbuffer[x][y]:
					pointf(x, y)
					zbuffer[x][y] = z

def prod(v0,v1):
	return (v0.x*v1.x)+(v0.y*v1.y)+(v0.z*v1.z)
def restVec(v0,v1):
	return V3(v0.x-v1.x,v0.y-v1.y,v0.z-v1.z)
def prodx(v0,v1):
	return V3(
	v0.y * v1.z - v0.z * v1.y,
	v0.z * v1.x - v0.x * v1.z,
	v0.x * v1.y - v0.y * v1.x
		)
def magVec(v0):
	return (v0.x**2 + v0.y**2 + v0.z**2)**0.5
def normVec(v0):
	l = magVec(v0)
	if not l:
		return V3(0, 0, 0)
	return V3(v0.x/l, v0.y/l, v0.z/l)



glCreateWindow(width,height)
val = get_var()
trans = [0.0,0.8]
sca = [1.0,1.0]
load("BMONorm.obj", trans, sca)
#draw()
glFinish()




