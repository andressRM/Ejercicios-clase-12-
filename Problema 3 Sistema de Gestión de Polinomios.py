from typing import Optional

class Termino:
    """nodo de la lista enlazada que representa un termino del polinomio."""
    def __init__(self, coeficiente: float, exponente: int):
        self.coeficiente: float = coeficiente
        self.exponente: int = exponente
        self.siguiente: Optional['Termino'] = None

class Polinomio:
    """lista simplemente enlazada que mantiene los terminos ordenados por exponente mayor a menor."""
    def __init__(self):
        self.cabeza: Optional[Termino] = None

    def insertar_termino(self, coeficiente: float, exponente: int) -> None:
        """inserta un termino manteniendo el orden descendente. si el exponente existe, suma los coeficientes."""
        if coeficiente == 0:
            return # no almacenamos ceros (ahorro de memoria)
            
        nuevo = Termino(coeficiente, exponente)
        
        # caso 1: lista vacia o el nuevo termino tiene el exponente mayor
        if not self.cabeza or self.cabeza.exponente < exponente:
            nuevo.siguiente = self.cabeza
            self.cabeza = nuevo
            return
            
        # caso 2: buscar posicion o exponente igual
        actual = self.cabeza
        anterior = None
        
        while actual and actual.exponente >= exponente:
            if actual.exponente == exponente:
                actual.coeficiente += coeficiente
                # si al sumar se hace 0, eliminamos el nodo para mantener la lista dispersa
                if actual.coeficiente == 0:
                    if anterior:
                        anterior.siguiente = actual.siguiente
                    else:
                        self.cabeza = actual.siguiente
                return
            anterior = actual
            actual = actual.siguiente
            
        # insertar en el medio o al final
        anterior.siguiente = nuevo
        nuevo.siguiente = actual

    def sumar(self, otro: 'Polinomio') -> 'Polinomio':
        """crea un nuevo polinomio sumando los terminos de self y otro."""
        resultado = Polinomio()
        for p in [self, otro]:
            actual = p.cabeza
            while actual:
                resultado.insertar_termino(actual.coeficiente, actual.exponente)
                actual = actual.siguiente
        return resultado

    def restar(self, otro: 'Polinomio') -> 'Polinomio':
        """crea un nuevo polinomio restando los terminos de otro a self."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            resultado.insertar_termino(actual.coeficiente, actual.exponente)
            actual = actual.siguiente
            
        actual = otro.cabeza
        while actual:
            resultado.insertar_termino(-actual.coeficiente, actual.exponente)
            actual = actual.siguiente
        return resultado

    def multiplicar(self, otro: 'Polinomio') -> 'Polinomio':
        """multiplica dos polinomios (O(n*m)) combinando coeficientes y sumando exponentes."""
        resultado = Polinomio()
        actual1 = self.cabeza
        while actual1:
            actual2 = otro.cabeza
            while actual2:
                nuevo_coef = actual1.coeficiente * actual2.coeficiente
                nuevo_exp = actual1.exponente + actual2.exponente
                resultado.insertar_termino(nuevo_coef, nuevo_exp)
                actual2 = actual2.siguiente
            actual1 = actual1.siguiente
        return resultado

    def evaluar(self, x: float) -> float:
        """evalua el polinomio reemplazando la incognita x."""
        resultado = 0.0
        actual = self.cabeza
        while actual:
            resultado += actual.coeficiente * (x ** actual.exponente)
            actual = actual.siguiente
        return resultado

    def derivar(self) -> 'Polinomio':
        """aplica la regla de la potencia para derivar: c*x^e -> (c*e)*x^(e-1)."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            if actual.exponente > 0:
                resultado.insertar_termino(actual.coeficiente * actual.exponente, actual.exponente - 1)
            actual = actual.siguiente
        return resultado

    def integrar(self) -> 'Polinomio':
        """aplica la regla de la potencia inversa: c*x^e -> (c/(e+1))*x^(e+1)."""
        resultado = Polinomio()
        actual = self.cabeza
        while actual:
            resultado.insertar_termino(actual.coeficiente / (actual.exponente + 1), actual.exponente + 1)
            actual = actual.siguiente
        return resultado

    def mostrar(self) -> str:
        """construye la representacion visual en formato estandar."""
        if not self.cabeza:
            return "0"
            
        terminos_str = []
        actual = self.cabeza
        while actual:
            coef = actual.coeficiente
            exp = actual.exponente
            
            # formatear signo
            signo = "+" if coef > 0 and terminos_str else ("-" if coef < 0 else "")
            if signo and signo == "-":
                signo = "- " if terminos_str else "-"
            elif signo:
                signo = "+ "
                
            coef_abs = abs(coef)
            # ocultar el 1 si hay variable
            coef_str = f"{coef_abs:g}" if coef_abs != 1 or exp == 0 else ""
            
            # formatear la variable x
            if exp == 0:
                var_str = ""
            elif exp == 1:
                var_str = "x"
            else:
                var_str = f"x^{exp}"
                
            termino = f"{signo}{coef_str}{var_str}"
            terminos_str.append(termino)
            actual = actual.siguiente
            
        return " ".join(terminos_str)

def menu_polinomios():
    # creamos 3 polinomios de ejemplo (requerimiento)
    p1 = Polinomio()
    p1.insertar_termino(3, 4)
    p1.insertar_termino(-2, 2)
    p1.insertar_termino(5, 0)  # P1: 3x^4 - 2x^2 + 5
    
    p2 = Polinomio()
    p2.insertar_termino(1, 2)
    p2.insertar_termino(-1, 0) # P2: x^2 - 1
    
    p3 = Polinomio()
    p3.insertar_termino(2, 3)
    p3.insertar_termino(4, 1)  # P3: 2x^3 + 4x

    polinomios = {"P1": p1, "P2": p2, "P3": p3}

    while True:
        print("\n--- gestor de polinomios dispersos ---")
        for nombre, pol in polinomios.items():
            print(f"{nombre}(x) = {pol.mostrar()}")
        
        print("\n1. sumar (P1 + P2)")
        print("2. restar (P1 - P2)")
        print("3. multiplicar (P2 * P3)")
        print("4. evaluar P1 en x")
        print("5. derivar P3")
        print("6. integrar P2")
        print("7. salir")
        
        opcion = input("seleccione una operacion: ")
        
        try:
            if opcion == "1":
                res = p1.sumar(p2)
                print(f"resultado: {res.mostrar()}")
            elif opcion == "2":
                res = p1.restar(p2)
                print(f"resultado: {res.mostrar()}")
            elif opcion == "3":
                res = p2.multiplicar(p3)
                print(f"resultado: {res.mostrar()}")
            elif opcion == "4":
                valor_x = float(input("ingrese el valor de x: "))
                res = p1.evaluar(valor_x)
                print(f"P1({valor_x}) = {res}")
            elif opcion == "5":
                res = p3.derivar()
                print(f"P3'(x) = {res.mostrar()}")
            elif opcion == "6":
                res = p2.integrar()
                print(f"integral de P2(x) = {res.mostrar()} + C")
            elif opcion == "7":
                print("cerrando gestor...")
                break
            else:
                print("opcion invalida.")
        except Exception as e:
            print(f"error en la operacion: {e}")

def ejecutar_pruebas_automatizadas():
    print("\n--- INICIANDO PRUEBAS DE POLINOMIOS ---")
    
    # 1. Creación de los 3 polinomios de ejemplo
    p1 = Polinomio()
    p1.insertar_termino(3, 4)
    p1.insertar_termino(-2, 2)
    p1.insertar_termino(5, 0)
    
    p2 = Polinomio()
    p2.insertar_termino(1, 2)
    p2.insertar_termino(-1, 0)
    
    p3 = Polinomio()
    p3.insertar_termino(2, 3)
    p3.insertar_termino(4, 1)

    # Mostrar formato estándar
    print(f"P1(x) = {p1.mostrar()}")
    print(f"P2(x) = {p2.mostrar()}")
    print(f"P3(x) = {p3.mostrar()}")
    print("-" * 40)

    # 2. Suma: P1 + P2
    suma = p1.sumar(p2)
    print(f"Suma (P1 + P2): {suma.mostrar()}")

    # 3. Resta: P1 - P2
    resta = p1.restar(p2)
    print(f"Resta (P1 - P2): {resta.mostrar()}")

    # 4. Multiplicación: P2 * P3
    multiplicacion = p2.multiplicar(p3)
    print(f"Multiplicación (P2 * P3): {multiplicacion.mostrar()}")

    # 5. Evaluación: P1 cuando x = 2
    valor_x = 2
    evaluacion = p1.evaluar(valor_x)
    print(f"Evaluación de P1 en x={valor_x}: {evaluacion}")

    # 6. Derivada: Derivar P3
    derivada = p3.derivar()
    print(f"Derivada P3'(x): {derivada.mostrar()}")

    # 7. Integral: Integrar P2
    integral = p2.integrar()
    print(f"Integral de P2(x): {integral.mostrar()} + C")
    print("--- FIN DE LAS PRUEBAS ---\n")

# Punto de entrada para las pruebas directas
if __name__ == "__main__":
    ejecutar_pruebas_automatizadas()