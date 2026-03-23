from typing import Optional

class Proceso:
    """
    (explicacion de la estructura)
    representa el nodo de nuestra lista enlazada.
    almacena los datos del proceso y el puntero al siguiente nodo.
    """
    def __init__(self, id_proceso: str, nombre: str, tiempo_creacion: int, tiempo_cpu: int, tiempo_espera: int = 0):
        self.id_proceso: str = id_proceso
        self.nombre: str = nombre
        self.estado: str = "listo" # estados: listo, en ejecucion, bloqueado, terminado
        self.tiempo_creacion: int = tiempo_creacion
        self.tiempo_cpu: int = tiempo_cpu
        self.tiempo_espera: int = tiempo_espera
        self.siguiente: Optional['Proceso'] = None # puntero al siguiente nodo

class GestorProcesos:
    """
    gestiona la lista simplemente enlazada de procesos del sistema operativo.
    """
    def __init__(self):
        self.cabeza: Optional[Proceso] = None

    def anadir_proceso(self, id_proceso: str, nombre: str, tiempo_creacion: int, tiempo_cpu: int, tiempo_espera: int = 0) -> None:
        """
        inserta un nodo al final de la lista. complejidad: O(n).
        """
        nuevo_proceso = Proceso(id_proceso, nombre, tiempo_creacion, tiempo_cpu, tiempo_espera)
        
        if not self.cabeza:
            self.cabeza = nuevo_proceso
            return
            
        actual = self.cabeza
        while actual.siguiente:
            actual = actual.siguiente
        actual.siguiente = nuevo_proceso

    def cambiar_estado(self, id_proceso: str, nuevo_estado: str) -> bool:
        """
        busca un proceso por id y actualiza su estado. complejidad: O(n).
        """
        estados_validos = ["listo", "en ejecucion", "bloqueado", "terminado"]
        if nuevo_estado not in estados_validos:
            raise ValueError(f"estado invalido. use: {', '.join(estados_validos)}")
            
        actual = self.cabeza
        while actual:
            if actual.id_proceso == id_proceso:
                actual.estado = nuevo_estado
                return True
            actual = actual.siguiente
        raise KeyError(f"proceso con id {id_proceso} no encontrado.")

    def eliminar_terminados(self) -> int:
        """
        recorre la lista y elimina todos los nodos con estado 'terminado'.
        ajusta los punteros para no romper la cadena. complejidad: O(n).
        """
        eliminados = 0
        
        # si la cabeza es la que debe eliminarse (pueden ser varias seguidas)
        while self.cabeza and self.cabeza.estado == "terminado":
            self.cabeza = self.cabeza.siguiente
            eliminados += 1
            
        # si el nodo a eliminar esta en el medio o al final
        actual = self.cabeza
        while actual and actual.siguiente:
            if actual.siguiente.estado == "terminado":
                # saltamos el nodo terminado, conectando con el subsiguiente
                actual.siguiente = actual.siguiente.siguiente
                eliminados += 1
            else:
                actual = actual.siguiente
                
        return eliminados

    def mover_a_prioridad(self, id_proceso: str) -> None:
        """
        desconecta un nodo de su posicion actual y lo inserta al inicio (cabeza).
        simula la asignacion de maxima prioridad. complejidad: O(n) para buscar, O(1) para mover.
        """
        if not self.cabeza or self.cabeza.id_proceso == id_proceso:
            return # la lista esta vacia o el proceso ya es la cabeza
            
        anterior = None
        actual = self.cabeza
        
        # buscar el nodo y mantener referencia al anterior
        while actual and actual.id_proceso != id_proceso:
            anterior = actual
            actual = actual.siguiente
            
        if not actual:
            raise KeyError(f"proceso con id {id_proceso} no encontrado.")
            
        # desenlazar el nodo de su posicion actual
        anterior.siguiente = actual.siguiente
        # moverlo al inicio
        actual.siguiente = self.cabeza
        self.cabeza = actual

    def calcular_promedio_espera(self) -> float:
        """
        recorre la lista sumando los tiempos de espera. complejidad: O(n).
        """
        if not self.cabeza:
            return 0.0
            
        suma_espera = 0
        contador = 0
        actual = self.cabeza
        
        while actual:
            suma_espera += actual.tiempo_espera
            contador += 1
            actual = actual.siguiente
            
        return suma_espera / contador

    def mostrar_procesos(self) -> None:
        """
        imprime la lista completa en orden de ejecucion.
        """
        if not self.cabeza:
            print("no hay procesos en el sistema.")
            return
            
        print("\n--- cola de procesos ---")
        actual = self.cabeza
        posicion = 1
        while actual:
            print(f"{posicion}. [{actual.id_proceso}] {actual.nombre} | estado: {actual.estado} | cpu: {actual.tiempo_cpu}ms | espera: {actual.tiempo_espera}ms")
            actual = actual.siguiente
            posicion += 1
        print("------------------------\n")

def menu_interactivo():
    os_manager = GestorProcesos()
    
    # insertamos un par de procesos de prueba iniciales
    os_manager.anadir_proceso("p1", "navegador", 0, 150, 20)
    os_manager.anadir_proceso("p2", "antivirus", 5, 300, 50)
    
    while True:
        print("\nsimulador de procesos del sistema operativo (lista enlazada)")
        print("1. añadir nuevo proceso")
        print("2. cambiar estado de un proceso")
        print("3. eliminar procesos terminados")
        print("4. dar prioridad (mover al inicio)")
        print("5. mostrar cola de procesos")
        print("6. ver tiempo promedio de espera")
        print("7. salir")
        
        opcion = input("seleccione una opcion: ")
        
        try:
            if opcion == "1":
                id_p = input("ingrese id del proceso: ")
                nom = input("ingrese nombre: ")
                t_cpu = int(input("tiempo cpu requerido (ms): "))
                t_esp = int(input("tiempo en espera actual (ms): "))
                os_manager.anadir_proceso(id_p, nom, 0, t_cpu, t_esp)
                print("proceso añadido al final de la cola.")
                
            elif opcion == "2":
                id_p = input("ingrese id del proceso: ")
                est = input("nuevo estado (listo, en ejecucion, bloqueado, terminado): ")
                os_manager.cambiar_estado(id_p, est)
                print("estado actualizado con exito.")
                
            elif opcion == "3":
                eliminados = os_manager.eliminar_terminados()
                print(f"limpieza completada. se eliminaron {eliminados} procesos terminados de la memoria.")
                
            elif opcion == "4":
                id_p = input("ingrese id del proceso a priorizar: ")
                os_manager.mover_a_prioridad(id_p)
                print("proceso movido al inicio de la cola (O(1) en insercion).")
                
            elif opcion == "5":
                os_manager.mostrar_procesos()
                
            elif opcion == "6":
                promedio = os_manager.calcular_promedio_espera()
                print(f"tiempo promedio de espera en la cola: {promedio:.2f}ms")
                
            elif opcion == "7":
                print("apagando simulador...")
                break
                
            else:
                print("opcion no valida.")
                
        except ValueError as e:
            print(f"error de validacion: {e}")
        except KeyError as e:
            print(f"error de busqueda: {e}")
        except Exception as e:
            print(f"error inesperado: {e}")

if __name__ == "__main__":
    menu_interactivo()