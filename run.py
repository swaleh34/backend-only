"""
Swaleh AI - Application Runner
"""
import os
import sys
import subprocess

def main():
    """Main runner function"""
    print("=" * 60)
    print("🕌 SWALEH AI - LAUNCHER")
    print("=" * 60)
    
    # Check virtual environment
    if not hasattr(sys, 'real_prefix') and not sys.base_prefix != sys.prefix:
        print("⚠️  Virtual environment not activated!")
        print("Activating...")
        if os.name == 'nt':
            activate_script = os.path.join('venv', 'Scripts', 'activate.bat')
        else:
            activate_script = os.path.join('venv', 'bin', 'activate')
        print(f"Please run: {activate_script}")
        return
    
    print("\nSelect an option:")
    print("1. Start server")
    print("2. Seed database")
    print("3. Run tests")
    print("4. Start with auto-reload (development)")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Swaleh AI server...")
        os.system("python -m app.main")
    elif choice == "2":
        print("\n🌱 Seeding database...")
        os.system("python -m app.scripts.seed_database")
    elif choice == "3":
        print("\n🧪 Running tests...")
        os.system("pytest")
    elif choice == "4":
        print("\n🚀 Starting development server with auto-reload...")
        os.system("uvicorn app.main:app --reload --host 127.0.0.1 --port 8000")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
