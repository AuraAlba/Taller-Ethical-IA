# Taller: Auditoría de Sesgo y Documentación de Modelos de IA

[![Fairness Audit CI](../../actions/workflows/fairness-audit.yml/badge.svg)](../../actions/workflows/fairness-audit.yml)

Taller práctico de 30 minutos para estudiantes de ingeniería y software.
**No se entrena ningún modelo**: se audita uno ya existente a partir de sus predicciones.

## 🎯 Objetivo

Al finalizar el taller, el estudiante será capaz de:

1. Calcular métricas de equidad (**Disparate Impact**, **Statistical Parity Difference**, **Equal Opportunity Difference**) a partir de un CSV de predicciones.
2. Aplicar la **regla de los cuatro quintos** (DI ≥ 0.80) como criterio de aprobación.
3. Integrar la auditoría como un **quality gate en CI/CD** (GitHub Actions).
4. Documentar los hallazgos en una **Model Card**.

## 📁 Estructura

```
├── .github/workflows/fairness-audit.yml   # CI
├── data/model_predictions.csv             # Dataset a auditar (sesgado a propósito)
├── scripts/calculate_audit.py             # Script de auditoría
├── tests/                                 # Tests del script + datasets de referencia
├── MODEL_CARD_TEMPLATE.md                 # Plantilla a completar
└── docs/img/                              # Capturas de CI
```

## ⚙️ Instalación

Requiere Python 3.9+.

```bash
git clone <URL-DE-TU-REPO>
cd bias-audit-workshop

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements-dev.txt
```

## ▶️ Ejecución

```bash
python scripts/calculate_audit.py                       # audita data/model_predictions.csv
python scripts/calculate_audit.py --data <otro.csv>     # audita otro archivo
pytest -v                                               # tests del script
echo $?                                                 # 0 = aprueba, 1 = viola la regla 4/5
```

## 🤖 Integración continua (CI)

El workflow tiene **dos jobs con propósitos distintos**:

| Job             | Qué verifica                                                                                             | Resultado esperado                 |
| --------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `unit-tests`    | Que **el script** calcula bien (DI, SPD, EOD, códigos de salida) con datasets fijos en `tests/fixtures/` | ✅ Siempre verde                   |
| `fairness-gate` | Que **el modelo** en `data/model_predictions.csv` cumple DI ≥ 0.80                                       | ❌ Rojo al inicio, ✅ tras mitigar |

> **¿Por qué hay un check en rojo?** El script no está roto: está funcionando.
> Detecta que el _modelo_ es sesgado y devuelve `exit 1`, lo que hace fallar el job.
> Es exactamente el comportamiento deseado en MLOps: un modelo discriminatorio no pasa a producción.

### Flujo del taller (rojo → verde)

1. Haz push con el dataset original → `fairness-gate` ❌ (evidencia 1).
2. Aplica una mitigación. Para la demo, simúlala así:
   ```bash
   cp tests/fixtures/fair_predictions.csv data/model_predictions.csv
   ```
3. Haz push de nuevo → ambos jobs ✅ (evidencia 2).

### 📸 Evidencias de CI

> Los estudiantes deben capturar sus propias pantallas desde la pestaña **Actions** de su repo
> y guardarlas en `docs/img/`.

| #   | Captura                                  | Archivo                        | Qué debe verse                                                    |
| --- | ---------------------------------------- | ------------------------------ | ----------------------------------------------------------------- |
| 1   | Compuerta en rojo con el dataset sesgado | `docs/img/ci-1-gate-rojo.png`  | `unit-tests` ✅ y `fairness-gate` ❌                              |
| 2   | Log del job fallido                      | `docs/img/ci-2-log-alerta.png` | Mensaje "VIOLACIÓN DE LA REGLA DE LOS CUATRO QUINTOS", DI = 0.333 |
| 3   | Compuerta en verde tras mitigar          | `docs/img/ci-3-gate-verde.png` | Ambos jobs ✅                                                     |
| 4   | Pestaña _Summary_                        | `docs/img/ci-4-summary.png`    | Tabla con DI, SPD, EOD                                            |

![CI en rojo](docs/img/ci-1-gate-rojo.png)
![Log de alerta](docs/img/ci-2-log-alerta.png)
![CI en verde](docs/img/ci-3-gate-verde.png)
![Resumen](docs/img/ci-4-summary.png)

---

## 🧠 Reflexión

### Salida en consola (dataset sesgado: `data/model_predictions.csv`)

```
Registros cargados: 24

Accuracy global: 62.5%
Tasa de aceptación - Grupo mayoritario (0): 75.0%
Tasa de aceptación - Grupo minoritario (1): 25.0%

Matriz de confusión - Grupo Mayoritario (0):
   TN=2  FP=3  FN=1  TP=6
   TPR (Recall) = 85.7%   FPR = 60.0%

Matriz de confusión - Grupo Minoritario (1):
   TN=4  FP=0  FN=5  TP=3
   TPR (Recall) = 37.5%   FPR = 0.0%

--- Métricas de equidad ---
Disparate Impact Ratio (DI):          0.333
Statistical Parity Difference (SPD):  -0.500
Equal Opportunity Difference (EOD):   -0.482
(!) Brecha mayor a 0.10 en SPD y/o EOD: revisar. ...

============================================================
🚨 ALERTA: VIOLACIÓN DE LA REGLA DE LOS CUATRO QUINTOS 🚨
   DI = 0.333  <  umbral = 0.80
   El modelo presenta IMPACTO DISPAR contra el grupo minoritario.
   Acción: devolver a desarrollo para mitigación de sesgos.
============================================================
```

### Salida tras la mitigación simulada (`tests/fixtures/fair_predictions.csv`)

```
Accuracy global: 75.0%
Tasa de aceptación - Grupo mayoritario (0): 75.0%
Tasa de aceptación - Grupo minoritario (1): 66.7%
   Grupo 0: TN=2 FP=3 FN=1 TP=6   TPR=85.7%  FPR=60.0%
   Grupo 1: TN=3 FP=1 FN=1 TP=7   TPR=87.5%  FPR=25.0%
DI = 0.889   SPD = -0.083   EOD = +0.018
✅ APROBADO: el modelo cumple la regla de los cuatro quintos.
```

### Cálculos

| Métrica          | Fórmula             | Cálculo       | Resultado  |
| ---------------- | ------------------- | ------------- | ---------- |
| **DI**           | rate_min / rate_maj | 0.25 / 0.75   | **0.333**  |
| **SPD** (TODO 2) | rate_min − rate_maj | 0.25 − 0.75   | **−0.500** |
| **EOD** (TODO 1) | TPR_min − TPR_maj   | 0.375 − 0.857 | **−0.482** |

### ¿Coincide la EOD con la conclusión del DI?

**Sí.** Las tres métricas señalan en la misma dirección: el Grupo 1 sale perjudicado.
Aun así, miden cosas distintas:

- **DI y SPD** miran solo _cuántos_ son aceptados, sin considerar si merecían serlo.
- **EOD** compara a las personas _realmente calificadas_ (`true_label = 1`) de cada grupo.

Que coincidan aquí refuerza la conclusión, pero no siempre ocurre.

### ¿Qué podemos inferir?

1. **La brecha no se explica por mérito.** El 66.7% del Grupo 1 está realmente calificado (8/12), frente al 58.3% del Grupo 0 (7/12). El grupo con _más_ personas calificadas es el que menos se acepta.
2. **El modelo rechaza talento.** De 8 personas calificadas del Grupo 1, 5 fueron rechazadas (FN). Es un daño directo, no solo una diferencia estadística.
3. **Estándares asimétricos.** El FPR del Grupo 0 es 60% y el del Grupo 1 es 0%. El modelo es permisivo con el mayoritario (acepta a 3 no calificados) y excesivamente estricto con el minoritario. Esto también viola _equalized odds_.
4. **El accuracy global (62.5%) esconde el problema.** Por sí solo no revela la inequidad: hay que desagregar por grupo.
5. **Cautela:** con 12 registros por grupo, cambiar una sola predicción mueve la tasa 8.3 puntos porcentuales. Los datos son simulados y con fines didácticos; en un caso real se requiere mayor muestra e intervalos de confianza.

### Conclusión: auditoría vs. Model Cards

Los valores de ejemplo de la plantilla (entre corchetes) frente a lo que arrojó la auditoría:

| Métrica                          | Ejemplo en la plantilla | Obtenido en la auditoría | Observación                             |
| -------------------------------- | ----------------------- | ------------------------ | --------------------------------------- |
| Accuracy global                  | 88%                     | **62.5%**                | No cumple el umbral > 85%               |
| Tasa de aprobación (mayoritario) | 75%                     | **75.0%**                | Coincide                                |
| Tasa de aprobación (minoritario) | 32%                     | **25.0%**                | La brecha real es mayor a la supuesta   |
| TPR (mayoritario)                | 86%                     | **85.7%**                | Coincide                                |
| TPR (minoritario)                | 38%                     | **37.5%**                | Coincide                                |
| Disparate Impact                 | 0.42                    | **0.333**                | Violación más severa que la del ejemplo |

Los ejemplos de la plantilla eran **hipótesis optimistas**. Al ejecutar el script, el modelo resultó peor en accuracy (62.5% vs. 88%) y en equidad (DI 0.333 vs. 0.42). Esto demuestra por qué una Model Card no debe llenarse con valores estimados: **debe completarse con la salida real de la auditoría**, y su conclusión debe ser coherente con ella.

**Decisión documentada:** el modelo original **no es apto para despliegue** y vuelve a desarrollo.
Mitigaciones recomendadas: re-ponderación de muestras, ajuste de umbrales por grupo, revisión de variables proxy y supervisión humana para los rechazos.

> ✍️ **Tu turno:** completa `MODEL_CARD_TEMPLATE.md` con tus resultados y verifica que
> tu "Conclusión de la Auditoría" sea consistente con el DI, SPD y EOD obtenidos.

## 📦 Entregables

- [ ] `MODEL_CARD_TEMPLATE.md` completada con los valores reales
- [ ] Capturas de CI en `docs/img/` (rojo y verde)
- [ ] Respuestas de la sección Reflexión
