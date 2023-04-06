#!/usr/bin/env python3

import os

import grass.script as gs


def run_hydro(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.watershed",
        elevation=scanned_elev,
        accumulation="flow_accum",
        basin="watersheds",
        threshold=1000,
        flags="a",
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_slope(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
