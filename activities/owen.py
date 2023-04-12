#!/usr/bin/env python3

import os

import grass.script as gs


def run_drain_accum(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.watershed",
        elevation=scanned_elev,
        drainage="drain_directions",
        flags="sa",
        env=env,
    )

    try:
        gs.run_command(
            "r.accumulate",
            direction="drain_directions",
            threshold=100,
            stream="streams",
            overwrite=True,
        )
    except FileNotFoundError:
        UserWarning("r.accumulate is not installed")
        pass


def main():
    """Function which runs when testing without Tangible Landscape"""

    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command(
        "r.resamp.stats",
        input=elevation,
        output=elev_resampled,
        env=env,
    )
    # ------

    run_drain_accum(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
