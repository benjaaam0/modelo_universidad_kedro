import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

def crear_tabla_maestra(df_est: pd.DataFrame, df_insc: pd.DataFrame, df_cal: pd.DataFrame, df_asis: pd.DataFrame) -> pd.DataFrame:
    """Cruza los 4 CSV crudos y crea la tabla maestra."""
    # Limpiar notas
    df_cal['nota'] = pd.to_numeric(df_cal['nota'].astype(str).str.replace(',', '.'), errors='coerce')
    notas_prom = df_cal.groupby('id_inscripcion')['nota'].mean().reset_index().rename(columns={'nota': 'nota_final'})
    
    # Calcular asistencia
    asis_tot = df_asis.groupby('id_inscripcion').size().reset_index(name='total')
    ausentes = df_asis[df_asis['estado_asistencia'].str.lower().str.contains('ausente|injustificado', na=False)]
    asis_aus = ausentes.groupby('id_inscripcion').size().reset_index(name='faltas')
    asis_res = pd.merge(asis_tot, asis_aus, on='id_inscripcion', how='left').fillna(0)
    asis_res['porcentaje_asistencia'] = 100 - ((asis_res['faltas'] / asis_res['total']) * 100)
    
    # Unir todo
    df_master = pd.merge(df_insc, df_est, on='id_estudiante', how='left')
    df_master = pd.merge(df_master, notas_prom, on='id_inscripcion', how='left')
    df_master = pd.merge(df_master, asis_res[['id_inscripcion', 'porcentaje_asistencia']], on='id_inscripcion', how='left')
    
    # Variables limpias y Target
    df_master = df_master.dropna(subset=['porcentaje_asistencia', 'nota_final'])
    df_master['aprueba'] = np.where(df_master['nota_final'] >= 4.0, 1, 0)
    
    return df_master

def entrenar_modelo_optuna(df_master: pd.DataFrame, test_size: float, random_state: int):
    """Entrena el RandomForest inicial."""
    df_features = df_master[['porcentaje_asistencia', 'carrera', 'sede', 'aprueba']].dropna()
    
    X = pd.get_dummies(df_features[['porcentaje_asistencia', 'carrera', 'sede']], drop_first=True)
    y = df_features['aprueba']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    pipeline_final = Pipeline([
        ('scaler', StandardScaler()),
        ('clasificador', RandomForestClassifier(n_estimators=100, max_depth=5, class_weight='balanced', random_state=random_state))
    ])
    
    pipeline_final.fit(X_train, y_train)
    return pipeline_final