# 🔑 Setting up Trello API Token

## 🚨 Current Token Issue

The current token is invalid. Error: `invalid app token`.

## 🔧 Proper Token Setup

### Step 1: Get API Key

1. Go to https://trello.com/app-key
2. Login to your Trello account
3. Copy the **API Key** (this is a long string of characters)

### Step 2: Get Token

**IMPORTANT:** The token needs to be generated properly!

1. On the same page https://trello.com/app-key
2. Find the **"Token"** section
3. Click the **"Token"** button (don't copy the old token!)
4. Trello will show you a **new token** - copy it
5. The token should be long (usually 64 characters)

### Step 3: Verify Token

After getting the new token, run diagnostics:

```bash
uv run python debug_trello_token.py
```

### Step 4: Update Configuration

Update your `~/.cursor/mcp.json` file:

```json
{
  "task-orchestrator": {
    "command": "npx",
    "args": ["@daymanking990/task-orchectrator-mcp"],
    "env": {
      "TRELLO_API_KEY": "your_new_api_key",
      "TRELLO_TOKEN": "your_new_token",
      "TRELLO_WORKING_BOARD_ID": "your_board_id"
    }
  }
}
```

## 🔍 Possible Causes of the Problem

### 1. Incorrect Token Copying
- Make sure you copied the entire token
- Check that there are no extra spaces

### 2. Token Expired
- Tokens can expire
- Generate a new token

### 3. Incorrect Access Rights
- Make sure the token has read/write permissions for boards

### 4. Account Issues
- Check that the account is active
- Make sure the board is accessible to your account

## 🧪 Testing

After updating the token:

1. **Run diagnostics:**
   ```bash
   uv run python debug_trello_token.py
   ```

2. **Check system status:**
   ```
   "Show system status"
   ```

3. **Create a test task:**
   ```
   "Create task: Test Trello - Check integration"
   ```

## 📋 Expected Result

With proper setup, you should see:

```
✅ Token is valid!
User: Your Name
Username: your_username

✅ Found X boards:
  - Your Board Name (ID: your_board_id)

✅ Target board found: Your Board Name

✅ py-trello library works!
Found X boards
✅ Target board found via py-trello: Your Board Name
```

## 🚨 If the Problem Persists

1. **Try a different browser** to get the token
2. **Clear browser cache**
3. **Check that the board exists** and is accessible
4. **Create a new board** for testing
5. **Contact Trello support** if it's a systemic issue

## 💡 Alternative Solution

If Trello doesn't work, the system will use **local storage**:

- Tasks are saved in `tasks_backup.json`
- Transitions are saved in `transitions_backup.json`
- The system works completely offline
- When Trello connection is restored, data can be synchronized

## ✅ Done!

After proper token setup, the system will be fully integrated with Trello! 