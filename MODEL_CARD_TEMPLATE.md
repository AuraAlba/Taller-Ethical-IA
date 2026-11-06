# Model Card: [Nombre del Modelo / Sistema]

> Plantilla basada en _Model Cards for Model Reporting_ (Mitchell et al., 2019).
> Reemplaza todo el texto entre corchetes `[ ]` con información real.

## Model Details

- **Developed by:** [Tu Nombre / Equipo]
- **Model Date:** [Fecha de Creación]
- **Model Version:** v1.0.0
- **Model Type:** [Ej. Clasificador Binario / Random Forest]
- **License:** MIT
- **Contact:** [Correo o repositorio para reportar problemas]

## Intended Use

- **Primary Intended Uses:** [Para qué fue diseñado este modelo, ej. automatización inicial de filtrado de solicitudes].
- **Primary Intended Users:** [Quién operará el sistema, ej. analistas de riesgo].
- **Out-of-Scope Uses:** [Para qué NO debe usarse jamás, ej. decisiones judiciales, diagnósticos médicos definitivos o exclusión total sin supervisión humana].

## Training & Evaluation Data

- **Dataset Overview:** [Descripción breve del dataset utilizado para su validación: origen, tamaño, periodo].
- **Protected Attributes:** [Variables demográficas o sensibles consideradas en la auditoría, ej. `protected_group`].
- **Group Definition:** [Qué representa 0 (mayoritario) y 1 (minoritario) en este caso].

## Quantitative Performance & Fairness Audit

_Resultados obtenidos tras ejecutar `scripts/calculate_audit.py`:_

| Métrica                                    | Valor Obtenido | Umbral Objetivo |
| :----------------------------------------- | :------------- | :-------------- |
| **Accuracy Global**                        | _[Ej. 88%]_    | $> 85\%$        |
| **Tasa de Aprobación (Grupo Mayoritario)** | _[Ej. 75%]_    | -               |
| **Tasa de Aprobación (Grupo Minoritario)** | _[Ej. 32%]_    | -               |
| **TPR / Recall (Grupo Mayoritario)**       | _[Ej. 86%]_    | -               |
| **TPR / Recall (Grupo Minoritario)**       | _[Ej. 38%]_    | -               |
| **Disparate Impact Ratio (DI)**            | _[Ej. 0.42]_   | **$\ge 0.80$**  |

- **Resultado de la regla de los 4/5:** [ ] Aprobado [ ] Violación detectada
- **Conclusión de la Auditoría:** [¿El modelo pasa la prueba de equidad o debe volver a desarrollo para mitigación de sesgos? Justifica en 2 líneas].

## Ethical Considerations & Limitations

- **Known Biases:** [¿Qué sesgos históricos arrastra el dataset que afectaron al modelo?].
- **Limitations of this Audit:** [Ej. tamaño de muestra pequeño, un solo atributo protegido, sin análisis interseccional].
- **Mitigations Applied / Recommended:** [Medidas técnicas tomadas o recomendadas: re-muestreo, re-ponderación, ajuste de umbrales por grupo, supervisión humana, etc.].

## Sign-off

- **Auditor:** [Nombre]
- **Audit Date:** [Fecha]
- **Decision:** [ ] Aprobado para despliegue [ ] Devuelto a desarrollo
