from kedro.pipeline import Pipeline, node
from .nodes import generar_reportes_y_clustering

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=generar_reportes_y_clustering,
            inputs=["modelo_random_forest", "tabla_maestra"],
            outputs="tabla_maestra_con_clusters",
            name="nodo_generar_reportes_finales"
        )
    ])