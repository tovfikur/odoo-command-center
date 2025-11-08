# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class AddonUpload(models.Model):
    _name = 'developer.addon.upload'
    _description = 'Addon Upload History'
    _order = 'create_date desc'

    name = fields.Char(
        string='Module Name',
        required=True,
        help='Name of the uploaded addon'
    )
    filename = fields.Char(
        string='File Name',
        required=True,
        help='Original filename of the uploaded zip'
    )
    file_size = fields.Integer(
        string='File Size (bytes)',
        help='Size of the uploaded file'
    )
    state = fields.Selection([
        ('uploading', 'Uploading'),
        ('extracting', 'Extracting'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ], string='State', default='uploading', required=True)

    upload_path = fields.Char(
        string='Upload Path',
        help='Path where the addon was uploaded'
    )
    error_message = fields.Text(
        string='Error Message',
        help='Error message if upload failed'
    )
    user_id = fields.Many2one(
        'res.users',
        string='Uploaded By',
        default=lambda self: self.env.user,
        required=True,
        ondelete='cascade'
    )
    create_date = fields.Datetime(
        string='Upload Date',
        readonly=True
    )

    @api.model
    def log_upload(self, name, filename, file_size, upload_path, state='success', error_message=None):
        """
        Create a log entry for an addon upload
        """
        return self.create({
            'name': name,
            'filename': filename,
            'file_size': file_size,
            'upload_path': upload_path,
            'state': state,
            'error_message': error_message,
        })
