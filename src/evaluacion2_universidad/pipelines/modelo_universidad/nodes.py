import pandas as pd
import numpy as np
import optuna
from sklearn.model_selection import train_test_split, cross_val_score
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
    """Usa Optuna para encontrar los mejores parámetros y entrena el RandomForest."""
    df_features = df_master[['porcentaje_asistencia', 'carrera', 'sede', 'aprueba']].dropna()
    
    # One-Hot Encoding
    X = pd.get_dummies(df_features[['porcentaje_asistencia', 'carrera', 'sede']], drop_first=True)
    y = df_features['aprueba']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state, stratify=y)
    
    # --- LA MAGIA DE OPTUNA ---
    def objective(trial):
        # Que la IA pruebe distintas profundidades y cantidades de árboles
        rf_max_depth = trial.suggest_int('max_depth', 2, 10)
        rf_n_estimators = trial.suggest_categorical('n_estimators', [50, 100, 150])
        
        pipeline_tmp = Pipeline([
            ('scaler', StandardScaler()),
            ('clasificador', RandomForestClassifier(max_depth=rf_max_depth, n_estimators=rf_n_estimators, class_weight='balanced', random_state=random_state))
        ])
        # Probamos el modelo rápido
        score = cross_val_score(pipeline_tmp, X_train, y_train, n_jobs=-1, cv=3, scoring='accuracy')
        return score.mean()

    # Optuna busca la combinación ganadora (solo 10 intentos para ser rápidos)
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials=10)
    best_params = study.best_params
    
    import logging
    log = logging.getLogger(__name__)
    log.info(f"✅ Optuna encontró los mejores parámetros: {best_params}")

    # --- ENTRENAMOS EL MODEL FINAL ---
    pipeline_final = Pipeline([
        ('scaler', StandardScaler()),
        ('clasificador', RandomForestClassifier(
            max_depth=best_params['max_depth'], 
            n_estimators=best_params['n_estimators'], 
            class_weight='balanced', 
            random_state=random_state))
    ])
    
    pipeline_final.fit(X_train, y_train)
    return pipeline_final