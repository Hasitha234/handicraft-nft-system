"""
Utility Functions - Error Handling & Logging
"""

import logging
from pathlib import Path
from functools import wraps
import traceback

# Setup logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def handle_errors(func):
    """Decorator for error handling"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    return wrapper

def check_model_exists(model_path="models/best_model.pth"):
    """Check if model file exists"""
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model not found: {model_path}. Train model first.")
    return True

def check_designs_exist():
    """Check if designs exist"""
    designs_dir = Path("generated_designs")
    metadata_path = designs_dir / "metadata.json"
    if not metadata_path.exists():
        raise FileNotFoundError("No designs found. Run batch_generate.py first.")
    return True

def check_database_exists():
    """Check if database exists"""
    db_path = Path("user_preferences.db")
    if not db_path.exists():
        logger.warning("Database not found. Will be created on first use.")
    return True