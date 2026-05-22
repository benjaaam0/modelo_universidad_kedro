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

## Configuración y Ejecución
Este proyecto utiliza `uv` para la gestión de dependencias.

1. **Instalación:**
   Asegúrate de tener instalado `uv` y luego sincroniza las dependencias:
   ```bash
   uv sync
