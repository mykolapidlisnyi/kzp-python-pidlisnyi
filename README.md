# KZP Python — Лабораторна робота № 6 (Варіант 20: Тренажерний зал)

Консольний Python-пакет `kzp-gym-report` (`kzp_lab06`) для зчитування, валідації та аналізу абонементів тренажерного залу з CSV-файла.

## Структура проєкту
* `src/kzp_lab06/errors.py` — власний виняток `DataError`.
* `src/kzp_lab06/loader.py` — читання та валідація CSV через `csv.DictReader` (UTF-8).
* `src/kzp_lab06/analysis.py` — аналіз записів (`comprehensions`, множини, словники, `summarize` із `*args`/`**kwargs`).
* `src/kzp_lab06/reporting.py` — детерміноване форматування та запис звіту у UTF-8.
* `src/kzp_lab06/cli.py` — точка входу командного рядка.

## Запуск та перевірка
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m ruff format --check .
python -m kzp_lab06.cli data\input.csv reports\summary.txt

---

### 4. Відправте початкову базу в `main` і створіть гілку `python/lab06`
*(Переконайтеся, що `.gitignore` уже є у корені проєкту, щоб `.venv`, `.venv-wheel` і `dist` не потрапили в Git)*[cite: 8].

```powershell
# 1. Перевіряємо, які файли бачить Git (не має бути .venv чи dist!)
git status

# 2. Перший коміт у main і підключення віддаленого репозиторію
git add .
git commit -m "Initial Python project setup and Lab 6 implementation (Variant 20)"
git remote add origin https://github.com/mykolapidlisnyi/kzp-python-pidlisnyi.git
git push -u origin main

# 3. Створення робочої гілки для Pull Request (як вимагає методичка)
git switch -c python/lab06
git push -u origin python/lab06