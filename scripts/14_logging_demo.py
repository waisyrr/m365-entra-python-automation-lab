import os
import logging
from datetime import datetime

os.makedirs("outputs/logs", exist_ok=True)

log_file = f"outputs/logs/automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.info("Microsoft Entra automation logging demo started")
logging.info("Authenticated to Microsoft Graph")
logging.info("Exported user inventory report")
logging.info("Created bulk onboarding users")
logging.info("Disabled bulk offboarding users")
logging.info("Generated department, group, and license reports")
logging.info("Automation workflow completed successfully")

print("✅ Logging demo completed successfully!")
print(f"Log file created: {log_file}")