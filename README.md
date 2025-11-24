### Hexlet tests and linter status:
[![Actions Status](https://github.com/MlkProduction/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/MlkProduction/python-project-52/actions)

## Локальный запуск

1. Установите зависимости (используется [uv](https://github.com/astral-sh/uv)):
   ```
   uv sync
   ```
2. Активируйте виртуальное окружение:
   ```
   source .venv/bin/activate
   ```
3. Запустите dev-сервер Django:
   ```
   python hexlet-code/manage.py runserver
   ```
4. Откройте `http://127.0.0.1:8000/` и убедитесь, что на главной странице выводится приветствие.