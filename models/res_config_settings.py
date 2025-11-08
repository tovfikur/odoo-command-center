# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    terminal_venv_path = fields.Char(
        string='Virtual Environment Path',
        config_parameter='developer_terminal.venv_path',
        help='Path to the Python virtual environment (e.g., /opt/odoo-venv/bin/python). Leave empty to use system Python.'
    )

    terminal_allowed_commands = fields.Text(
        string='Allowed Commands (Whitelist)',
        config_parameter='developer_terminal.allowed_commands',
        default='pip,python,python3,ls,pwd,cat,grep,find,which,echo,whoami,uname,df,du,ps',
        help='Comma-separated list of allowed shell commands. Leave empty to allow all (not recommended).'
    )

    terminal_blocked_commands = fields.Text(
        string='Blocked Commands (Blacklist)',
        config_parameter='developer_terminal.blocked_commands',
        default='rm,rmdir,del,format,shutdown,reboot,halt,init,systemctl,service,kill,killall,pkill,dd,mkfs,fdisk',
        help='Comma-separated list of blocked shell commands. These will always be denied.'
    )

    terminal_max_output_size = fields.Integer(
        string='Max Output Size (bytes)',
        config_parameter='developer_terminal.max_output_size',
        default=1048576,  # 1MB
        help='Maximum size of command output to capture (in bytes). Prevents memory issues with large outputs.'
    )

    terminal_timeout = fields.Integer(
        string='Command Timeout (seconds)',
        config_parameter='developer_terminal.timeout',
        default=300,  # 5 minutes
        help='Maximum time allowed for a command to execute before being terminated.'
    )

    terminal_enable_python_exec = fields.Boolean(
        string='Enable Python Code Execution',
        config_parameter='developer_terminal.enable_python_exec',
        default=True,
        help='Allow execution of Python code directly in the terminal.'
    )

    terminal_log_retention_days = fields.Integer(
        string='Log Retention (days)',
        config_parameter='developer_terminal.log_retention_days',
        default=30,
        help='Number of days to keep terminal command logs. Set to 0 to keep forever.'
    )

    @api.model
    def get_terminal_config(self):
        """
        Get all terminal configuration parameters
        """
        ICP = self.env['ir.config_parameter'].sudo()
        return {
            'venv_path': ICP.get_param('developer_terminal.venv_path', ''),
            'allowed_commands': ICP.get_param('developer_terminal.allowed_commands', '').split(',') if ICP.get_param('developer_terminal.allowed_commands') else [],
            'blocked_commands': ICP.get_param('developer_terminal.blocked_commands', '').split(',') if ICP.get_param('developer_terminal.blocked_commands') else [],
            'max_output_size': int(ICP.get_param('developer_terminal.max_output_size', 1048576)),
            'timeout': int(ICP.get_param('developer_terminal.timeout', 300)),
            'enable_python_exec': ICP.get_param('developer_terminal.enable_python_exec', 'True') == 'True',
            'log_retention_days': int(ICP.get_param('developer_terminal.log_retention_days', 30)),
        }
