from kedro.pipeline import Pipeline, node, pipeline
from .nodes import crear_tabla_maestra, entrenar_modelo_optuna

def create_pipeline(**kwargs) -> Pipeline:
    return pipeline([
        node(
            func=crear_tabla_maestra,
            inputs=["estudiantes", "inscripciones", "calificaciones", "asistencia"],
            outputs="tabla_maestra",
            name="nodo_crear_tabla_maestra"
        ),
        node(
            func=entrenar_modelo_optuna,
            # Fíjate que aquí quitamos los parámetros estáticos, Optuna hace el trabajo ahora
            inputs=["tabla_maestra", "params:test_size", "params:random_state"],
            outputs="modelo_random_forest",
            name="nodo_entrenar_modelo_optuna"
        )
    ])