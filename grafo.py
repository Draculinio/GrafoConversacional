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

def cargar_juego():
    try:
        with open('./savegames/savegames.json') as f:
            print('Juego Cargado')
            return json.load(f)
    except:
        print('No esta el archivo de carga')

def obtener_informacion(archivo):
    try:
        with open('./datos/'+archivo+'.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print('No se puede encontrar el archivo '+ './datos/'+archivo+'.json')


class Juego:
    def __init__(self):
        self.mundo = Grafo()
        self.personaje = None
    def comandos(self, comando):
        if comando[0] == 'caminar':
            try:
                if comando[1] in self.mundo.vertices[self.personaje.personaje['ubicacion']].aristas:
                    self.personaje.personaje['ubicacion'] = comando[1]
                    print('Caminando a '+comando[1])
                else:
                    print('No puedes ir ahi')
            except IndexError:
                print('Debe especificar adonde caminar')
        elif comando[0] == 'mirar':
            try:
                if comando[1] in self.mundo.vertices[self.personaje.personaje['ubicacion']].aristas:
                    self.mundo.vertices[comando[1]].informacion(False)
                else:
                    print('No puedes mirar eso')
            except IndexError:
                self.mundo.vertices[self.personaje.personaje['ubicacion']].informacion()
        elif comando[0] == 'status':
            self.personaje.status()
        elif comando[0] == 'save':
            guardar_juego(self.personaje)
        elif comando[0] == 'load':
            cargar_juego()
        else:
            print('Comando no disponible')

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
    juego = Juego()
    juego.mundo.insertar_vertice('casa')
    juego.mundo.insertar_vertice('puerta')
    juego.mundo.insertar_vertice('camino')
    juego.mundo.insertar_vertice('camino_oeste')
    juego.mundo.insertar_vertice('camino_este')
    juego.mundo.insertar_arista('casa','puerta')
    juego.mundo.insertar_arista('puerta','camino')
    juego.mundo.insertar_arista('camino','camino_este')
    juego.mundo.insertar_arista('camino','camino_oeste')
    for i in juego.mundo.vertices:
        print(i)
        print(juego.mundo.vertices[i].aristas)
    print('****Fin de Crear Mundo****')
    #TODO: proceso de creacion de personaje
    personaje = Personaje('Draculinio', 'casa')
    personaje.generar_personaje()
    juego.personaje = personaje
    salir = False
    while not salir:
        comando = input('>').lower().split()
        if comando[0] == 'salir':
            print('Gracias por jugar')
            salir = True
        else:
            juego.comandos(comando)