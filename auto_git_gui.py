import os
import time
import subprocess
import logging
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import paramiko
from datetime import datetime
import re
import shutil

class SSHGitBackup:
    def __init__(self, notes_path, repo_url, ssh_key_path=None, branch='main'):
        self.notes_path = os.path.abspath(notes_path)
        self.repo_url = repo_url
        self.branch = branch
        self.repo_name = self._extract_repo_name(repo_url)
        self.ssh_key_path = ssh_key_path or self._find_default_ssh_key()
        self.backup_status = {}  # Track backup status of individual files

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
        self.logger = logging.getLogger(__name__)

    def _extract_repo_name(self, repo_url):
        """Extract repository name from URL handling different formats."""
        if match := re.search(r'[:/]([^/]+?/[^/]+?)(?:\.git)?$', repo_url):
            return match.group(1).replace('/', '_')
        return 'backup_repo'

    def _find_default_ssh_key(self):
        """Find default SSH key with expanded key types."""
        key_types = ['id_rsa', 'id_ed25519', 'id_ecdsa', 'id_dsa']
        for key_type in key_types:
            path = os.path.expanduser(f'~/.ssh/{key_type}')
            if os.path.exists(path):
                return path
        return None

    def _test_ssh_connection(self):
        """Test SSH connection with improved error handling."""
        try:
            if self.ssh_key_path.endswith('.pub'):
                raise ValueError("Cannot use public key for SSH authentication")

            key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect('github.com', username='git', pkey=key, timeout=10)
            client.close()
            return True
        except paramiko.SSHException as e:
            self.logger.error(f"SSH Authentication failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"SSH Connection Test Failed: {e}")
            return False

    def init_repository(self):
        """Initialize repository if it doesn't exist."""
        try:
            repo_path = os.path.join(os.path.expanduser('~'), self.repo_name)

            if not os.path.exists(repo_path):
                os.makedirs(repo_path)
                os.chdir(repo_path)

                # Initialize git repository
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'checkout', '-b', self.branch], check=True)

                # Configure remote
                subprocess.run(['git', 'remote', 'add', 'origin', self.repo_url], check=True)

                # Create .gitignore
                self._create_gitignore(repo_path)

                self.logger.info(f"Initialized new repository at {repo_path}")
                return True
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Repository initialization failed: {e}")
            return False

    def _create_gitignore(self, repo_path):
        """Create .gitignore with common patterns."""
        gitignore_content = """
        .*
        !.gitignore
        !.github/
        .DS_Store
        Thumbs.db
        *.swp
        *.bak
        *.tmp
        .env
        node_modules/
        __pycache__/
        *.pyc
        """
        with open(os.path.join(repo_path, '.gitignore'), 'w') as f:
            f.write(gitignore_content.strip())

    def setup_git_config(self):
        """Setup git configuration with error handling."""
        try:
            ssh_command = f"ssh -i {self.ssh_key_path} -o StrictHostKeyChecking=no"
            subprocess.run(['git', 'config', '--global', 'core.sshCommand', ssh_command], check=True)
            subprocess.run(['git', 'config', '--global', 'pull.rebase', 'false'], check=True)
            self.logger.info("Git SSH configuration updated")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git config failed: {e}")
            return False


    def init_repository(self):
        """Initialize repository with improved setup."""
        try:
            repo_path = os.path.join(os.path.expanduser('~'), self.repo_name)

            if not os.path.exists(repo_path):
                os.makedirs(repo_path)

            os.chdir(repo_path)

            # Check if git is already initialized
            if not os.path.exists(os.path.join(repo_path, '.git')):
                # Initialize new repository
                subprocess.run(['git', 'init'], check=True)
                subprocess.run(['git', 'checkout', '-b', self.branch], check=True)

                # Configure remote
                try:
                    subprocess.run(['git', 'remote', 'remove', 'origin'], check=True)
                except subprocess.CalledProcessError:
                    pass  # Ignore if remote doesn't exist

                subprocess.run(['git', 'remote', 'add', 'origin', self.repo_url], check=True)

                # Create .gitignore
                self._create_gitignore(repo_path)

                # Make initial commit if needed
                try:
                    subprocess.run(['git', 'add', '.gitignore'], check=True)
                    subprocess.run(['git', 'commit', '-m', "Initial commit: Setup repository"], check=True)
                except subprocess.CalledProcessError:
                    pass  # Ignore if commit fails

            self.logger.info(f"Repository ready at {repo_path}")
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Repository initialization failed: {e}")
            return False

    def _clean_submodule_state(self):
        """Clean up problematic submodule state."""
        try:
            # Remove submodule from .gitmodules if it exists
            if os.path.exists('.gitmodules'):
                subprocess.run(['git', 'config', '--file', '.gitmodules', '--remove-section',
                              'submodule.Turtle_notes/cs_notes'], check=False)

            # Remove submodule from .git/config
            subprocess.run(['git', 'config', '--remove-section',
                           'submodule.Turtle_notes/cs_notes'], check=False)

            # Clean up submodule directories
            subprocess.run(['git', 'rm', '--cached', '-f', 'Turtle_notes/cs_notes'], check=False)

            # Remove the submodule directory from .git
            git_submodule_path = os.path.join('.git', 'modules', 'Turtle_notes/cs_notes')
            if os.path.exists(git_submodule_path):
                shutil.rmtree(git_submodule_path, ignore_errors=True)

            # Commit the cleanup if there are changes
            try:
                subprocess.run(['git', 'add', '.gitmodules'], check=False)
                subprocess.run(['git', 'commit', '-m', "Clean up submodule state"], check=False)
            except:
                pass

            return True
        except Exception as e:
            self.logger.error(f"Error cleaning submodule state: {e}")
            return False

    def _initialize_submodule(self, submodule_path):
        """Initialize a submodule with proper error handling."""
        try:
            # Get absolute path of the submodule
            abs_submodule_path = os.path.join(self.notes_path, 'Turtle_notes/cs_notes')
            rel_submodule_path = 'Turtle_notes/cs_notes'

            # Check if it's already a submodule
            submodule_status = subprocess.run(
                ['git', 'submodule', 'status', rel_submodule_path],
                capture_output=True,
                text=True
            ).stdout.strip()

            if not submodule_status:
                # Clean up any existing problematic state
                self._clean_submodule_state()

                # Initialize new submodule
                try:
                    # First, check if the target directory exists and is a git repo
                    target_git_dir = os.path.join(abs_submodule_path, '.git')
                    if os.path.exists(target_git_dir):
                        # Get the remote URL from the existing repository
                        os.chdir(abs_submodule_path)
                        remote_url = subprocess.run(
                            ['git', 'config', '--get', 'remote.origin.url'],
                            capture_output=True,
                            text=True
                        ).stdout.strip()
                        os.chdir(self.repo_path)

                        if remote_url:
                            # Add submodule using the existing remote URL
                            subprocess.run(['git', 'submodule', 'add', remote_url, rel_submodule_path], check=True)
                        else:
                            raise Exception("No remote URL found in existing repository")
                    else:
                        raise Exception("Target directory is not a git repository")

                except subprocess.CalledProcessError as e:
                    if "already exists in the index" in str(e.stderr):
                        # If it's already in the index, try to recover
                        subprocess.run(['git', 'submodule', 'init'], check=False)
                        subprocess.run(['git', 'submodule', 'update'], check=False)
                    else:
                        raise

            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize submodule: {e}")
            return False

    def backup(self, force=False):
        """Improved backup method with enhanced submodule handling."""
        try:
            repo_path = os.path.join(os.path.expanduser('~'), self.repo_name)
            self.repo_path = repo_path

            # Initialize repository if needed
            if not self.init_repository():
                return False

            os.chdir(repo_path)

            # Initialize submodule with error handling
            submodule_success = self._initialize_submodule('Turtle_notes/cs_notes')
            if not submodule_success:
                self.logger.warning("Continuing backup without submodule initialization")

            # Sync files
            self._sync_files(self.notes_path, repo_path)

            # Try to update submodules if they exist
            try:
                subprocess.run(['git', 'submodule', 'foreach', 'git', 'add', '-A'], check=False)
                subprocess.run(['git', 'submodule', 'foreach', 'git', 'commit', '-m',
                              f"Submodule update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"],
                              check=False)
            except Exception as e:
                self.logger.warning(f"Submodule update warning: {e}")

            # Add all changes including submodule references
            subprocess.run(['git', 'add', '-A'], check=True)

            # Get status
            status_output = subprocess.run(
                ['git', 'status', '--porcelain'],
                capture_output=True,
                text=True
            ).stdout.strip()

            if status_output or force:
                # Create commit with detailed message
                commit_msg = self._generate_commit_message()

                try:
                    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                except subprocess.CalledProcessError as e:
                    if "nothing to commit" not in str(e.stderr):
                        raise
                    self.logger.info("No changes to commit")
                    return True

                # Pull and push with error handling
                try:
                    subprocess.run(['git', 'pull', '--no-rebase'], check=True)
                except subprocess.CalledProcessError:
                    self.logger.warning("Pull failed, attempting to continue")

                try:
                    subprocess.run(['git', 'push', 'origin', self.branch], check=True)
                except subprocess.CalledProcessError:
                    self.logger.warning("Normal push failed, attempting force push")
                    subprocess.run(['git', 'push', '-f', 'origin', self.branch], check=True)

                self.logger.info("Changes successfully pushed to repository")
                return True
            else:
                self.logger.info("No changes detected to backup")
                return True

        except subprocess.CalledProcessError as e:
            error_message = str(e)
            if hasattr(e, 'stderr') and e.stderr:
                error_message = e.stderr.decode()
            self.logger.error(f"Backup failed: {error_message}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return False

    def _sync_files(self, source, destination):
        """Improved sync method with better change detection."""
        try:
            # Reset backup status for new sync
            self.backup_status = {}

            # Ensure destination directory exists
            os.makedirs(destination, exist_ok=True)

            # Get lists of files
            source_files = set()
            for root, _, files in os.walk(source):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), source)
                    source_files.add(rel_path)

            dest_files = set()
            for root, _, files in os.walk(destination):
                if '.git' not in root.split(os.sep):  # Skip .git directory
                    for file in files:
                        rel_path = os.path.relpath(os.path.join(root, file), destination)
                        dest_files.add(rel_path)

            # Copy new and modified files
            for rel_path in source_files:
                src_file = os.path.join(source, rel_path)
                dest_file = os.path.join(destination, rel_path)

                # Create destination directory if needed
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

                try:
                    # Copy if file is new or modified
                    if not os.path.exists(dest_file) or \
                       os.path.getmtime(src_file) > os.path.getmtime(dest_file) or \
                       os.path.getsize(src_file) != os.path.getsize(dest_file):
                        shutil.copy2(src_file, dest_file)
                        self.backup_status[rel_path] = 'updated'
                        self.logger.info(f"Updated: {rel_path}")
                except Exception as e:
                    self.logger.error(f"Failed to copy {rel_path}: {e}")
                    self.backup_status[rel_path] = 'failed'

            # Remove deleted files
            for rel_path in dest_files - source_files:
                if not rel_path.startswith('.git'):  # Skip .git files
                    try:
                        file_to_delete = os.path.join(destination, rel_path)
                        if os.path.exists(file_to_delete):
                            os.remove(file_to_delete)
                            self.backup_status[rel_path] = 'deleted'
                            self.logger.info(f"Deleted: {rel_path}")
                    except Exception as e:
                        self.logger.error(f"Failed to delete {rel_path}: {e}")

            # Remove empty directories
            for root, dirs, _ in os.walk(destination, topdown=False):
                for dir_name in dirs:
                    dir_path = os.path.join(root, dir_name)
                    if '.git' not in dir_path and not os.listdir(dir_path):
                        os.rmdir(dir_path)
                        self.logger.info(f"Removed empty directory: {dir_path}")

        except Exception as e:
            self.logger.error(f"Sync error: {e}")
            raise

    def _generate_commit_message(self):
        """Generate detailed commit message including deletions."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_files = len([f for f, status in self.backup_status.items() if status == 'updated'])
        deleted_files = len([f for f, status in self.backup_status.items() if status == 'deleted'])
        failed_files = len([f for f, status in self.backup_status.items() if status == 'failed'])

        msg = f"Backup: {timestamp}\n\n"
        if updated_files > 0:
            msg += f"Files updated: {updated_files}\n"
        if deleted_files > 0:
            msg += f"Files deleted: {deleted_files}\n"
        if failed_files > 0:
            msg += f"Files failed: {failed_files}\n"
        return msg

    def handle_git_pull(self):
        """Enhanced git pull handling."""
        try:
            subprocess.run(['git', 'fetch', 'origin'], check=True)
            subprocess.run(['git', 'pull', '--no-rebase'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            if "CONFLICT" in subprocess.run(['git', 'status'], capture_output=True, text=True).stdout:
                self.logger.error("Merge conflicts detected")
                self._handle_conflicts()
                return False
            self.logger.error(f"Pull failed: {e}")
            return False

    def _handle_conflicts(self):
        """Handle merge conflicts."""
        try:
            # Create backup of conflicted files
            status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
            for line in status.stdout.splitlines():
                if line.startswith('UU'):
                    file_path = line[3:].strip()
                    backup_path = f"{file_path}.backup"
                    shutil.copy2(file_path, backup_path)
                    self.logger.info(f"Created backup of conflicted file: {backup_path}")

            # Reset to pre-conflict state
            subprocess.run(['git', 'reset', '--hard', 'HEAD'], check=True)
            self.logger.info("Reset to pre-conflict state")
        except Exception as e:
            self.logger.error(f"Error handling conflicts: {e}")

# BackupApp class and other UI methods...

class BackupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Git SSH Backup Tool")
        self.root.geometry("800x600")
        self.create_widgets()
        self.backup_thread = None
        self.is_backing_up = False

    def create_widgets(self):
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Backup Settings", padding="10")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)

        # Grid layout for settings
        self.notes_path_entry = self._create_path_entry(settings_frame, "Notes Path:", 0, self.browse_notes_path)
        self._create_repo_url_entry(settings_frame, "Repository URL:", 1)
        self._create_ssh_key_entry(settings_frame, "SSH Key Path:", 2, self.browse_ssh_key)
        self._create_branch_entry(settings_frame, "Branch:", 3)

        # Backup button
        self.backup_button = ttk.Button(main_frame, text="Start Backup", command=self.start_backup)
        self.backup_button.pack(pady=10)

        # Status text box
        self.status_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _create_path_entry(self, parent, label_text, row, browse_command):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        path_entry = ttk.Entry(parent, width=50)
        path_entry.grid(row=row, column=1, padx=5, pady=5)
        browse_button = ttk.Button(parent, text="Browse", command=browse_command)
        browse_button.grid(row=row, column=2, padx=5, pady=5)
        return path_entry

    def _create_repo_url_entry(self, parent, label_text, row):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.repo_url_entry = ttk.Entry(parent, width=50)
        self.repo_url_entry.grid(row=row, column=1, padx=5, pady=5)

    def _create_ssh_key_entry(self, parent, label_text, row, browse_command):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.ssh_key_entry = ttk.Entry(parent, width=50)
        self.ssh_key_entry.grid(row=row, column=1, padx=5, pady=5)
        browse_button = ttk.Button(parent, text="Browse", command=browse_command)
        browse_button.grid(row=row, column=2, padx=5, pady=5)

    def _create_branch_entry(self, parent, label_text, row):
        label = ttk.Label(parent, text=label_text)
        label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)
        self.branch_entry = ttk.Entry(parent, width=50)
        self.branch_entry.grid(row=row, column=1, padx=5, pady=5)

    def browse_notes_path(self):
        path = filedialog.askdirectory()
        if path:
            self.notes_path_entry.delete(0, tk.END)
            self.notes_path_entry.insert(0, path)



    def browse_ssh_key(self):
        # Open the file dialog with filter for RSA files and all files
        ssh_key_path = filedialog.askopenfilename(
            title="Select SSH Key",
            filetypes=[("RSA Key Files", "*.rsa"), ("All Files", "*.*")]
        )

        # If the user selects a file, update the entry
        if ssh_key_path:
            self.ssh_key_entry.delete(0, tk.END)  # Clear the entry
            self.ssh_key_entry.insert(0, ssh_key_path)

    def start_backup(self):
        if self.is_backing_up:
            messagebox.showinfo("Backup In Progress", "A backup is already in progress.")
            return

        # Gather input values
        notes_path = self.notes_path_entry.get()
        repo_url = self.repo_url_entry.get()
        ssh_key_path = self.ssh_key_entry.get()
        branch = self.branch_entry.get() or 'main'

        # Initialize backup process
        backup = SSHGitBackup(notes_path, repo_url, ssh_key_path, branch)
        self.is_backing_up = True
        self.update_status("Starting backup...")

        self.backup_thread = threading.Thread(target=self.run_backup, args=(backup,))
        self.backup_thread.start()

    def run_backup(self, backup):
        success = backup.backup()
        self.is_backing_up = False
        if success:
            self.update_status("Backup completed successfully.")
        else:
            self.update_status("Backup failed. Check the logs for more details.")

    def update_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.yview(tk.END)
        self.status_text.config(state=tk.DISABLED)

# Running the application
if __name__ == "__main__":
    root = tk.Tk()
    app = BackupApp(root)
    root.mainloop()
