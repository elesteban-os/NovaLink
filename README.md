# NovaLink

## Desarrollo local

Para habilitar el pre-commit local y ejecutar los hooks de análisis estático:

1. Instala dependencias de desarrollo:

```powershell
python -m pip install -r requirements-dev.txt
```

2. Instala el hook de Git:

```powershell
python -m pre_commit install
```

3. Ejecuta los checks manualmente:

```powershell
python -m pre_commit run --all-files
```

4. Después de instalarlo, `git commit` ejecutará automáticamente los hooks configurados.

## CI / GitHub Actions

El workflow de SAST está en `.github/workflows/sast.yml` y ejecuta:

- `black --check services/`
- `flake8 services/`

También puedes ejecutar el workflow manualmente desde la pestaña `Actions`.

## Archivos relevantes

- `.pre-commit-config.yaml`
- `requirements-dev.txt`
