#!/usr/bin/env python3

import os

import grass.script as gs


def run_flow(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.fill.dir",
        input=scanned_elev,
        output="filledpits",
        direction="flow_direct",
        env=env,
    )

    gs.run_command(
        "r.flow", elevation="filledpits", flowaccumulation="flowaccumulation", env=env
    )

    gs.run_command(
        "r.stream.extract",
        elevation="filledpits",
        threshold=32.2115,
        accumulation="flowaccumulation",
        stream_vector="my_stream",
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_flow(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
