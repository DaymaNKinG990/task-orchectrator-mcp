# 🚀 Публикация MCP сервера СЕЙЧАС

## Что нужно сделать:

### 1. Создать npm аккаунт (если нет)
```bash
# Перейти на https://www.npmjs.com/signup
# Создать аккаунт
```

### 2. Войти в npm
```bash
npm login
# Ввести username, password, email
```

### 3. Опубликовать на npm
```bash
npm publish --access public
```

### 4. Зарегистрировать в официальном реестре MCP

#### Вариант A: Через веб-интерфейс
1. Перейти на https://registry.modelcontextprotocol.io
2. Войти через GitHub
3. Добавить новый сервер с данными из `server.json`

#### Вариант B: Через API
```bash
# Создать GitHub токен на https://github.com/settings/tokens
# Использовать MCP Publisher Tool (если доступен)
```

## Проверка после публикации:

### npm
```bash
# Установить с npm
npm install -g @daymanking990/task-orchectrator-mcp

# Протестировать
task-orchectrator-mcp
```

### Реестр MCP
```bash
# Проверить в реестре
curl https://registry.modelcontextprotocol.io/v0/servers | grep task-orchectrator
```

## Использование в mcp.json:

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

## Готово! 🎉

После публикации ваш MCP сервер будет доступен:
- **npm**: `npm install @daymanking990/task-orchectrator-mcp`
- **npx**: `npx @daymanking990/task-orchectrator-mcp`
- **Реестр MCP**: https://registry.modelcontextprotocol.io 