#!/usr/bin/env python3

import os

import grass.script as gs


def run_lcp(scanned_elev, env, points=None **kwargs):
    if not points:
        points = "points"
        import analyses
        
        analyses.change_detection(
            "scan_saved",
            scanned_elev,
            points,
            height_threshold=[10, 100],
            cells_threshold=[5, 50],
            add=True,
            max_detected=5,
            debug=True,
            env=env,
          )
    point_list = []
    data = (
        gs.read_command(
            "v.out.ascii",
            input=points,
            type="point",
            format="point",
            separator="comma",
            env=env,
            )
            .strip()
            .splitlines()
    )
    if len(data) < 2:
        return
    for point in data:
        point_list.append([float(p) for p in point.split(",")][:2])
    gs.run_command("r.slope.aspect", elevation=scanned_elev, slope="slope", env=env)
    gs.run_command(
        "r.cost",
        input="slope",
        output="cost",
        start_coordinates=start_coordinate,
        outdir="outdir",
        flags="k",
        env=env,
    )
    gs.run_command("r.colors", map="cost", color="gyr", env=env)
    gs.run_command(
        "r.drain",
        input="cost",
        output="drain",
        direction="outdir",
        drain="drain",
        flags="d",
        start_coordinates=end_coordinate,
        env=env,
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    env = env
    start = [638469, 220070]
    end = [638928, 220472]
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_lcp(
        scanned_elev=elev_resampled,
        env=env,
        points=points
    )


if __name__ == "__main__":
    main()
