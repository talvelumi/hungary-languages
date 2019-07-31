# -*- coding: utf-8 -*-
"""
Created on Fri Jun 14 12:57:35 2019

@author: LokalAdm
"""

#import geonames.adapters.search
#
#_USERNAME = 'talvi'
#sa = geonames.adapters.search.Search(_USERNAME)
#
#result = sa.query('detroit').country('us').max_rows(5).execute()
#for id_, name in result.get_flat_results():
#    # make_unicode() is only used here for Python version-compatibility.
#    print(geonames.compat.make_unicode("[{0}]: [{1}]").format(id_, name))
latlong=[[1,2],[3,4]]
f = open("D:/sopronll.txt","w+")
for lines in latlong:
    f.write('\t'.join([str(j) for j in lines]))
    f.write('\n')
f.close()