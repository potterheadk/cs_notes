import os
import sys
import time
import subprocess
import threading
import logging
import watchdog.observers
import watchdog.events
import schedule
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import paramiko
import configparser

class SSHGitBackup:
    def __init__(self, notes_path, repo_url, ssh_key_path=None):
        """
        Initialize SSH-based Git Backup
        
        :param notes_path: Local path to notes directory
        :param repo_url: SSH repository URL (git@github.com:user/repo.git)
        :param ssh_key_path: Optional custom SSH key path
        """
        self.notes_path = os.path.abspath(notes_path)
        self.repo_url = repo_url
        self.repo_name = repo_url.split(':')[-1].replace('.git', '')
        
        # Determine SSH key path
        self.ssh_key_path = ssh_key_path or self._find_default_ssh_key()
        
        # Logging setup
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def _find_default_ssh_key(self):
        """
        Find default SSH keys in standard locations
        
        :return: Path to SSH private key
        """
        default_key_paths = [
            os.path.expanduser('~/.ssh/id_rsa'),
            os.path.expanduser('~/.ssh/id_ed25519'),
            os.path.expanduser('~/.ssh/github_rsa')
        ]
        
        for key_path in default_key_paths:
            if os.path.exists(key_path):
                return key_path
        
        return None
    
    def _test_ssh_connection(self):
        """
        Test SSH connection to GitHub
        
        :return: Boolean indicating successful connection
        """
        try:
            # Use paramiko to test SSH connection
            key = paramiko.RSAKey.from_private_key_file(self.ssh_key_path)
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            client.connect(
                'github.com', 
                username='git', 
                pkey=key
            )
            client.close()
            return True
        except Exception as e:
            self.logger.error(f"SSH Connection Test Failed: {e}")
            return False
    
    def setup_git_config(self):
        """
        Configure Git to use SSH key
        """
        try:
            # Set SSH command with specific key
            ssh_command = f"ssh -i {self.ssh_key_path}"
            subprocess.run([
                'git', 'config', '--global', 
                'core.sshCommand', 
                ssh_command
            ], check=True)
            
            self.logger.info("Git SSH configuration updated")
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Git config failed: {e}")
    
    def clone_or_sync_repo(self):
        """
        Clone repository if not exists, or pull latest changes
        """
        repo_path = os.path.join(
            os.path.expanduser('~'), 
            self.repo_name.split('/')[-1]
        )
        
        if not os.path.exists(repo_path):
            # Clone repository
            try:
                subprocess.run([
                    'git', 'clone', 
                    self.repo_url, 
                    repo_path
                ], check=True)
                self.logger.info(f"Cloned repository to {repo_path}")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Repository clone failed: {e}")
                return None
        
        return repo_path
    
    def backup(self, force=False):
        """
        Perform backup to GitHub
        
        :param force: Force backup even without changes
        """
        try:
            repo_path = self.clone_or_sync_repo()
            if not repo_path:
                return False
            
            os.chdir(repo_path)
            
            # Copy notes to repository
            sync_command = [
                'rsync', '-avz', 
                '--delete',  # Ensure mirror sync
                f'{self.notes_path}/', 
                f'{repo_path}/'
            ]
            subprocess.run(sync_command, check=True)
            
            # Check for changes
            status = subprocess.run(
                ['git', 'status', '--porcelain'], 
                capture_output=True, 
                text=True
            )
            
            if not status.stdout.strip() and not force:
                self.logger.info("No changes to backup")
                return True
            
            # Stage changes
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            subprocess.run([
                'git', 'commit', 
                '-m', f'Auto backup: {timestamp}'
            ], check=True)
            
            # Push changes
            subprocess.run(['git', 'push'], check=True)
            
            self.logger.info(f"Backup completed at {timestamp}")
            return True
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Backup failed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Unexpected backup error: {e}")
            return False

class BackupConfigManager:
    @staticmethod
    def save_config(notes_path, repo_url, ssh_key_path):
        """
        Save backup configuration to config file
        """
        config = configparser.ConfigParser()
        config['BACKUP'] = {
            'notes_path': notes_path,
            'repo_url': repo_url,
            'ssh_key_path': ssh_key_path
        }
        
        config_dir = os.path.expanduser('~/.config/obsidian-backup')
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, 'config.ini'), 'w') as configfile:
            config.write(configfile)
    
    @staticmethod
    def load_config():
        """
        Load backup configuration
        """
        config_path = os.path.expanduser('~/.config/obsidian-backup/config.ini')
        if not os.path.exists(config_path):
            return None
        
        config = configparser.ConfigParser()
        config.read(config_path)
        
        return dict(config['BACKUP']) if 'BACKUP' in config else None

def main():
    # Example usage
    notes_path = '/home/turtle_secure/Documents/notes_ALL/cs_notes'
    repo_url = 'git@github.com:user/repo.git'
    ssh_key_path = '/home/turtle_secure/Documents/notes_ALL/cs_notes/id_rsa.pub'
    
    backup = SSHGitBackup(notes_path, repo_url, ssh_key_path)
    
    # Test SSH connection
    if backup._test_ssh_connection():
        backup.setup_git_config()
        backup.backup(force=True)
    else:
        print("SSH connection failed. Check your SSH key.")

if __name__ == '__main__':
    main()