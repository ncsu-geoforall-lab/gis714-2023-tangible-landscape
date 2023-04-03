#!/usr/bin/env python3

import os

import grass.script as gs

def run_ponds(scanned_elev, env, **kwargs):
    repeat = 2
    input_dem = scanned_elev
    output = "tmp_filldir"
    for i in range(repeat):
        gs.run_command('r.fill.dir', input=input_dem, output=output, direction="tmp_dir", env=env)
        input_dem = output
  
    gs.mapcalc('{new} = if({out} - {scan} > 0.1, {out} - {scan}, null())'.format(new='ponds', out=output, scan=scanned_elev), env=env)
    gs.write_command('r.colors', map='ponds', rules='-', stdin='0% aqua\n100% blue', env=env)

    
def run_hydro(scanned_elev, env, **kwargs):
    gs.run_command('r.watershed', elevation=scanned_elev, accumulation='flow_accum', basin='watersheds', threshold=1000, flags='a', env=env)
 
def run_watershed_slope(scanned_elev, env, **kwargs):
    gs.run_command('r.watershed', elevation=scanned_elev, accumulation='flow_accum',
                   basin='watersheds', threshold=1000, env=env)
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', env=env)
    gs.run_command('r.stats.zonal', base='watersheds', cover='slope', method='average',
                   output='watersheds_slope', env=env)
    gs.run_command('r.colors', map='watersheds_slope', color='bgyr', env=env)
    

def main():

    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)

    run_hydro(scanned_elev=elev_resampled, env=env)
