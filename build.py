#!/usr/bin/env python3
"""
Build script for Terminal Chat Client
Creates standalone executables for Windows and Linux
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, cwd=cwd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return False

def create_spec_file():
    """Create PyInstaller spec file"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'textual',
        'rich',
        'websockets',
        'requests',
        'pydantic',
        'asyncio',
        'pyaudio',
        'aiortc',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='terminal-chat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if platform.system() == 'Windows' else None,
)
'''
    
    with open('terminal-chat.spec', 'w') as f:
        f.write(spec_content)

def build_client():
    """Build the client executable"""
    print("Building Terminal Chat Client...")
    
    # Change to client directory
    client_dir = Path(__file__).parent / "client"
    os.chdir(client_dir)
    
    # Create spec file
    create_spec_file()
    
    # Install dependencies
    print("Installing dependencies...")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("Failed to install dependencies")
        return False
    
    # Build with PyInstaller
    print("Building executable...")
    if not run_command("pyinstaller terminal-chat.spec --clean"):
        print("Failed to build executable")
        return False
    
    # Move executable to dist folder in root
    root_dist = Path(__file__).parent / "dist"
    root_dist.mkdir(exist_ok=True)
    
    exe_name = "terminal-chat.exe" if platform.system() == "Windows" else "terminal-chat"
    source_exe = client_dir / "dist" / exe_name
    target_exe = root_dist / exe_name
    
    if source_exe.exists():
        shutil.copy2(source_exe, target_exe)
        print(f"Executable created: {target_exe}")
        return True
    else:
        print("Executable not found after build")
        return False

def create_installer_script():
    """Create installation script"""
    if platform.system() == "Windows":
        installer_content = '''@echo off
echo Installing Terminal Chat...

REM Copy executable to Program Files
if not exist "%ProgramFiles%\\TerminalChat" mkdir "%ProgramFiles%\\TerminalChat"
copy terminal-chat.exe "%ProgramFiles%\\TerminalChat\\"

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\Terminal Chat.lnk'); $Shortcut.TargetPath = '%ProgramFiles%\\TerminalChat\\terminal-chat.exe'; $Shortcut.Save()"

REM Add to PATH (optional)
echo Adding to system PATH...
setx PATH "%PATH%;%ProgramFiles%\\TerminalChat"

echo Installation complete!
echo You can now run Terminal Chat from anywhere by typing 'terminal-chat'
pause
'''
        with open("install.bat", "w") as f:
            f.write(installer_content)
    
    else:  # Linux
        installer_content = '''#!/bin/bash
echo "Installing Terminal Chat..."

# Copy executable to /usr/local/bin
sudo cp terminal-chat /usr/local/bin/
sudo chmod +x /usr/local/bin/terminal-chat

# Create desktop entry
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/terminal-chat.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Terminal Chat
Comment=Minimalist terminal-based chat client
Exec=/usr/local/bin/terminal-chat
Terminal=true
Categories=Network;Chat;
EOF

echo "Installation complete!"
echo "You can now run Terminal Chat from anywhere by typing 'terminal-chat'"
'''
        with open("install.sh", "w") as f:
            f.write(installer_content)
        os.chmod("install.sh", 0o755)

def main():
    """Main build function"""
    print("=" * 50)
    print("Terminal Chat - Build Script")
    print("=" * 50)
    
    # Build client
    if not build_client():
        print("Build failed!")
        sys.exit(1)
    
    # Create installer
    create_installer_script()
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print(f"Platform: {platform.system()} {platform.architecture()[0]}")
    print(f"Executable: dist/terminal-chat{'exe' if platform.system() == 'Windows' else ''}")
    print(f"Installer: install.{'bat' if platform.system() == 'Windows' else 'sh'}")
    print("\nTo install:")
    if platform.system() == "Windows":
        print("  Run install.bat as Administrator")
    else:
        print("  Run ./install.sh")

if __name__ == "__main__":
    main()