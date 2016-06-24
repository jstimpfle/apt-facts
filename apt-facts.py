#!/usr/bin/python3                                                              

# Convert apt list to an easier to process facts database format
#
# Unfortunately the interesting aspect of the database, package dependencies
# (which includes Depends:, PreDepends:, Conflicts:, Replaces:, Suggests:,
# Recommends:, ...?) is difficult to handle in a relational database, since
# there are dependency alternatives. So this script makes an ID for each list of
# alternative dependencies. The format of the output is best explained with an
# example:
#
# ...
# Depends 0ad * 0.0.17-1 7 libenet7  
# Depends 0ad * 0.0.17-1 8 libgcc1 >= 1:4.1.1
# Depends 0ad * 0.0.17-1 9 libgl1-mesa-glx  
# Depends 0ad * 0.0.17-1 9 libgl1  
# Depends 0ad * 0.0.17-1 10 libgloox12
# ...
#
# It can be seen that the Package 0ad (on Architecture * i.e. native, in version
# 0.0.17-1) has a dependency "8" which can only be satisfied by libgcc1 (version
# >= 1:4.11), but a more flexible dependency "9" which can be satisfied by
# either libgl1-mesa-glx (any version) or libgl1 (any version).

import apt

# this works with python-apt 0.9.3.12 as in Debian jessie
# Version 1.1... as in Debian stretch has a slightly different API, so this
# script won't work.

cache = apt.Cache()

for pkg in cache:
    if ':' in pkg.name:
        p, a = pkg.name.split(':', 1)
    else:
        p = pkg.name
        a = '*'
    for o in pkg.versions:
        v = o.version
        pv = o._cand

        print("Package", p, a, v)

        for dep_type, dep in pv.depends_list_str.items():
            for i, dep_alt in enumerate(dep):
                for dep_p, dep_v, dep_r in dep_alt:
                    print(dep_type, p, a, v, i, dep_p, dep_r, dep_v)

        for vpkg,_,_ in pv.provides_list:
            print("Provides", p, a, v, vpkg)

        print("Section", p, a, v, pv.section)
