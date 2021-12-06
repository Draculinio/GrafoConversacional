import json
import random
import os


class Colores:
    black='\033[30m'
    red='\033[31m'
    green='\033[32m'
    orange='\033[33m'
    blue='\033[34m'
    purple='\033[35m'
    cyan='\033[36m'
    lightgrey='\033[37m'
    darkgrey='\033[90m'
    lightred='\033[91m'
    lightgreen='\033[92m'
    yellow='\033[93m'
    lightblue='\033[94m'
    pink='\033[95m'
    lightcyan='\033[96m'
    reset='\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

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
        if comando[0] == 'investigar':
            try:
                encontrado = False
                for i in range(0,len(self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos)):
                    if comando[1] == self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos[i].datos['nombre']:
                        encontrado = True
                        self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos[i].status()
                        break
                if not encontrado:
                    print('No puedo investigar eso')
            except:
                print('Debes indicar a quien investigar')
        elif comando[0] == 'caminar':
            try:
                if comando[1] in self.mundo.vertices[self.personaje.personaje['ubicacion']].aristas:
                    self.personaje.personaje['ubicacion'] = comando[1]
                    self.personaje.personaje['pasos']+=1
                    print(self.personaje.personaje['pasos'])
                    print('Caminando a '+comando[1])
                else:
                    print('No puedes ir ahi')
            except IndexError:
                print('Debe especificar adonde caminar')
        elif comando[0] == 'mirar':
            try:
                encontrado = False
                if comando[1] in self.mundo.vertices[self.personaje.personaje['ubicacion']].aristas: #Busco aristas
                    encontrado = True
                    self.mundo.vertices[comando[1]].informacion(False)
                if not encontrado: #busco elementos
                    for i in range(0, len(self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos)):
                        if self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i].datos['nombre'] == comando[1]:
                            encontrado = True
                            self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i].informacion()
                            break
                if not encontrado: #enemigos
                    for i in range(0, len(self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos)):
                        if self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos[i].datos['nombre'] == comando[1]:
                            encontrado = True
                            self.mundo.vertices[self.personaje.personaje['ubicacion']].enemigos[i].informacion()
                            break
                if not encontrado:
                    print('No puedes mirar eso')
            except IndexError:
                self.mundo.vertices[self.personaje.personaje['ubicacion']].informacion()
        elif comando[0] == 'status':
            self.personaje.status()
        elif comando[0] == 'save':
            self.guardar_juego()
        elif comando[0] == 'load':
            self.personaje.personaje = self.cargar_juego()
        elif comando[0] == 'tomar':
            encontrado = False
            for i in range(0, len(self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos)):
                if self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i].datos['nombre'] == comando[1]:
                    encontrado = True
                    if self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i].datos['tomable'] == 'si':
                        self.personaje.personaje['elementos'].append(self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i])
                        self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos.remove(self.mundo.vertices[self.personaje.personaje['ubicacion']].elementos[i])
                        print('Tomaste el elemento')
                    else:
                        print('No puedes tomar este elemento')
                    break
            if not encontrado:
                print('No existe el elemento que quieres tomar')
        elif comando[0] == 'equipar':
            try:
                self.personaje.equipar(comando[1])
            except:
                print('Debe indicar que equipar')
        else:
            print('Comando no disponible')

    def guardar_juego(self):
        try:
            with open('./savegames/savegame.json','w') as f:
                json.dump(self.personaje.personaje,f)
                f.close()
                print('Juego guardado')
        except FileNotFoundError:
            print('Falta el directorio savegame')

    def cargar_juego(self):
        try:
            with open('./savegames/savegame.json') as f:
                print('Juego Cargado')
                return json.load(f)
        except:
            print('No esta el archivo de carga')

class Enemigo:
    def __init__(self,nombre):
        self.datos = obtener_informacion(nombre)
        self.datos['vida_actual'] = self.datos['vida']
    
    def informacion(self):
        print(self.datos['descripcion'])

    def status(self):
        print('{}---{}---{}'.format(Colores.blue,self.datos['nombre'],Colores.reset))
        print('{}>>>>Nivel: {}{}'.format(Colores.orange,Colores.reset,str(self.datos['nivel'])))
        print('{}Vida: {}{}/{}'.format(Colores.orange,Colores.reset,str(self.datos['vida_actual']),str(self.datos['vida'])))
        print('{}Fuerza: {}{}'.format(Colores.orange,Colores.reset,str(self.datos['fuerza'])))
        print('{}Inteligencia: {}{}'.format(Colores.orange,Colores.reset,str(self.datos['inteligencia'])))
        print('{}Constitucion: {}{}'.format(Colores.orange,Colores.reset,str(self.datos['constitucion'])))

#TODO: (items tienen peso)
class Personaje:
    def __init__(self,nombre,id):
        self.personaje = {
            'pasos':0,
            'nombre':nombre, 
            'ubicacion':id, 
            'status': {
                'dinero':0,
                'nivel':1, 
                'experiencia': 0, 
                'fuerza':0, 
                'inteligencia':0, 
                'constitucion':0,
                'vida': 0,
                'vida_maxima': 0
            },
            
            'elementos': [],
            'equipo':{
                'brazo_derecho': None,
                'brazo_izquierdo': None,
                'cabeza': None,
                'pecho': None,
                'piernas': None,
                'anillo_izquierdo': None,
                'anillo_derecho': None
            }
        }
        

    def generar_personaje(self):
        self.personaje['status']['dinero'] = random.randrange(100, 500)
        self.personaje['status']['fuerza'] = random.randrange(1,10)
        self.personaje['status']['inteligencia'] = random.randrange(1,10)
        self.personaje['status']['constitucion'] = random.randrange(1,10)
        self.personaje['status']['vida'] = self.personaje['status']['vida_maxima'] = random.randrange(50,100)
    
    def calculo_total(self, status):
        s = self.personaje['status'][status]
        for i in self.personaje['equipo'].values():
            if i is not None:
                s += int(i.datos[status])
        return s
    
    def status(self):
        print('{}---{}---{}'.format(Colores.blue,self.personaje['nombre'],Colores.reset))
        print('{}>>>>Nivel: {}{}({})'.format(Colores.orange,Colores.reset,str(self.personaje['status']['nivel']),str(self.personaje['status']['experiencia'])))
        print('{}Vida: {}{}/{}'.format(Colores.orange,Colores.reset,str(self.personaje['status']['vida']),str(self.personaje['status']['vida_maxima'])))
        print('{}Dinero: {}{}'.format(Colores.orange,Colores.reset,str(self.personaje['status']['dinero'])))
        print('{}Fuerza: {}{}'.format(Colores.orange,Colores.reset,str(self.calculo_total('fuerza'))))
        print('{}Inteligencia: {}{}'.format(Colores.orange,Colores.reset,str(self.calculo_total('inteligencia'))))
        print('{}Constitucion: {}{}'.format(Colores.orange,Colores.reset,str(self.calculo_total('constitucion'))))
        
        print('{} >>>En tu bolsa: {}'.format(Colores.blue,Colores.reset))
        if len(self.personaje['elementos'])==0:
            print('->Bolsa vacia')
        else:
            for elemento in self.personaje['elementos']:
                print('->{}'.format(elemento.datos['nombre']))
        print('{} >>>Equipo: {}'.format(Colores.blue,Colores.reset))
        for key, value in self.personaje['equipo'].items():
            if value == None:
                print('{}-> {}: {}-'.format(Colores.orange,key,Colores.reset))
            else:
                print('{}-> {}{}: {}'.format(Colores.orange,key,Colores.reset,value.datos['nombre']))
    
    def caminar(self, id):
        self.personaje['ubicacion'] = id

    def equipar(self, elemento):
        encontrado = False
        for i in range(0,len(self.personaje['elementos'])):
            if self.personaje['elementos'][i].datos['nombre'] == elemento:
                encontrado = True
                if self.personaje['elementos'][i].datos['equipable'] is not 'no':
                    if self.personaje['equipo'][self.personaje['elementos'][i].datos['equipable']] is not None:
                        self.personaje['elementos'].append(self.personaje['equipo'][self.personaje['elementos'][i].datos['equipable']])
                    self.personaje['equipo'][self.personaje['elementos'][i].datos['equipable']] = self.personaje['elementos'][i]
                    self.personaje['elementos'].remove(self.personaje['elementos'][i])
                    print('Elemento equipado')
                else:
                    print('No se puede equipar este objeto')
                break
        if not encontrado:
            print('No puede equipar algo que no tiene.')

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
        self.elementos = []
        self.enemigos = []
        

    def insertar_arista(self,id):
        if id not in self.aristas:
            self.aristas.append(id)

    def insertar_elemento(self, elemento):
        self.elementos.append(elemento)

    def insertar_enemigo(self, enemigo):
        self.enemigos.append(enemigo)
    
    def informacion(self, propio = True):
        if propio:
            print('Tu ubicacion: {}'.format(self.id))
            print(self.datos['descripcion'])
            for indice in range(len(self.elementos)):
                print('En el lugar encuentras {}'.format(self.elementos[indice].datos['nombre']))
            for i in range(len(self.enemigos)):
                print('Hay un/a {} que quiere matarte'.format(self.enemigos[i].datos['nombre']))
            print('Posibles salidas: ')
            for arista in self.aristas:
                print('-> {}'.format(arista))
        else:
            print('Estas viendo: {}'.format(self.id))
            print(self.datos['descripcion_lejana'])

            
class Elemento:
    def __init__(self,nombre):
        self.datos = obtener_informacion(nombre)

    def informacion(self):
        print(self.datos['descripcion'])

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
    juego.mundo.vertices['casa'].insertar_elemento(Elemento('mesa'))
    juego.mundo.vertices['casa'].insertar_elemento(Elemento('espada'))
    juego.mundo.vertices['casa'].insertar_elemento(Elemento('martillo'))
    juego.mundo.vertices['casa'].insertar_elemento(Elemento('botas_cuero'))
    juego.mundo.vertices['casa'].insertar_enemigo(Enemigo('rata'))
    
    print('****Fin de Crear Mundo****')
    #TODO: proceso de creacion de personaje
    personaje = Personaje('Draculinio', 'casa')
    personaje.generar_personaje()
    juego.personaje = personaje
    salir = False
    clear()
    while not salir:
        comando = input('>').lower().split(" ", 1)
        if comando[0] == 'salir':
            print('Gracias por jugar')
            salir = True
        else:
            juego.comandos(comando)