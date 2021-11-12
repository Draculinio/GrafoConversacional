import json

def obtener_informacion(archivo):
    with open('./datos/'+archivo+'.json') as f:
        return json.load(f)

class Personaje:
    def __init__(self,nombre,id):
        self.nombre = nombre
        self.ubicacion = id
    
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

    def informacion(self):
        print('Tu ubicacion: '+self.id)
        print(self.datos['descripcion'])
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
                mundo.vertices[personaje.ubicacion].informacion()
            else:
                print('Comando no disponible')
            