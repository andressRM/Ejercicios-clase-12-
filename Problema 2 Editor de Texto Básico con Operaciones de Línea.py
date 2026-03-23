import os
from typing import Optional

class Linea:
    """nodo de la lista doblemente enlazada que representa una linea de texto."""
    def __init__(self, contenido: str):
        self.contenido: str = contenido
        self.anterior: Optional['Linea'] = None
        self.siguiente: Optional['Linea'] = None

class EditorTexto:
    """gestor del editor basado en una lista doblemente enlazada."""
    def __init__(self):
        self.cabeza: Optional[Linea] = None
        self.total_lineas: int = 0

    def mostrar_texto(self) -> None:
        """imprime todo el contenido del editor con su numero de linea."""
        if not self.cabeza:
            print("--- [ documento vacio ] ---")
            return
            
        print("\n--- contenido del documento ---")
        actual = self.cabeza
        num = 1
        while actual:
            print(f"{num:02d} | {actual.contenido}")
            actual = actual.siguiente
            num += 1
        print("-------------------------------\n")

    def _obtener_nodo(self, posicion: int) -> Optional[Linea]:
        """metodo auxiliar para encontrar un nodo por su posicion (1-indexado)."""
        if posicion < 1 or posicion > self.total_lineas:
            return None
        actual = self.cabeza
        for _ in range(1, posicion):
            actual = actual.siguiente
        return actual

    def insertar_linea(self, posicion: int, contenido: str) -> None:
        """inserta una nueva linea en cualquier posicion. O(n) busqueda, O(1) insercion."""
        nueva_linea = Linea(contenido)
        
        # insertar al principio o en lista vacia
        if posicion <= 1 or not self.cabeza:
            nueva_linea.siguiente = self.cabeza
            if self.cabeza:
                self.cabeza.anterior = nueva_linea
            self.cabeza = nueva_linea
        # insertar al final o en el medio
        else:
            if posicion > self.total_lineas:
                posicion = self.total_lineas + 1
                
            anterior_nodo = self._obtener_nodo(posicion - 1)
            siguiente_nodo = anterior_nodo.siguiente
            
            nueva_linea.anterior = anterior_nodo
            nueva_linea.siguiente = siguiente_nodo
            
            anterior_nodo.siguiente = nueva_linea
            if siguiente_nodo:
                siguiente_nodo.anterior = nueva_linea
                
        self.total_lineas += 1

    def eliminar_linea(self, posicion: int) -> str:
        """elimina una linea y devuelve su contenido. O(n) busqueda, O(1) eliminacion."""
        nodo_eliminar = self._obtener_nodo(posicion)
        if not nodo_eliminar:
            raise ValueError(f"la linea {posicion} no existe.")
            
        if nodo_eliminar.anterior:
            nodo_eliminar.anterior.siguiente = nodo_eliminar.siguiente
        else:
            self.cabeza = nodo_eliminar.siguiente
            
        if nodo_eliminar.siguiente:
            nodo_eliminar.siguiente.anterior = nodo_eliminar.anterior
            
        self.total_lineas -= 1
        return nodo_eliminar.contenido

    def mover_linea(self, pos_origen: int, pos_destino: int) -> None:
        """mueve una linea de una posicion a otra reconectando punteros."""
        if pos_origen == pos_destino:
            return
        # reutilizamos la logica de eliminacion e insercion
        contenido_movido = self.eliminar_linea(pos_origen)
        
        # si la movemos hacia abajo, la eliminacion previa redujo el total de lineas
        if pos_origen < pos_destino:
            pos_destino -= 1
            
        self.insertar_linea(pos_destino, contenido_movido)

    def buscar_texto(self, subcadena: str) -> None:
        """busca una palabra o frase en todos los nodos y muestra sus posiciones."""
        actual = self.cabeza
        num = 1
        encontrado = False
        print(f"\nresultados de busqueda para '{subcadena}':")
        while actual:
            if subcadena.lower() in actual.contenido.lower():
                print(f"linea {num}: {actual.contenido}")
                encontrado = True
            actual = actual.siguiente
            num += 1
        if not encontrado:
            print("no se encontraron coincidencias.")

    def reemplazar_texto(self, posicion: int, viejo_texto: str, nuevo_texto: str) -> None:
        """reemplaza un fragmento de texto dentro de una linea especifica."""
        nodo = self._obtener_nodo(posicion)
        if not nodo:
            raise ValueError(f"la linea {posicion} no existe.")
        nodo.contenido = nodo.contenido.replace(viejo_texto, nuevo_texto)

    def guardar_archivo(self, ruta: str) -> None:
        """recorre la lista enlazada y escribe cada linea en un archivo fisico."""
        with open(ruta, 'w', encoding='utf-8') as archivo:
            actual = self.cabeza
            while actual:
                archivo.write(actual.contenido + "\n")
                actual = actual.siguiente

    def cargar_archivo(self, ruta: str) -> None:
        """lee un archivo y crea la lista enlazada linea por linea."""
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"el archivo {ruta} no existe.")
            
        self.cabeza = None
        self.total_lineas = 0
        with open(ruta, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                self.insertar_linea(self.total_lineas + 1, linea.strip('\n'))

def menu_editor():
    editor = EditorTexto()
    editor.insertar_linea(1, "bienvenido al editor de texto dinamico.")
    editor.insertar_linea(2, "esta es una prueba de la lista doblemente enlazada.")
    
    while True:
        editor.mostrar_texto()
        print("opciones: 1.insertar | 2.eliminar | 3.mover | 4.buscar | 5.reemplazar | 6.guardar | 7.cargar | 8.salir")
        opcion = input("seleccione una accion: ")
        
        try:
            if opcion == "1":
                pos = int(input("posicion a insertar (ej. 1): "))
                txt = input("contenido de la linea: ")
                editor.insertar_linea(pos, txt)
            elif opcion == "2":
                pos = int(input("numero de linea a eliminar: "))
                editor.eliminar_linea(pos)
            elif opcion == "3":
                ori = int(input("numero de linea a mover: "))
                dest = int(input("posicion de destino: "))
                editor.mover_linea(ori, dest)
            elif opcion == "4":
                txt = input("texto a buscar: ")
                editor.buscar_texto(txt)
                input("presione enter para continuar...")
            elif opcion == "5":
                pos = int(input("numero de linea a editar: "))
                viejo = input("texto a reemplazar: ")
                nuevo = input("nuevo texto: ")
                editor.reemplazar_texto(pos, viejo, nuevo)
            elif opcion == "6":
                ruta = input("nombre del archivo (ej. doc.txt): ")
                editor.guardar_archivo(ruta)
                print("archivo guardado con exito.")
            elif opcion == "7":
                ruta = input("nombre del archivo a cargar: ")
                editor.cargar_archivo(ruta)
                print("archivo cargado con exito.")
            elif opcion == "8":
                print("cerrando editor...")
                break
            else:
                print("opcion invalida.")
        except ValueError as e:
            print(f"error de validacion: {e}")
        except FileNotFoundError as e:
            print(f"error de archivo: {e}")
        except Exception as e:
            print(f"error inesperado: {e}")

if __name__ == "__main__":
    menu_editor()