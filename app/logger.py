import logging
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s | %(levelname)-8s | %(message)s',
    datefmt='%Y-%m-%d %H:%M',
    filename=log_dir / "app.log",
    encoding='utf-8'
)
logger = logging.getLogger(__name__)