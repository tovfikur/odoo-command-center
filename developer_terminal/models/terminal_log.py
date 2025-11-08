# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class TerminalLog(models.Model):
    _name = 'developer.terminal.log'
    _description = 'Terminal Command Log'
    _order = 'create_date desc'
    _rec_name = 'command'

    command = fields.Text(
        string='Command',
        required=True,
        help='The command that was executed'
    )
    command_type = fields.Selection([
        ('shell', 'Shell Command'),
        ('python', 'Python Code'),
        ('package', 'Package Manager'),
    ], string='Command Type', required=True, default='shell')

    output = fields.Text(
        string='Output',
        help='The output of the command execution'
    )
    error_output = fields.Text(
        string='Error Output',
        help='Any error messages from the command'
    )
    return_code = fields.Integer(
        string='Return Code',
        help='The exit code of the command (0 = success)'
    )
    execution_time = fields.Float(
        string='Execution Time (seconds)',
        help='Time taken to execute the command'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Executed By',
        default=lambda self: self.env.user,
        required=True,
        ondelete='cascade'
    )
    state = fields.Selection([
        ('running', 'Running'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='running', required=True)

    create_date = fields.Datetime(
        string='Executed At',
        readonly=True
    )

    @api.model
    def log_command(self, command, command_type='shell', output='', error_output='', return_code=0, execution_time=0.0, state='success'):
        """
        Create a log entry for a command execution
        """
        return self.create({
            'command': command,
            'command_type': command_type,
            'output': output,
            'error_output': error_output,
            'return_code': return_code,
            'execution_time': execution_time,
            'state': state,
        })

    @api.model
    def get_user_history(self, limit=50):
        """
        Get command history for current user
        """
        commands = self.search([
            ('user_id', '=', self.env.user.id),
        ], limit=limit, order='create_date desc')

        return [{
            'id': cmd.id,
            'command': cmd.command,
            'command_type': cmd.command_type,
            'state': cmd.state,
            'create_date': cmd.create_date.strftime('%Y-%m-%d %H:%M:%S') if cmd.create_date else '',
        } for cmd in commands]

    def action_view_details(self):
        """
        Open form view with full command details
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Command Details',
            'res_model': 'developer.terminal.log',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
