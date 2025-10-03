"""
EXAMEN PRINCIPIOS SOLID - 2 HORAS
Sistema de Mini-Biblioteca

INSTRUCCIONES:
1. NO modifiques este archivo
2. Crea archivos nuevos para tus refactorizaciones
3. Asegúrate que el código siga funcionando

CÓDIGO BASE CON VIOLACIONES DELIBERADAS DE SOLID
"""

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

# VIOLACIÓN: Esta clase hace DEMASIADAS cosas (SRP)
# VIOLACIÓN: Búsqueda con if/elif (OCP)
# VIOLACIÓN: Dependencia directa de implementación (DIP)
class SistemaBiblioteca:
    def __init__(self):
        self.libros = []
        self.prestamos = []
        self.contador_libro = 1
        self.contador_prestamo = 1
        self.archivo = "biblioteca.txt"
    
    # VIOLACIÓN SRP: Mezcla validación + lógica de negocio + persistencia
    def agregar_libro(self, titulo, autor, isbn):
        # Validación inline
        if not titulo or len(titulo) < 2:
            return "Error: Título inválido"
        if not autor or len(autor) < 3:
            return "Error: Autor inválido"
        if not isbn or len(isbn) < 10:
            return "Error: ISBN inválido"
        
        # Lógica de negocio
        libro = Libro(self.contador_libro, titulo, autor, isbn)
        self.libros.append(libro)
        self.contador_libro += 1
        
        # Persistencia
        self._guardar_en_archivo()
        
        return f"Libro '{titulo}' agregado exitosamente"
    
    # VIOLACIÓN OCP: Método cerrado a extensión
    def buscar_libro(self, criterio, valor):
        resultados = []
        
        if criterio == "titulo":
            for libro in self.libros:
                if valor.lower() in libro.titulo.lower():
                    resultados.append(libro)
        
        elif criterio == "autor":
            for libro in self.libros:
                if valor.lower() in libro.autor.lower():
                    resultados.append(libro)
        
        elif criterio == "isbn":
            for libro in self.libros:
                if libro.isbn == valor:
                    resultados.append(libro)
        
        elif criterio == "disponible":
            disponible = valor.lower() == "true"
            for libro in self.libros:
                if libro.disponible == disponible:
                    resultados.append(libro)
        
        return resultados
    
    # VIOLACIÓN SRP: Mezcla validación + lógica + persistencia
    def realizar_prestamo(self, libro_id, usuario):
        # Validación
        if not usuario or len(usuario) < 3:
            return "Error: Nombre de usuario inválido"
        
        # Buscar libro
        libro = None
        for l in self.libros:
            if l.id == libro_id:
                libro = l
                break
        
        if not libro:
            return "Error: Libro no encontrado"
        
        if not libro.disponible:
            return "Error: Libro no disponible"
        
        # Lógica de negocio
        from datetime import datetime
        prestamo = Prestamo(
            self.contador_prestamo,
            libro_id,
            usuario,
            datetime.now().strftime("%Y-%m-%d")
        )
        
        self.prestamos.append(prestamo)
        self.contador_prestamo += 1
        libro.disponible = False
        
        # Persistencia
        self._guardar_en_archivo()
        
        # Notificación
        self._enviar_notificacion(usuario, libro.titulo)
        
        return f"Préstamo realizado a {usuario}"
    
    def devolver_libro(self, prestamo_id):
        prestamo = None
        for p in self.prestamos:
            if p.id == prestamo_id:
                prestamo = p
                break
        
        if not prestamo:
            return "Error: Préstamo no encontrado"
        
        if prestamo.devuelto:
            return "Error: Libro ya devuelto"
        
        for libro in self.libros:
            if libro.id == prestamo.libro_id:
                libro.disponible = True
                break
        
        prestamo.devuelto = True
        self._guardar_en_archivo()
        
        return "Libro devuelto exitosamente"
    
    def obtener_todos_libros(self):
        return self.libros
    
    def obtener_libros_disponibles(self):
        return [libro for libro in self.libros if libro.disponible]
    
    def obtener_prestamos_activos(self):
        return [p for p in self.prestamos if not p.devuelto]
    
    # VIOLACIÓN SRP: Persistencia mezclada
    def _guardar_en_archivo(self):
        with open(self.archivo, 'w') as f:
            f.write(f"Libros: {len(self.libros)}\n")
            f.write(f"Préstamos: {len(self.prestamos)}\n")
    
    def _cargar_desde_archivo(self):
        try:
            with open(self.archivo, 'r') as f:
                data = f.read()
            return True
        except:
            return False
    
    # VIOLACIÓN SRP: Notificación es otra responsabilidad
    def _enviar_notificacion(self, usuario, libro):
        print(f"[NOTIFICACIÓN] {usuario}: Préstamo de '{libro}'")


# VIOLACIÓN DIP: Dependencia directa de implementación
def main():
    sistema = SistemaBiblioteca()
    
    print("=== AGREGANDO LIBROS ===")
    print(sistema.agregar_libro("Cien Años de Soledad", "Gabriel García Márquez", "9780060883287"))
    print(sistema.agregar_libro("El Principito", "Antoine de Saint-Exupéry", "9780156012195"))
    print(sistema.agregar_libro("1984", "George Orwell", "9780451524935"))
    
    print("\n=== BÚSQUEDA POR AUTOR ===")
    resultados = sistema.buscar_libro("autor", "Garcia")
    for libro in resultados:
        print(f"- {libro.titulo} por {libro.autor}")
    
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
