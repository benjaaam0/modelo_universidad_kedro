from typing import Dict
from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline

from evaluacion2_universidad.pipelines import modelo_universidad

def register_pipelines() -> Dict[str, Pipeline]:
    """Register the project's pipelines."""
    
    # Aquí cargamos SOLO nuestra tubería
    pipeline_universidad = modelo_universidad.create_pipeline()

    return {
        "__default__": pipeline_universidad,
        "modelo_universidad": pipeline_universidad,
    }