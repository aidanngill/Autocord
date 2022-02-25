import hashlib
import json
import logging
import sys
import time
from datetime import datetime
from os import PathLike
from typing import List, Optional

from .models import Instance
from .net import send_message
from .timing import Timing

log = logging.getLogger(__name__)

logging.basicConfig(
    format="[%(asctime)s] [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


class Configuration:
    """Manager for all given instances."""

    def __init__(self, path: PathLike):
        self.path = path

        with open(self.path, "r", encoding="utf-8") as file:
            self.instances: List[Instance] = json.load(file)

        if len(self.instances) == 0:
            raise Exception("No instances were provided in the configuration file.")

    def run(self) -> None:
        """Iterate over and run every instance."""
        earliest_run: Optional[datetime] = None
        current_time = datetime.now()

        for instance in self.instances:
            if instance.get("id") is None:
                instance["id"] = hashlib.md5(str(instance).encode()).hexdigest()

            next_run: Optional[datetime] = None
            next_run_raw: Optional[int] = Timing.get(instance)

            if not next_run_raw:
                Timing.update_instance(instance)
                next_run_raw = Timing.get(instance)

            next_run = datetime.fromtimestamp(next_run_raw)

            if current_time < next_run:
                if earliest_run is None or earliest_run > next_run:
                    earliest_run = next_run

                continue

            log.info(f"Started running instance '{instance['id']}'...")

            for action in instance["actions"]:
                for _ in range(action["repeat"]):
                    for message in action["messages"]:
                        send_message(
                            instance["prefix"] + message,
                            channel_id=instance["channel"],
                            authorization=instance["authorization"],
                            with_typing=True,
                        )

                        time.sleep(instance["delay"])

            Timing.update_instance(instance)

            # Update the earliest run value again.
            next_run = datetime.fromtimestamp(Timing.get(instance))

            if earliest_run is None or earliest_run > next_run:
                earliest_run = next_run

        # Update the configuration and timing files.
        with open(self.path, "w+", encoding="utf-8") as file:
            json.dump(self.instances, file, indent=4)

        Timing.save_values()

        # Then wait until the next instance can be run.
        earliest_run_delta = 30

        if isinstance(earliest_run, datetime):
            earliest_run_delta = (earliest_run - current_time).total_seconds()

        log.info(
            f"Waiting {(earliest_run_delta / 60):.1f} minutes before running the next instance."
        )

        time.sleep(earliest_run_delta)


def main() -> None:
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"
    config = Configuration(config_file)

    while True:
        config.run()


if __name__ == "__main__":
    main()
