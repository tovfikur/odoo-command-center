# Odoo Command Center

**The Ultimate Command & Control Interface for Odoo**

This repository contains the Odoo Command Center module - a production-grade addon that provides complete command and control interface for developers and administrators directly inside Odoo.

## Module

- **developer_terminal** - The main Odoo Command Center module

## Features

- Integrated terminal for shell and Python command execution
- Addon uploader with automatic deployment
- Smart restart system (Docker and systemd support)
- Environment information dashboard
- Command history and audit trail
- Enterprise-grade security

## Installation

### From Odoo Apps Store

Search for "Odoo Command Center" in the Odoo Apps menu and install directly.

### Manual Installation

1. Clone this repository:
```bash
git clone https://github.com/tovfikur/odoo-command-center.git
```

2. Copy the `developer_terminal` folder to your Odoo addons directory:
```bash
cp -r odoo-command-center/developer_terminal /path/to/odoo/addons/
```

3. Restart Odoo and update the apps list

4. Install "Odoo Command Center" from the Apps menu

## Compatibility

- Odoo 16.0 (Community & Enterprise)
- Odoo 17.0 (Community & Enterprise)

## Documentation

See the [module README](developer_terminal/README.md) for detailed documentation, usage instructions, and configuration options.

## License

LGPL-3

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Contact through Odoo Apps Store

---

**Odoo Command Center** - Manage. Debug. Deploy. All without SSH.
