#!/usr/bin/env python3
"""
Script para ejecutar las pruebas del servicio `orders`.

Uso:
  python run_tests.py           # ejecuta todos los tests en tests/
  python run_tests.py --unit    # ejecuta solo tests unitarios (services + handlers)
  python run_tests.py --persistence  # ejecuta solo tests de persistencia
  python run_tests.py --coverage    # añade reporte de cobertura

Este script usa `pytest` programáticamente y debe correrse desde el directorio `services/orders`.
"""
from __future__ import annotations
import argparse
import sys
import pytest


def build_test_list(unit: bool, persistence: bool) -> list:
    if not unit and not persistence:
        return ["tests"]

    tests: list[str] = []
    if unit:
        tests.extend(["tests/test_services.py", "tests/test_handlers.py"])
    if persistence:
        tests.append("tests/test_persistence.py")
    return tests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run orders service tests")
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--persistence", action="store_true", help="Run persistence tests only")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose pytest output")

    args = parser.parse_args(argv)

    tests = build_test_list(unit=args.unit, persistence=args.persistence)

    pytest_args: list[str] = []
    if args.coverage:
        pytest_args += ["--cov=app", "--cov-report=term-missing"]
    if args.verbose:
        pytest_args.append("-vv")

    pytest_args += tests

    # Llamada a pytest
    return pytest.main(pytest_args)


if __name__ == "__main__":
    raise SystemExit(main())
