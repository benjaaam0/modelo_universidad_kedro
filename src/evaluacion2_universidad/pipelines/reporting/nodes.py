import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
import json

def generar_reportes_y_clustering(modelo, df_master: pd.DataFrame):
    df_features = df_master[['porcentaje_asistencia', 'carrera', 'sede', 'aprueba']].dropna()
    X = pd.get_dummies(df_features[['porcentaje_asistencia', 'carrera', 'sede']], drop_first=True)
    y_test = df_features['aprueba']
    
    y_pred = modelo.predict(X)
    
    # Métricas
    reporte = classification_report(y_test, y_pred, output_dict=True)
    reporte['accuracy'] = accuracy_score(y_test, y_pred)
    
    with open("data/08_reporting/metricas_clasificacion.json", "w") as f:
        json.dump(reporte, f)
        
    # Gráficos
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.savefig("data/08_reporting/matriz_confusion.png")
    
    return df_master