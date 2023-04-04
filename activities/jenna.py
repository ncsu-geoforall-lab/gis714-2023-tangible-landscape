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

import grass.script as gs


def run_twi(scanned_elev, env, **kwargs):
    gs.run_command("r.topidx", input=scanned_elev, output="twi", env=env)
    gs.run_command("r.colors", map="twi", color="sepia", env=env, flags="n")


def run_ponds(scanned_elev, env, **kwargs):
    repeat = 2
    input_dem = scanned_elev
    output = "tmp_filldir"
    for i in range(repeat):
        gs.run_command(
            "r.fill.dir", input=input_dem, output=output, direction="tmp_dir", env=env
        )
        input_dem = output
    # filter depression deeper than 0.1 m to
    gs.mapcalc(
        "{new} = if({out} - {scan} > 0.1, {out} - {scan}, null())".format(
            new="ponds", out=output, scan=scanned_elev
        ),
        env=env,
    )
    gs.run_command(
        "r.colors", map="ponds", rules="-", stdin="0% aqua\n100% blue", env=env
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
    # This will run both examples (slope and contours).
    run_twi(scanned_elev=elev_resampled, env=env)
    run_ponds(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
