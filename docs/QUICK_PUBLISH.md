# Быстрая публикация MCP сервера

## Предварительные требования

1. **npm аккаунт**: Создайте на [npmjs.com](https://www.npmjs.com/signup)
2. **Вход в npm**: `npm login`
3. **uv**: `pip install uv`

## Быстрая публикация

### 1. Обновление версии

Обновите версию в трех файлах:
- `package.json`: `"version": "0.2.1"`
- `pyproject.toml`: `version = "0.2.1"`
- `src/task_orchectrator_mcp/__init__.py`: `__version__ = "0.2.1"`

### 2. Тестирование

```bash
# Создание пакета
npm pack

# Тестирование локально
npm install -g ./daymanking990-task-orchectrator-mcp-0.2.1.tgz
task-orchectrator-mcp

# Удаление тестовой установки
npm uninstall -g @daymanking990/task-orchectrator-mcp
```

### 3. Публикация

```bash
# Публикация на npm
npm publish --access public
```

### 4. Проверка

```bash
# Установка с npm
npm install -g @daymanking990/task-orchectrator-mcp

# Тестирование
task-orchectrator-mcp
```

## Использование в mcp.json

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

## Автоматическая публикация

Создайте GitHub релиз - пакет автоматически опубликуется на npm. 