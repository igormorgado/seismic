#!/usr/bin/env python

from __future__ import print_function

data = ( "01", "02", "03", "04" )
seq = ( "018", "039" )

project = "416j604"
datapath = "/fat/test/t2181_qc2d_3rd"
dataname = "list_data_d{}_s{}"
headers = ( "cmp2d", "offset2d", "avo_time", "sample_value" )


import lscapi
import sys

capifd = lscapi.LsCapi()
fields = ", ".join(headers)
query = "select {} from a::uds:{}:{}/{}".format(fields, project, datapath, dataname)


for d in data:
    for s in seq:

        fquery = query.format(d,s)
        print(fquery, end=' ')
        sys.stdout.flush()

        try:
            qdf = capifd.query(fquery)
        except:
            print("Error")
        else:
            print("Success")
            qdf.to_csv('avo_cmpoffset_d{}_s{}.csv'.format(d, s), index=False)
            del qdf




