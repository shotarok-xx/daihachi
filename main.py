import logging
import sys
from app import app

# Configure logging with more detailed format
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        # Start the Flask server
        logger.info("Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}", exc_info=True)
        sys.exit(1)