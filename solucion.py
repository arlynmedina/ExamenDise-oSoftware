from abc import ABC, abstractmethod
from datetime import datetime

class Libro:
    def __init__(self, id, titulo, autor, isbn, disponible=True):
        self.id = id
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = disponible

class Prestamo:
    def __init__(self, id, libro_id, usuario, fecha):
        self.id = libro_id
        self.libro_id = libro_id
        self.usuario = usuario
        self.fecha = fecha
        self.devuelto = False

#EJERCICIO 1:
class Busqueda(ABC):
    @abstractmethod
    def buscar(self, libro: Libro, valor) -> bool:
        pass

class BusquedaPorTitulo(Busqueda):
    def buscar(self, libro: Libro, valor) -> bool:
        if valor is None:
            return False
        return valor.lower() in libro.titulo.lower()

class BusquedaPorAutor(Busqueda):
    def buscar(self, libro: Libro, valor) -> bool:
        if valor is None:
            return False
        return valor.lower() in libro.autor.lower()

class BusquedaPorISBN(Busqueda):
    def buscar(self, libro: Libro, valor) -> bool:
        if valor is None:
            return False
        return libro.isbn == valor

class BusquedaPorDisponibilidad(Busqueda):
    def buscar(self, libro: Libro, valor) -> bool:
        if valor is None:
            return False
        disponible = valor.lower() == "true"
        return libro.disponible == disponible
    
#EJERCICIO 2:
class ValidadorTitulo:
    def validar(self, titulo):
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        return None

class ValidadorAutor:
    def validar(self, autor):
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        return None

class ValidadorISBN:
    def validar(self, isbn):
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"
        return None

class ValidadorUsuario:
    def validar(self, usuario):
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"
        return None

class ValidadorBiblioteca:
    def __init__(self):
        self.titulo = ValidadorTitulo()
        self.autor = ValidadorAutor()
        self.isbn = ValidadorISBN()
        self.usuario = ValidadorUsuario()

    def validar_libro(self, titulo, autor, isbn):
        for validador, valor in [(self.titulo, titulo),
                                 (self.autor, autor),
                                 (self.isbn, isbn)]:
            error = validador.validar(valor)
            if error:
                return error
        return None

    def validar_usuario(self, usuario):
        return self.usuario.validar(usuario)
    
class RepositorioBiblioteca:
    def __init__(self, archivo="biblioteca.txt"):
        self.archivo = archivo
    
    def guardar(self, libros, prestamos):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(libros)}\n")
            f.write(f"Préstamos: {len(prestamos)}\n")
    
    def cargar(self):
        try:
            with open(self.archivo, 'r') as f:
                f.read()
            return True
        except:
            return False
    
class ServicioNotificaciones:
    def enviar(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")

#EJERCICIO 3:
class IRepositorio(ABC):
    @abstractmethod
    def guardar(self, libros, prestamos):
        pass

    @abstractmethod
    def cargar(self):
        pass

class RepositorioArchivo(IRepositorio):
    def __init__(self, archivo="biblioteca.txt"):
        self.archivo = archivo

    def guardar(self, libros, prestamos):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(libros)}\n")
            f.write(f"Préstamos: {len(prestamos)}\n")

    def cargar(self):
        try:
            with open(self.archivo, 'r') as f:
                f.read()
            return True
        except:
            return False
        
class SistemaBiblioteca:
    def __init__(self, repositorio: IRepositorio, validador: ValidadorBiblioteca, notificaciones: ServicioNotificaciones):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.repositorio = repositorio
        self.validador = validador
        self.notificaciones = notificaciones

    def agregar_libro(self, titulo, autor, isbn):
        error = self.validador.validar_libro(titulo, autor, isbn)
        if error:
            return error

        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        self.repositorio.guardar(self.libros, self.prestamos)
        return f"Libro '{titulo}' agregado exitosamente"

    def buscar_libro(self, estrategia: Busqueda, valor):
        resultados = []
        for libro in self.libros:
            if estrategia.buscar(libro, valor):
                resultados.append(libro)
        return resultados


    def realizar_prestamo(self, libro_id, usuario):
        error = self.validador.validar_usuario(usuario)
        if error:
            return error

        libro = next((l for l in self.libros if l.id == libro_id), None)
        if not libro:
            return "Error: Libro no encontrado"
        if not libro.disponible:
            return "Error: Libro no disponible"

        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False

        self.repositorio.guardar(self.libros, self.prestamos)
        self.notificaciones.enviar(usuario, libro.titulo)
        return f"Préstamo realizado a {usuario}"

    def devolver_libro(self, prestamo_id):
        prestamo = next((p for p in self.prestamos if p.id == prestamo_id), None)
        if not prestamo:
            return "Error: Préstamo no encontrado"
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"

        libro = next((l for l in self.libros if l.id == prestamo.libro_id), None)
        if libro:
            libro.disponible = True

        prestamo.devuelto = True
        self.repositorio.guardar(self.libros, self.prestamos)
        return "Libro devuelto exitosamente"

    def obtener_todos_libros(self):
        return self.libros

    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]

    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]
    
def main():
    repositorio = RepositorioArchivo() 
    notificador = ServicioNotificaciones()
    validador = ValidadorBiblioteca()
    sistema = SistemaBiblioteca(repositorio, validador, notificador)

    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))

    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro(BusquedaPorAutor(), "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")

    print("\n=== BÚSQUEDA POR DISPONIBILIDAD ===")
    resultados_disp = sistema.buscar_libro(BusquedaPorDisponibilidad(), "true")
    for libro in resultados_disp:
        print(f"- {libro.titulo} (disponible)")

    print("\n=== REALIZAR PRÉSTAMO ===")
    print(sistema.realizar_prestamo(1, "Juan Pérez"))

    print("\n=== LIBROS DISPONIBLES ===")
    disponibles = sistema.obtener_libros_disponibles()
    for libro in disponibles:
        print(f"- {libro.titulo}")

    print("\n=== DEVOLVER LIBRO ===")
    print(sistema.devolver_libro(1))

    print("\n=== PRÉSTAMOS ACTIVOS ===")
    activos = sistema.obtener_prestamos_activos()
    print(f"Total de préstamos activos: {len(activos)}")

if __name__ == "__main__":
    main()
