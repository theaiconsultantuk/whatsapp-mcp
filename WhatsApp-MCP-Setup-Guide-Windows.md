# 🚀 WhatsApp MCP Server - Complete Setup Guide (Windows)

> **Training Objective**: Set up a fully functional WhatsApp integration with Claude Desktop using the Model Context Protocol (MCP) on Windows

---

## 📋 Prerequisites Checklist

Before starting, ensure you have:

- [ ] **Windows 10/11** (64-bit)
- [ ] **Claude Desktop** installed ([Download here](https://claude.ai/download))
- [ ] **Active WhatsApp account** on your smartphone
- [ ] **VPN access** (recommended for some regions)
- [ ] **PowerShell or Command Prompt access**
- [ ] **Administrative privileges** on your computer
- [ ] **Git for Windows** ([Download here](https://git-scm.com/download/win))

---

## 🛠 Part 1: Install Required Dependencies

### Step 1.1: Install Go Programming Language

1. **Visit the Go website**: https://golang.org/dl/
2. **Download** the Windows installer (.msi file)
3. **Run the installer** with administrative privileges
4. **Restart Command Prompt/PowerShell**
5. **Verify installation** by opening Command Prompt and running:
   ```cmd
   go version
   ```
   ✅ You should see something like: `go version go1.21.0 windows/amd64`

### Step 1.2: Install C Compiler (Required for Windows)

⚠️ **Critical for Windows**: Go's SQLite package requires CGO, which needs a C compiler.

**Option 1: Install MSYS2 (Recommended)**

1. **Download MSYS2**: https://www.msys2.org/
2. **Run the installer** and follow the setup wizard
3. **After installation, open MSYS2 terminal**
4. **Update package database**:
   ```bash
   pacman -Syu
   ```
5. **Install GCC compiler**:
   ```bash
   pacman -S mingw-w64-ucrt-x86_64-gcc
   ```
6. **Add to Windows PATH**:
   - Open **System Properties** → **Environment Variables**
   - Add `C:\msys64\ucrt64\bin` to your **PATH** variable
   - **Restart Command Prompt**

**Option 2: Install TDM-GCC (Alternative)**

1. **Download TDM-GCC**: https://jmeubank.github.io/tdm-gcc/
2. **Install with default settings**
3. **Verify GCC is in PATH**:
   ```cmd
   gcc --version
   ```

### Step 1.3: Install UV (Python Package Manager)

1. **Open PowerShell as Administrator**
2. **Run the installation command**:
   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
3. **Restart PowerShell**
4. **Verify installation**:
   ```cmd
   uv --version
   ```

### Step 1.4: Install FFmpeg (Optional - for Audio Messages)

**Using Chocolatey (Recommended)**:

1. **Install Chocolatey** (if not already installed):
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Install FFmpeg**:
   ```cmd
   choco install ffmpeg
   ```

**Manual Installation**:
1. **Download FFmpeg**: https://ffmpeg.org/download.html#build-windows
2. **Extract to** `C:\ffmpeg`
3. **Add** `C:\ffmpeg\bin` **to your PATH**

---

## 📦 Part 2: Download and Setup the WhatsApp MCP Server

### Step 2.1: Clone the Repository

1. **Open Command Prompt or PowerShell**
2. **Navigate to your preferred directory** (e.g., Desktop):
   ```cmd
   cd %USERPROFILE%\Desktop
   ```
3. **Clone the improved repository**:
   ```cmd
   git clone https://github.com/theaiconsultantuk/whatsapp-mcp.git
   ```
4. **Navigate into the project**:
   ```cmd
   cd whatsapp-mcp
   ```

### Step 2.2: Enable CGO and Build the WhatsApp Bridge

1. **Navigate to the bridge directory**:
   ```cmd
   cd whatsapp-bridge
   ```

2. **Enable CGO** (Critical for Windows):
   ```cmd
   go env -w CGO_ENABLED=1
   ```

3. **Download Go dependencies**:
   ```cmd
   go mod tidy
   ```

4. **Build the application**:
   ```cmd
   go build -o whatsapp-bridge.exe main.go
   ```

✅ **Success indicator**: `whatsapp-bridge.exe` file created with no error messages

⚠️ **If you get CGO errors**:
- Ensure GCC is installed and in PATH
- Restart Command Prompt
- Verify: `gcc --version` works

---

## 📱 Part 3: Connect to WhatsApp

### Step 3.1: Start the WhatsApp Bridge

1. **Ensure you're in the whatsapp-bridge directory**:
   ```cmd
   cd
   ```
   Should show: `C:\Users\YourName\Desktop\whatsapp-mcp\whatsapp-bridge`

2. **If you're in a restricted region, connect to VPN now** (recommended: US server)

3. **Run the WhatsApp bridge**:
   ```cmd
   go run main.go
   ```

   **Alternative** (using the built executable):
   ```cmd
   whatsapp-bridge.exe
   ```

### Step 3.2: Scan QR Code with WhatsApp

1. **Wait for QR code to appear** in your Command Prompt (large ASCII square pattern)
2. **On your smartphone**:
   - Open **WhatsApp**
   - Go to **Settings** → **Linked Devices**
   - Tap **"Link a Device"**
   - **Scan the QR code** displayed in your Command Prompt

3. **Wait for connection**:
   - You should see: `"Successfully connected and authenticated!"`
   - Messages will start syncing: `"Stored XXXX messages"`
   - Server starts: `"Starting REST API server on :8080..."`

✅ **Success indicators**:
- ✓ Connected to WhatsApp
- ✓ Messages synced
- ✓ REST server running

### Step 3.3: Keep the Bridge Running

⚠️ **Important**: Leave this Command Prompt window open and the process running. The WhatsApp bridge must stay active for the MCP server to work.

---

## 🔧 Part 4: Configure the MCP Server

### Step 4.1: Setup Python Environment

1. **Open a NEW Command Prompt window** (keep the first one running)
2. **Navigate to the MCP server directory**:
   ```cmd
   cd %USERPROFILE%\Desktop\whatsapp-mcp\whatsapp-mcp-server
   ```
3. **Install Python dependencies**:
   ```cmd
   uv sync
   ```

✅ **Success indicator**: Virtual environment created at `.venv`

### Step 4.2: Test MCP Server (Optional)

1. **Test the server can start**:
   ```cmd
   uv run main.py --help
   ```
2. **You should see the MCP server help output**

---

## ⚙️ Part 5: Configure Claude Desktop

### Step 5.1: Get Required Paths

1. **Find the UV executable path**:
   ```cmd
   where uv
   ```
   📝 **Copy this path** (e.g., `C:\Users\YourName\.local\bin\uv.exe`)

2. **Get the project directory path**:
   ```cmd
   cd %USERPROFILE%\Desktop\whatsapp-mcp && cd
   ```
   📝 **Copy this path** (e.g., `C:\Users\YourName\Desktop\whatsapp-mcp`)

### Step 5.2: Create Claude Configuration Directory

```cmd
mkdir "%APPDATA%\Claude"
```

### Step 5.3: Create Configuration File

1. **Create the Claude config file**:
   ```cmd
   notepad "%APPDATA%\Claude\claude_desktop_config.json"
   ```

2. **Add this configuration** (replace the paths with your actual paths):

```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "C:\\Users\\YourName\\.local\\bin\\uv.exe",
      "args": [
        "--directory",
        "C:\\Users\\YourName\\Desktop\\whatsapp-mcp\\whatsapp-mcp-server",
        "run",
        "main.py"
      ],
      "env": {
        "PATH": "C:\\Users\\YourName\\.local\\bin;C:\\Windows\\System32;C:\\Windows"
      }
    }
  }
}
```

⚠️ **Important Windows Path Notes**:
- Use **double backslashes** (`\\`) in JSON paths
- Replace `YourName` with your actual Windows username
- Use full absolute paths

3. **Save and close Notepad**

### Step 5.4: Restart Claude Desktop

1. **Quit Claude Desktop completely** (check system tray)
2. **Reopen Claude Desktop**
3. **Wait 10-15 seconds** for MCP servers to initialize

---

## ✅ Part 6: Verify Everything Works

### Step 6.1: Check WhatsApp Bridge Status

In your first Command Prompt (where the bridge is running), you should see:
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

## 🆘 Troubleshooting (Windows-Specific)

### Common Windows Issues and Solutions:

#### 🔴 "CGO Error: Binary was compiled with 'CGO_ENABLED=0'"
- **Solution**: Install GCC compiler (MSYS2 or TDM-GCC)
- **Enable CGO**: `go env -w CGO_ENABLED=1`
- **Verify GCC**: `gcc --version`

#### 🔴 "UV Command Not Found"
- **Solution**: Add UV to PATH manually
- **Check installation**: Reinstall with PowerShell as admin
- **Alternative**: Use full path to `uv.exe`

#### 🔴 "Permission Denied Errors"
- **Solution**: Run Command Prompt as Administrator
- **Check antivirus**: Whitelist the project directory
- **Windows Defender**: Add exclusions for the project folder

#### 🔴 "Path with Spaces Issues"
- **Solution**: Use quotes around paths
- **Example**: `"C:\Users\Your Name\Desktop\whatsapp-mcp"`

#### 🔴 "Firewall Blocking Connection"
- **Windows Firewall**: Allow Go application through firewall
- **Port 8080**: Ensure it's not blocked
- **Antivirus**: Check if blocking network connections

#### 🔴 "QR Code Characters Not Displaying"
- **Solution**: Use Windows Terminal instead of Command Prompt
- **Alternative**: Use PowerShell
- **Font issue**: Install a Unicode-compatible font

#### 🔴 "MCP Server Path Issues"
- **Double-check backslashes** in JSON configuration
- **Use full absolute paths** (not relative)
- **Windows username spaces**: Use quotes if needed

### Windows Environment Variables

If you need to set environment variables permanently:

1. **Open System Properties**:
   - Press `Win + R`, type `sysdm.cpl`
   - Click **Environment Variables**

2. **Add to PATH**:
   - Select **PATH** in User Variables
   - Click **Edit** → **New**
   - Add your UV bin directory

3. **Add CGO_ENABLED**:
   - Click **New** in User Variables
   - Variable name: `CGO_ENABLED`
   - Variable value: `1`

---

## 🛡️ Security Notes

- 🔒 **Local storage**: All messages stored locally on your computer
- 🔒 **No cloud sync**: WhatsApp data stays on your machine
- 🔒 **Claude access**: Only when you explicitly use WhatsApp tools
- 🔒 **Windows Defender**: May flag the executable - add to exclusions
- 🔒 **Firewall**: Allow necessary network connections

---

## 📞 Training Support

If you encounter issues during the training session:

1. **Raise your hand** for immediate assistance
2. **Check the Windows-specific troubleshooting** section above
3. **Share your Command Prompt output** for debugging
4. **Try PowerShell** if Command Prompt has issues
5. **Don't worry** - we'll get it working together!

---

## 🔧 Windows-Specific Tips

- **Use Windows Terminal** for better Unicode support
- **Run as Administrator** when in doubt
- **Check Windows Defender** exclusions
- **Use PowerShell** over Command Prompt when possible
- **Keep paths short** to avoid Windows path length limits
- **Use quotes** around paths with spaces

---

*Happy WhatsApp + Claude integration on Windows! 🚀📱🤖*