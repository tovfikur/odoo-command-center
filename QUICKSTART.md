# Quick Start Guide - Developer Terminal

Get up and running with Developer Terminal in 5 minutes!

## Installation (3 steps)

### 1. Restart Odoo Container
```bash
cd K:\Odoo
docker-compose restart odoo
```

### 2. Update Apps List
- Open http://localhost:8069
- Login as Administrator
- Go to **Apps**
- Click **⋮** → **Update Apps List** → **Update**

### 3. Install Module
- In Apps, remove "Apps" filter
- Search: **"Developer Terminal"**
- Click **Install**

## First Steps

### Access the Terminal
**Settings → Developer Terminal → Terminal**

### Run Your First Command

**Shell Command:**
```bash
echo "Hello from Developer Terminal!"
```

**Python Code:**
```python
print(f"Current user: {env.user.name}")
print(f"Database: {env.cr.dbname}")
```

## Common Tasks

### 1. Check System Info
```bash
# Python version
python --version

# Installed packages
pip list

# Disk space
df -h
```

### 2. Query Odoo Data
```python
# Count partners
partners = env['res.partner'].search_count([])
print(f"Total partners: {partners}")

# List users
users = env['res.users'].search([])
for user in users:
    print(f"{user.name} - {user.login}")
```

### 3. Install Python Package
Go to: **Settings → Developer Terminal → Package Manager**
- Package name: `requests`
- Action: `Install`
- Click **Execute**

### 4. View Environment
Go to: **Settings → Developer Terminal → Environment Info**
- See Python version, Odoo version, OS info
- View installed packages
- Check configuration

## Keyboard Shortcuts

- **Ctrl+Enter** - Execute command
- **Up Arrow** - Previous command from history
- **Down Arrow** - Next command from history

## Security Tips

⚠️ **Only for System Administrators**
⚠️ **Test commands in development first**
⚠️ **Be careful with write operations**

## Configure Security

**Settings → Developer Terminal → Settings**

**Recommended for Production:**
- Allowed Commands: `pip,python,ls,pwd,cat,grep,find,which,echo,whoami,df`
- Blocked Commands: `rm,rmdir,shutdown,reboot,kill,systemctl`
- Command Timeout: `300` seconds
- Python Execution: ✅ Enabled

## Need Help?

- **Full documentation:** [README.md](README.md)
- **Installation guide:** [INSTALL.md](INSTALL.md)
- **Examples:** [EXAMPLES.md](EXAMPLES.md)

## Next Steps

1. ✅ Try the example commands above
2. ✅ Check command history: **Settings → Developer Terminal → Command History**
3. ✅ Configure security settings
4. ✅ Install packages you need
5. ✅ Explore environment information

## Troubleshooting

### Can't see the module?
- Restart Odoo: `docker-compose restart odoo`
- Update Apps List again

### Permission denied?
- Login as **Administrator**
- User must be in **Settings / Administration** access group

### Command blocked?
- Check **Settings → Developer Terminal → Settings**
- Add command to **Allowed Commands**
- Or remove from **Blocked Commands**

---

**You're all set! Happy coding! 🚀**

For detailed examples and advanced usage, see [EXAMPLES.md](EXAMPLES.md)
