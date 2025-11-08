/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component, useState, useRef, onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

// Terminal Widget Component
class DeveloperTerminal extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            command: "",
            commandType: "shell",
            output: "",
            errorOutput: "",
            isExecuting: false,
            history: [],
            historyIndex: -1,
        });
        this.inputRef = useRef("commandInput");
        this.outputRef = useRef("outputArea");

        onMounted(() => {
            this.loadHistory();
            if (this.inputRef.el) {
                this.inputRef.el.focus();
            }
        });
    }

    async loadHistory() {
        try {
            const result = await this.rpc("/developer_terminal/get_history", {
                limit: 100,
            });
            if (result.success) {
                this.state.history = result.history || [];
            }
        } catch (error) {
            console.error("Error loading history:", error);
        }
    }

    async executeCommand() {
        if (!this.state.command.trim()) {
            this.notification.add("Please enter a command", { type: "warning" });
            return;
        }

        this.state.isExecuting = true;
        this.state.output = "Executing...\n";
        this.state.errorOutput = "";

        try {
            const result = await this.rpc("/developer_terminal/execute", {
                command: this.state.command,
                command_type: this.state.commandType,
            });

            if (result.error) {
                this.state.errorOutput = `Error: ${result.error}\n${result.message || ""}`;
                this.state.output = result.output || "";
                this.notification.add(result.error, { type: "danger" });
            } else {
                this.state.output = result.output || "Command executed successfully (no output)";
                this.state.errorOutput = result.error || "";

                const execTime = result.execution_time ? ` (${result.execution_time}s)` : "";
                this.notification.add(`Command executed${execTime}`, { type: "success" });
            }

            // Reload history
            await this.loadHistory();

            // Scroll output to bottom
            if (this.outputRef.el) {
                this.outputRef.el.scrollTop = this.outputRef.el.scrollHeight;
            }

        } catch (error) {
            this.state.errorOutput = `Error: ${error.message || error}`;
            this.notification.add("Execution failed", { type: "danger" });
        } finally {
            this.state.isExecuting = false;
        }
    }

    clearTerminal() {
        this.state.command = "";
        this.state.output = "";
        this.state.errorOutput = "";
        if (this.inputRef.el) {
            this.inputRef.el.focus();
        }
    }

    onKeyDown(ev) {
        // Execute on Ctrl+Enter
        if (ev.ctrlKey && ev.key === "Enter") {
            ev.preventDefault();
            this.executeCommand();
        }
        // Navigate history with Up/Down arrows
        else if (ev.key === "ArrowUp") {
            ev.preventDefault();
            if (this.state.historyIndex < this.state.history.length - 1) {
                this.state.historyIndex++;
                this.state.command = this.state.history[this.state.historyIndex]?.command || "";
            }
        } else if (ev.key === "ArrowDown") {
            ev.preventDefault();
            if (this.state.historyIndex > 0) {
                this.state.historyIndex--;
                this.state.command = this.state.history[this.state.historyIndex]?.command || "";
            } else {
                this.state.historyIndex = -1;
                this.state.command = "";
            }
        }
    }

    loadFromHistory(historyItem) {
        this.state.command = historyItem.command;
        this.state.commandType = historyItem.command_type;
        if (this.inputRef.el) {
            this.inputRef.el.focus();
        }
    }
}

DeveloperTerminal.template = "developer_terminal.Terminal";

// Environment Info Widget Component
class EnvironmentInfo extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            info: null,
            isLoading: true,
            restartUsername: "",
            restartPassword: "",
        });

        onMounted(() => {
            this.loadEnvironmentInfo();
        });
    }

    async loadEnvironmentInfo() {
        this.state.isLoading = true;
        try {
            const result = await this.rpc("/developer_terminal/get_env_info", {});

            if (result.error) {
                this.notification.add(result.error, { type: "danger" });
            } else {
                this.state.info = result.info;
            }

        } catch (error) {
            this.notification.add("Failed to load environment info", { type: "danger" });
        } finally {
            this.state.isLoading = false;
        }
    }

    async restartOdoo() {
        if (!confirm("Are you sure you want to restart the Odoo service? This will disconnect all users.")) {
            return;
        }

        try {
            // First try without password
            let result = await this.rpc("/developer_terminal/restart_odoo", {});

            // If Docker environment, show instructions
            if (result.is_docker) {
                alert(result.message);
                return;
            }

            // If password required, prompt for it
            if (result.need_password || (result.error && result.error === 'Sudo Password Required')) {
                const password = prompt("Enter sudo password for system restart:");
                if (!password) {
                    this.notification.add("Restart cancelled", { type: "info" });
                    return;
                }

                // Retry with password
                result = await this.rpc("/developer_terminal/restart_odoo", {
                    sudo_password: password
                });
            }

            if (result.error) {
                this.notification.add(result.error + ": " + result.message, { type: "warning" });
            } else {
                this.notification.add(result.message, { type: "success" });
            }

        } catch (error) {
            this.notification.add("Failed to restart Odoo", { type: "danger" });
        }
    }

    async clearOldLogs() {
        if (!confirm("Are you sure you want to clear old terminal logs based on retention policy?")) {
            return;
        }

        try {
            const result = await this.rpc("/developer_terminal/clear_logs", {});

            if (result.error) {
                this.notification.add(result.error, { type: "danger" });
            } else {
                this.notification.add(result.message, { type: "success" });
            }

        } catch (error) {
            this.notification.add("Failed to clear logs", { type: "danger" });
        }
    }

    async restartOdooWithCredentials() {
        if (!confirm("Are you sure you want to restart Odoo? This will disconnect all users and reload the page.")) {
            return;
        }

        try {
            const result = await this.rpc("/developer_terminal/restart_odoo", {
                username: this.state.restartUsername || null,
                sudo_password: this.state.restartPassword || null
            });

            if (result.error) {
                this.notification.add(result.error + ": " + result.message, { type: "danger" });
            } else if (result.success) {
                this.notification.add(result.message + " Page will reload in 3 seconds...", { type: "success" });
                this.clearRestartForm();

                // Reload the page after 3 seconds to reconnect to restarted Odoo
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            } else {
                this.notification.add(result.message || "Restart command sent", { type: "info" });
            }

        } catch (error) {
            this.notification.add("Failed to restart Odoo: " + error.message, { type: "danger" });
        }
    }

    clearRestartForm() {
        this.state.restartUsername = "";
        this.state.restartPassword = "";
    }
}

EnvironmentInfo.template = "developer_terminal.EnvironmentInfo";

// Addon Uploader Widget Component
class AddonUploader extends Component {
    setup() {
        this.rpc = useService("rpc");
        this.notification = useService("notification");
        this.state = useState({
            uploadHistory: [],
            isUploading: false,
            uploadProgress: 0,
            selectedFile: null,
            restartUsername: "",
            restartPassword: "",
        });

        onMounted(() => {
            this.loadUploadHistory();
        });
    }

    async loadUploadHistory() {
        try {
            const result = await this.rpc("/developer_terminal/get_upload_history", {
                limit: 20,
            });

            if (result.success) {
                this.state.uploadHistory = result.uploads || [];
            }
        } catch (error) {
            console.error("Error loading upload history:", error);
        }
    }

    onFileSelected(ev) {
        const file = ev.target.files[0];
        if (file) {
            if (!file.name.endsWith('.zip')) {
                this.notification.add("Only .zip files are allowed", { type: "warning" });
                ev.target.value = '';
                return;
            }
            this.state.selectedFile = file;
            this.notification.add(`Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`, { type: "info" });
        }
    }

    async uploadAddon() {
        if (!this.state.selectedFile) {
            this.notification.add("Please select a .zip file first", { type: "warning" });
            return;
        }

        this.state.isUploading = true;
        this.state.uploadProgress = 0;

        try {
            const formData = new FormData();
            formData.append('file', this.state.selectedFile);

            // Upload using XMLHttpRequest for progress tracking
            const result = await new Promise((resolve, reject) => {
                const xhr = new XMLHttpRequest();

                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        this.state.uploadProgress = Math.round((e.loaded / e.total) * 100);
                    }
                });

                xhr.addEventListener('load', () => {
                    if (xhr.status === 200) {
                        try {
                            resolve(JSON.parse(xhr.responseText));
                        } catch (e) {
                            reject(new Error('Invalid response from server'));
                        }
                    } else {
                        reject(new Error(`Upload failed with status ${xhr.status}`));
                    }
                });

                xhr.addEventListener('error', () => reject(new Error('Network error')));
                xhr.addEventListener('abort', () => reject(new Error('Upload cancelled')));

                xhr.open('POST', '/developer_terminal/upload_addon');
                xhr.send(formData);
            });

            if (result.success) {
                this.notification.add(result.message, { type: "success", sticky: true });
                this.state.selectedFile = null;
                document.querySelector('input[type="file"]').value = '';
                await this.loadUploadHistory();
            } else {
                this.notification.add(result.error + ": " + result.message, { type: "danger" });
            }

        } catch (error) {
            this.notification.add("Upload failed: " + error.message, { type: "danger" });
        } finally {
            this.state.isUploading = false;
            this.state.uploadProgress = 0;
        }
    }

    formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / 1024 / 1024).toFixed(2) + ' MB';
    }

    async restartOdooWithCredentials() {
        if (!confirm("Are you sure you want to restart Odoo? This will disconnect all users and reload the page.")) {
            return;
        }

        try {
            const result = await this.rpc("/developer_terminal/restart_odoo", {
                username: this.state.restartUsername || null,
                sudo_password: this.state.restartPassword || null
            });

            if (result.error) {
                this.notification.add(result.error + ": " + result.message, { type: "danger" });
            } else if (result.success) {
                this.notification.add(result.message + " Page will reload in 3 seconds...", { type: "success" });
                this.clearRestartForm();

                // Reload the page after 3 seconds to reconnect to restarted Odoo
                setTimeout(() => {
                    window.location.reload();
                }, 3000);
            } else {
                this.notification.add(result.message || "Restart command sent", { type: "info" });
            }

        } catch (error) {
            this.notification.add("Failed to restart Odoo: " + error.message, { type: "danger" });
        }
    }

    clearRestartForm() {
        this.state.restartUsername = "";
        this.state.restartPassword = "";
    }
}

AddonUploader.template = "developer_terminal.AddonUploader";

// Register widgets
registry.category("actions").add("developer_terminal_widget", DeveloperTerminal);
registry.category("actions").add("developer_terminal_env_info", EnvironmentInfo);
registry.category("actions").add("developer_terminal_addon_uploader", AddonUploader);
