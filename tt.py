import os
import sys
import time
import subprocess
import threading
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import paramiko
import configparser

class SSHGitBackup:
    def __init__(self, notes_path, repo_url, ssh_key_path=None):
        self.notes_path = os.path.abspath(notes_path)
        self.repo_url = repo_url
        self.repo_name = repo_url.split(':')[-1].replace('.git', '')
        self.ssh_key_path = ssh_key_path or self._find_default_ssh_key()
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)

    def _find_default_ssh_key(self):
        default_key_paths = [
            os.path.expanduser('~/.ssh/id_rsa'),
            os.path.expanduser('~/.ssh/id_ed25519')
        ]
        for key_path in default_key_paths:
            if os.path.exists(key_path):
                return key_path
        return None

    def _test_ssh_connection(self):
        try:
            key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('github.com', username='git', pkey=key)
            client.close()
            return True
        except Exception as e:
            self.logger.error(f"SSH Connection Test Failed: {e}")
            return False

    def setup_git_config(self):
        try:
            ssh_command = f"ssh -i {self.ssh_key_path}"
            subprocess.run(['git', 'config', '--global', 'core.sshCommand', ssh_command], check=True)
            self.logger.info("Git SSH configuration updated")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git config failed: {e}")

    def backup(self, force=False):
        try:
            repo_path = os.path.join(os.path.expanduser('~'), self.repo_name.split('/')[-1])
            if not os.path.exists(repo_path):
                subprocess.run(['git', 'clone', self.repo_url, repo_path], check=True)
                self.logger.info(f"Cloned repository to {repo_path}")
            os.chdir(repo_path)
            subprocess.run(['rsync', '-avz', '--delete', f'{self.notes_path}/', f'{repo_path}/'], check=True)
            
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if not status.stdout.strip() and not force:
                self.logger.info("No changes to backup")
                return True
            
            subprocess.run(['git', 'add', '.'], check=True)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            subprocess.run(['git', 'commit', '-m', f'Auto backup: {timestamp}'], check=True)
            subprocess.run(['git', 'push'], check=True)
            self.logger.info(f"Backup completed at {timestamp}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Backup failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git SSH Backup GUI")
        
        tk.Label(root, text="Notes Path:").grid(row=0, column=0)
        self.notes_entry = tk.Entry(root, width=50)
        self.notes_entry.grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_notes_path).grid(row=0, column=2)

        tk.Label(root, text="Repo URL:").grid(row=1, column=0)
        self.repo_entry = tk.Entry(root, width=50)
        self.repo_entry.grid(row=1, column=1)

        tk.Label(root, text="SSH Key Path:").grid(row=2, column=0)
        self.ssh_entry = tk.Entry(root, width=50)
        self.ssh_entry.grid(row=2, column=1)
        tk.Button(root, text="Browse", command=self.browse_ssh_key).grid(row=2, column=2)

        tk.Button(root, text="Start Backup", command=self.start_backup).grid(row=3, column=1)
    
    def browse_notes_path(self):
        path = filedialog.askdirectory()
        self.notes_entry.insert(0, path)
    
    def browse_ssh_key(self):
        path = filedialog.askopenfilename(filetypes=[("Private Keys", "*.pem *.rsa *.ed25519")])
        self.ssh_entry.insert(0, path)

    def start_backup(self):
        notes_path = self.notes_entry.get()
        repo_url = self.repo_entry.get()
        ssh_key_path = self.ssh_entry.get()

        if not all([notes_path, repo_url, ssh_key_path]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        backup = SSHGitBackup(notes_path, repo_url, ssh_key_path)
        if backup._test_ssh_connection():
            backup.setup_git_config()
            success = backup.backup(force=True)
            if success:
                messagebox.showinfo("Success", "Backup completed successfully!")
            else:
                messagebox.showerror("Error", "Backup failed. Check logs.")
        else:
            messagebox.showerror("SSH Error", "SSH connection failed. Check your SSH key.")

if __name__ == '__main__':
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
