import os
import time
import subprocess
import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import paramiko

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

            # Sync files
            subprocess.run(['rsync', '-avz', '--delete', f'{self.notes_path}/', f'{repo_path}/'], check=True)

            # Check if there are changes
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if not status.stdout.strip() and not force:
                self.logger.info("No changes to backup")
                return True

            subprocess.run(['git', 'add', '.'], check=True)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            subprocess.run(['git', 'commit', '-m', f'Auto backup: {timestamp}'], check=True)

            # Handle remote changes before pushing
            if not self.handle_git_pull():
                self.logger.error("Cannot push: Pull failed or conflicts unresolved.")
                return False

            subprocess.run(['git', 'push'], check=True)
            self.logger.info(f"Backup completed at {timestamp}")
            return True

        except subprocess.CalledProcessError as e:
            self.logger.error(f"Backup failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False


    def handle_git_pull(self):
        try:
            subprocess.run(['git', 'pull', '--rebase'], check=True)
            self.logger.info("Pulled latest changes with rebase.")
            return True  # No conflicts detected
        except subprocess.CalledProcessError as e:
            self.logger.warning(f"Git pull/rebase failed: {e}")
            if "CONFLICT" in subprocess.run(['git', 'status'], capture_output=True, text=True).stdout:
                self.logger.error("Merge conflicts detected during rebase.")
                subprocess.run(['git', 'rebase', '--abort'], check=True)
                return False  # Aborted due to conflicts
            return False  # Other errors


    def handle_merge_conflicts(self):
        try:
            # Check for conflicts after the rebase
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            if "UU" in status.stdout:  # "UU" indicates unresolved conflicts
                self.logger.warning("Merge conflicts detected.")
                subprocess.run(['git', 'rebase', '--abort'], check=True)  # Abort rebase to avoid broken state
                return False
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Error handling merge conflicts: {e}")
            return False



class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git SSH Backup GUI")
        self.create_widgets()

    def create_widgets(self):
        # Path selection frame
        frame = tk.LabelFrame(self.root, text="Backup Settings", padx=10, pady=10)
        frame.pack(padx=10, pady=10, fill="both", expand="yes")

        tk.Label(frame, text="Notes Path:").grid(row=0, column=0, sticky='w')
        self.notes_entry = tk.Entry(frame, width=50)
        self.notes_entry.grid(row=0, column=1)
        tk.Button(frame, text="Browse", command=self.browse_notes_path).grid(row=0, column=2)

        tk.Label(frame, text="Repo URL:").grid(row=1, column=0, sticky='w')
        self.repo_entry = tk.Entry(frame, width=50)
        self.repo_entry.grid(row=1, column=1, columnspan=2)

        tk.Label(frame, text="SSH Key Path:").grid(row=2, column=0, sticky='w')
        self.ssh_entry = tk.Entry(frame, width=50)
        self.ssh_entry.grid(row=2, column=1)
        tk.Button(frame, text="Browse", command=self.browse_ssh_key).grid(row=2, column=2)

        # Start button and progress bar
        self.start_button = tk.Button(root, text="Start Backup", command=self.start_backup)
        self.start_button.pack(pady=5)

        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=5)

        # Log display
        self.log_display = scrolledtext.ScrolledText(root, height=15, width=80)
        self.log_display.pack(pady=10)
        self.redirect_logs()

    def browse_notes_path(self):
        path = filedialog.askdirectory()
        if path:
            self.notes_entry.delete(0, tk.END)
            self.notes_entry.insert(0, path)

    def browse_ssh_key(self):
        path = filedialog.askopenfilename(filetypes=[("Private Keys", "*.pem *.rsa *.ed25519")])
        if path:
            self.ssh_entry.delete(0, tk.END)
            self.ssh_entry.insert(0, path)

    def start_backup(self):
        notes_path = self.notes_entry.get()
        repo_url = self.repo_entry.get()
        ssh_key_path = self.ssh_entry.get()

        if not all([notes_path, repo_url, ssh_key_path]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return


        threading.Thread(target=self.run_backup, args=(notes_path, repo_url, ssh_key_path)).start()

    def run_backup(self, notes_path, repo_url, ssh_key_path):
        backup = SSHGitBackup(notes_path, repo_url, ssh_key_path)
        self.progress.start()
        if backup._test_ssh_connection():
            backup.setup_git_config()
            success = backup.backup(force=True)
            self.progress.stop()
            if success:
                messagebox.showinfo("Success", "Backup completed successfully!")
            else:
                messagebox.showerror("Error", "Backup failed. Check logs.")
        else:
            self.progress.stop()
            messagebox.showerror("SSH Error", "SSH connection failed. Check your SSH key.")

    def redirect_logs(self):
        logging.getLogger().addHandler(logging.StreamHandler(self))

    def write(self, message):
        self.log_display.insert(tk.END, message)
        self.log_display.see(tk.END)

    def flush(self):
        pass

if __name__ == '__main__':
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
