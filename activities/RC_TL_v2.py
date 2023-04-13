#!/usr/bin/env python3

import os

import grass.script as gs


# Add in new command for the TL to do
# Rename function
def run_the_lake(scanned_elev, env, **kwargs):
    coordinates = [638830, 220150]
    gs.run_command(
        "r.lake",
        elevation=scanned_elev,
        lake="output_lake",
        coordinates=coordinates,
        water_level=120,
        env=env,
    )
    gs.run_command("r.colors", map="output_lake", color="purple", env=env)


def run_the_stream(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.stream.extract",
        elevation=scanned_elev,
        threshold=100,
        stream_rast="output_stream",
        env=env,
    )
    gs.run_command("r.colors", map="output_stream", color="blue", env=env)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_the_lake(scanned_elev=elev_resampled, env=env)
    run_the_stream(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
