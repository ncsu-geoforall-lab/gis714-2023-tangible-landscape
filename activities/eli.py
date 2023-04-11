#!/usr/bin/env python3

"""
Instructions
- Functions intended to run for each scan
  need to start with `run_`, e.g., `run_slope`.
- Do not modify the parameters of the `run_` function
  unless you know what you are doing.
  See optional parameters at:
  https://github.com/tangible-landscape/grass-tangible-landscape/wiki/Running-analyses-and-developing-workflows#python-workflows
- All gs.run_command/read_command/write_command/parse_command
  need to be passed *env* parameter like this: `(..., env=env)`.
"""

import os
from datetime import datetime

import grass.script as gs

# Edit here:
# The following functions starting with the word run follwed by an underscore
# are the analysis which will run on Tangible Landscape (and during testing).


def get_day():
    return datetime.now().timetuple().tm_yday


def run_sun(scanned_elev, current_day, env, **kwargs):
    gs.run_command(
        "r.sun", elevation=scanned_elev, day=current_day, env=env, glob_rad="sun"
    )


def main():
    """Function which runs when testing without Tangible Landscape"""

    # No need to edit this block. It should stay the same.
    # Get the current environment variables as a copy.
    env = os.environ.copy()
    # We want to run this repetitively and replace the old data by the new data.
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    # We use resampling to get a similar resolution as with Tangible Landscape.
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    # The end of the block which needs no editing.

    # Edit here:
    # Place your function call or calls here.
    now_day = get_day()
    run_sun(scanned_elev=elev_resampled, current_day=now_day, env=env)


if __name__ == "__main__":
    main()
