#!/bin/bash
set -e
ruff format --check
ruff check
pytest

echo "所有检查通过"
