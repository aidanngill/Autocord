import json
import os
import random
from datetime import datetime, timedelta
from os import PathLike
from pathlib import Path
from typing import Any, Optional

from .models import Instance
from .util import expand_time_string


class Timing:
    """Manage when instances will be run."""

    def __init__(self):
        self.data = Timing.fetch_values()

    @staticmethod
    def get_file_path() -> PathLike:
        """Get the location of the timing file. Will typically reside in
        `$HOME/.ramadan/autocord.json`. If it does not exist, then we will
        create it and populate it."""
        path_base = Path.home()
        path_conf = os.path.join(path_base, ".ramadan")

        if not os.path.isdir(path_conf):
            os.mkdir(path_conf)

        path_file = os.path.join(path_conf, "autocord.json")

        if not os.path.isfile(path_file):
            with open(path_file, "w+", encoding="utf-8") as file:
                json.dump({}, file)

        return path_file

    @staticmethod
    def fetch_values() -> dict:
        """Get the timing values for instances, being the time they will next be
        run."""
        with open(Timing.get_file_path(), "r", encoding="utf-8") as file:
            return json.load(file)

    def get(self, key: Instance | str) -> Optional[Any]:
        return self.data.get(key["id"] if isinstance(key, dict) else key)

    def update_instance(self, instance: Instance) -> None:
        """Calculate the next time an instance should be run, then update the
        timings file with the new value."""
        ts = datetime.now() + timedelta(days=1)

        sh, sm, ss = expand_time_string(instance["timing"][0])
        sts = ts.replace(hour=sh, minute=sm, second=ss)

        eh, em, es = expand_time_string(instance["timing"][1])
        ets = ts.replace(hour=eh, minute=em, second=es)

        if ets < sts:
            tmp = ets
            ets = sts
            sts = tmp

        ts = sts + timedelta(seconds=random.randint(0, (ets - sts).total_seconds()))

        self.data[instance["id"]] = int(ts.timestamp())

    def save_values(self) -> None:
        """Update the timings file with the latest data."""
        with open(Timing.get_file_path(), "w+", encoding="utf-8") as file:
            json.dump(self.data, file, separators=(",", ":"))


# Make it a singleton to reduce file I/O.
Timing = Timing()
