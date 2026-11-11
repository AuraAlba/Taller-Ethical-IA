# Model Card: Modelo de Evaluación de Riesgo / Selección

## 1. Detalles del Modelo
- **Desarrollador:** Aura Milena Alba Suarez
- **Versión del modelo:** 1.0.0 (Evaluación inicial de auditoría)
- **Tipo de modelo:** Clasificador binario de evaluación y selección
- **Licencia:** MIT

## 2. Uso Intencionado
- **Casos de uso principales:** Selección y evaluación de candidatos / solicitudes.
- **Usuarios intencionados:** Equipos de evaluación y tomadores de decisiones.
- **Casos de uso no intencionados:** Toma de decisiones 100% automatizada sin supervisión humana en contextos de alto impacto socioeconómico.

## 3. Datos de Evaluación
- **Dataset evaluado:** `data/model_predictions.csv`
- **Tamaño del dataset:** 24 registros en total (12 del grupo mayoritario, 12 del grupo minoritario)
- **Atributo protegido:** `protected_group` (0 = Grupo Mayoritario, 1 = Grupo Minoritario)

## 4. Métricas de Rendimiento Global
- **Accuracy global:** 62.5%

## 5. Auditoría de Equidad y Sesgo
- **Tasa de aceptación - Grupo Mayoritario (0):** 75.0%
- **Tasa de aceptación - Grupo Minoritario (1):** 25.0%
- **TPR (Recall) - Grupo Mayoritario (0):** 85.7%
- **TPR (Recall) - Grupo Minoritario (1):** 37.5%
- **FPR - Grupo Mayoritario (0):** 60.0%
- **FPR - Grupo Minoritario (1):** 0.0%

### Métricas Cuantitativas de Equidad
| Métrica | Valor Obtenido | Umbral de Aprobación | Estado |
| :--- | :---: | :---: | :---: |
| **Disparate Impact Ratio (DI)** | 0.333 | $\ge 0.80$ (Regla 4/5) | ❌ Violación |
| **Statistical Parity Difference (SPD)** | -0.500 | ideal 0.0 ($\pm 0.10$) | ❌ Brecha severa |
| **Equal Opportunity Difference (EOD)** | -0.482 | ideal 0.0 ($\pm 0.10$) | ❌ Brecha severa |

## 6. Conclusión de la Auditoría
🚨 **NO APTO PARA DESPLIEGUE EN PRODUCCIÓN** 🚨

El modelo presenta una **violación crítica de la regla de los cuatro quintos** con un Disparate Impact de **0.333** (muy por debajo del umbral mínimo tolerable de 0.80). Adicionalmente, presenta un marcado doble rasero reflejado en el EOD (-0.482) y en las tasas de falsos positivos (FPR del 60.0% para la mayoría frente a 0.0% para la minoría), rechazando injustamente al 62.5% de las personas verdaderamente calificadas del grupo minoritario.

**Acción requerida:** El modelo debe retornar a la fase de desarrollo para la aplicación de técnicas de mitigación de sesgos (como re-sopesado de datos o calibración de umbrales por grupo) antes de cualquier reevaluación para pase a producción.