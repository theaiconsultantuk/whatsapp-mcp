# 🚀 WhatsApp MCP Server - Complete Setup Guide

> **Training Objective**: Set up a fully functional WhatsApp integration with Claude Desktop using the Model Context Protocol (MCP)

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **macOS** (this guide is macOS-focused)
- [ ] **Claude Desktop** installed ([Download here](https://claude.ai/download))
- [ ] **Active WhatsApp account** on your smartphone
- [ ] **VPN access** (recommended for some regions)
- [ ] **Terminal access** and basic command line knowledge
- [ ] **Administrative privileges** on your computer

---

## 🛠 Part 1: Install Required Dependencies

### Step 1.1: Install Go Programming Language

1. **Visit the Go website**: https://golang.org/dl/
2. **Download** the macOS installer (.pkg file)
3. **Run the installer** and follow the setup wizard
4. **Verify installation** by opening Terminal and running:
   ```bash
   go version
   ```
   ✅ You should see something like: `go version go1.21.0 darwin/arm64`

### Step 1.2: Install UV (Python Package Manager)

1. **Open Terminal**
2. **Run the installation command**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Restart Terminal** or run:
   ```bash
   source ~/.bashrc
   ```
4. **Verify installation**:
   ```bash
   uv --version
   ```

### Step 1.3: Install FFmpeg (Optional - for Audio Messages)

Using Homebrew (install Homebrew first if you don't have it):
```bash
# Install Homebrew if needed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install FFmpeg
brew install ffmpeg
```

---

## 📦 Part 2: Download and Setup the WhatsApp MCP Server

### Step 2.1: Clone the Repository

1. **Open Terminal**
2. **Navigate to your preferred directory** (e.g., Desktop):
   ```bash
   cd ~/Desktop
   ```
3. **Clone the improved repository**:
   ```bash
   git clone https://github.com/theaiconsultantuk/whatsapp-mcp.git
   ```
4. **Navigate into the project**:
   ```bash
   cd whatsapp-mcp
   ```

### Step 2.2: Build the Go WhatsApp Bridge

1. **Navigate to the bridge directory**:
   ```bash
   cd whatsapp-bridge
   ```
2. **Download Go dependencies**:
   ```bash
   go mod tidy
   ```
3. **Build the application**:
   ```bash
   go build -o whatsapp-bridge main.go
   ```

✅ **Success indicator**: No error messages during build

---

## 📱 Part 3: Connect to WhatsApp

### Step 3.1: Start the WhatsApp Bridge

1. **Ensure you're in the whatsapp-bridge directory**:
   ```bash
   pwd
   # Should show: /path/to/whatsapp-mcp/whatsapp-bridge
   ```

2. **If you're in a restricted region, connect to VPN now** (recommended: US server)

3. **Run the WhatsApp bridge**:
   ```bash
   go run main.go
   ```

### Step 3.2: Scan QR Code with WhatsApp

1. **Wait for QR code to appear** in your terminal (large ASCII square pattern)
2. **On your smartphone**:
   - Open **WhatsApp**
   - Go to **Settings** → **Linked Devices**
   - Tap **"Link a Device"**
   - **Scan the QR code** displayed in your terminal

3. **Wait for connection**:
   - You should see: `"Successfully connected and authenticated!"`
   - Messages will start syncing: `"Stored XXXX messages"`
   - Server starts: `"Starting REST API server on :8080..."`

✅ **Success indicators**:
- ✓ Connected to WhatsApp
- ✓ Messages synced
- ✓ REST server running

### Step 3.3: Keep the Bridge Running

⚠️ **Important**: Leave this terminal window open and the process running. The WhatsApp bridge must stay active for the MCP server to work.

---

## 🔧 Part 4: Configure the MCP Server

### Step 4.1: Setup Python Environment

1. **Open a NEW terminal window** (keep the first one running)
2. **Navigate to the MCP server directory**:
   ```bash
   cd ~/Desktop/whatsapp-mcp/whatsapp-mcp-server
   ```
3. **Install Python dependencies**:
   ```bash
   uv sync
   ```

✅ **Success indicator**: Virtual environment created at `.venv`

### Step 4.2: Test MCP Server (Optional)

1. **Test the server can start**:
   ```bash
   uv run main.py --help
   ```
2. **You should see the MCP server help output**

---

## ⚙️ Part 5: Configure Claude Desktop

### Step 5.1: Get Required Paths

1. **Find the UV executable path**:
   ```bash
   which uv
   ```
   📝 **Copy this path** (e.g., `/Users/yourname/.local/bin/uv`)

2. **Get the project directory path**:
   ```bash
   cd ~/Desktop/whatsapp-mcp && pwd
   ```
   📝 **Copy this path** (e.g., `/Users/yourname/Desktop/whatsapp-mcp`)

### Step 5.2: Create Claude Configuration Directory

```bash
mkdir -p ~/Library/Application\ Support/Claude
```

### Step 5.3: Create Configuration File

1. **Create/edit the Claude config file**:
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration** (replace the paths with your actual paths):

```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "/Users/yourname/.local/bin/uv",
      "args": [
        "--directory",
        "/Users/yourname/Desktop/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "PATH": "/Users/yourname/.local/bin:/usr/local/bin:/usr/bin:/bin"
      }
    }
  }
}
```

3. **Save and exit** (in nano: Ctrl+X, then Y, then Enter)

### Step 5.4: Restart Claude Desktop

1. **Quit Claude Desktop completely**
2. **Reopen Claude Desktop**
3. **Wait 10-15 seconds** for MCP servers to initialize

---

## ✅ Part 6: Verify Everything Works

### Step 6.1: Check WhatsApp Bridge Status

In your first terminal (where the bridge is running), you should see:
```
✓ Connected to WhatsApp! Type 'help' for commands.
REST server is running. Press Ctrl+C to disconnect and exit.
```

### Step 6.2: Check Claude Integration

1. **Open Claude Desktop**
2. **Look for the tools icon** (🔧) in the chat interface
3. **Click on it** - you should see WhatsApp tools like:
   - `search_contacts`
   - `list_messages`
   - `send_message`
   - `list_chats`

### Step 6.3: Test the Integration

Try asking Claude:
```
"Show me my recent WhatsApp chats"
```

✅ **Success**: Claude should be able to access and display your WhatsApp data

---

## 🎉 Part 7: You're Ready!

### What You Can Now Do:

- 📱 **Search WhatsApp contacts** by name or phone
- 💬 **Read message history** from any chat
- 📤 **Send messages** through Claude to any contact or group
- 📎 **Send files and media** (images, documents, audio)
- 🔍 **Search conversations** by content, date, or sender
- 📊 **Analyze conversation patterns** using Claude's AI capabilities

### Example Commands to Try:

```
"Find all messages from John in the last week"
"Send a message to [contact name] saying 'Hello from Claude!'"
"Show me the most active group chats"
"Summarize my conversations from yesterday"
"Download the latest image from [chat name]"
```

---

## 🆘 Troubleshooting

### Common Issues and Solutions:

#### 🔴 "QR Code Won't Scan"
- **Solution**: Use a VPN (US server recommended)
- **Alternative**: Switch between WiFi and mobile data

#### 🔴 "Compilation Errors"
- **Already Fixed**: This fork includes all necessary fixes
- **If issues persist**: Run `go mod tidy` and `go build` again

#### 🔴 "MCP Server Not Connecting"
- **Check paths** in your Claude config file are correct
- **Restart Claude Desktop** completely
- **Verify UV installation**: `which uv`

#### 🔴 "WhatsApp Bridge Disconnects"
- **Normal**: Restart with `go run main.go`
- **If frequent**: Check your internet connection stability

#### 🔴 "No WhatsApp Tools in Claude"
- **Wait 15 seconds** after Claude restart
- **Check Claude logs**: `~/Library/Logs/Claude/`
- **Verify config file syntax** (use a JSON validator)

---

## 🛡️ Security Notes

- 🔒 **Local storage**: All messages stored locally on your computer
- 🔒 **No cloud sync**: WhatsApp data stays on your machine
- 🔒 **Claude access**: Only when you explicitly use WhatsApp tools
- 🔒 **API keys**: Keep your OpenAI/Anthropic keys secure

---

## 📞 Training Support

If you encounter issues during the training session:

1. **Raise your hand** for immediate assistance
2. **Check the troubleshooting section** above
3. **Share your terminal output** for debugging
4. **Don't worry** - we'll get it working together!

---

*Happy WhatsApp + Claude integration! 🚀📱🤖*