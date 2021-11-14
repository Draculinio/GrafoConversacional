import json
import random

def guardar_juego(personaje):
    try:
        with open('./savegames/savegame.json','w') as f:
            json.dump(personaje.personaje,f)
            f.close()
            print('Juego guardado')
    except FileNotFoundError:
        print('Falta el directorio savegame')

def obtener_informacion(archivo):
    try:
        with open('./datos/'+archivo+'.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print('No se puede encontrar el archivo '+ './datos/'+archivo+'.json')

#TODO: Agregar inventario (items tienen peso)
class Personaje:
    def __init__(self,nombre,id):
        self.personaje = {'nombre':nombre, 'ubicacion':id, 'dinero':0,'nivel':1, 'experiencia': 0, 'fuerza':0, 'inteligencia':0, 'constitucion':0}
        

    def generar_personaje(self):
        self.personaje['dinero'] = random.randrange(100, 500)
        self.personaje['fuerza'] = random.randrange(1,10)
        self.personaje['inteligencia'] = random.randrange(1,10)
        self.personaje['constitucion'] = random.randrange(1,10)

    def status(self):
        print('---'+self.personaje['nombre']+'---')
        print('>>>>Nivel: '+str(self.personaje['nivel'])+'('+str(self.personaje['experiencia'])+')')
        print('Dinero: '+str(self.personaje['dinero']))
        print('Fuerza: '+str(self.personaje['fuerza']))
        print('Inteligencia: '+str(self.personaje['inteligencia']))
        print('Constitucion: '+str(self.personaje['constitucion']))
    
    def caminar(self, id):
        self.personaje['ubicacion'] = id

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
        self.id = id'./datos/'+archivo+'.json'
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
                    if comando[1] in mundo.vertices[personaje.personaje['ubicacion']].aristas:
                        personaje.personaje['ubicacion'] = comando[1]
                        print('Caminando a '+comando[1])
                    else:
                        print('No puedes ir ahi')
                except IndexError:
                    print('Debe especificar adonde caminar')
            elif comando[0] == 'mirar':
                try:
                    if comando[1] in mundo.vertices[personaje.personaje['ubicacion']].aristas:
                        mundo.vertices[comando[1]].informacion(False)
                    else:
                        print('No puedes mirar eso')
                except IndexError:
                    mundo.vertices[personaje.personaje['ubicacion']].informacion()
            elif comando[0] == 'status':
                personaje.status()
            elif comando[0] == 'save':
                guardar_juego(personaje)
            else:
                print('Comando no disponible')
            

