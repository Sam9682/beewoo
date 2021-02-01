from gluon import DAL, Field

db = DAL('postgres://postgres:Asbaasba1@db/othsec')
db.define_table('ipligence2',
  Field('ip_from', 'integer',10,'0000000000'),
  Field('ip_to', 'integer',10,'0000000000'),
  Field('country_code', 'string',10),
  Field('country_name', 'string',255),
  Field('continent_code', 'string',10),
  Field('continent_name', 'string',255),
  Field('time_zone', 'string',10),
  Field('region_code', 'string',10),
  Field('region_name', 'string',255),
  Field('the_owner', 'string',255),
  Field('city_name', 'string',255),
  Field('county_name', 'string',255),
  Field('latitude', 'double'),
  Field('longitude', 'double'))
db.ipligence2.import_from_csv_file(open('/home/www-data/web2py/applications/TrackR/private/ipligence-max.mysqldump.sql'),'rb')
db.commit()
