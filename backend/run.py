"""
Alternative server runner with proper reload exclusions.
Use this instead of uvicorn directly to avoid watching venv.

This prevents uvicorn from watching the venv directory and causing
hundreds of reload warnings.
"""
import uvicorn
import os
from pathlib import Path
from config import Config

if __name__ == "__main__":
    # Change to backend directory to avoid watching parent directories
    backend_dir = Path(__file__).parent.absolute()
    original_dir = os.getcwd()
    os.chdir(str(backend_dir))

    try:
        # Use reload-include to only watch backend directory, avoiding venv
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=True,
            reload_includes=["*.py"],  # Only watch Python files
            reload_excludes=["venv/**", "__pycache__/**", "*.pyc",
                             ".git/**"] if hasattr(uvicorn, 'reload') else []
        )
    except TypeError:
        # Fallback for older uvicorn versions
        uvicorn.run(
            "main:app",
            host=Config.HOST,
            port=Config.PORT,
            reload=True
        )
    finally:
        os.chdir(original_dir)
