# Taller 3 Práctico: Caso de Estudio "Reserva de un Viaje"

## Intergrantes
- Jhon Munarco
- Shirley Otuna
- Cristopher Zambrano

Este repositorio contiene el código fuente desarrollado durante el taller práctico sobre el caso de estudio "Reserva de un Viaje".  El objetivo principal del taller es comprender la importancia de integrar pruebas unitarias y prácticas de desarrollo seguro desde las primeras etapas del desarrollo de software.

## 1. Introducción

En este taller, se aborda la importancia de integrar pruebas unitarias desde las primeras etapas del desarrollo, combinando prácticas de desarrollo seguro. A través del caso de estudio “Reserva de un viaje”, aprenderemos a:

*   Implementar funcionalidades del backend (búsqueda, reserva, cancelación, etc.).
*   Identificar y cumplir con requisitos funcionales y de seguridad.
*   Diseñar y ejecutar pruebas unitarias que validen el correcto funcionamiento y la seguridad de cada función.

## 2. Objetivos

*   Comprender la relevancia de las pruebas unitarias en el ciclo de desarrollo seguro de software.
*   Desarrollar funciones backend para un sistema de reserva de viajes, cumpliendo con requisitos funcionales y de seguridad.
*   Implementar pruebas unitarias para cada función, describiendo detalladamente su propósito, herramientas, criterios de aceptación y umbral de aprobación.
*   Evaluar los resultados de las pruebas unitarias, alcanzando un mínimo del 90% de éxito en cada ejecución.

## 3. Metodología

*   **Desarrollo iterativo:** Se implementará el backend de forma modular, integrando pruebas unitarias para cada módulo o función.
*   **Enfoque práctico:** Cada sección incluirá ejemplos de código, ejercicios y análisis de resultados.
*   **Uso de herramientas:** Los estudiantes seleccionarán las herramientas de su preferencia para el desarrollo de pruebas.
*   **Documentación y retroalimentación:** Los estudiantes deberán documentar el proceso, los criterios de aceptación de cada prueba y discutir los resultados obtenidos.

## 4. Descripción del Caso de Estudio: "Reserva de un Viaje"

### 4.1. Contexto del caso de estudio

En la era digital actual, la industria del turismo se ha transformado con el auge de las plataformas en línea que permiten a los usuarios buscar, comparar y reservar viajes de forma rápida y segura. La compañía "Viajes Seguros S.A." busca ofrecer una experiencia integral a sus clientes mediante una PWA robusta y segura que gestione:

*   La búsqueda de viajes basándose en criterios como fechas, destinos y presupuestos.
*   La reserva de viajes, donde se verifique la disponibilidad, gestione la información del usuario e integre un sistema de pago confiable.
*   La cancelación de reservas, considerando políticas de reembolso y condiciones específicas.
*   La comunicación y notificación de los estados de reserva y cancelación mediante correos electrónicos o mensajes en la plataforma.

Este sistema debe cumplir estrictamente con las medidas de seguridad, tales como la autenticación de usuarios, encriptación de datos sensibles, validación de entradas y registro de actividades, para garantizar la integridad y confidencialidad de la información. El presente taller se enfoca en implementar y probar estas funcionalidades, integrando desde el inicio los conceptos de desarrollo seguro de software.

### 4.2. Requisitos Funcionales Específicos

*   **RF1: Búsqueda de viajes:** El sistema debe permitir a los usuarios buscar viajes disponibles según criterios como fecha, destino y precio.
*   **RF2: Reserva de un viaje:** Una vez seleccionado el viaje, el usuario podrá reservarlo. La función debe verificar la disponibilidad y registrar la reserva.
*   **RF3: Cancelación de reserva:** El sistema debe permitir la cancelación de una reserva, aplicando condiciones para posibles reembolsos según la política de cancelación.
*   **RF4: Confirmación y notificación:** Tras la reserva o cancelación, se generará un comprobante de la operación, que podrá enviarse al correo electrónico del usuario.
*   **RF5: Integración con sistema de pagos:** El proceso de reserva debe incluir la verificación y procesamiento de pagos de manera segura.

### 4.3. Requisitos de Seguridad

*   **RS1: Autenticación y autorización:** Solo usuarios autenticados podrán realizar operaciones sensibles (reservar o cancelar viajes).
*   **RS2: Encriptación de datos sensibles:** Información personal y de pago debe ser encriptada tanto en tránsito (usando https) como en reposo.
*   **RS3: Validación de entradas:** Se implementarán controles para evitar inyección de código, ataques XSS/SQL y otros vectores de ataque.
*   **RS4: Registro de actividades (logging):** Todas las transacciones y actividades críticas serán registradas para facilitar auditorías y detectar comportamientos anómalos.
*   **RS5: Gestión de errores y excepciones:** Se manejarán adecuadamente las excepciones, evitando la exposición de información sensible en mensajes de error.

### 4.4. Plan de Pruebas Unitarias

Para cada función del backend se debe diseñar una prueba unitaria que incluya:

*   **Descripción detallada:** Explicación de la funcionalidad a testear y el propósito de la prueba.
*   **Herramientas utilizadas:** Describir la herramienta utilizada, por ejemplo, pytest para python.
*   **Criterios de aceptación:** Definir los resultados esperados. Por ejemplo, que una función retorne un hash map con una clave "status" igual a "ok" y que incluya un identificador numérico.
*   **Umbral mínimo de aprobación:** Se considera que una prueba está aprobada cuando al menos el 90% de sus ejecuciones son exitosas.

