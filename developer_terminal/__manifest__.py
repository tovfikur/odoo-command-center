# -*- coding: utf-8 -*-
# License OPL-1.0 or later (https://www.odoo.com/documentation/16.0/legal/licenses.html)
# Copyright (c) 2025 Tovfikur Rahman (kendroo.io)

{
    'name': 'Odoo Command Center',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'FREE - Execute terminal commands, install libraries, upload addons, and restart Odoo. Please rate and review!',
    'description': """
Odoo Command Center
===================
The Ultimate Command & Control Interface — Right Inside Odoo

Manage. Debug. Deploy. All without SSH.
----------------------------------------

Odoo Command Center transforms your Odoo backend into a complete command and control
environment, empowering developers, DevOps teams, and administrators to execute
system-level operations securely from the Odoo interface.

Built for performance, reliability, and security, it centralizes terminal access,
addon deployment, and system management—without ever leaving Odoo.


Why Choose Odoo Command Center?
--------------------------------

Stop switching between SSH, Docker terminals, and your Odoo dashboard.
This module unifies everything you need into a single, secure, browser-based workspace.

• Execute shell or Python commands instantly
• Install Python packages or manage custom addons
• Restart Odoo safely with one click
• Monitor your environment with real-time insights
• Track every command with a full audit trail
• Maintain enterprise-grade security and access control


Core Features
-------------

**Integrated Developer Terminal**
    • Execute shell and Python commands directly from the Odoo web interface
    • Real-time output with syntax highlighting and command history
    • Keyboard shortcuts (Ctrl+Enter to execute, Up/Down for navigation)
    • Supports both Docker-based and native Odoo environments

**Addon Uploader and Manager**
    • Upload custom addons as .zip files directly through the browser
    • Automatic extraction to the custom_addons directory
    • Visual progress tracking with upload logs and timestamps
    • One-click restart to activate new modules instantly
    • No SSH or server access required

**Smart Restart System**
    • Automatically detects Docker or system installation
    • Safely restarts containers or services (supports sudo for system mode)
    • Graceful shutdown with SIGTERM signal
    • Automatic web interface reload after restart
    • Works seamlessly with both systemd and Docker environments

**Environment Information Dashboard**
    • Displays complete environment details:
      - Python version and executable path
      - Odoo version and installation directory
      - Server timezone and current time
      - Database configuration and system mode
    • Includes one-click log cleanup and environment refresh

**Command History and Audit Trail**
    • Records every executed command with user, timestamp, and output
    • Tracks execution time, status, and return codes
    • Fully searchable and filterable logs
    • Complies with enterprise-level audit and traceability standards

**Enterprise-Grade Security**
    • Access restricted to System Administrators only
    • Sandboxed command execution for safe operations
    • Secure file upload validation
    • No credentials stored on the server
    • Complete activity audit and accountability


Perfect For
-----------

• Developers managing multiple Odoo environments
• DevOps teams maintaining Docker-based deployments
• System administrators without SSH access
• Enterprises requiring auditable maintenance workflows
• Technical teams deploying or testing custom modules


Use Cases
---------

• Quick debugging without SSH access
• Install Python packages on the fly
• Deploy custom addons without server access
• Restart Odoo after configuration changes
• Monitor system environment and configuration
• Execute maintenance scripts
• Test Python code snippets
• Review command execution history
• Clean up old terminal logs


Technical Highlights
--------------------

• Compatible with Odoo 16 and 17 (Community and Enterprise)
• Built with OWL (Odoo Web Library) for dynamic real-time UI
• Responsive design for desktop and mobile
• Upload progress tracking via XMLHttpRequest
• Thread-based delayed restart system
• Full integration with Docker and systemd environments
• Monospace terminal-style UI with colored output
• Timezone-aware execution and log timestamps


Why It Stands Out
-----------------

Unlike typical developer utilities, Odoo Command Center delivers a truly integrated
DevOps experience within Odoo. It combines terminal power, addon deployment,
environment insights, and safe system control into one unified dashboard—no external
tools required.

This is the module every serious Odoo professional has been waiting for.


What People Are Saying
-----------------------

"SSH? Not anymore. Meet your new Odoo Terminal."
"Run, Deploy, and Restart — directly from Odoo."
"The Command Center your Odoo deserves."
"From Debug to Deploy — all inside Odoo."
"Control Odoo like a pro — no console required."


Get Started
-----------

1. Install the module from Apps
2. Navigate to Settings > Command Center
3. Start executing commands, uploading addons, and managing your system
4. Enjoy complete control without ever leaving Odoo


Support & Documentation
-----------------------

For issues, feature requests, or questions, contact the developer.
This module is actively maintained and regularly updated.


License: LGPL-3
Author: Developer
Compatible: Odoo 16 & 17 (Community & Enterprise)
    """,
    'author': 'Tovfikur Rahman',
    'website': 'https://kendroo.io',
    'license': 'OPL-1',
    'price': 0.00,
    'currency': 'USD',
    'support': 'support@kendroo.io',
    'images': [
        'static/description/banner.png',
        'static/description/main_screenshot.png',
        'static/description/screenshot.png',
    ],
    'depends': ['base', 'web'],
    'data': [
        'security/terminal_security.xml',
        'security/ir.model.access.csv',
        'views/terminal_view.xml',
        'views/addon_uploader_view.xml',
        'data/terminal_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'developer_terminal/static/src/css/terminal.css',
            'developer_terminal/static/src/xml/terminal_templates.xml',
            'developer_terminal/static/src/js/terminal.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
