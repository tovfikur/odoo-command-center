# Installation Guide - Developer Terminal

Complete installation instructions for Odoo 16 and 17.

## Table of Contents
1. [Quick Start (Docker)](#quick-start-docker)
2. [Manual Installation](#manual-installation)
3. [Post-Installation](#post-installation)
4. [Verification](#verification)
5. [Configuration](#configuration)

---

## Quick Start (Docker)

### For Docker Compose Setup

If you're using Docker Compose (like your current setup), follow these steps:

1. **Ensure Odoo is running:**
   ```bash
   cd K:\Odoo
   docker-compose up -d
   ```

2. **The module is already in place** at:
   ```
   K:\Odoo\custom_addons\developer_terminal\
   ```

3. **Restart Odoo container** to recognize the module:
   ```bash
   docker-compose restart odoo
   ```

4. **Update Apps List** in Odoo web interface:
   - Open browser: http://localhost:8069
   - Login as Administrator
   - Go to **Apps** menu
   - Click **"Update Apps List"** (top-right menu → Update Apps List)
   - Click **"Update"** in the confirmation dialog

5. **Install the module:**
   - Remove the "Apps" filter in the search bar
   - Search for **"Developer Terminal"**
   - Click **"Install"**

6. **Access the terminal:**
   - Go to **Settings → Developer Terminal → Terminal**

---

## Manual Installation

### Step 1: Copy Module Files

```bash
# Navigate to your Odoo addons directory
cd /path/to/odoo/custom_addons

# Copy the developer_terminal module
# (Already in place if following Docker setup)
```

### Step 2: Verify File Permissions

```bash
# Ensure Odoo can read the files
chmod -R 755 developer_terminal/
chown -R odoo:odoo developer_terminal/
```

### Step 3: Update Odoo Addons Path

Make sure your `odoo.conf` includes the custom addons directory:

```ini
[options]
addons_path = /mnt/extra-addons,/usr/lib/python3/dist-packages/odoo/addons
```

For your Docker setup, this is already configured in `docker-compose.yml`:
```yaml
volumes:
  - ./custom_addons:/mnt/extra-addons
```

### Step 4: Restart Odoo

**Docker:**
```bash
docker-compose restart odoo
```

**Systemd:**
```bash
sudo systemctl restart odoo
```

**Manual:**
```bash
# Stop Odoo
sudo killall odoo-bin

# Start Odoo
./odoo-bin -c odoo.conf
```

---

## Post-Installation

### Update Apps List

1. Login to Odoo as **Administrator**
2. Go to **Apps** menu
3. Click the **⋮** menu (top-right)
4. Select **"Update Apps List"**
5. Click **"Update"** in the dialog

### Install the Module

1. In the **Apps** menu:
   - Remove the default "Apps" filter from search
   - Type: **"Developer Terminal"**
   - Click **"Install"** on the module card

2. Wait for installation to complete

3. You should see the new menu: **Settings → Developer Terminal**

---

## Verification

### Check Installation Status

1. **Via UI:**
   - Go to **Apps**
   - Search for "Developer Terminal"
   - Status should show **"Installed"**

2. **Via Logs:**
   ```bash
   # Docker
   docker logs odoo-odoo-1 | grep developer_terminal

   # Should see lines like:
   # INFO ? odoo.modules.loading: module developer_terminal: loading objects
   # INFO ? odoo.modules.loading: module developer_terminal: creating or updating database tables
   ```

### Test Basic Functionality

1. **Access Terminal:**
   - Go to **Settings → Developer Terminal → Terminal**
   - You should see the terminal interface

2. **Run a test command:**
   ```bash
   echo "Hello from Developer Terminal"
   ```
   - Click Execute (or Ctrl+Enter)
   - You should see the output

3. **Check Command History:**
   - Go to **Settings → Developer Terminal → Command History**
   - Your test command should appear in the list

---

## Configuration

### Initial Configuration (Recommended)

1. **Go to Settings:**
   - **Settings → Developer Terminal → Settings**

2. **Configure Security (Important!):**

   **For Production:**
   ```
   Allowed Commands:
   pip,python,python3,ls,pwd,cat,grep,find,which,echo,whoami,df

   Blocked Commands:
   rm,rmdir,del,mv,format,shutdown,reboot,halt,init,systemctl,
   service,kill,killall,pkill,dd,mkfs,fdisk
   ```

   **For Development:**
   - You can be more permissive with allowed commands
   - Still keep dangerous commands in blocked list

3. **Set Timeouts:**
   - **Command Timeout:** 300 seconds (5 minutes)
   - Adjust based on your needs

4. **Configure Output Limits:**
   - **Max Output Size:** 1048576 bytes (1MB)
   - Increase if you need larger outputs

5. **Log Retention:**
   - **Log Retention Days:** 30
   - Set to 0 to keep logs forever
   - Set to lower value to save database space

6. **Python Execution:**
   - ✅ **Enable Python Code Execution** (checked)
   - Uncheck if you only want shell commands

7. **Save Settings**

### Virtual Environment (Optional)

If you want to use a separate Python virtual environment:

1. **Create a virtual environment:**
   ```bash
   # Inside Docker container
   docker exec -it odoo-odoo-1 bash
   python -m venv /opt/odoo-terminal-venv
   source /opt/odoo-terminal-venv/bin/activate
   pip install --upgrade pip
   ```

2. **Configure in Odoo:**
   - Go to **Settings → Developer Terminal → Settings**
   - Set **Virtual Environment Path:** `/opt/odoo-terminal-venv/bin/python`
   - Save

3. **Test:**
   - Go to Terminal
   - Run: `which python`
   - Should show the venv path

---

## Troubleshooting Installation

### Module Not Showing in Apps List

**Solution:**
1. Verify files are in correct location:
   ```bash
   ls -la custom_addons/developer_terminal/
   ```
2. Check `__manifest__.py` exists and is valid
3. Restart Odoo and update apps list again
4. Check Odoo logs for errors

### Installation Fails

**Check logs:**
```bash
# Docker
docker logs odoo-odoo-1 --tail 100

# Look for errors mentioning developer_terminal
```

**Common issues:**
- Missing dependencies: Ensure `base` and `web` modules are installed
- Syntax errors: Check Python files for errors
- Permission issues: Verify file permissions

### Cannot Access Terminal (Permission Denied)

**Solution:**
1. Ensure you're logged in as **Administrator**
2. Check you're in **Settings** group:
   - Go to **Settings → Users → Your User**
   - Verify **Access Rights** includes "Administration: Settings"

### Commands Not Executing

**Check configuration:**
1. Go to **Settings → Developer Terminal → Settings**
2. Verify command is in **Allowed Commands**
3. Verify command is NOT in **Blocked Commands**
4. Check **Command Timeout** is sufficient

### Python Code Won't Execute

**Solution:**
1. Go to **Settings → Developer Terminal → Settings**
2. Check **Enable Python Code Execution** is enabled
3. Save settings
4. Try again

---

## Upgrading

### To Upgrade Module

1. **Stop Odoo:**
   ```bash
   docker-compose stop odoo
   ```

2. **Update module files:**
   ```bash
   # Copy new version to custom_addons/developer_terminal/
   ```

3. **Start Odoo:**
   ```bash
   docker-compose start odoo
   ```

4. **Upgrade in UI:**
   - Go to **Apps**
   - Search for "Developer Terminal"
   - If upgrade available, click **"Upgrade"**

   **OR via command line:**
   ```bash
   docker exec odoo-odoo-1 odoo -u developer_terminal -d your_database
   ```

---

## Uninstallation

### To Completely Remove Module

1. **Uninstall via UI:**
   - Go to **Apps**
   - Search for "Developer Terminal"
   - Click **"Uninstall"**
   - Confirm

2. **Remove files (optional):**
   ```bash
   rm -rf custom_addons/developer_terminal/
   ```

3. **Restart Odoo:**
   ```bash
   docker-compose restart odoo
   ```

**Note:** Uninstalling will remove:
- Menu items
- Command history logs
- Configuration settings
- All module data from database

---

## Docker-Specific Notes

### Your Current Setup

Based on your `docker-compose.yml`:

- **Odoo Image:** odoo:17.0
- **Custom Addons:** `./custom_addons` → `/mnt/extra-addons`
- **Config:** `./odoo.conf` → `/etc/odoo/odoo.conf`
- **Port:** 8069

### Useful Docker Commands

```bash
# View Odoo logs
docker logs -f odoo-odoo-1

# Access Odoo container shell
docker exec -it odoo-odoo-1 bash

# Restart just Odoo
docker-compose restart odoo

# Check module is visible
docker exec odoo-odoo-1 ls -la /mnt/extra-addons/developer_terminal

# Install module via CLI
docker exec odoo-odoo-1 odoo -d postgres -i developer_terminal --stop-after-init
```

---

## Support

If you encounter issues:

1. **Check logs** first (most issues are logged)
2. **Review configuration** in Settings
3. **Verify permissions** (file and user access)
4. **Test with simple commands** first
5. **Check Odoo version compatibility** (16 or 17)

For specific errors, check the Odoo server logs for detailed information.

---

## Next Steps

After successful installation:

1. ✅ Read the [README.md](README.md) for usage instructions
2. ✅ Configure security settings
3. ✅ Test with basic commands
4. ✅ Explore package manager
5. ✅ Review command history
6. ✅ Check environment info

**Enjoy your Developer Terminal! 🚀**
