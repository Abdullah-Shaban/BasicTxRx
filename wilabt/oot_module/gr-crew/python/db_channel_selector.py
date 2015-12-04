#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 iMinds - University Ghent.
# This module is tested with GNU Radio 3.7.5 
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy
from gnuradio import gr
import string
import psycopg2 
from datetime import datetime
class db_channel_selector(gr.sync_block):
    """
    docstring for block db_channel_selector
    """
    def __init__(self, dbname,standard,detmode,berthr):
        gr.sync_block.__init__(self, name="db_channel_selector", in_sig=[numpy.float32], out_sig=None)
        # construct the table name 
        tbname = 'usrpse_'+standard+'_'+detmode 
        # construct the query 
        self.qstatement = string.Template("select * from $tbname s where s.oml_ts_server=(select max(oml_ts_server) from $tbname )  ;").substitute({'tbname':tbname})
        try:
            self.conn = psycopg2.connect("dbname='%s' user='wilabuser' host='ops.wilab2.ilabt.iminds.be' password='wilabuser'" % dbname)
        except:
            print "I am unable to connect to the database"    
            
        self.cur = self.conn.cursor()
        self.standard = standard
        self.freq = 2405000000 # default frequency 
        self.ber_thr = berthr
        self.ber = 0 # default bit error rate is 0        
        self.time_ref = datetime.now()

    def work(self, input_items, output_items):
        in0 = input_items[0]
        self.ber = sum(in0) / float( len(in0) )
        return len(input_items[0])
        
    def get_freq(self):
        # if the bit error rate is higher than threshold, look for new channel
        if(self.ber > self.ber_thr):
        
            # query database for the best channel
            try:
                self.cur.execute(self.qstatement)
            except:
                print "execute statement failed "
                
            onerow = self.cur.fetchone()    
            rssi_list = onerow[7:]
            # print rssi_list 
            index=numpy.argmin(rssi_list)
            
            # translate channel index into frequency
            if(self.standard == 'zigbee'):
                freq = index*5000000+2405000000.0  
            elif(self.standard == 'wlan_g'):
                freq = index*5000000+2412000000.0
            elif(self.standard == 'bluetooth'):
                freq = index*1000000+2402000000.0
            else:
                print 'unknown standard, not supported, using default freq 2.4GHz'
                freq = 2400000000.0
                
            # assign the new freq value to the class variable if it is different
            t2 = datetime.now()
            delta = t2-self.time_ref 
            delta.total_seconds()
            if(self.freq != freq and delta.total_seconds() > 6):
                self.freq = freq 
                print "INFO: update frequency to ", freq
                self.time_ref = datetime.now()
            
        return self.freq        

