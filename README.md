# Agrivoltaica ganadera asturiana

Calculadora accesible de fotovoltaica con doble uso del suelo (pasto + placa) para la Asturias rural. Proyecto para la convocatoria de innovación de la Fundación Caja Rural de Asturias.

Ver `PROJECT.md` y `docs/2026-06-27-design-spec.md`.

## Uso

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements-dev.txt
.venv/bin/streamlit run streamlit_app.py   # app
.venv/bin/python -m pytest -q                # tests
```
