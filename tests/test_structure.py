"""
Lightweight tests for MedGemma HealthConnect modules (no dependencies)
"""

import sys
from pathlib import Path


def test_imports():
    """Test that all module files exist and are importable structurally"""
    src_path = Path(__file__).parent.parent / "src"
    sys.path.insert(0, str(src_path))
    
    modules = [
        '__init__.py',
        'speech_to_text.py',
        'medgemma_summarizer.py',
        'clinical_trial_matcher.py',
        'privacy_manager.py'
    ]
    
    for module in modules:
        module_path = src_path / module
        assert module_path.exists(), f"Module {module} not found"
        print(f"✅ Module found: {module}")
    
    print("✅ All module files present: PASSED")


def test_app_exists():
    """Test that main app file exists"""
    app_path = Path(__file__).parent.parent / "app.py"
    assert app_path.exists(), "app.py not found"
    print("✅ Main application file: PASSED")


def test_config_files():
    """Test that configuration files exist"""
    base_path = Path(__file__).parent.parent
    
    config_files = [
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'setup.py',
        'README.md',
        'ARCHITECTURE.md',
        'DEPLOYMENT.md',
        'LICENSE'
    ]
    
    for config_file in config_files:
        file_path = base_path / config_file
        assert file_path.exists(), f"{config_file} not found"
        print(f"✅ Config file found: {config_file}")
    
    print("✅ All configuration files present: PASSED")


def test_streamlit_config():
    """Test Streamlit configuration exists"""
    config_path = Path(__file__).parent.parent / ".streamlit" / "config.toml"
    assert config_path.exists(), "Streamlit config not found"
    
    # Check config content
    with open(config_path, 'r') as f:
        content = f.read()
        assert '[theme]' in content, "Theme configuration missing"
        assert '[server]' in content, "Server configuration missing"
    
    print("✅ Streamlit configuration: PASSED")


def test_privacy_principles():
    """Test privacy-related configuration"""
    env_path = Path(__file__).parent.parent / ".env.example"
    
    with open(env_path, 'r') as f:
        content = f.read()
        assert 'STORE_TRANSCRIPTS=false' in content, "Privacy setting missing"
        assert 'ENABLE_LOGGING=false' in content, "Logging setting missing"
        assert 'SESSION_TIMEOUT' in content, "Session timeout missing"
    
    print("✅ Privacy configuration: PASSED")


def test_gitignore_privacy():
    """Test that gitignore protects sensitive data"""
    gitignore_path = Path(__file__).parent.parent / ".gitignore"
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
        assert '.env' in content, ".env not in gitignore"
        assert '*.wav' in content, "Audio files not in gitignore"
        assert 'data/transcripts/' in content, "Transcripts not in gitignore"
    
    print("✅ Privacy gitignore rules: PASSED")


def test_documentation_completeness():
    """Test that documentation is comprehensive"""
    readme_path = Path(__file__).parent.parent / "README.md"
    
    with open(readme_path, 'r') as f:
        content = f.read()
        
        # Check for key sections
        required_sections = [
            'Features',
            'Architecture',
            'Quick Start',
            'Usage',
            'Privacy',
            'Configuration'
        ]
        
        for section in required_sections:
            assert section in content, f"Documentation missing section: {section}"
        
        # Check for privacy emphasis
        assert 'privacy' in content.lower(), "Privacy not emphasized in README"
        assert 'PII' in content or 'personal' in content.lower(), "PII handling not documented"
    
    print("✅ Documentation completeness: PASSED")


def test_project_structure():
    """Test overall project structure"""
    base_path = Path(__file__).parent.parent
    
    required_dirs = ['src', 'data', '.streamlit', 'tests']
    
    for directory in required_dirs:
        dir_path = base_path / directory
        assert dir_path.exists(), f"Directory {directory} not found"
        print(f"✅ Directory present: {directory}/")
    
    print("✅ Project structure: PASSED")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("Running MedGemma HealthConnect Structure Tests")
    print("="*60 + "\n")
    
    tests = [
        test_imports,
        test_app_exists,
        test_config_files,
        test_streamlit_config,
        test_privacy_principles,
        test_gitignore_privacy,
        test_documentation_completeness,
        test_project_structure,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
            print()
        except AssertionError as e:
            print(f"❌ {test.__name__}: FAILED - {e}")
            failed += 1
            print()
        except Exception as e:
            print(f"❌ {test.__name__}: ERROR - {e}")
            failed += 1
            print()
    
    print("="*60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
