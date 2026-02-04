**Introducción y Dominio del Sistema**

Eventum Center se ha diseñado como una solución informática avanzada para la administración de centros de convenciones, donde la coordinación de espacios, equipos técnicos y personal especializado es crítica. El sistema actúa como un regulador lógico que impide errores operativos comunes, tales como el uso incompatible de tecnología en áreas no aptas.

El dominio gestionado abarca tres ejes fundamentales:
 -Eventos: Actividades de diversa índole (conferencias, grabaciones, talleres) que requieren una ventana temporal específica.
(No se permiten eventos de varios dias )

 - Recursos: Un inventario jerarquizado que incluye espacios físicos (Sala Central, Área Abierta), hardware (Sistemas de Sonido, Cámaras) y capital humano (Técnicos de Sonido, Moderadores).

 - Restricciones de Negocio: Un conjunto de reglas que definen la viabilidad de un evento basadas en la compatibilidad técnica y física de los recursos solicitados.


**Estructura y Justificación de Diseño**

Para garantizar la integridad del sistema, se ha optado por una arquitectura modular que separa la interfaz de usuario de la lógica de procesamiento. Esta estructura facilita la detección de errores y permite futuras actualizaciones sin comprometer el núcleo del programa.

Arquitectura de Archivos:
 -main.py: Funciona como el orquestador principal, gestionando el menú de usuario y derivando las peticiones a los módulos correspondientes.
 - planificador.py: Contiene el motor de cálculo del sistema. Aquí se procesan las colisiones de horario, la búsqueda automática de disponibilidad y la persistencia de datos en formato JSON.
 - recursos.py: Define el ecosistema de activos. Utiliza una estructura de diccionarios para establecer las capacidades y limitaciones de cada recurso.

 **Lógica Avanzada de Recursos**

El valor diferencial de Eventum Center reside en su motor de validación de recursos, el cual opera bajo dos principios de lógica relacional:

-Sistema de Co-requisitos (requiere)
Se implementó una lógica de dependencia para asegurar que ningún equipo técnico sea subutilizado o asignado sin las condiciones necesarias para su funcionamiento. Por ejemplo:
 1. La Cámara de Grabación requiere obligatoriamente de la Sala Central y un Sistema de Sonido.
 2. El Técnico de Sonido no puede ser asignado si no existe un Sistema de Sonido reservado previamente.

-Sistema de Exclusión Mutua (excluye)
Esta funcionalidad previene conflictos espaciales o técnicos insalvables. Se han configurado reglas de exclusión para garantizar la calidad operativa:
 1. Exclusión Espacial: La Sala Central, la Sala Pequeña y el Área Abierta son mutuamente excluyentes entre sí para evitar la duplicidad de reservas en un mismo espacio geográfico.

 2. Incompatibilidad Técnica: El Proyector tiene una restricción de uso en el Área Abierta, previendo problemas de visibilidad por luz ambiental o falta de infraestructura de proyección en exteriores.

**Desafíos y Soluciones de Ingeniería**

Durante el ciclo de desarrollo, se identificaron y resolvieron puntos críticos de fallo para asegurar la robustez del software:
 - Detección de Colisiones Multidía: La comparación inicial de horas resultaba insuficiente para eventos que atravesaban la medianoche (madrugada). Se implementó una lógica que detecta cuando la hora_fin es menor o igual a la hora_inicio, calculando automáticamente un salto de fecha para el cierre del evento y validando la disponibilidad en ambos días.
 - Buscador Automático de Disponibilidad: Ante un choque de horarios, se desarrolló una función iterativa que analiza los próximos dos días en intervalos de 30 minutos. Este algoritmo filtra los resultados para sugerir espacios únicamente dentro del horario laboral establecido (07:00 a 22:00), optimizando la respuesta al usuario.

 -Integridad de la Persistencia: Se enfrentó el riesgo de corrupción de datos al leer el archivo data.json. Se implementaron manejadores de excepciones (JSONDecodeError y FileNotFoundError) para asegurar que el programa inicie de manera segura incluso si el archivo de datos falta o está dañado.


**Operación y Ejecución**

Para operar el sistema, se deben seguir estos pasos:
 - Ejecutar el comando python main.py desde la consola.
 - El sistema cargará automáticamente los registros existentes desde data.json.
 - A través de menús numéricos, se pueden realizar las operaciones de gestión. Cada acción (creación o edición) desencadena una serie de verificaciones automáticas de disponibilidad y compatibilidad de recursos.

**Conclusiones**
Se ha logrado un sistema que no solo registra información, sino que aplica inteligencia de negocio para prevenir fallos logísticos. La rigurosidad en la validación de dependencias de recursos y la gestión avanzada del tiempo posicionan a Eventum Center como una herramienta de alta fiabilidad para la administración profesional de centros de convenciones.
