#!/usr/bin/env python

from gluon import *
db = DAL('postgres://postgres:Asbaasba1@db/othsec')
db.define_table('othsec',
  Field('IDN', 'string',20,''),
  Field('protocol', 'string',8,'IP'),
  Field('datetime', 'string',12,'00:00:00'),
  Field('addr_from', 'string',40,'aa.aa.aa.aa'),
  Field('addr_to', 'string',40,'bb.bb.bb.bb'),
  Field('port_from', 'string',10,'0000'),
  Field('port_to', 'string',10,'0000'),
  Field('mac_from', 'string',12,''),
  Field('mac_to', 'string',12,''),
  Field('body_message', 'string',255))
db.define_table('ipanalyzed',
  Field('IDN', 'string',20,''),
  Field('origin', 'string',20,'IP'),
  Field('datetime', 'string',12,'00:00:00'),
  Field('protocol', 'string',8,'IP'),
  Field('IP_addr', 'string',40,'aa.aa.aa.aa'),
  Field('port', 'string',10,'0000'),
  Field('mac', 'string',12,''),
  Field('status', 'string',10),
  Field('risk', 'integer',0),
  Field('hits', 'integer',0),
  Field('longitude', 'double',0),
  Field('latitude', 'double',0))

