"""
Main entry point for Polygon UI.
"""

import logging
from polygon_ui import hello

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""
    logger.info("Starting Polygon UI...")
    print(hello())
    logger.info("Application completed successfully")


if __name__ == "__main__":
    main()
