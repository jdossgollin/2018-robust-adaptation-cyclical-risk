import xarray as xr

import argparse

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser()
parser.add_argument("--infile")
parser.add_argument("--outfile")

def main():
    args = parser.parse_args()

    ds = xr.open_dataarray(args.infile)
    df = ds.to_pandas()
    df.to_csv(args.outfile)
    
if __name__ == '__main__':
    main()