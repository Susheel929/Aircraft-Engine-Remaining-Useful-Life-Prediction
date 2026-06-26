#!/usr/bin/env python3
"""
Aircraft Engine RUL Dashboard - Automated Setup & Launcher
Simplifies installation and startup of the entire application
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
import platform

class Dashboard:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        self.python_exe = sys.executable
        self.venv_dir = self.project_dir / "venv"
        self.requirements_file = self.project_dir / "requirements.txt"
        
    def print_header(self):
        print("\n" + "="*60)
        print("🛩️  AIRCRAFT ENGINE RUL PREDICTION DASHBOARD")
        print("="*60 + "\n")
    
    def check_python(self):
        """Check if Python version is adequate"""
        print("✓ Checking Python version...", end=" ")
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"Python {version.major}.{version.minor} ✓")
            return True
        else:
            print(f"✗ Python 3.8+ required (found {version.major}.{version.minor})")
            return False
    
    def check_requirements_file(self):
        """Check if requirements.txt exists"""
        print("✓ Checking requirements.txt...", end=" ")
        if self.requirements_file.exists():
            print("Found ✓")
            return True
        else:
            print("✗ Not found")
            return False
    
    def create_venv(self):
        """Create virtual environment"""
        print("✓ Creating virtual environment...", end=" ")
        try:
            subprocess.run([self.python_exe, "-m", "venv", str(self.venv_dir)], 
                         check=True, capture_output=True)
            print("Created ✓")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed: {e}")
            return False
    
    def get_pip_executable(self):
        """Get the pip executable path"""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "pip.exe"
        else:
            return self.venv_dir / "bin" / "pip"
    
    def get_python_executable(self):
        """Get the python executable path"""
        if platform.system() == "Windows":
            return self.venv_dir / "Scripts" / "python.exe"
        else:
            return self.venv_dir / "bin" / "python"
    
    def install_dependencies(self):
        """Install Python dependencies"""
        print("✓ Installing dependencies (this may take 5-10 minutes)...", end=" ", flush=True)
        pip_exe = self.get_pip_executable()
        
        try:
            # Upgrade pip first
            subprocess.run([str(pip_exe), "install", "--upgrade", "pip"], 
                         check=True, capture_output=True, timeout=60)
            
            # Install requirements
            subprocess.run([str(pip_exe), "install", "-r", str(self.requirements_file)], 
                         check=True, capture_output=True, timeout=300)
            print("Installed ✓")
            return True
        except subprocess.TimeoutExpired:
            print("✗ Installation timed out (network issue?)")
            return False
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed: {e}")
            return False
    
    def check_backend_file(self):
        """Check if backend.py exists"""
        print("✓ Checking backend.py...", end=" ")
        backend_file = self.project_dir / "backend.py"
        if backend_file.exists():
            print("Found ✓")
            return True
        else:
            print("✗ Not found")
            return False
    
    def check_dashboard_file(self):
        """Check if dashboard.html exists"""
        print("✓ Checking dashboard.html...", end=" ")
        dashboard_file = self.project_dir / "dashboard.html"
        if dashboard_file.exists():
            print("Found ✓")
            return True
        else:
            print("✗ Not found")
            return False
    
    def start_backend(self):
        """Start the Flask backend server"""
        print("\n" + "="*60)
        print("🚀 STARTING BACKEND SERVER")
        print("="*60)
        
        python_exe = self.get_python_executable()
        backend_file = self.project_dir / "backend.py"
        
        try:
            process = subprocess.Popen(
                [str(python_exe), str(backend_file)],
                cwd=str(self.project_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for server to start
            print("\n⏳ Waiting for server to initialize...")
            time.sleep(3)
            
            # Check if process is still running
            if process.poll() is None:
                print("✓ Backend server started successfully!")
                print("📍 Server running on: http://localhost:5000")
                return process
            else:
                stdout, stderr = process.communicate()
                print(f"✗ Backend failed to start:\n{stderr}")
                return None
        
        except Exception as e:
            print(f"✗ Failed to start backend: {e}")
            return None
    
    def open_dashboard(self):
        """Open dashboard in browser"""
        dashboard_file = self.project_dir / "dashboard.html"
        dashboard_url = dashboard_file.as_uri()
        
        print("\n" + "="*60)
        print("🌐 OPENING DASHBOARD")
        print("="*60)
        print(f"\n📂 Dashboard file: {dashboard_file}")
        print(f"🔗 URL: {dashboard_url}\n")
        
        try:
            webbrowser.open(dashboard_url)
            print("✓ Dashboard opened in your default browser!")
        except Exception as e:
            print(f"⚠ Could not auto-open browser: {e}")
            print(f"📌 Manually open this URL: {dashboard_url}")
    
    def print_instructions(self):
        """Print final instructions"""
        print("\n" + "="*60)
        print("📋 QUICK START GUIDE")
        print("="*60 + "\n")
        
        print("✅ Everything is set up! You're ready to go.\n")
        
        print("📊 Dashboard URL:")
        dashboard_file = self.project_dir / "dashboard.html"
        print(f"   {dashboard_file.as_uri()}\n")
        
        print("🔌 API Base URL:")
        print("   http://localhost:5000/api\n")
        
        print("🧪 Test the API:")
        print("   curl http://localhost:5000/api/health\n")
        
        print("📖 Full documentation:")
        print(f"   {self.project_dir / 'SETUP_GUIDE.md'}\n")
        
        print("⚙️  Available API Endpoints:")
        endpoints = [
            ("GET", "/api/engines", "Get all engines"),
            ("GET", "/api/engine/<id>", "Get engine details"),
            ("GET", "/api/models", "Get model performance"),
            ("GET", "/api/overview", "Get fleet overview"),
            ("POST", "/api/predict", "Run RUL prediction"),
            ("POST", "/api/maintenance-schedule", "Get maintenance plan"),
        ]
        
        for method, endpoint, desc in endpoints:
            print(f"   {method:6} {endpoint:30} - {desc}")
        
        print("\n💡 Tips:")
        print("   • Refresh dashboard if API call fails initially")
        print("   • Backend training takes ~30 seconds on first run")
        print("   • Use LSTM model for best accuracy")
        print("   • Check browser console (F12) for detailed errors")
        print("\n" + "="*60 + "\n")
    
    def run_setup(self):
        """Run complete setup"""
        self.print_header()
        
        # Checks
        print("📋 SYSTEM CHECKS\n")
        
        if not self.check_python():
            print("\n❌ Setup failed: Python 3.8+ required")
            return False
        
        if not self.check_requirements_file():
            print("\n❌ Setup failed: requirements.txt not found")
            return False
        
        if not self.check_backend_file():
            print("\n❌ Setup failed: backend.py not found")
            return False
        
        if not self.check_dashboard_file():
            print("\n❌ Setup failed: dashboard.html not found")
            return False
        
        # Setup
        print("\n📦 INSTALLATION\n")
        
        # Check if venv already exists
        if not self.venv_dir.exists():
            if not self.create_venv():
                print("\n❌ Setup failed: Could not create virtual environment")
                return False
            
            if not self.install_dependencies():
                print("\n❌ Setup failed: Could not install dependencies")
                print("\n💡 Tip: Try installing manually:")
                print(f"   pip install -r {self.requirements_file}")
                return False
        else:
            print(f"✓ Virtual environment already exists")
            pip_exe = self.get_pip_executable()
            if pip_exe.exists():
                print("✓ Dependencies appear to be installed")
            else:
                print("⚠ Virtual environment may be incomplete")
        
        # Start backend
        backend_process = self.start_backend()
        if not backend_process:
            print("\n❌ Failed to start backend server")
            return False
        
        # Open dashboard
        self.open_dashboard()
        
        # Print instructions
        self.print_instructions()
        
        print("⏰ Backend is running. Press Ctrl+C to stop.\n")
        
        # Keep the backend running
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Shutting down backend server...")
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("✓ Backend stopped")
        
        return True

def main():
    """Main entry point"""
    launcher = Dashboard()
    
    success = launcher.run_setup()
    
    if not success:
        print("\n❌ Setup encountered errors. Please check above for details.")
        print("📖 For help, see SETUP_GUIDE.md")
        sys.exit(1)

if __name__ == "__main__":
    main()
