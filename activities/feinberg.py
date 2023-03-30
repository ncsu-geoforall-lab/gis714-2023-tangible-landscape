#!/usr/bin/env python3

import os

import grass.script as gs


# def run_slope(scanned_elev, env, **kwargs):
#     gs.run_command("r.slope.aspect", elevation=scanned_elev, slope="slope", env=env)

# def run_lake(scanned_elev, env, **kwargs):
#     coordinates = [638830, 220150]
#     gs.run_command('r.lake', elevation=scanned_elev, lake='output_lake',
#                    coordinates=coordinates, water_level=120, env=env)

from grass.pygrass.vector import VectorTopo
from grass.pygrass.vector.geometry import Point


def create_vector(name, coordinates):
    my_points = VectorTopo(name)
    my_points.open(mode="w")
    point1 = Point(coordinates[0], coordinates[1])
    my_points.write(point1)
    my_points.close()


def run_lake(scanned_elev, env, **kwargs):
    coordinates = [638830, 220150]
    res = gs.raster_what(map=scanned_elev, coord=[coordinates])
    elev_value = float(res[0][scanned_elev]["value"])
    gs.run_command(
        "r.lake",
        elevation=scanned_elev,
        lake="output_lake",
        coordinates=coordinates,
        water_level=elev_value + 5,
        env=env,
    )
    create_vector(name="source", coordinates=coordinates)


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_lake(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
