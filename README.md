# Evaluación 2: Modelado Predictivo de Rendimiento Académico

## Resumen Ejecutivo
Este proyecto tiene como objetivo desarrollar un sistema de análisis predictivo para identificar el riesgo de reprobación académica en estudiantes del DuocUC, sede Puerto Montt. Utilizando una arquitectura basada en **Kedro**, el sistema integra, limpia y procesa datos de cuatro fuentes distintas (registros estudiantiles, inscripciones, calificaciones y asistencia) para generar una tabla maestra unificada.

El modelo implementado permite:
1. **Predecir el éxito académico:** Segmentar perfiles estudiantiles y estimar la probabilidad de aprobación.
2. **Identificar patrones (Clustering):** Detectar comportamientos atípicos en la asistencia, actuando como un sistema de alerta temprana.
3. **Automatización:** Ejecutar flujos de trabajo de datos reproducibles y escalables.

## Estructura del Proyecto
El proyecto sigue la estructura estándar de Kedro:
* `src/evaluacion2_universidad/`: Contiene la lógica del pipeline.
    * `pipelines/modelo_universidad/`: Lógica de creación de tabla maestra y entrenamiento con Optuna.
    * `pipelines/reporting/`: Generación de métricas, matrices de confusión y análisis de clusters.
* `data/`: Almacena los datasets crudos y los resultados procesados (reportes, métricas y modelos serializados).
* `conf/`: Configuraciones del proyecto y logs.

## Metodología
Para asegurar la calidad y la rigurosidad científica, hemos aplicado:
* **Optimización de Hiperparámetros:** Uso de `Optuna` para automatizar la búsqueda de los mejores parámetros para el modelo de `Random Forest`.
* **Manejo de Desbalance:** Implementación de técnicas de balanceo (clases pesadas) para mitigar el sesgo hacia la clase mayoritaria.
* **Análisis Crítico:** Los resultados (55% de exactitud) han sido analizados bajo un enfoque de ingeniería, concluyendo que el rendimiento académico es un fenómeno multifactorial que requiere futuras iteraciones con variables sociodemográficas e históricas para aumentar su capacidad predictiva.

## Justificación Técnica del Rendimiento (55% de Accuracy)
El modelo actual alcanzó una exactitud (*accuracy*) del 55% utilizando el algoritmo de Random Forest. Desde una perspectiva de ingeniería de datos, este resultado no representa un fallo en el sistema, sino un diagnóstico realista basado en las fuentes de información disponibles. 

Las razones principales por las cuales el rendimiento se encuentra en este rango son:
1. **Naturaleza Multifactorial del Éxito Académico:** El dataset actual incluye registros de asistencia, calificaciones e inscripciones. Si bien estos datos son fundamentales, omiten variables críticas que impactan directamente el rendimiento de un estudiante, tales como la situación socioeconómica, el entorno familiar, la salud mental, la conectividad o el tiempo de traslado a la sede.
2. **Ausencia de Historial a Largo Plazo:** Al no contar con un histórico académico de semestres anteriores de los mismos alumnos, el modelo no puede identificar tendencias previas de comportamiento o patrones de aprendizaje rezagados.
3. **Desbalance de Clases:** Existe una disparidad natural entre la cantidad de alumnos que aprueban y los que están en riesgo de reprobación. Este desbalance introduce un sesgo que afecta la capacidad de generalización del algoritmo en métricas globales.

### Valor de la Línea Base (Baseline)
Este 55% constituye nuestra **línea base** de experimentación. El valor principal de este proyecto no radica exclusivamente en el porcentaje actual, sino en la **arquitectura modular (Kedro)** construida. El pipeline está completamente estructurado, automatizado y desacoplado, lo que significa que el sistema está listo para absorber nuevas variables (como encuestas socioeconómicas o datos históricos) en el futuro, permitiendo incrementar la precisión del modelo sin necesidad de reescribir la infraestructura de software.

## Configuración y Ejecución
Este proyecto utiliza `uv` para la gestión de dependencias.

1. **Instalación:**
   Asegúrate de tener instalado `uv` y luego sincroniza las dependencias:
   ```bash
   uv sync
