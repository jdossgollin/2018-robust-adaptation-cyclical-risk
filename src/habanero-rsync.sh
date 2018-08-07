# Pull data to local computer from habanero
rsync -avz -e ssh jwd2136@habanero.rcs.columbia.edu:/rigel/cwc/users/jwd2136/STXCluster/src/codebase/data/cached/lfv-only-bias-variance.nc  ./codebase/data/lfv-only-bias-variance.nc
rsync -avz -e ssh jwd2136@habanero.rcs.columbia.edu:/rigel/cwc/users/jwd2136/STXCluster/src/codebase/data/cached/lfv-only-bias-variance.nc  ./codebase/data/secular-only-bias-variance.nc
rsync -avz -e ssh jwd2136@habanero.rcs.columbia.edu:/rigel/cwc/users/jwd2136/STXCluster/src/codebase/data/cached/lfv-secular-bias-variance.nc  ./codebase/data/lfv-secular-bias-variance.nc