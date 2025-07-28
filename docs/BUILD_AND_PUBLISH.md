# Сборка и публикация MCP сервера

Это руководство описывает процесс сборки и публикации MCP сервера `@daymanking990/task-orchectrator-mcp` как npm пакета для использования в других проектах.

## Предварительные требования

### 1. Установка инструментов

```bash
# Установка Node.js и npm (если еще не установлены)
# Скачайте с https://nodejs.org/

# Установка uv для Python зависимостей
pip install uv

# Проверка версий
node --version
npm --version
uv --version
```

### 2. Настройка npm аккаунта

1. Создайте аккаунт на [npmjs.com](https://www.npmjs.com/signup)
2. Войдите в npm в терминале:
```bash
npm login
```
3. Создайте организацию (опционально):
```bash
npm org create daymanking990
```

## Локальная сборка и тестирование

### 1. Проверка проекта

```bash
# Проверка синтаксиса Python
python -m py_compile src/task_orchectrator_mcp/server.py

# Проверка зависимостей
uv sync

# Тестирование сервера
uv run python -m task_orchectrator_mcp.server
```

### 2. Тестирование npm пакета локально

```bash
# Создание локального пакета
npm pack

# Установка пакета глобально для тестирования
npm install -g ./daymanking990-task-orchectrator-mcp-0.2.0.tgz

# Тестирование команды
task-orchectrator-mcp

# Удаление тестовой установки
npm uninstall -g @daymanking990/task-orchectrator-mcp
```

### 3. Тестирование через npx

```bash
# Запуск через npx
npx ./daymanking990-task-orchectrator-mcp-0.2.0.tgz
```

## Публикация на npm

### 1. Подготовка к публикации

```bash
# Проверка package.json
npm run test

# Проверка содержимого пакета
npm pack --dry-run

# Проверка метаданных
npm view @daymanking990/task-orchectrator-mcp
```

### 2. Публикация

```bash
# Публикация на npm
npm publish

# Для публикации в организацию (если используете scope)
npm publish --access public
```

### 3. Проверка публикации

```bash
# Проверка на npmjs.com
# https://www.npmjs.com/package/@daymanking990/task-orchectrator-mcp

# Установка с npm
npm install -g @daymanking990/task-orchectrator-mcp

# Тестирование установленного пакета
task-orchectrator-mcp
```

## Использование в других проектах

### 1. Установка как зависимость

```bash
# В новом проекте
npm install @daymanking990/task-orchectrator-mcp
```

### 2. Использование в MCP клиентах

#### Claude Desktop

Добавьте в `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "task-orchectrator": {
      "command": "npx",
      "args": ["@daymanking990/task-orchectrator-mcp"],
      "env": {
        "TRELLO_API_KEY": "your_trello_api_key",
        "TRELLO_TOKEN": "your_trello_token",
        "TRELLO_WORKING_BOARD_ID": "your_board_id"
      }
    }
  }
}
```

#### Другие MCP клиенты

```bash
# Прямой запуск
npx @daymanking990/task-orchectrator-mcp

# С переменными окружения
TRELLO_API_KEY=your_key TRELLO_TOKEN=your_token npx @daymanking990/task-orchectrator-mcp
```

## Автоматизация с GitHub Actions

### 1. Создание workflow

Создайте `.github/workflows/publish-npm.yml`:

```yaml
name: Publish to npm

on:
  release:
    types: [published]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: ["18", "20"]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js ${{ matrix.node-version }}
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    
    - name: Install uv
      run: |
        pip install uv
        uv --version
    
    - name: Install dependencies
      run: uv sync
    
    - name: Check syntax
      run: python -m py_compile src/task_orchectrator_mcp/server.py
    
    - name: Test import
      run: uv run python -c "import task_orchectrator_mcp; print('✅ Import successful')"

  publish:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'release'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Use Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '20'
        registry-url: 'https://registry.npmjs.org'
    
    - name: Install uv
      run: |
        pip install uv
        uv --version
    
    - name: Install dependencies
      run: uv sync
    
    - name: Publish to npm
      run: npm publish --access public
      env:
        NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

### 2. Настройка секретов

В настройках GitHub репозитория добавьте:
- `NPM_TOKEN` - npm access token (создайте на https://www.npmjs.com/settings/tokens)

## Версионирование

### 1. Обновление версии

```bash
# В package.json измените версию
"version": "0.2.1"  # или следующая версия

# Также обновите версию в pyproject.toml и __init__.py
```

### 2. Создание релиза

```bash
# Создание тега
git tag v0.2.1
git push origin v0.2.1

# Или через GitHub UI создайте новый релиз
```

## Troubleshooting

### Ошибки сборки

```bash
# Проверка Node.js и npm
node --version
npm --version

# Очистка npm кэша
npm cache clean --force

# Проверка package.json
npm run test
```

### Ошибки публикации

```bash
# Проверка авторизации
npm whoami

# Проверка пакета перед публикацией
npm pack --dry-run

# Проверка метаданных
npm view @daymanking990/task-orchectrator-mcp
```

### Проблемы с установкой

```bash
# Принудительная переустановка
npm install -g @daymanking990/task-orchectrator-mcp --force

# Проверка установленных пакетов
npm list -g | grep task-orchectrator
```

## Полезные команды

```bash
# Просмотр информации о пакете
npm view @daymanking990/task-orchectrator-mcp

# Проверка совместимости
npx @daymanking990/task-orchectrator-mcp --help

# Запуск с отладкой
DEBUG=* npx @daymanking990/task-orchectrator-mcp
```

## Следующие шаги

1. **Документация**: Создайте документацию на npmjs.com или GitHub Pages
2. **Тесты**: Добавьте unit тесты для повышения качества
3. **CI/CD**: Настройте автоматические тесты и проверки качества кода
4. **Мониторинг**: Настройте мониторинг загрузок и использования пакета
5. **Обновления**: Настройте автоматические обновления зависимостей 