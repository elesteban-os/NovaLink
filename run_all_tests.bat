@echo off
setlocal enabledelayedexpansion

set "ROOT_DIR=%cd%"
set "EXIT_CODE=0"

echo Iniciando suite de pruebas de NovaLink...

for /d %%D in (services\*) do (
    set "HAS_TESTS=0"
    set "TEST_FOLDER="

    if exist "%%D\tests" (
        set "HAS_TESTS=1"
        set "TEST_FOLDER=tests"
    ) else if exist "%%D\test" (
        set "HAS_TESTS=1"
        set "TEST_FOLDER=test"
    )

    if "!HAS_TESTS!"=="1" (
        echo.
        echo ========================================
        echo [?] Ejecutando pruebas para: %%~nxD
        echo ========================================

        cd "%%D"

        set "PYTHONPATH=."
        python -m pytest "!TEST_FOLDER!"

        if errorlevel 1 (
            echo [X] ERROR: Las pruebas fallaron para %%~nxD
            set "EXIT_CODE=1"
        ) else (
            echo [OK] Todas las pruebas pasaron para %%~nxD
        )

        cd "%ROOT_DIR%"
    )
)

echo.
echo ========================================
if "!EXIT_CODE!"=="0" (
    echo [EXITO] Todas las pruebas en todos los microservicios han pasado.
) else (
    echo [FALLO] Hay pruebas fallidas. Revisa los logs de arriba.
)
echo ========================================

exit /b !EXIT_CODE!
