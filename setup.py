#!/usr/bin/env python3
"""
Setup and Installation Script for MedGemma HealthConnect
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible"""
    print_header("Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("⚠️  Virtual environment already exists")
        response = input("   Recreate? (y/n): ")
        if response.lower() != 'y':
            return True
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment created")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to create virtual environment")
        return False


def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    # Determine pip path
    if os.name == 'nt':  # Windows
        pip_path = Path("venv/Scripts/pip")
    else:  # Unix-like
        pip_path = Path("venv/bin/pip")
    
    try:
        print("📦 Installing packages (this may take several minutes)...")
        subprocess.run(
            [str(pip_path), "install", "-r", "requirements.txt"],
            check=True
        )
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    directories = ["data", "src", ".streamlit"]
    
    for directory in directories:
        path = Path(directory)
        path.mkdir(exist_ok=True)
        print(f"✅ {directory}/")
    
    return True


def setup_environment():
    """Setup environment file"""
    print_header("Setting Up Environment")
    
    env_path = Path(".env")
    env_example = Path(".env.example")
    
    if env_path.exists():
        print("⚠️  .env file already exists")
        return True
    
    if env_example.exists():
        with open(env_example, 'r') as src:
            content = src.read()
        with open(env_path, 'w') as dst:
            dst.write(content)
        print("✅ .env file created from template")
    else:
        print("⚠️  .env.example not found, skipping")
    
    return True


def verify_installation():
    """Verify installation is complete"""
    print_header("Verifying Installation")
    
    checks = {
        "requirements.txt": Path("requirements.txt").exists(),
        "app.py": Path("app.py").exists(),
        "src/": Path("src").exists(),
        "data/": Path("data").exists(),
        ".streamlit/": Path(".streamlit").exists(),
    }
    
    all_good = True
    for item, exists in checks.items():
        status = "✅" if exists else "❌"
        print(f"{status} {item}")
        all_good = all_good and exists
    
    return all_good


def print_next_steps():
    """Print next steps for user"""
    print_header("Installation Complete!")
    
    print("🎉 MedGemma HealthConnect is ready to use!\n")
    print("Next steps:")
    print("1. Activate virtual environment:")
    
    if os.name == 'nt':  # Windows
        print("   venv\\Scripts\\activate")
    else:  # Unix-like
        print("   source venv/bin/activate")
    
    print("\n2. Run the application:")
    print("   streamlit run app.py")
    
    print("\n3. Open your browser to:")
    print("   http://localhost:8501")
    
    print("\n📖 For more information:")
    print("   - README.md: General information")
    print("   - ARCHITECTURE.md: Technical details")
    print("   - DEPLOYMENT.md: Deployment guide")
    
    print("\n⚠️  Note: First run will download AI models (~2-4GB)")
    print("   This is a one-time download and may take several minutes.\n")


def main():
    """Main setup function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║           MedGemma HealthConnect Setup                    ║
    ║           Privacy-First Healthcare AI                     ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating directories", create_directories),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment),
        ("Verifying installation", verify_installation),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please check the error messages above and try again.")
            return 1
    
    print_next_steps()
    return 0


if __name__ == "__main__":
    sys.exit(main())
