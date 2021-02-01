from pydal import *
db = DAL('postgres://postgres:Asbaasba1@db/othsec')
db.define_table('othsec',
  Field('idn', 'string',20,''),
  Field('username', 'string',30,''),
  Field('protocol', 'string',8,'IP'),
  Field('datetime_remote', 'datetime'),
  Field('datetime_othsec', 'datetime'),
  Field('addr_from', 'string',40,'aa.aa.aa.aa'),
  Field('addr_to', 'string',40,'bb.bb.bb.bb'),
  Field('port_from', 'string',10,'0000'),
  Field('port_to', 'string',10,'0000'),
  Field('mac_from', 'string',12,''),
  Field('mac_to', 'string',12,''),
  Field('flags', 'string',5,''),
  Field('body_message', 'string',255))
db.define_table('ipanalyzed',
  Field('idn', 'string',20,''),
  Field('username', 'string',30,''),
  Field('datetime', 'datetime'),
  Field('protocol', 'string',8,'IP'),
  Field('IP_addr', 'string',40,'aa.aa.aa.aa'),
  Field('port', 'string',10,'0000'),
  Field('mac', 'string',12,''),
  Field('status', 'string',10),
  Field('risk', 'integer',0),
  Field('hits', 'integer',0),
  Field('longitude', 'double',0),
  Field('latitude', 'double',0))
db.define_table('loganalyzed',
  Field('IDN', 'string',20,''),
  Field('username', 'string',30,''),
  Field('datetime', 'datetime'),
  Field('protocol', 'string',8,'IP'),
  Field('IP_addr', 'string',40,'aa.aa.aa.aa'),
  Field('port', 'string',10,'0000'),
  Field('service', 'string',50,'0000'),
  Field('status', 'string',10),
  Field('conn_tries', 'integer',0),
  Field('auth_failure', 'integer',0))
db(db.othsec).delete()
db(db.ipanalyzed).delete()
db(db.loganalyzed).delete()
db.commit()
