# 📝 EXAMEN: Principios SOLID - Sistema de Biblioteca

## ⏱️ DURACIÓN: 2 HORAS
## ⏱️ REPOSITORIO: Subir a Github

### Distribución de Tiempo Sugerida:
- ⏰ **0:00 - 0:10**: Lectura y setup (10 min)
- ⏰ **0:10 - 0:35**: Ejercicio 1 - OCP (25 min)
- ⏰ **0:35 - 1:15**: Ejercicio 2 - SRP (40 min)
- ⏰ **1:15 - 1:50**: Ejercicio 3 - DIP (35 min)
- ⏰ **1:50 - 2:00**: Revisión y entrega (10 min)

---

## 📋 INSTRUCCIONES GENERALES

### ✅ Qué DEBES hacer:
1. Leer completamente este documento
2. Verificar que el código base funciona
3. Crear archivos nuevos para tus refactorizaciones
4. Mantener la funcionalidad original
5. Comentar tus cambios
6. Entregar todos los archivos Python

### ❌ Qué NO debes hacer:
1. Modificar biblioteca_examen.py original
2. Agregar funcionalidades nuevas
3. Usar librerías externas
4. Copiar código

---

## 📊 EVALUACIÓN (100 puntos)

| Ejercicio | Principio | Puntos | Tiempo |
|-----------|-----------|--------|--------|
| Ejercicio 1 | OCP | 30 | 25 min |
| Ejercicio 2 | SRP | 30 | 40 min |
| Ejercicio 3 | DIP | 30 | 35 min |
| Teórico | LSP + ISP | 10 | 20 min |
| **TOTAL** | | **100** | **120 min** |

---

## 🟢 EJERCICIO 1: Open/Closed Principle (30 pts - 25 min)

### Problema:
El método `buscar_libro()` viola OCP con múltiples.

### Tu Tarea:
1. Crea clase abstracta para generar una estrategia de búsqueda
2. Implementa 3 estrategias de busqueda
3. Refactoriza el método para usar estrategias
4. Agrega BusquedaPorDisponibilidad SIN modificar código existente

### Entregable:
- Clase abstracta + 4 estrategias
- Método refactorizado
- Documentación demostrando uso (como probar que funciona)

---

## 🟡 EJERCICIO 2: Single Responsibility Principle (30 pts - 40 min)

### Problema:
`SistemaBiblioteca` tiene múltiples responsabilidades.

### Tu Tarea:
1. Crea `ValidadorBiblioteca` (solo validación)
2. Crea `RepositorioBiblioteca` (solo persistencia)
3. Crea `ServicioNotificaciones` (solo notificaciones)
4. Refactoriza `SistemaBiblioteca` para usar estas clases

### Entregable:
- 3 clases separadas
- SistemaBiblioteca refactorizada
- main() funcionando
- Documentación demostrando uso (como probar que funciona)

---

## 🔴 EJERCICIO 3: Dependency Inversion Principle (30 pts - 35 min)

### Problema:
Dependencia directa de implementaciones concretas.

### Tu Tarea:
1. Crea interfaz para el repositorio (clase abstracta)
2. Implementa `RepositorioArchivo`
3. Refactoriza `SistemaBiblioteca` con inyección de dependencias
4. Refactoriza main() con configuración de dependencias
5. BONUS: Crea `RepositorioMemoria`

### Entregable:
- Interfaz IRepositorio
- RepositorioArchivo
- Inyección de dependencias
- main() con DI

---

## 📝 PREGUNTAS TEÓRICAS (10 puntos)

### Pregunta 1: LSP (5 pts)

**a) (5 pts)** Explica qué es LSP y cómo se aplica al ejemplo:

```python
class Usuario:
    def calcular_limite_prestamos(self):
        return 3

class Estudiante(Usuario):
    def calcular_limite_prestamos(self):
        return 3
```

**Respuesta:**
```
_________________________________________________________________
LSP es cuando una subclase sustituye a su clase base sin necesidad de que se altere el comportamiento del programa. En el ejemplo, la clase Estudiante sobrescribe el método "calcular_limite_prestamos" pero sigue devolviendo el mismo valor que su clase base Usuario.
_________________________________________________________________
```

**b) (5 pts)** Da un ejemplo que VIOLE LSP y explica por qué:

```python
# Tu código aquí
class Usuario:
    def calcular_limite_prestamos(self):
        return 3
class Profesor(Usuario):
    def calcular_limite_prestamos(self):
        return "Son limite"


# Explicación:
_________________________________________________________________
```
Esta implemetación viola LSP ya que la clase Profesor devuelve un tipo diferente al de su clase base Usuario. 
---

### Pregunta 2: ISP (5 pts)

**a) (5 pts)** ¿Por qué esta interfaz VIOLA ISP?

```python
class IGestionBiblioteca:
    def agregar_libro(self): pass
    def buscar_libro(self): pass
    def realizar_prestamo(self): pass
    def generar_reporte(self): pass
    def hacer_backup(self): pass
```

**Respuesta:**
```
_________________________________________________________________
La interfaz IGestionBiblioteca viola ISP porque obliga a que cualquier clase que la implemente tenga que definir todos esos métodos y hay veces en donde estas clases no las va a necesitar.
_________________________________________________________________
```

**b) (5 pts)** Propón cómo segregar esta interfaz:

```
Interface 1: IAdministrarLibros - Métodos: agregar_libro(), buscar_libro()

Interface 2: IPrestamos - Métodos: realizar_prestamo()

Interface 3: IReportes - Métodos: generar_reporte(), hacer_backup()
```

---

## 📦 ENTREGA

### Archivos a entregar:
1. Repositorio en GIT
2. Respuestas del examen teorico en un folder aparte on en el README principal
3. Puedes separar los archivos de cada ejercicio en carpetas si así lo deseas
4.PAra puntos extra, puedes generar los archivos de clase y ponerlos en la carpeta llamada "templates"
4. Considera el checklist de abajo como una Guia de entrega

### Checklist:
- [ ] Todos los archivos ejecutan sin errores
- [ ] Funcionalidad original mantenida
- [ ] Código comentado
- [ ] Preguntas respondidas
- [ ] Nombre en primera página

---

## 💡 CONSEJOS

1. Administra tu tiempo
2. Prueba tu código
3. Comenta tus decisiones
4. Si te atoras, pasa al siguiente

---

**¡MUCHO ÉXITO! 🚀**

