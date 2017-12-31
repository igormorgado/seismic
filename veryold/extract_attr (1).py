#!/usr/bin/env python

import pandas as pd
import lscapi

seqs = ( 249, 251, 252, 253, 254, 255, 256, 257, 258, 260, 261, 262 )

lsc = lscapi.LsCapi()
#query = 'select shotx,shoty,shotz,recx,recy,recz,offset,channel,tr_gainx from a::uds:416j604:/fat/prod/p2000_updgeom_lc_anp_exp/{}'
query = 'select channel,tr_gainx from a::uds:416j604:/fat/prod/p2000_updgeom_lc_anp_exp/{}'

for seq in seqs:
    print("Reading sequence {}".format(seq))
    df = lsc.query(query.format(seq))
    print("\tDropping duplicates")
    df = df.drop_duplicates()
    print("\tRenaming columns")
    df.columns = map(str.lower, df.columns)
    print("\tSaving to file\n")
    df.to_csv('tr_gainx_seq{}.csv'.format(seq),index=False)
    
    del df

