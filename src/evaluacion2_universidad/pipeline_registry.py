"""Project pipelines."""
from typing import Dict
from kedro.pipeline import Pipeline

# Importamos las tuberías de tu proyecto
from evaluacion2_universidad.pipelines import modelo_universidad, reporting

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines."""
    
    # Traemos la tubería de tu modelo y la de reportes
    pipeline_modelo = modelo_universidad.create_pipeline()
    pipeline_reportes = reporting.create_pipeline()

    # Sumamos las dos para que se ejecuten juntas por defecto
    return {
        "__default__": pipeline_modelo + pipeline_reportes,
        "modelo_universidad": pipeline_modelo,
        "reporting": pipeline_reportes,
    }