import os

import grass.script as gs


def run_fill(scanned_elev, env, **kwargs):
    gs.run_command(
        "r.fill.dir", input=scanned_elev, output="fill", direction="direction", env=env
    )


def run_contours(scanned_elev, env, **kwargs):
    interval = 5
    gs.run_command(
        "r.contour",
        input=scanned_elev,
        output="contours",
        step=interval,
        flags="t",
        env=env,
    )

    gs.run_command(
        "r.param.scale",
        input=scanned_elev,
        output="tangential_curv",
        method="crosc",
        size=11,
        env=env,
    )
    gs.run_command(
        "r.colors", map=["profile_curv", "tangential_curv"], color="curvature", env=env
    )


def main():
    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_relief(scanned_elev=elev_resampled, env=env)
    run_fill(scanned_elev=elev_resampled, env=env)
    run_curvatures(scanned_elev=elev_resampled, env=env)


if __name__ == "__main__":
    main()
