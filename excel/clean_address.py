#!/usr/bin/env python2

import xlrd, xlwt
import geocoder

import json

import sys 

class Cleaner():

    def __init__(self, filename, new_filename):
        self.new_filename = new_filename

        self.book = xlrd.open_workbook(filename)

        self.clean_sheet = self.book.sheet_by_index(1)
        self.dirty_sheet = self.book.sheet_by_index(0)

        self.sheet_limit = (4501, 6000)

    def get_clean_codes(self):
        self.latlng_dict = dict()

        with open('org_latlng.json','r') as json_file:
            
            geocode_dict = json.load(json_file)

            #print geocode_dict.keys()

            for row in range( 1, self.clean_sheet.nrows ):
                name_cell = self.clean_sheet.cell( row, 1 )
                name = name_cell.value
                
                try:                    
                    lat = geocode_dict[name]['properties']['lat']
                    lng = geocode_dict[name]['properties']['lng']
                except KeyError:
                    continue

                geocode = (lat, lng)

                if not geocode:
                    continue

                self.latlng_dict[ geocode ] = {
                    'clean_name': name,
                    'row': row
                }
        #print self.latlng_dict.keys()

    def match_dirty_addresses(self):
        
        for row in range( self.sheet_limit[0], self.sheet_limit[0] + 10 ):
            try:
                name_cell = self.dirty_sheet.cell( row, 1 )
                name = name_cell.value

                print name

                g = geocoder.google( name )
                
                geo_tmp = g.latlng
             
                if not geo_tmp:
                    continue

                lat, lng = geo_tmp

                geocode = (lat, lng)

                print name +': '+ str(geocode)

                if not geocode:
                    continue

                if geocode not in self.latlng_dict.keys():
                    print 'nope'
                    continue
                
                self.latlng_dict[ geocode ]['dirty_name'] = name

                print self.latlng_dict[ geocode ]['clean_name'] + ': ' + self.latlng_dict[ geocode ]['dirty_name']
            except KeyboardInterrupt:
                break

    def write(self):

        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Clean addresses')

        sheet.write(0, 0, 'Address')
        sheet.write(0, 1, 'Organization- Cleaned')

        for sn, key in enumerate( self.latlng_dict ):
            try:
                sheet.write( sn+1, 0, self.latlng_dict[key]['dirty_name'] )
                sheet.write( sn+1, 1, self.latlng_dict[key]['clean_name'] )
            except KeyError:
                continue

        workbook.save(self.new_filename)

if __name__=='__main__':
    if len(sys.argv) is not 3:
        sys.exit('Invalid usage.\n Usage: clean_address <dirtysheet.xls> <newsheet.xls>')

    sheet_filename = sys.argv[1]
    new_filename = sys.argv[2]

    cleaner = Cleaner(sheet_filename, new_filename)
    cleaner.get_clean_codes()
    cleaner.match_dirty_addresses()
    cleaner.write()