import logging
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

logger = logging.getLogger("docs_assistant")
logger.setLevel(logging.INFO)

app_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
app_handler.setLevel(logging.INFO)
app_handler.setFormatter(formatter)

error_handler = logging.FileHandler(log_dir / "error.log", encoding="utf-8")
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(formatter)

console_handler = logging.FileHandler(log_dir / "console.log", encoding="utf-8")
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(app_handler)
logger.addHandler(error_handler)
logger.addHandler(console_handler)
