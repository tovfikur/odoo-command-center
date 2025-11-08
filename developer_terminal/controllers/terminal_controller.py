# -*- coding: utf-8 -*-

import json
import subprocess
import sys
import os
import time
import platform
import shlex
import zipfile
import shutil
import base64
import signal
import threading
from io import StringIO, BytesIO
from contextlib import redirect_stdout, redirect_stderr

from odoo import http
from odoo.http import request, Response
import logging

_logger = logging.getLogger(__name__)


class TerminalController(http.Controller):

    def _check_access(self):
        """
        Verify that the current user has System Administrator rights
        """
        if not request.env.user.has_group('base.group_system'):
            return {
                'error': 'Access Denied',
                'message': 'Only System Administrators can access the Developer Terminal.'
            }
        return None

    def _is_command_allowed(self, command):
        """
        Check if a command is allowed based on whitelist/blacklist configuration
        """
        config = request.env['res.config.settings'].sudo().get_terminal_config()

        # Extract the base command (first word)
        cmd_parts = shlex.split(command) if command else []
        if not cmd_parts:
            return False, "Empty command"

        base_command = cmd_parts[0]

        # Check blacklist first (highest priority)
        blocked = [c.strip() for c in config.get('blocked_commands', []) if c.strip()]
        if base_command in blocked:
            return False, f"Command '{base_command}' is blocked for security reasons"

        # Check whitelist if configured
        allowed = [c.strip() for c in config.get('allowed_commands', []) if c.strip()]
        if allowed and base_command not in allowed:
            return False, f"Command '{base_command}' is not in the allowed commands list"

        return True, ""

    def _get_python_path(self):
        """
        Get the Python executable path (from venv if configured)
        """
        config = request.env['res.config.settings'].sudo().get_terminal_config()
        venv_path = config.get('venv_path', '')

        if venv_path and os.path.exists(venv_path):
            return venv_path

        return sys.executable

    @http.route('/developer_terminal/execute', type='json', auth='user', methods=['POST'])
    def execute_command(self, command, command_type='shell', **kwargs):
        """
        Execute a shell command or Python code
        """
        # Check access rights
        access_error = self._check_access()
        if access_error:
            return access_error

        if not command or not command.strip():
            return {'error': 'Empty command', 'message': 'Please enter a command to execute.'}

        start_time = time.time()
        log_data = {
            'command': command,
            'command_type': command_type,
        }

        try:
            if command_type == 'shell':
                result = self._execute_shell_command(command)
            elif command_type == 'python':
                result = self._execute_python_code(command)
            else:
                result = {
                    'error': 'Invalid command type',
                    'message': f"Unknown command type: {command_type}"
                }

            # Calculate execution time
            execution_time = time.time() - start_time

            # Log the command
            log_data.update({
                'output': result.get('output', ''),
                'error_output': result.get('error', ''),
                'return_code': result.get('return_code', 0),
                'execution_time': execution_time,
                'state': 'success' if not result.get('error') else 'failed',
            })

            request.env['developer.terminal.log'].sudo().log_command(**log_data)

            # Add execution time to result
            result['execution_time'] = round(execution_time, 3)

            return result

        except Exception as e:
            _logger.exception("Error executing command: %s", command)
            execution_time = time.time() - start_time

            log_data.update({
                'error_output': str(e),
                'return_code': -1,
                'execution_time': execution_time,
                'state': 'failed',
            })
            request.env['developer.terminal.log'].sudo().log_command(**log_data)

            return {
                'error': 'Execution Error',
                'message': str(e),
                'execution_time': round(execution_time, 3)
            }

    def _execute_shell_command(self, command):
        """
        Execute a shell command with security checks
        """
        # Check if command is allowed
        is_allowed, message = self._is_command_allowed(command)
        if not is_allowed:
            return {
                'error': 'Command Blocked',
                'message': message,
                'return_code': 1
            }

        config = request.env['res.config.settings'].sudo().get_terminal_config()
        timeout = config.get('timeout', 300)
        max_output_size = config.get('max_output_size', 1048576)

        try:
            # Set up environment with user's local bin in PATH
            env = os.environ.copy()
            user_bin = os.path.expanduser('~/.local/bin')
            if user_bin not in env.get('PATH', ''):
                env['PATH'] = f"{user_bin}:{env.get('PATH', '')}"

            # Execute the command
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                # Set working directory to a safe location
                cwd=os.path.expanduser('~')
            )

            # Wait for command to complete with timeout
            stdout, stderr = process.communicate(timeout=timeout)

            # Limit output size
            if len(stdout) > max_output_size:
                stdout = stdout[:max_output_size] + f"\n\n[Output truncated - exceeded {max_output_size} bytes]"
            if len(stderr) > max_output_size:
                stderr = stderr[:max_output_size] + f"\n\n[Error output truncated - exceeded {max_output_size} bytes]"

            return {
                'output': stdout,
                'error': stderr if stderr else None,
                'return_code': process.returncode,
                'success': process.returncode == 0
            }

        except subprocess.TimeoutExpired:
            process.kill()
            return {
                'error': 'Command Timeout',
                'message': f'Command execution exceeded {timeout} seconds timeout',
                'return_code': -1
            }
        except Exception as e:
            return {
                'error': 'Execution Failed',
                'message': str(e),
                'return_code': -1
            }

    def _execute_python_code(self, code):
        """
        Execute Python code in a restricted environment
        """
        config = request.env['res.config.settings'].sudo().get_terminal_config()

        if not config.get('enable_python_exec', True):
            return {
                'error': 'Python Execution Disabled',
                'message': 'Python code execution is disabled in settings',
                'return_code': 1
            }

        max_output_size = config.get('max_output_size', 1048576)

        # Capture stdout and stderr
        stdout_capture = StringIO()
        stderr_capture = StringIO()

        try:
            # Create a restricted globals dictionary with access to common modules
            safe_globals = {
                '__builtins__': __builtins__,
                'env': request.env,
                'request': request,
                'self': self,
            }

            # Execute the code
            with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                exec(code, safe_globals)

            stdout_output = stdout_capture.getvalue()
            stderr_output = stderr_capture.getvalue()

            # Limit output size
            if len(stdout_output) > max_output_size:
                stdout_output = stdout_output[:max_output_size] + f"\n\n[Output truncated - exceeded {max_output_size} bytes]"
            if len(stderr_output) > max_output_size:
                stderr_output = stderr_output[:max_output_size] + f"\n\n[Error output truncated - exceeded {max_output_size} bytes]"

            return {
                'output': stdout_output if stdout_output else 'Code executed successfully (no output)',
                'error': stderr_output if stderr_output else None,
                'return_code': 0,
                'success': True
            }

        except Exception as e:
            stderr_output = stderr_capture.getvalue()
            error_message = f"{type(e).__name__}: {str(e)}"

            if stderr_output:
                error_message = f"{stderr_output}\n{error_message}"

            return {
                'output': stdout_capture.getvalue(),
                'error': error_message,
                'return_code': 1,
                'success': False
            }


    @http.route('/developer_terminal/get_history', type='json', auth='user', methods=['POST'])
    def get_command_history(self, limit=50, **kwargs):
        """
        Get command history for the current user
        """
        # Check access rights
        access_error = self._check_access()
        if access_error:
            return access_error

        try:
            history = request.env['developer.terminal.log'].sudo().get_user_history(limit=limit)
            return {'success': True, 'history': history}
        except Exception as e:
            _logger.exception("Error fetching command history")
            return {'error': 'Error', 'message': str(e)}

    @http.route('/developer_terminal/get_env_info', type='json', auth='user', methods=['POST'])
    def get_environment_info(self, **kwargs):
        """
        Get system and environment information
        """
        # Check access rights
        access_error = self._check_access()
        if access_error:
            return access_error

        try:
            # Get Python version
            python_version = sys.version

            # Get Odoo version
            import odoo
            odoo_version = odoo.release.version

            # Get OS information
            os_info = {
                'system': platform.system(),
                'release': platform.release(),
                'version': platform.version(),
                'machine': platform.machine(),
                'processor': platform.processor(),
            }

            # Get installed packages (top 100)
            try:
                pip_list = subprocess.run(
                    [sys.executable, '-m', 'pip', 'list', '--format=json'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                packages = json.loads(pip_list.stdout) if pip_list.returncode == 0 else []
            except:
                packages = []

            # Get environment variables (filtered for safety)
            safe_env_vars = {
                'PATH': os.environ.get('PATH', ''),
                'PYTHONPATH': os.environ.get('PYTHONPATH', ''),
                'HOME': os.environ.get('HOME', ''),
                'USER': os.environ.get('USER', ''),
            }

            config = request.env['res.config.settings'].sudo().get_terminal_config()

            return {
                'success': True,
                'info': {
                    'python_version': python_version,
                    'python_executable': sys.executable,
                    'odoo_version': odoo_version,
                    'os_info': os_info,
                    'packages': packages[:100],  # Limit to first 100
                    'total_packages': len(packages),
                    'environment_vars': safe_env_vars,
                    'terminal_config': config,
                }
            }

        except Exception as e:
            _logger.exception("Error fetching environment info")
            return {'error': 'Error', 'message': str(e)}

    @http.route('/developer_terminal/restart_odoo', type='json', auth='user', methods=['POST'])
    def restart_odoo_service(self, username=None, sudo_password=None, **kwargs):
        """
        Restart the Odoo service (requires appropriate system permissions)
        For Docker: restarts the container from inside
        For systemd: uses sudo with provided password and optional username
        WARNING: This is a dangerous operation
        """
        # Check access rights
        access_error = self._check_access()
        if access_error:
            return access_error

        try:
            # Detect if we're in a Docker container
            in_docker = os.path.exists('/.dockerenv') or os.path.exists('/run/.containerenv')

            if in_docker:
                # In Docker, restart by killing the current process
                # The container will exit and can be restarted by Docker (if restart policy is set)
                # or the user can restart manually with docker-compose restart

                _logger.info(f"Attempting to restart Odoo in Docker container")

                try:
                    # Kill the current Odoo process
                    # Since we're running as the odoo user, we can kill our own process
                    _logger.info("Sending SIGTERM to current process")

                    # Schedule the kill to happen after we return the response
                    def delayed_exit():
                        time.sleep(1)  # Wait 1 second to ensure response is sent
                        _logger.info("Executing delayed exit...")
                        os.kill(1, signal.SIGTERM)  # Kill PID 1 (main Odoo process)

                    # Start the delayed exit in a separate thread
                    thread = threading.Thread(target=delayed_exit)
                    thread.daemon = True
                    thread.start()

                    return {
                        'success': True,
                        'message': 'Odoo restart initiated! Container will restart automatically in a few seconds.',
                        'output': 'Termination signal scheduled - Docker will auto-restart the container'
                    }

                except Exception as e:
                    _logger.error(f"Restart attempt failed: {e}")
                    return {
                        'error': 'Restart Failed',
                        'message': f'Could not restart Odoo: {str(e)}. Please restart from host:\n\ndocker-compose restart odoo'
                    }

            # For non-Docker Linux systems
            if platform.system() == 'Linux':
                if sudo_password:
                    # Try with provided sudo password
                    commands = [
                        'systemctl restart odoo',
                        'service odoo restart',
                        '/etc/init.d/odoo restart',
                    ]

                    for cmd in commands:
                        try:
                            _logger.info(f"Attempting system restart with command: {cmd}")

                            # Use su to switch user if provided, otherwise use sudo
                            if username:
                                # Format: echo 'password' | su -c 'command' username
                                full_cmd = f"echo {shlex.quote(sudo_password)} | su -c {shlex.quote(cmd)} {shlex.quote(username)}"
                            else:
                                # Use sudo with password
                                full_cmd = f"echo {shlex.quote(sudo_password)} | sudo -S {cmd}"

                            result = subprocess.run(
                                full_cmd,
                                shell=True,
                                capture_output=True,
                                text=True,
                                timeout=10
                            )

                            _logger.info(f"Command result - returncode: {result.returncode}, stdout: {result.stdout}, stderr: {result.stderr}")

                            # Check for authentication errors
                            if 'authentication failure' in result.stderr.lower() or 'incorrect password' in result.stderr.lower():
                                return {
                                    'error': 'Authentication Failed',
                                    'message': 'Incorrect username or password. Please check your credentials and try again.'
                                }

                            if result.returncode == 0:
                                return {
                                    'success': True,
                                    'message': 'Odoo restart command sent successfully!',
                                    'output': result.stdout
                                }

                        except Exception as e:
                            _logger.error(f"Command '{cmd}' failed: {e}")
                            continue

                    return {
                        'error': 'Restart Failed',
                        'message': 'Could not restart Odoo. Please verify credentials and Odoo service name.'
                    }
                else:
                    # Try without password (passwordless sudo)
                    commands = [
                        'sudo systemctl restart odoo',
                        'sudo service odoo restart',
                        'sudo /etc/init.d/odoo restart',
                    ]

                    for cmd in commands:
                        try:
                            result = subprocess.run(
                                cmd.split(),
                                capture_output=True,
                                text=True,
                                timeout=10
                            )
                            if result.returncode == 0:
                                return {
                                    'success': True,
                                    'message': 'Odoo restart command sent successfully',
                                    'output': result.stdout
                                }
                        except:
                            continue

                    return {
                        'error': 'Sudo Password Required',
                        'message': 'Sudo password required to restart Odoo. Please provide credentials.',
                        'need_password': True
                    }
            else:
                return {
                    'error': 'Not Supported',
                    'message': f'Odoo restart is not supported on {platform.system()}. Please restart manually.'
                }

        except Exception as e:
            _logger.exception("Error restarting Odoo")
            return {'error': 'Error', 'message': str(e)}

    @http.route('/developer_terminal/clear_logs', type='json', auth='user', methods=['POST'])
    def clear_old_logs(self, **kwargs):
        """
        Clear old terminal logs based on retention policy
        """
        # Check access rights
        access_error = self._check_access()
        if access_error:
            return access_error

        try:
            config = request.env['res.config.settings'].sudo().get_terminal_config()
            retention_days = config.get('log_retention_days', 30)

            if retention_days <= 0:
                return {'success': True, 'message': 'Log retention is disabled (keeping all logs)'}

            # Delete logs older than retention period
            from datetime import datetime, timedelta
            cutoff_date = datetime.now() - timedelta(days=retention_days)

            old_logs = request.env['developer.terminal.log'].sudo().search([
                ('create_date', '<', cutoff_date)
            ])

            count = len(old_logs)
            old_logs.unlink()

            return {
                'success': True,
                'message': f'Deleted {count} log entries older than {retention_days} days'
            }

        except Exception as e:
            _logger.exception("Error clearing logs")
            return {'error': 'Error', 'message': str(e)}

    @http.route('/developer_terminal/upload_addon', type='http', auth='user', methods=['POST'], csrf=False)
    def upload_addon(self, **kwargs):
        """
        Upload a custom addon zip file, extract it to custom_addons, and optionally restart Odoo
        """
        # Check access rights
        if not request.env.user.has_group('base.group_system'):
            return request.make_json_response({
                'error': 'Access Denied',
                'message': 'Only System Administrators can upload addons.'
            })

        try:
            # Get the uploaded file
            uploaded_file = request.httprequest.files.get('file')
            if not uploaded_file:
                return request.make_json_response({
                    'error': 'No File',
                    'message': 'No file was uploaded.'
                })

            filename = uploaded_file.filename
            if not filename.endswith('.zip'):
                return request.make_json_response({
                    'error': 'Invalid File',
                    'message': 'Only .zip files are allowed.'
                })

            # Read file content
            file_content = uploaded_file.read()
            file_size = len(file_content)

            # Determine custom_addons path
            custom_addons_path = None

            # Check if /mnt/extra-addons exists (Docker default)
            if os.path.exists('/mnt/extra-addons'):
                custom_addons_path = '/mnt/extra-addons'
            else:
                # Try to find custom addons path from config
                import odoo
                from odoo.tools import config
                addons_paths = config.get('addons_path', '').split(',')
                for path in addons_paths:
                    path = path.strip()
                    if 'custom' in path.lower() or 'extra' in path.lower():
                        custom_addons_path = path
                        break

                if not custom_addons_path:
                    for path in addons_paths:
                        path = path.strip()
                        if os.access(path, os.W_OK):
                            custom_addons_path = path
                            break

            if not custom_addons_path or not os.path.exists(custom_addons_path):
                return request.make_json_response({
                    'error': 'Path Not Found',
                    'message': f'Could not find custom addons directory.'
                })

            # Create a temporary file for the zip
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as temp_file:
                temp_file.write(file_content)
                temp_zip_path = temp_file.name

            try:
                # Extract the zip file
                with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                    zip_contents = zip_ref.namelist()

                    # Find the module directory
                    module_name = None
                    for item in zip_contents:
                        if '__manifest__.py' in item or '__openerp__.py' in item:
                            module_name = item.split('/')[0] if '/' in item else os.path.dirname(item)
                            break

                    if not module_name:
                        return request.make_json_response({
                            'error': 'Invalid Addon',
                            'message': 'No __manifest__.py or __openerp__.py found in the zip file.'
                        })

                    # Check if module already exists
                    module_path = os.path.join(custom_addons_path, module_name)
                    if os.path.exists(module_path):
                        backup_path = f"{module_path}_backup_{int(time.time())}"
                        shutil.move(module_path, backup_path)
                        _logger.info(f"Backed up existing module to: {backup_path}")

                    # Extract all files
                    zip_ref.extractall(custom_addons_path)
                    _logger.info(f"Extracted addon to: {module_path}")

                os.unlink(temp_zip_path)

                # Log the upload
                request.env['developer.addon.upload'].sudo().log_upload(
                    name=module_name,
                    filename=filename,
                    file_size=file_size,
                    upload_path=module_path,
                    state='success'
                )

                restart_message = '\n\nNote: In Docker, restart with: docker-compose restart odoo\nOr go to Apps and update the module list.'

                return request.make_json_response({
                    'success': True,
                    'message': f'Addon "{module_name}" uploaded successfully!{restart_message}',
                    'module_name': module_name,
                    'module_path': module_path,
                    'file_size': file_size
                })

            finally:
                if os.path.exists(temp_zip_path):
                    try:
                        os.unlink(temp_zip_path)
                    except:
                        pass

        except zipfile.BadZipFile:
            return request.make_json_response({
                'error': 'Invalid Zip',
                'message': 'The uploaded file is not a valid zip file.'
            })
        except Exception as e:
            _logger.exception("Error uploading addon")
            return request.make_json_response({
                'error': 'Upload Failed',
                'message': str(e)
            })

    @http.route('/developer_terminal/get_upload_history', type='json', auth='user', methods=['POST'])
    def get_upload_history(self, limit=50, **kwargs):
        """
        Get addon upload history
        """
        access_error = self._check_access()
        if access_error:
            return access_error

        try:
            uploads = request.env['developer.addon.upload'].sudo().search(
                [],
                limit=limit,
                order='create_date desc'
            )

            return {
                'success': True,
                'uploads': [{
                    'id': upload.id,
                    'name': upload.name,
                    'filename': upload.filename,
                    'file_size': upload.file_size,
                    'state': upload.state,
                    'upload_path': upload.upload_path,
                    'error_message': upload.error_message,
                    'user': upload.user_id.name,
                    'create_date': upload.create_date.strftime('%Y-%m-%d %H:%M:%S') if upload.create_date else '',
                } for upload in uploads]
            }

        except Exception as e:
            _logger.exception("Error fetching upload history")
            return {'error': 'Error', 'message': str(e)}
