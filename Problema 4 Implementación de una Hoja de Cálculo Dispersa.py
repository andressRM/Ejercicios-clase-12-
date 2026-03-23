import os
from typing import Optional, Tuple, Dict

class NodoCelda:
    """nodo de la lista ortogonal. guarda el valor y punteros en dos direcciones."""
    def __init__(self, fila: int, columna: int, valor: float):
        self.fila: int = fila
        self.columna: int = columna
        self.valor: float = valor
        self.derecha: Optional['NodoCelda'] = None  # puntero al siguiente en la misma fila
        self.abajo: Optional['NodoCelda'] = None    # puntero al siguiente en la misma columna

class HojaCalculoDispersa:
    """gestor de la matriz ortogonal dispersa usando listas enlazadas cruzadas."""
    def __init__(self):
        # diccionarios que actuan como los arreglos de cabeceras para filas y columnas
        self.cabezas_filas: Dict[int, NodoCelda] = {}
        self.cabezas_cols: Dict[int, NodoCelda] = {}
        self.max_fila: int = 0
        self.max_col: int = 0
        self.total_nodos: int = 0

    def insertar_valor(self, fila: int, columna: int, valor: float) -> None:
        """inserta o actualiza una celda entrelazando punteros horizontales y verticales."""
        if valor == 0:
            self.eliminar_valor(fila, columna)
            return

        self.max_fila = max(self.max_fila, fila)
        self.max_col = max(self.max_col, columna)

        # verificamos si ya existe para actualizar
        actual = self.cabezas_filas.get(fila)
        while actual:
            if actual.columna == columna:
                actual.valor = valor
                return
            actual = actual.derecha

        # si no existe, creamos el nodo
        nuevo = NodoCelda(fila, columna, valor)
        self.total_nodos += 1

        # 1. enlazar en la fila (horizontal)
        if fila not in self.cabezas_filas or self.cabezas_filas[fila].columna > columna:
            nuevo.derecha = self.cabezas_filas.get(fila)
            self.cabezas_filas[fila] = nuevo
        else:
            act_f = self.cabezas_filas[fila]
            while act_f.derecha and act_f.derecha.columna < columna:
                act_f = act_f.derecha
            nuevo.derecha = act_f.derecha
            act_f.derecha = nuevo

        # 2. enlazar en la columna (vertical)
        if columna not in self.cabezas_cols or self.cabezas_cols[columna].fila > fila:
            nuevo.abajo = self.cabezas_cols.get(columna)
            self.cabezas_cols[columna] = nuevo
        else:
            act_c = self.cabezas_cols[columna]
            while act_c.abajo and act_c.abajo.fila < fila:
                act_c = act_c.abajo
            nuevo.abajo = act_c.abajo
            act_c.abajo = nuevo

    def eliminar_valor(self, fila: int, columna: int) -> None:
        """elimina un nodo liberando memoria y reconectando los puentes."""
        # desenlazar horizontalmente
        if fila in self.cabezas_filas:
            act_f = self.cabezas_filas[fila]
            if act_f.columna == columna:
                self.cabezas_filas[fila] = act_f.derecha
                if not self.cabezas_filas[fila]:
                    del self.cabezas_filas[fila]
            else:
                while act_f.derecha and act_f.derecha.columna != columna:
                    act_f = act_f.derecha
                if act_f.derecha:
                    act_f.derecha = act_f.derecha.derecha

        # desenlazar verticalmente
        if columna in self.cabezas_cols:
            act_c = self.cabezas_cols[columna]
            if act_c.fila == fila:
                self.cabezas_cols[columna] = act_c.abajo
                if not self.cabezas_cols[columna]:
                    del self.cabezas_cols[columna]
            else:
                while act_c.abajo and act_c.abajo.fila != fila:
                    act_c = act_c.abajo
                if act_c.abajo:
                    act_c.abajo = act_c.abajo.abajo
                    self.total_nodos -= 1

    def obtener_valor(self, fila: int, columna: int) -> float:
        """busca el valor de una celda. si no existe el nodo, por definicion es 0."""
        actual = self.cabezas_filas.get(fila)
        while actual and actual.columna <= columna:
            if actual.columna == columna:
                return actual.valor
            actual = actual.derecha
        return 0.0

    def rango_estadisticas(self, f1: int, c1: int, f2: int, c2: int) -> Tuple[float, float]:
        """calcula la suma y el promedio de un rango cruzando solo los nodos existentes."""
        suma = 0.0
        nodos_en_rango = 0
        area_total = (abs(f2 - f1) + 1) * (abs(c2 - c1) + 1)
        
        f_min, f_max = min(f1, f2), max(f1, f2)
        c_min, c_max = min(c1, c2), max(c1, c2)

        for f in range(f_min, f_max + 1):
            actual = self.cabezas_filas.get(f)
            while actual and actual.columna <= c_max:
                if actual.columna >= c_min:
                    suma += actual.valor
                    nodos_en_rango += 1
                actual = actual.derecha
                
        promedio = suma / area_total if area_total > 0 else 0
        return suma, promedio

    def insertar_fila_completa(self, fila_objetivo: int) -> None:
        """desplaza las coordenadas de todas las celdas debajo de la fila insertada."""
        nodos_a_mover = []
        for f in list(self.cabezas_filas.keys()):
            if f >= fila_objetivo:
                actual = self.cabezas_filas[f]
                while actual:
                    nodos_a_mover.append((actual.fila, actual.columna, actual.valor))
                    actual = actual.derecha
                    
        # eliminamos desde abajo hacia arriba
        for f, c, v in sorted(nodos_a_mover, key=lambda x: x[0], reverse=True):
            self.eliminar_valor(f, c)
            self.insertar_valor(f + 1, c, v)

    def mostrar_tabular(self) -> None:
        """imprime la matriz visualizando vacios como [   ]."""
        if self.max_fila == 0:
            print("[ hoja vacia ]")
            return
            
        print("\n    " + "".join([f" COL {c:2d} " for c in range(1, self.max_col + 1)]))
        for f in range(1, self.max_fila + 1):
            fila_str = f"F{f:02d} "
            for c in range(1, self.max_col + 1):
                val = self.obtener_valor(f, c)
                if val == 0:
                    fila_str += "[      ] "
                else:
                    fila_str += f"[{val:6.1f}] "
            print(fila_str)
        print("")

    def mostrar_eficiencia(self) -> None:
        """demuestra la comparacion de memoria ram."""
        celdas_totales = self.max_fila * self.max_col
        if celdas_totales == 0: return
        porcentaje_ahorro = 100 - ((self.total_nodos / celdas_totales) * 100)
        print(f"--- ANALISIS DE EFICIENCIA EN MEMORIA ---")
        print(f"matriz tradicional requeriria: {celdas_totales} espacios en memoria.")
        print(f"lista ortogonal dispersa usa : {self.total_nodos} nodos en memoria.")
        print(f"ahorro total de ram: {porcentaje_ahorro:.2f}%\n")


def ejecutar_pruebas_excel():
    print("--- INICIANDO PRUEBAS: HOJA DE CALCULO DISPERSA ---")
    hoja = HojaCalculoDispersa()
    
    # 1. insertar valores esparcidos
    hoja.insertar_valor(1, 1, 150.5)
    hoja.insertar_valor(1, 4, 300.0)
    hoja.insertar_valor(3, 2, 45.2)
    hoja.insertar_valor(5, 5, 900.8)
    
    print("\n1. hoja inicial despues de inserciones dispersas:")
    hoja.mostrar_tabular()
    
    # 2. obtener valor especifico
    val = hoja.obtener_valor(3, 2)
    print(f"2. valor en Fila 3, Col 2: {val}")
    
    # 3. actualizar y eliminar celdas
    hoja.insertar_valor(3, 2, 50.0) # actualiza
    hoja.eliminar_valor(1, 4)       # elimina
    print("\n3. hoja despues de actualizar (3,2)->50 y eliminar (1,4):")
    hoja.mostrar_tabular()
    
    # 4. suma y promedio en rango
    suma, prom = hoja.rango_estadisticas(1, 1, 5, 5)
    print(f"4. rango (1,1) a (5,5) -> suma: {suma}, promedio global: {prom:.2f}")
    
    # 5. insertar fila completa desplazando datos
    hoja.insertar_fila_completa(2)
    print("\n5. hoja despues de insertar una fila vacia en la posicion 2:")
    hoja.mostrar_tabular()
    
    # 6. analisis de eficiencia matematico
    hoja.mostrar_eficiencia()
    print(" FIN DE LAS PRUEBAS ")

if __name__ == "__main__":
    ejecutar_pruebas_excel()