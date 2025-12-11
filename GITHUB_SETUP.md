# Инструкция по загрузке на GitHub

## Если Git уже установлен

### 1. Настройка Git (если первый раз)
```bash
git config --global user.name "Ваше имя"
git config --global user.email "ваш.email@example.com"
```

### 2. Инициализация репозитория и первый коммит

В корне проекта `C:\Users\User\LAB MAKEEV`:

```bash
git init
git add .
git commit -m "Initial commit: Monolith + 6 microservices with Docker"
git branch -M main
```

### 3. Создание репозитория на GitHub

Переходим на https://github.com/new и создаем новый репозиторий (не добавляем README, .gitignore и лицензию - они уже в проекте)

### 4. Связываем локальный репозиторий с GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/your-repo-name.git
git push -u origin main
```

Замените `YOUR_USERNAME` и `your-repo-name` на ваши данные.

## Если GitHub CLI установлен

Проще всего:

```bash
cd C:\Users\User\LAB MAKEEV
gh repo create microservices-app --public --source=. --remote=origin --push
```

## Если Git не установлен

### Скачайте и установите Git:
- **Windows**: https://git-scm.com/download/win
- **Mac**: `brew install git`
- **Linux**: `sudo apt-get install git` (Ubuntu/Debian)

После установки повторите шаги выше.

## Список файлов, которые будут загружены

```
monolith/
├── Dockerfile
├── requirements.txt
├── app/
│   ├── __init__.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_main.py

services/
├── service1/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py
│   └── tests/
│       ├── __init__.py
│       └── test_main.py
├── service2/ ... service6/ (аналогично)

.gitignore
docker-compose.yml
README.md
GITHUB_SETUP.md
```

**Примечание**: Папки `venv` и `.pytest_cache` будут исключены благодаря `.gitignore`.

## Проверка что всё готово

```bash
git status
```

Должна отобразиться информация о коммитах и удаленном репозитории.
