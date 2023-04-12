#!/usr/bin/env python3


import grass.script as gs


def run_slope(scanned_elev, env, **kwargs):
    gs.run_command("r.slope.aspect", elevation=scanned_elev, slope="slope", env=env)


# creating points
def run_function_with_points(scanned_elev, env, points=None, **kwargs):
    """Doesn't do anything, except loading points from a vector map to Python
    If *points* is provided, the function assumes it is name of an existing vector map.
    This is used during testing.
    If *points* is not provided, the function assumes it runs in Tangible Landscape.
    """
    if not points:
        # If there are no points, ask Tangible Landscape to generate points from
        # a change in the surface.
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
    # Output point coordinates from GRASS GIS and read coordinates into a Python list.
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
        # For the cases when the analysis expects at least 2 points, we check the
        # number of points and return from the function if there is less than 2
        # points. (No points is a perfectly valid state in Tangible Landscape,
        # so we need to deal with it here.)
        return
    for point in data:
        point_list.append([float(p) for p in point.split(",")][:2])


def LCP(elevation, start_coordinate, end_coordinate, env):
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


if __name__ == "__main__":
    elevation = "elev_lid792_1m"
    env = None
    start = [638469, 220070]
    end = [638928, 220472]
    LCP(elevation, start, end, env)
