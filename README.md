# Odoo Command Center

**The Ultimate Command & Control Interface — Right Inside Odoo**

Manage. Debug. Deploy. All without SSH.

## Overview

Odoo Command Center transforms your Odoo backend into a complete command and control environment, empowering developers, DevOps teams, and administrators to execute system-level operations securely from the Odoo interface.

Built for performance, reliability, and security, it centralizes terminal access, addon deployment, and system management—without ever leaving Odoo.

## Why Choose Odoo Command Center?

Stop switching between SSH, Docker terminals, and your Odoo dashboard. This module unifies everything you need into a single, secure, browser-based workspace.

- Execute shell or Python commands instantly
- Install Python packages or manage custom addons
- Restart Odoo safely with one click
- Monitor your environment with real-time insights
- Track every command with a full audit trail
- Maintain enterprise-grade security and access control

## Core Features

### Integrated Developer Terminal
- Execute shell and Python commands directly from the Odoo web interface
- Real-time output with syntax highlighting and command history
- Keyboard shortcuts (Ctrl+Enter to execute, Up/Down for navigation)
- Supports both Docker-based and native Odoo environments

### Addon Uploader and Manager
- Upload custom addons as .zip files directly through the browser
- Automatic extraction to the custom_addons directory
- Visual progress tracking with upload logs and timestamps
- One-click restart to activate new modules instantly
- No SSH or server access required

### Smart Restart System
- Automatically detects Docker or system installation
- Safely restarts containers or services (supports sudo for system mode)
- Graceful shutdown with SIGTERM signal
- Automatic web interface reload after restart
- Works seamlessly with both systemd and Docker environments

### Environment Information Dashboard
- Displays complete environment details:
  - Python version and executable path
  - Odoo version and installation directory
  - Server timezone and current time
  - Database configuration and system mode
- Includes one-click log cleanup and environment refresh

### Command History and Audit Trail
- Records every executed command with user, timestamp, and output
- Tracks execution time, status, and return codes
- Fully searchable and filterable logs
- Complies with enterprise-level audit and traceability standards

### Enterprise-Grade Security
- Access restricted to System Administrators only
- Sandboxed command execution for safe operations
- Secure file upload validation
- No credentials stored on the server
- Complete activity audit and accountability

## Perfect For

- Developers managing multiple Odoo environments
- DevOps teams maintaining Docker-based deployments
- System administrators without SSH access
- Enterprises requiring auditable maintenance workflows
- Technical teams deploying or testing custom modules

## Use Cases

- Quick debugging without SSH access
- Install Python packages on the fly
- Deploy custom addons without server access
- Restart Odoo after configuration changes
- Monitor system environment and configuration
- Execute maintenance scripts
- Test Python code snippets
- Review command execution history
- Clean up old terminal logs

## Technical Highlights

- Compatible with Odoo 16 and 17 (Community and Enterprise)
- Built with OWL (Odoo Web Library) for dynamic real-time UI
- Responsive design for desktop and mobile
- Upload progress tracking via XMLHttpRequest
- Thread-based delayed restart system
- Full integration with Docker and systemd environments
- Monospace terminal-style UI with colored output
- Timezone-aware execution and log timestamps

## Installation

### From Odoo Apps Store
1. Search for "Odoo Command Center" in the Apps menu
2. Click Install
3. Navigate to Settings > Command Center

### Manual Installation
1. Download or clone this repository
2. Copy the `developer_terminal` folder to your Odoo addons directory
3. Update the addons list in Odoo
4. Install the module from Apps menu

### For Docker Installations
Add restart policy to your `docker-compose.yml`:

```yaml
odoo:
  image: odoo:17.0
  restart: unless-stopped
  depends_on:
    - db
```

## Usage

### Terminal Interface
1. Navigate to Settings > Command Center > Terminal
2. Select command type (Shell or Python)
3. Enter your command
4. Press Ctrl+Enter or click Execute
5. View real-time output

### Upload Addons
1. Navigate to Settings > Command Center > Addon Uploader
2. Click "Choose File" and select your .zip addon
3. Click "Upload Addon"
4. Wait for upload to complete
5. Click "Restart Odoo Now" to activate

### Environment Info
1. Navigate to Settings > Command Center > Environment Info
2. View system information
3. Use restart functionality when needed
4. Clean up old logs with one click

## Security Considerations

- Only System Administrators can access this module
- All commands are logged with full audit trail
- File uploads are validated for .zip format only
- Restart functionality requires confirmation
- No passwords are stored on the server
- All operations are sandboxed

## Why It Stands Out

Unlike typical developer utilities, Odoo Command Center delivers a truly integrated DevOps experience within Odoo. It combines terminal power, addon deployment, environment insights, and safe system control into one unified dashboard—no external tools required.

This is the module every serious Odoo professional has been waiting for.

## What People Are Saying

> "SSH? Not anymore. Meet your new Odoo Terminal."

> "Run, Deploy, and Restart — directly from Odoo."

> "The Command Center your Odoo deserves."

> "From Debug to Deploy — all inside Odoo."

> "Control Odoo like a pro — no console required."

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Contact through Odoo Apps Store

This module is actively maintained and regularly updated.

## License

LGPL-3

## Compatibility

- Odoo 16 (Community & Enterprise)
- Odoo 17 (Community & Enterprise)

---

**Odoo Command Center** - The Ultimate Command & Control Interface for Odoo
