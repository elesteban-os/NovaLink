@echo off
setlocal enabledelayedexpansion

set "ROOT_DIR=%cd%"
set "EXIT_CODE=0"

rem Detectar el comando de Python disponible
set "PYTHON_CMD="
where py >nul 2>&1
if not errorlevel 1 (
    py -3.11 --version >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=py -3.11"
    ) else (
        py -3.12 --version >nul 2>&1
        if not errorlevel 1 (
            set "PYTHON_CMD=py -3.12"
        ) else (
            set "PYTHON_CMD=py -3"
        )
    )
) else (
    where python >nul 2>&1
    if not errorlevel 1 (
        set "PYTHON_CMD=python"
    )
)

if "%PYTHON_CMD%"=="" (
    echo ERROR: No se encontr? Python en el PATH. Instala Python 3.
    exit /b 1
)

echo Iniciando suite de pruebas de NovaLink...
%PYTHON_CMD% --version

echo.
for /d %%D in (services\*) do (
    set "HAS_TESTS=0"
    set "TEST_FOLDER="

    if exist "%%D\tests\*" (
        set "HAS_TESTS=1"
        set "TEST_FOLDER=tests"
    ) else if exist "%%D\test\*" (
        set "HAS_TESTS=1"
        set "TEST_FOLDER=test"
    )

    if "!HAS_TESTS!"=="1" (
        call :run_service "%%D"
    )
)

echo.
echo ========================================
if "%EXIT_CODE%"=="0" (
    echo [EXITO] Todas las pruebas en todos los microservicios han pasado.
) else (
    echo [FALLO] Hay pruebas fallidas. Revisa los logs de arriba.
)
echo ========================================
exit /b %EXIT_CODE%

:run_service
set "SERVICE_DIR=%~1"
for %%F in ("%SERVICE_DIR%") do set "SERVICE_NAME=%%~nxF"
set "TEST_FOLDER=tests"
if exist "%SERVICE_DIR%\test\*" set "TEST_FOLDER=test"

cd /d "%SERVICE_DIR%"
echo.
echo ========================================
echo [?] Ejecutando pruebas para: %SERVICE_NAME%
echo ========================================

echo Comprobando entorno virtual en %SERVICE_NAME%...
if not exist ".venv\Scripts\python.exe" (
    echo Creando entorno virtual .venv para %SERVICE_NAME%...
    %PYTHON_CMD% -m venv .venv
    if errorlevel 1 (
        echo [X] ERROR: No se pudo crear el entorno virtual en %SERVICE_NAME%
        set "EXIT_CODE=1"
        cd /d "%ROOT_DIR%"
        goto :eof
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo [X] ERROR: No se encontr? el ejecutable de Python en .venv para %SERVICE_NAME%
    set "EXIT_CODE=1"
    cd /d "%ROOT_DIR%"
    goto :eof
)

set "VENV_PYTHON=.venv\Scripts\python.exe"

echo Instalando dependencias para %SERVICE_NAME%...
"%VENV_PYTHON%" -m pip install --upgrade pip setuptools wheel
if exist "requirements.txt" (
    "%VENV_PYTHON%" -m pip install -r requirements.txt pytest
) else (
    echo Advertencia: no se encontró requirements.txt en %SERVICE_NAME%
    "%VENV_PYTHON%" -m pip install pytest
)

if errorlevel 1 (
    echo [X] ERROR: Fall? la instalaci?n de dependencias en %SERVICE_NAME%
    set "EXIT_CODE=1"
    cd /d "%ROOT_DIR%"
    goto :eof
)

echo Ejecutando pytest para %SERVICE_NAME%...
"%VENV_PYTHON%" -m pytest "%TEST_FOLDER%"
if errorlevel 1 (
    echo [X] ERROR: Las pruebas fallaron para %SERVICE_NAME%
    set "EXIT_CODE=1"
) else (
    echo [OK] Todas las pruebas pasaron para %SERVICE_NAME%
)

cd /d "%ROOT_DIR%"
goto :eof
