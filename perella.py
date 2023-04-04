import os

import grass.script as gs


def lcp(elevation, start_coordinate, end_coordinate, env, **kwargs):
    gs.run_command('r.slope.aspect', elevation=scanned_elev, slope='slope', env=env)
    gs.run_command('r.cost', input='slope', output='cost', start_coordinates=start_coordinate,
                   outdir='outdir', flags='k', env=env)
    gs.run_command('r.colors', map='cost', color='gyr', env=env)
    gs.run_command('r.drain', input='cost', output='drain', direction='outdir',
                   drain='drain', flags='d', start_coordinates=end_coordinate, env=env)

    
def main():

    env = os.environ.copy()
    env["GRASS_OVERWRITE"] = "1"
    elevation = "elev_lid792_1m"
    elev_resampled = "elev_resampled"
    gs.run_command("g.region", raster=elevation, res=4, flags="a", env=env)
    gs.run_command("r.resamp.stats", input=elevation, output=elev_resampled, env=env)
    
    
if __name__ == '__main__':
    elevation = 'elev_lid792_1m'
    env = None
    start = [638469, 220070]
    end = [638928, 220472]
    LCP(elevation, start, end, env)
