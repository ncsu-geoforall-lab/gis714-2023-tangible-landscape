#!/usr/bin/env python3

import os

import grass.script as gs


def run_drain(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.watershed",
        elevation=scanned_elev,
        drainage="drain_directions",
        flags="sa",
        env=env,
    )

    gs.run_command("r.colors", map="drain_directions", color="plasma", env=env)


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
    gs.run_command(
        "r.resamp.stats",
        input=elevation,
        output=elev_resampled,
        env=env,
    )
    # The end of the block which needs no editing.

    # Edit here:
    # Place your function call or calls here.
    # This will run both examples (slope and contours).
    run_drain(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
