import logging
from app import app, db

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        with app.app_context():
            logger.info("Checking database connection...")
            try:
                # Test database connection
                db.engine.execute("SELECT 1")
                logger.info("Database connection successful")
            except Exception as db_error:
                logger.error(f"Database connection failed: {str(db_error)}")
                raise

        logger.info("Starting Flask server...")
        app.run(host="0.0.0.0", port=5000, debug=True)
    except Exception as e:
        logger.error(f"Error starting application: {str(e)}", exc_info=True)
        raise