import json
import random

def obtener_informacion(archivo):
    with open('./datos/'+archivo+'.json') as f:
        return json.load(f)

#TODO: Agregar inventario (items tienen peso)
class Personaje:
    def __init__(self,nombre,id):
        self.nombre = nombre
        self.ubicacion = id
        self.dinero = 0
        self.nivel = 1
        self.experiencia = 0 #TODO: manejador de niveles y experiencia
        self.fuerza = 0
        self.inteligencia = 0
        self.constitucion = 0

    def generar_personaje(self):
        self.dinero = random.randrange(100, 500)
        self.fuerza = random.randrange(1,10)
        self.inteligencia = random.randrange(1,10)
        self.constitucion = random.randrange(1,10)

    def status(self):
        print('---'+self.nombre+'---')
        print('>>>>Nivel: '+str(self.nivel)+'('+str(self.experiencia)+')')
        print('Dinero: '+str(self.dinero))
        print('Fuerza: '+str(self.fuerza))
        print('Inteligencia: '+str(self.inteligencia))
        print('Constitucion: '+str(self.constitucion))
    
    def caminar(self, id):
        self.ubicacion = id

class Grafo:
    def __init__(self):
        self.vertices = {}

    def insertar_vertice(self,v):
        if v not in self.vertices:
            self.vertices[v] = Vertice(v)

    def insertar_arista(self,a,b):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].insertar_arista(b)
            self.vertices[b].insertar_arista(a)


class Vertice:
    def __init__(self,id):
        self.id = id
        self.aristas = []
        self.datos = obtener_informacion(self.id)

    def insertar_arista(self,id):
        if id not in self.aristas:
            self.aristas.append(id)

    def informacion(self, propio = True):
        if propio:
            print('Tu ubicacion: '+self.id)
        else:
            print('Estas viendo: '+self.id)
        print(self.datos['descripcion'])
        if propio:
            print('Posibles salidas: ')
            for arista in self.aristas:
                print('->'+arista)


if __name__ == "__main__":
    #TODO: hacer proceso de creacion del grafo
    print('****Creando Mundo****')
    mundo = Grafo()
    mundo.insertar_vertice('casa')
    mundo.insertar_vertice('puerta')
    mundo.insertar_vertice('camino')
    mundo.insertar_vertice('camino_oeste')
    mundo.insertar_vertice('camino_este')
    mundo.insertar_arista('casa','puerta')
    mundo.insertar_arista('puerta','camino')
    mundo.insertar_arista('camino','camino_este')
    mundo.insertar_arista('camino','camino_oeste')
    for i in mundo.vertices:
        print(i)
        print(mundo.vertices[i].aristas)
    print('****Fin de Crear Mundo****')
    #TODO: proceso de creacion de personaje
    personaje = Personaje('Draculinio', 'casa')
    personaje.generar_personaje()
    salir = False
    while not salir:
        comando = input('>').lower().split()
        if comando[0] == 'salir':
            print('Gracias por jugar')
            salir = True
        else:
            if comando[0] == 'caminar':
                try:
                    if comando[1] in mundo.vertices[personaje.ubicacion].aristas:
                        personaje.ubicacion = comando[1]
                        #personaje.caminar(comando[1])
                        print('Caminando a '+comando[1])
                    else:
                        print('No puedes ir ahi')
                except IndexError:
                    print('Debe especificar adonde caminar')
            elif comando[0] == 'mirar':
                try:
                    if comando[1] in mundo.vertices[personaje.ubicacion].aristas:
                        mundo.vertices[comando[1]].informacion(False)
                    else:
                        print('No puedes mirar eso')
                except IndexError:
                    mundo.vertices[personaje.ubicacion].informacion()
            elif comando[0] == 'status':
                personaje.status()
            else:
                print('Comando no disponible')
            