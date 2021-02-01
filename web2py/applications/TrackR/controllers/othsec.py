# -*- coding: utf-8 -*-
import simplejson as json
import sys, socket, datetime as dt, threading
import logging
import pyparsing as pp
import ctypes
import datetime

###########################################################################################################################################################
# def uint32_to_int32(i):
###########################################################################################################################################################
def uint32_to_int32(i):
    return ctypes.c_int32(i).value

###########################################################################################################################################################
# def int32_to_uint32(i):
###########################################################################################################################################################
def int32_to_uint32(i):
    return ctypes.c_uint32(i).value

###########################################################################################################################################################
# def MyLONG2IP(a):
###########################################################################################################################################################
# Converting IP Long / decimal (3232235521) to IP dotted address (192.168.0.1)
def MyLONG2IP(a):
   b = [0,0,0,0]
   c = 16777216.0
   a += 0.0
   for i in range(4):
      k = int((a / c))
      a -= c * k
      b[i]= k
      c /= 256.0
      d = '.'.join(str(x) for x in b)
   return(str(d))

###########################################################################################################################################################
# def MyIP2LONG(a):
###########################################################################################################################################################
def MyIP2LONG(a):
   d = 0.0
   if len(str(a)) > 0:
       b = str(a).split(".")
       if len(b) == 4:
         for i in range(4):
           d *= 256.0
           d += int(b[i])
   return(int(d))

###########################################################################################################################################################
# def LocalizeIpAddress(ip_client):
###########################################################################################################################################################
def LocalizeIpAddress(ip_client):
    myvalue = MyIP2LONG(ip_client)
    vlat = 0.0
    vlon = 0.0
    if myvalue != None:
        ipquery = (db.ipligence2.ip_from <= myvalue) & (db.ipligence2.ip_to >= myvalue)
        # Fetch data related to IP address (IPligence database)
        for row in db(ipquery).select():
            vlon = row['longitude']
            vlat = row['latitude']
            if (vlat + vlon > 0):
                break
    return([vlon, vlat])

###########################################################################################################################################################
# def InsertLocalizedInfoInDB(anobject):
###########################################################################################################################################################
def InsertLocalizedInfoInDB(anobject):
    if (len(anobject)==0 ):
        logger.debug('InsertLocalizedInfoInDB(IP): objects empty')
    else:
        logger.debug('InsertLocalizedInfoInDB(IP): %s ' % anobject['ip_addr'])

        IsAValidIP = False
        IPaddr = ''

        try:
            socket.inet_aton(anobject['ip_addr'])
        except socket.error:
            try:
                IPaddr = socket.gethostbyname(anobject['ip_addr'])
            except socket.error:
                IPaddr = 'Invalid'
            else:
                IPaddr = socket.gethostbyname(anobject['ip_addr'])
                IsAValidIP = True
        else:
            IPaddr = anobject['ip_addr']
            IsAValidIP = True

        if IsAValidIP :
            try:
                lon = 0
                lat = 0
                [lon, lat] = LocalizeIpAddress(IPaddr)
            except Exception, e:
                logger.debug('InsertLocalizedInfoInDB->LocalizeIpAddress(IP): Exception - %s' % e)
            else:
                try:
                    anobject['longitude'] = lon
                    anobject['latitude'] = lat
                    db.ipanalyzed.bulk_insert([anobject])
                except Exception, e:
                    logger.debug('InsertLocalizedInfoInDB(IP): Exception - %s' % e)
                    logger.debug('InsertLocalizedInfoInDB(IP): return = ' + str(anobject))
                else:
                    logger.debug('InsertLocalizedInfoInDB(IP): return = ' + str(anobject))
                    db.commit()
    return

###########################################################################################################################################################
# def InsertLocalizedInfoInDBLog(anobject):
###########################################################################################################################################################
def InsertLocalizedInfoInDBLog(anobject):
    if (len(anobject)==0 ):
        logger.debug('InsertLocalizedInfoInDBLog(IP): objects empty')
    else:
        logger.debug('InsertLocalizedInfoInDBLog(IP): %s ' % anobject['ip_addr'])

        IsAValidIP = False
        IPaddr = ''

        try:
            socket.inet_aton(anobject['ip_addr'])
        except socket.error:
            try:
                IPaddr = socket.gethostbyname(anobject['ip_addr'])
            except socket.error:
                IPaddr = 'Invalid'
            else:
                IPaddr = socket.gethostbyname(anobject['ip_addr'])
                IsAValidIP = True
        else:
            IPaddr = anobject['ip_addr']
            IsAValidIP = True

        if IsAValidIP :
            try:
                lon = 0
                lat = 0
                [lon, lat] = LocalizeIpAddress(IPaddr)
            except Exception, e:
                logger.debug('InsertLocalizedInfoInDBLog->LocalizeIpAddress(IP): Exception - %s' % e)
            else:
                try:
                    anobject['longitude'] = lon
                    anobject['latitude'] = lat
                    db.loganalyzed.bulk_insert([anobject])
                except Exception, e:
                    logger.debug('InsertLocalizedInfoInDBLog(IP): Exception - %s' % e)
                    logger.debug('InsertLocalizedInfoInDBLog(IP): return = ' + str(anobject))
                else:
                    logger.debug('InsertLocalizedInfoInDBLog(IP): return = ' + str(anobject))
                    db.commit()
    return

###########################################################################################################################################################
# def parseTCPTcpdump(stringToParse, theUsername):
###########################################################################################################################################################
def parseTCPTcpdump(stringToParse, theUsername):
    try:
        #logger.debug('parseTCPTcpdump(stringToParse): = ' + str(stringToParse))
        parseObjectOTHSEC = dict()
        parseObjectIPANALYZED1 = dict()
        parseObjectIPANALYZED2 = dict()
        DATETIME = pp.Word(pp.nums+'.')
        PROTOCOL = pp.Word(pp.alphas)
        IPFROM = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        IPTO = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        theIPFrom = ''
        thePortFrom = ''
        theIPTo = ''
        thePortTo = ''
        theFLAGS = ''
        theLine = DATETIME + PROTOCOL + IPFROM + pp.OneOrMore(pp.Literal('>')) + IPTO + pp.restOfLine
        resultLine = theLine.parseString(stringToParse)
        theRest = resultLine[5]
        txt=resultLine[0].split('.')
        theDateTime = dt.datetime.fromtimestamp(float(txt[0])).strftime('%Y-%m-%d %X')

        theProtocol = resultLine[1]
        if (theProtocol == 'IP'):
            varIP = resultLine[2].split('.')
            thePortFrom = varIP.pop()
            theIPFrom = ".".join(varIP)

            varIP = resultLine[4].split('.')
            thePortTo = varIP.pop()
            thePortTo = thePortTo[:-1]
            theIPTo = ".".join(varIP)

        else:
            varIP = resultLine[2].split('.')
            thePortFrom = varIP.pop()
            theIPFrom = varIP

            varIP = resultLine[4].split('.')
            thePortTo = varIP.pop()
            thePortTo = thePortTo[:-1]
            theIPTo = varIP

        try:
            FLAGS = pp.Word(pp.alphas+'.')
            theLineDetails = pp.SkipTo(pp.Literal('Flags ['), include=True) + FLAGS + pp.Literal('],') + pp.restOfLine
            resultLineDetails = theLineDetails.parseString(resultLine[5])
            theFLAGS = resultLineDetails[1]
        except Exception, e:
            logger.debug('parseTCPTcpdump(stringToParse): Exception - %s' % e)

        parseObjectOTHSEC = { 'body_message': theRest, 'flags': str(theFLAGS),'addr_from': theIPFrom, 'port_from': thePortFrom, 'addr_to': theIPTo, 'port_to': thePortTo, 'protocol': theProtocol, 'datetime_remote': theDateTime, 'datetime_othsec': datetime.datetime.now().strftime('%Y-%m-%d %X'), 'username': str(theUsername)  }
        parseObjectIPANALYZED1 = { 'username': str(theUsername), 'ip_addr': theIPTo, 'port': thePortTo, 'protocol': theProtocol, 'datetime': theDateTime }
        parseObjectIPANALYZED2 = { 'username': str(theUsername), 'ip_addr': theIPFrom, 'port': thePortFrom, 'protocol': theProtocol, 'datetime': theDateTime }
    except Exception, e:
        logger.debug('parseTCPTcpdump(stringToParse): Exception - %s' % e)
        #logger.debug('parseTCP(stringToParse): parseObjectOTHSEC = ' + str(parseObjectOTHSEC))
        #logger.debug('parseTCP(stringToParse): parseObjectIPANALYZED1 = ' + str(parseObjectIPANALYZED1))
        #logger.debug('parseTCP(stringToParse): parseObjectIPANALYZED2 = ' + str(parseObjectIPANALYZED2))
    else:
        return([parseObjectOTHSEC,parseObjectIPANALYZED1,parseObjectIPANALYZED2])
    return

###########################################################################################################################################################
# def parseTCPSnif(stringToParse, theUsername):
###########################################################################################################################################################
def parseTCPSnif(stringToParse, theUsername):
    try:
        parseObjectOTHSEC = dict()
        parseObjectIPANALYZED1 = dict()
        parseObjectIPANALYZED2 = dict()

        logger.debug('parseTCPSnif(stringToParse): = ' + str(stringToParse))

        now_datetime = pp.Word(pp.nums)								# datetime

        iph_version = pp.Word(pp.nums)					            # IP Version
        iph_iphdrlen = pp.Word(pp.nums)						        # IP Header Length
        iph_tos = pp.Word(pp.nums)						            # Type Of Service
        iph_tot_len = pp.Word(pp.nums)							    # IP Total Length
        iph_id = pp.Word(pp.nums)								    # Identification
        iph_offset = pp.Word(pp.nums)								# Offset
        iph_ttl = pp.Word(pp.nums)						            # TTL
        iph_protocol  = pp.Word(pp.nums)				            # Protocol
        iph_check = pp.Word(pp.nums)				                # Checksum

        iph_vfc = pp.Word(pp.nums)						        # IP Version
        iph_flow = pp.Word(pp.nums)						        # Flow
        iph_plen = pp.Word(pp.nums)							    # IP Header Length
        iph_nxt = pp.Word(pp.nums)								# Next Header
        iph_hlim = pp.Word(pp.nums)						        # Limit
        iph_hops  = pp.Word(pp.nums)				            # Hops

        source_sin_addr = pp.Word(pp.alphanums+'.'+':'+'-'+'_')     # Source IP
        dest_sin_addr = pp.Word(pp.alphanums+'.'+':'+'-'+'_')       # Destination IP

        tcph_source = pp.Word(pp.nums)							    # Source Port
        tcph_dest = pp.Word(pp.nums)							    # Destination Port
        tcph_seq = pp.Word(pp.nums)							        # Sequence Number
        tcph_ack_seq = pp.Word(pp.nums)						        # Acknowledge Number
        tcph_doff = pp.Word(pp.nums)					            # Header Length
        tcph_urg = pp.Word(pp.alphanums+'-')						# Urgent Flag
        tcph_ack = pp.Word(pp.alphanums+'-')						# Acknowledgement Flag
        tcph_psh = pp.Word(pp.alphanums+'-')						# Push Flag
        tcph_rst = pp.Word(pp.alphanums+'-')						# Reset Flag
        tcph_syn = pp.Word(pp.alphanums+'-')						# Synchronise Flag
        tcph_fin = pp.Word(pp.alphanums+'-')						# Finish Flag
        tcph_window = pp.Word(pp.nums)							    # Window
        tcph_check = pp.Word(pp.nums)							    # Checksum
        tcph_urg_ptr = pp.Word(pp.nums)							    # Urgent Pointer

        theLineBeg = now_datetime + iph_version + pp.restOfLine
        resultLine = theLineBeg.parseString(stringToParse)
        ip_version = int(resultLine[1])

        parseObjectOTHSEC['datetime_othsec'] = str(dt.datetime.now().strftime('%Y-%m-%d %X'))	 # datetime
        parseObjectOTHSEC['username'] = str(theUsername)                                         # username

        if (ip_version == 4):

            theLine = now_datetime + iph_version + iph_iphdrlen + iph_tos + iph_tot_len + iph_id + iph_offset + iph_ttl + iph_protocol + \
                iph_check + source_sin_addr + dest_sin_addr + tcph_source + tcph_dest + tcph_seq + tcph_ack_seq + \
                tcph_doff + tcph_urg + tcph_ack + tcph_psh + tcph_rst + tcph_syn + tcph_fin + \
                tcph_window + tcph_check + tcph_urg_ptr + pp.restOfLine

            resultLine = theLine.parseString(stringToParse)

            theDateTime = dt.datetime.fromtimestamp(float(resultLine[0])).strftime('%Y-%m-%d %X')
            parseObjectOTHSEC['datetime_remote'] = str(theDateTime)								         # datetime
            parseObjectOTHSEC['iph_version'] = int(resultLine[1])				                         # IP Version
            parseObjectOTHSEC['iph_iphdrlen'] = int(resultLine[2])						                 # IP Header Length
            parseObjectOTHSEC['iph_tos'] = int(resultLine[3])						                     # Type Of Service
            parseObjectOTHSEC['iph_tot_len'] = int(resultLine[4])							             # IP Total Length
            parseObjectOTHSEC['iph_id'] = int(resultLine[5])							                 # Identification
            parseObjectOTHSEC['iph_offset'] = int(resultLine[6])							             # Offset
            parseObjectOTHSEC['iph_ttl'] = int(resultLine[7])						                     # TTL
            parseObjectOTHSEC['protocol']  = str(resultLine[8])				                             # Protocol
            parseObjectOTHSEC['iph_check'] = int(resultLine[9])				                             # Checksum
            parseObjectOTHSEC['addr_from'] = str(resultLine[10])				                         # Source IP
            parseObjectOTHSEC['addr_to'] = str(resultLine[11])					                         # Destination IP
            parseObjectOTHSEC['port_from'] = str(resultLine[12])			                	         # Source Port
            parseObjectOTHSEC['port_to'] = str(resultLine[13])							                 # Destination Port
            parseObjectOTHSEC['tcph_seq'] = uint32_to_int32(int(resultLine[14]))							                 # Sequence Number
            parseObjectOTHSEC['tcph_ack_seq'] = uint32_to_int32(int(resultLine[15]))						                 # Acknowledge Number
            parseObjectOTHSEC['tcph_doff'] = int(resultLine[16])					                     # Header Length
            parseObjectOTHSEC['tcph_urg'] = int(resultLine[17] == 'U')							         # Urgent Flag
            parseObjectOTHSEC['tcph_ack'] = int(resultLine[18] == 'A')							         # Acknowledgement Flag
            parseObjectOTHSEC['tcph_psh'] = int(resultLine[19] == 'P')						             # Push Flag
            parseObjectOTHSEC['tcph_rst'] = int(resultLine[20] == 'R')						             # Reset Flag
            parseObjectOTHSEC['tcph_syn'] = int(resultLine[21] == 'S')							         # Synchronise Flag
            parseObjectOTHSEC['tcph_fin'] = int(resultLine[22] == 'F')							         # Finish Flag
            parseObjectOTHSEC['tcph_window'] = uint32_to_int32(int(resultLine[23]))							             # Window
            parseObjectOTHSEC['tcph_check'] = uint32_to_int32(int(resultLine[24]))							             # Checksum
            parseObjectOTHSEC['tcph_urg_ptr'] = uint32_to_int32(int(resultLine[25]))						                 # Urgent Pointer
            parseObjectOTHSEC['body_message'] = str(resultLine[26])						                 # Body

            parseObjectIPANALYZED1 = { 'username': str(theUsername), 'ip_addr': parseObjectOTHSEC['addr_from'], 'port': str(parseObjectOTHSEC['port_from']), 'ip_version': int(resultLine[1]), 'tcp_protocol': uint32_to_int32(int(parseObjectOTHSEC['protocol'])), 'datetime': theDateTime, 'tcph_urg': int(parseObjectOTHSEC['tcph_urg']), 'tcph_ack': int(parseObjectOTHSEC['tcph_ack']), 'tcph_psh': int(parseObjectOTHSEC['tcph_psh']), 'tcph_rst': int(parseObjectOTHSEC['tcph_rst']), 'tcph_syn': int(parseObjectOTHSEC['tcph_syn']), 'tcph_fin': int(parseObjectOTHSEC['tcph_fin']) }
            parseObjectIPANALYZED2 = { 'username': str(theUsername), 'ip_addr': parseObjectOTHSEC['addr_to'], 'port': str(parseObjectOTHSEC['port_to']), 'ip_version': int(resultLine[1]), 'tcp_protocol': uint32_to_int32(int(parseObjectOTHSEC['protocol'])), 'datetime': theDateTime, 'tcph_urg': int(parseObjectOTHSEC['tcph_urg']), 'tcph_ack': int(parseObjectOTHSEC['tcph_ack']), 'tcph_psh': int(parseObjectOTHSEC['tcph_psh']), 'tcph_rst': int(parseObjectOTHSEC['tcph_rst']), 'tcph_syn': int(parseObjectOTHSEC['tcph_syn']), 'tcph_fin': int(parseObjectOTHSEC['tcph_fin']) }

        elif (ip_version == 96):

            theLine = now_datetime + iph_vfc + iph_flow + iph_plen + iph_nxt + iph_hlim + iph_hops + \
                source_sin_addr + dest_sin_addr + \
                tcph_source + tcph_dest + tcph_seq + tcph_ack_seq + tcph_doff + tcph_urg + \
                tcph_ack + tcph_psh + tcph_rst + tcph_syn + tcph_fin +\
                tcph_window + tcph_check + tcph_urg_ptr + pp.restOfLine

            resultLine = theLine.parseString(stringToParse)

            theDateTime = dt.datetime.fromtimestamp(float(resultLine[0])).strftime('%Y-%m-%d %X')
            parseObjectOTHSEC['datetime_remote'] = str(theDateTime)								         # datetime
            parseObjectOTHSEC['iph_vfc'] = int(resultLine[1])				                             # IP Version
            parseObjectOTHSEC['iph_flow'] = int(resultLine[2])						                     # IP Header Length
            parseObjectOTHSEC['iph_plen'] = int(resultLine[3])						                     # Type Of Service
            parseObjectOTHSEC['iph_nxt'] = int(resultLine[4])							                 # IP Total Length
            parseObjectOTHSEC['iph_hlim'] = int(resultLine[5])							                 # Identification
            parseObjectOTHSEC['iph_offset'] = int(resultLine[6])							             # Offset
            parseObjectOTHSEC['iph_hops'] = int(resultLine[7])						                     # TTL
            parseObjectOTHSEC['addr_from'] = str(resultLine[8])				                             # Source IP
            parseObjectOTHSEC['addr_to'] = str(resultLine[9])					                         # Destination IP
            parseObjectOTHSEC['port_from'] = str(resultLine[10])			                	         # Source Port
            parseObjectOTHSEC['port_to'] = str(resultLine[11])							                 # Destination Port
            parseObjectOTHSEC['tcph_seq'] = uint32_to_int32(int(resultLine[12]))							                 # Sequence Number
            parseObjectOTHSEC['tcph_ack_seq'] = uint32_to_int32(int(resultLine[13]))						                 # Acknowledge Number
            parseObjectOTHSEC['tcph_doff'] = int(resultLine[14])					                     # Header Length
            parseObjectOTHSEC['tcph_urg'] = int(resultLine[15] == 'U')							         # Urgent Flag
            parseObjectOTHSEC['tcph_ack'] = int(resultLine[16] == 'A')							         # Acknowledgement Flag
            parseObjectOTHSEC['tcph_psh'] = int(resultLine[17] == 'P')							         # Push Flag
            parseObjectOTHSEC['tcph_rst'] = int(resultLine[18] == 'R')						             # Reset Flag
            parseObjectOTHSEC['tcph_syn'] = int(resultLine[19] == 'S')							         # Synchronise Flag
            parseObjectOTHSEC['tcph_fin'] = int(resultLine[20] == 'F')							         # Finish Flag
            parseObjectOTHSEC['tcph_window'] = uint32_to_int32(int(resultLine[21]))							             # Window
            parseObjectOTHSEC['tcph_check'] = uint32_to_int32(int(resultLine[22]))							             # Checksum
            parseObjectOTHSEC['tcph_urg_ptr'] = uint32_to_int32(int(resultLine[23]))						                 # Urgent Pointer
            parseObjectOTHSEC['body_message'] = str(resultLine[24])						                 # rest of mess

            parseObjectIPANALYZED1 = { 'username': str(theUsername), 'ip_addr': parseObjectOTHSEC['addr_from'], 'port': parseObjectOTHSEC['port_from'], 'ip_version': int(resultLine[1]), 'tcp_protocol': uint32_to_int32(int(parseObjectOTHSEC['iph_flow'])), 'datetime': theDateTime, 'tcph_urg': int(parseObjectOTHSEC['tcph_urg']), 'tcph_ack': int(parseObjectOTHSEC['tcph_ack']), 'tcph_psh': int(parseObjectOTHSEC['tcph_psh']), 'tcph_rst': int(parseObjectOTHSEC['tcph_rst']), 'tcph_syn': int(parseObjectOTHSEC['tcph_syn']), 'tcph_fin': int(parseObjectOTHSEC['tcph_fin']) }
            parseObjectIPANALYZED2 = { 'username': str(theUsername), 'ip_addr': parseObjectOTHSEC['addr_to'], 'port': parseObjectOTHSEC['port_from'], 'ip_version': int(resultLine[1]), 'tcp_protocol': uint32_to_int32(int(parseObjectOTHSEC['iph_flow'])), 'datetime': theDateTime, 'tcph_urg': int(parseObjectOTHSEC['tcph_urg']), 'tcph_ack': int(parseObjectOTHSEC['tcph_ack']), 'tcph_psh': int(parseObjectOTHSEC['tcph_psh']), 'tcph_rst': int(parseObjectOTHSEC['tcph_rst']), 'tcph_syn': int(parseObjectOTHSEC['tcph_syn']), 'tcph_fin': int(parseObjectOTHSEC['tcph_fin']) }

        else:
            return;

    except Exception, e:
        logger.debug('parseTCPSnif(stringToParse): Exception - %s' % e)

    else:
        return([parseObjectOTHSEC,parseObjectIPANALYZED1,parseObjectIPANALYZED2])
    return

###########################################################################################################################################################
# def parseTCPTail(stringToParse, theUsername):
###########################################################################################################################################################
def parseTCPTail(stringToParse, theUsername):
    try:
        #logger.debug('parseTCPTail(stringToParse): = ' + str(stringToParse))
        parseObjectLOGANALYZED = dict()
        DATETIME = pp.Word(pp.alphas) + pp.Word(pp.nums+'.') + pp.Word(pp.nums+':')
        HOST = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        SERVICE = pp.Word(pp.alphanums+'.'+':'+'-'+'_'+'['+']')
        IP = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        USER = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        PORT = pp.Word(pp.alphanums+'.'+':'+'-'+'_')
        theIP = ''
        theUser = ''
        theLine1 = DATETIME + pp.SkipTo(pp.Literal('authentication failure;'), include=True) + pp.SkipTo(pp.Literal('rhost='), include=True) + IP + pp.SkipTo(pp.Literal('user='), include=True) + USER + pp.restOfLine
        theLine2 = DATETIME + HOST + SERVICE + pp.SkipTo(pp.Literal('Failed password for'), include=True) + USER + pp.Literal('from') + IP + pp.Literal('port') + PORT + pp.restOfLine

        resultLine1 = None
        resultLine2 = None

        try:
            resultLine1 = theLine1.parseString(stringToParse)
        except Exception, e:
            logger.debug('parseTCPTail(stringToParse): Exception - %s' % e)
        else:
            logger.debug('parseTCPTail() match rule 1 - authentication failure ')
            theDateTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            theService = resultLine1[4]
            theUser = resultLine1[7]
            theIP = resultLine1[9]
            thePort = resultLine1[11]

        try:
            resultLine2 = theLine2.parseString(stringToParse)
        except Exception, e:
            logger.debug('parseTCPTail(stringToParse): Exception - %s' % e)
        else:
            logger.debug('parseTCPTail() match rule 2 - Failed password')
            theDateTime = datetime.datetime.now().strftime('%Y-%m-%d %X')
            theService = resultLine2[4]
            theUser = resultLine2[7]
            theIP = resultLine2[8]
            thePort = resultLine2[10]

            parseObjectLOGANALYZED = { 'username': str(theUsername), 'logon': str(theUser), 'ip_addr': theIP, 'port': thePort, 'service': theService, 'auth_failure': 1, 'datetime': theDateTime }
            return([parseObjectLOGANALYZED])

    except Exception, e:
        logger.debug('parseTCPTail(stringToParse): Exception - %s' % e)

    return

###########################################################################################################################################################
# def InsertTraceInDB():
###########################################################################################################################################################
def InsertTraceInDB():
  try:
    lock = threading.Lock()
    lock.acquire()
    myParam = ''
    theUsername = ''
    SQLtext = dict()
    if not request.vars.aTrace:
        logger.debug('InsertTraceInDB(): with empty param')
    else:
        myParam = request.vars.aTrace;
        theUsername = request.vars.aUsername;

        try:
            #logger.debug('InsertTraceInDB(): myParam = ' + str(myParam))
            ListObjects = parseTCPTcpdump(myParam, theUsername)
            db.othsec.bulk_insert([ListObjects[0]])
            InsertLocalizedInfoInDB(ListObjects[1])
            InsertLocalizedInfoInDB(ListObjects[2])
        except Exception, e:
            logger.debug('InsertTraceInDB(): Exception - %s' % e)
            logger.debug('InsertTraceInDB(IPoth): anobject0 = ' + str(ListObjects[0]))
            logger.debug('InsertTraceInDB(IPFrom): anobject1 = ' + str(ListObjects[1]))
            logger.debug('InsertTraceInDB(IPto): anobject2 = ' + str(ListObjects[2]))
        else:
            db.commit()
            logger.debug('InsertTraceInDB(IPoth): anobject0 = ' + str(ListObjects[0]))
            logger.debug('InsertTraceInDB(IPFrom): anobject1 = ' + str(ListObjects[1]))
            logger.debug('InsertTraceInDB(IPto): anobject2 = ' + str(ListObjects[2]))
        return
  finally:
    lock.release()

###########################################################################################################################################################
# def InsertLogInDB():
###########################################################################################################################################################
def InsertLogInDB():
  try:
    lock = threading.Lock()
    lock.acquire()
    myParam = ''
    theUsername = ''
    SQLtext = dict()
    if not request.vars.aLog:
        logger.debug('InsertLogInDB(): error since empty param received from web client ajax')
    else:
        myParam = request.vars.aLog;
        theUsername = request.vars.aUsername;

        try:
            #logger.debug('InsertLogInDB(): myParam = ' + str(myParam))
            ListObjects = parseTCPTail(myParam, theUsername)
            logger.debug('InsertLogInDB(): anobject = ' + str(ListObjects[0]))
            InsertLocalizedInfoInDBLog(ListObjects[0])
        except Exception, e:
            logger.debug('InsertLogInDB(): Exception - %s' % e)
            logger.debug('InsertLogInDB(IPoth): Exception - anobject0 = ' + str(ListObjects[0]))
        else:
            db.commit()
            logger.debug('InsertLogInDB(IPoth): anobject0 = ' + str(ListObjects[0]))
        return
  finally:
      lock.release()

###########################################################################################################################################################
# def InsertSnifInDB():
###########################################################################################################################################################
def InsertSnifInDB():
  try:
    lock = threading.Lock()
    lock.acquire()
    myParam = ''
    theUsername = ''
    SQLtext = dict()
    if not request.vars.aSnif:
        logger.debug('InsertSnifInDB(): with empty param')
    else:
        myParam = request.vars.aSnif;
        theUsername = request.vars.aUsername;

        try:
            logger.debug('InsertTraceInDB(): myParam = ' + str(myParam))
            ListObjects = parseTCPSnif(myParam, theUsername)
            db.othsec.bulk_insert([ListObjects[0]])
            InsertLocalizedInfoInDB(ListObjects[1])
            InsertLocalizedInfoInDB(ListObjects[2])
        except Exception, e:
            logger.debug('InsertSnifInDB(): Exception - %s' % e)
            if (ListObjects[0]): logger.debug('InsertSnifInDB(IPoth): Exception - anobject0 = ' + str(ListObjects[0]))
            else: logger.debug('InsertSnifInDB(IPoth): anobject0 = EMPTY')
            if (ListObjects[1]): logger.debug('InsertSnifInDB(IPFrom): Exception - anobject1 = ' + str(ListObjects[1]))
            else: logger.debug('InsertSnifInDB(IPoth): anobject1 = EMPTY')
            if (ListObjects[2]): logger.debug('InsertSnifInDB(IPto): Exception - anobject2 = ' + str(ListObjects[2]))
            else: logger.debug('InsertSnifInDB(IPoth): anobject2 = EMPTY')
        else:
            db.commit()
            logger.debug('InsertSnifInDB(IPoth): anobject0 = ' + str(ListObjects[0]))
            logger.debug('InsertSnifInDB(IPFrom): anobject1 = ' + str(ListObjects[1]))
            logger.debug('InsertSnifInDB(IPto): anobject2 = ' + str(ListObjects[2]))
        return
  finally:
    lock.release()

###########################################################################################################################################################
# def lookup(addr):
###########################################################################################################################################################
def lookup(addr):
     try:
         return socket.gethostbyaddr(addr)
     except socket.herror:
         return addr, None, None

###########################################################################################################################################################
# def GetListMarkers():
###########################################################################################################################################################
@auth.requires_login()
def GetListMarkers():
    if ((not request.vars.aUsername) or (not request.vars.aPeriod)):
        logger.debug('GetListMarkers(): with empty param')
    else:
        try:
            lock = threading.Lock()
            lock.acquire()
            theUsername = request.vars['aUsername']
            thePeriod = request.vars['aPeriod']
            arrayOfMarks = []
            theDate = dt.datetime.now()
            logger.debug('GetListMarkers(): params = %s, %s' % (theUsername, thePeriod))
            if (thePeriod):
                if (thePeriod == 'TODAY'):
                    queryPeriod = (db.ipanalyzed.datetime >= theDate.replace(hour=0,minute=0,second=0,microsecond=0)) & (db.ipanalyzed.datetime < theDate)
                elif (thePeriod == '24H'):
                    queryPeriod = (db.ipanalyzed.datetime >= theDate - dt.timedelta(hours=24)) & (db.ipanalyzed.datetime < theDate)
                elif (thePeriod == '30D'):
                    queryPeriod = (db.ipanalyzed.datetime >= theDate - dt.timedelta(days=30)) & (db.ipanalyzed.datetime < theDate)
                elif (thePeriod == 'YEAR'):
                    queryPeriod = (db.ipanalyzed.datetime >= theDate.replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)) & (db.ipanalyzed.datetime < theDate)
                elif (thePeriod[:5] == 'FROM='):
                    try:
                        theDate = datetime.datetime.strptime(thePeriod[5:],'%Y-%m-%d %H:%M:%S')
                        logger.debug('GetListMarkers(params): DateTime FROM= %s' % (thePeriod[5:]))
                        queryPeriod = (db.ipanalyzed.datetime >= theDate)
                    except:
                        logger.error('GetListMarkers(): datetime = %s' % (thePeriod[5:]))
                        queryPeriod = (db.ipanalyzed.datetime >= theDate - dt.timedelta(hours=1)) & (db.ipanalyzed.datetime < theDate)
                else: # 1H = default
                    queryPeriod = (db.ipanalyzed.datetime >= theDate - dt.timedelta(hours=1)) & (db.ipanalyzed.datetime < theDate)
            else: # 1H = default
                queryPeriod = (db.ipanalyzed.datetime >= theDate)

            query = queryPeriod & (db.ipanalyzed.username == theUsername) & (~db.ipanalyzed.ip_addr.like("224.%")) & (~db.ipanalyzed.ip_addr.like("127.%")) & (~db.ipanalyzed.ip_addr.like("169.254.%")) & (~db.ipanalyzed.ip_addr.like("192.168.%")) & (~db.ipanalyzed.ip_addr.like("172.16.%")) & ((db.ipanalyzed.latitude > 0) | (db.ipanalyzed.longitude > 0)) & (db.ipanalyzed.username == auth.user.email) & (db.ipanalyzed.tcp_protocol != 17)
            rows = db(query).select( db.ipanalyzed.latitude, db.ipanalyzed.longitude, db.ipanalyzed.ip_addr, distinct=True)
            for row in rows:
                ip_hostname =  ''
                ip_hostname, alias, addresslist  = lookup(row.ip_addr)

                #queryBan = (db.loganalyzed.ip_addr.like(str(row.ip_addr)))
                queryBan = (db.loganalyzed.longitude == row.longitude) & (db.loganalyzed.latitude == row.latitude) & (db.loganalyzed.banned > 0)
                rowBanned = db(queryBan).select( db.loganalyzed.banned).first()

                if (rowBanned is not None):
                    IPIsBanned = rowBanned['banned']
                else:
                    IPIsBanned = 0

                if ((ip_hostname == '') or (ip_hostname is None)):
                    arrayOfMarks.append( [row.latitude, row.longitude, row.ip_addr, IPIsBanned])
                else:
                    arrayOfMarks.append( [row.latitude, row.longitude, ip_hostname, IPIsBanned])

            logger.debug('GetListMarkers(): return= %s' % (json.dumps(arrayOfMarks)))
        finally:
            lock.release()

        return json.dumps(arrayOfMarks)

    ###########################################################################################################################################################
# def GetListAnoMarkers():
###########################################################################################################################################################
@auth.requires_login()
def GetListAnoMarkers():
    if ((not request.vars.aUsername) or (not request.vars.aPeriod)):
        logger.debug('GetListMarkers(): with empty param')
    else:
        try:
            lock = threading.Lock()
            lock.acquire()
            theUsername = request.vars['aUsername']
            thePeriod = request.vars['aPeriod']
            arrayOfMarks = []
            theDate = dt.datetime.now()
            logger.debug('GetListAnoMarkers(params): %s, %s' % (theUsername, thePeriod))

            if (thePeriod == 'TODAY'):
                queryPeriod = (db.loganalyzed.datetime >= theDate.replace(hour=0,minute=0,second=0,microsecond=0)) & (db.loganalyzed.datetime < theDate)
            elif (thePeriod == '24H'):
                queryPeriod = (db.loganalyzed.datetime >= theDate - dt.timedelta(hours=24)) & (db.loganalyzed.datetime < theDate)
            elif (thePeriod == '30D'):
                queryPeriod = (db.loganalyzed.datetime >= theDate - dt.timedelta(days=30)) & (db.loganalyzed.datetime < theDate)
            elif (thePeriod == '1H'):
                queryPeriod = (db.loganalyzed.datetime >= theDate - dt.timedelta(hours=1)) & (db.loganalyzed.datetime < theDate)
            else: # YEAR = default
                queryPeriod = (db.loganalyzed.datetime >= theDate.replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)) & (db.loganalyzed.datetime < theDate)

            query = queryPeriod & (db.loganalyzed.username == auth.user.email)
            rows = db(query).select( db.loganalyzed.latitude, db.loganalyzed.longitude, db.loganalyzed.ip_addr, db.loganalyzed.banned, distinct=True)
            for row in rows:
                ip_hostname =  ''
                ip_hostname, alias, addresslist  = lookup(row.ip_addr)

                arrayOfMarks.append( [row.latitude, row.longitude, row.ip_addr, row.banned])

            logger.debug('GetListAnoMarkers([%s,%s]): %s' % (theUsername, thePeriod, json.dumps(arrayOfMarks)))
        finally:
            lock.release()

        return json.dumps(arrayOfMarks)

###########################################################################################################################################################
# def index():
###########################################################################################################################################################
@auth.requires_login()
def index():
    return locals()

###########################################################################################################################################################
# def ClientoThSecWebSocket():
###########################################################################################################################################################
@auth.requires_login()
def ClientoThSecWebSocket():
    return locals()

###########################################################################################################################################################
# def DisplayXtermForm():
###########################################################################################################################################################
@auth.requires_login()
def DisplayXtermForm():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    myquery = (db.othsec.idn != None) | (db.othsec.idn < 10)
    gridOTHSEC = SQLFORM.grid(myquery, showbuttontext=False, exportclasses=export_classes)
    return dict( gridOTHSEC = gridOTHSEC)

###########################################################################################################################################################
# def DisplayXtermFormSniffer():
###########################################################################################################################################################
@auth.requires_login()
def DisplayXtermFormSniffer():
    return dict()

###########################################################################################################################################################
# def DisplayXtermFormSnifferAndGeolocMap():
###########################################################################################################################################################
@auth.requires_login()
def DisplayXtermFormSnifferAndGeolocMap():
    return dict()

###########################################################################################################################################################
# def DisplayXtermFormTail():
###########################################################################################################################################################
@auth.requires_login()
def DisplayXtermFormTail():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    myquery = (db.othsec.idn != None) | (db.othsec.idn < 10)
    gridOTHSEC = SQLFORM.grid(myquery, showbuttontext=False, exportclasses=export_classes)
    return dict( gridOTHSEC = gridOTHSEC)


###########################################################################################################################################################
# tryconvertport(value):
###########################################################################################################################################################
def tryconvertport(value):
    default = value
    try:
        return socket.getservbyport(int(value))
    except:
        return default


###########################################################################################################################################################
# trymakelinkToViewOnMap(anIP):
###########################################################################################################################################################
def trymakelinkToViewOnMap(anIP):
    try:
        return A('<Voir sur MAP>',_href=URL("trackrctrl","DisplayTrackRIPGeo", vars=dict(Enter_IP_Address=anIP)))
    except:
        return '---'

###########################################################################################################################################################
# trymakelinkAddTrustee(anIP):
###########################################################################################################################################################
def trymakelinkAddTrustee(anIP, anID):
    try:
        return A('<Croire en '+lookup(anIP)[0]+'>',_href=URL("trackrctrl","AddTrusteeIPInDB", vars=dict(Enter_ID=anID)))
    except:
        return '---'


###########################################################################################################################################################
# def DisplayOTHSECDbGrid():
###########################################################################################################################################################
@auth.requires_login()
def DisplayOTHSECDbGrid():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)

        #Define headers as tuples/dictionaries
    headers = {'othsec.id':   'ID',
           'othsec.datetime_remote': 'Date',
           'othsec.iph_version': 'Version',
           'othsec.protocol': 'Protocol',
           'othsec.addr_from': 'IP Addr From',
           'othsec.addr_to': 'IP Addr To',
           'othsec.port_from': 'Port From',
           'othsec.port_to': 'Port To',
           'othsec.tcph_urg': 'URGENT',
           'othsec.tcph_ack': 'ACKNOW',
           'othsec.tcph_psh': 'PUSH',
           'othsec.tcph_rst': 'RESET',
           'othsec.tcph_syn': 'SYNC',
           'othsec.tcph_fin': 'FIN'
              }

    fields = (db.othsec.id,
           db.othsec.datetime_remote,
           db.othsec.iph_version,
           db.othsec.protocol,
           db.othsec.addr_from,
           db.othsec.addr_to,
           db.othsec.port_from,
           db.othsec.port_to,
           db.othsec.tcph_urg,
           db.othsec.tcph_ack,
           db.othsec.tcph_psh,
           db.othsec.tcph_rst,
           db.othsec.tcph_syn,
           db.othsec.tcph_fin)

    db.othsec.protocol.represent = lambda r, row: 'TCP' if (row.protocol == '6') else ('UDP' if (row.protocol == '17') else ('ICMP' if (row.protocol == '1') else ('IGMP' if (row.protocol == '2') else r)))
    db.othsec.iph_version.represent = lambda r, row: 'IP4' if (row.iph_version == 4) else ('IP6' if (row.iph_version == 6) else r)
    db.othsec.port_from.represent = lambda r, row: tryconvertport(row.port_from)
    db.othsec.port_to.represent = lambda r, row: tryconvertport(row.port_to)

    links = [lambda row: trymakelinkToViewOnMap(row.addr_to)]
    myquery = (db.othsec.idn != None) & (db.othsec.username == auth.user.email)
    gridOTHSEC = SQLFORM.grid(query=myquery, showbuttontext=False, exportclasses=export_classes, orderby=~db.othsec.datetime_othsec, fields=fields, headers=headers, deletable=False, editable=False, details=False, selectable=False, links=links)
    return dict( gridOTHSEC = gridOTHSEC)

###########################################################################################################################################################
# def DisplayIPANALYZEDDbGrid():
###########################################################################################################################################################
@auth.requires_login()
def DisplayIPANALYZEDDbGrid():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)

    #Define headers as tuples/dictionaries
    headers = {'ipanalyzed.id':   'ID',
           'ipanalyzed.datetime': 'datetime',
           'ipanalyzed.ip_version': 'ip_version',
           'ipanalyzed.tcp_protocol': 'protocol',
           'ipanalyzed.ip_addr': 'IP_addr',
           'ipanalyzed.port': 'port',
           'ipanalyzed.status': 'status',
           'ipanalyzed.longitude': 'longitude',
           'ipanalyzed.latitude': 'latitude',
           'ipanalyzed.tcph_syn': 'synch_conn',
           'ipanalyzed.tcph_rst': 'reset_conn'
              }

    fields = (db.ipanalyzed.id,
           db.ipanalyzed.datetime,
           db.ipanalyzed.ip_version,
           db.ipanalyzed.tcp_protocol,
           db.ipanalyzed.ip_addr,
           db.ipanalyzed.port,
           db.ipanalyzed.status,
           db.ipanalyzed.longitude,
           db.ipanalyzed.latitude,
           db.ipanalyzed.tcph_syn,
           db.ipanalyzed.tcph_rst)

    myquery = (db.ipanalyzed.tcp_protocol != 17) & (~db.ipanalyzed.ip_addr.like("127.%")) & (~db.ipanalyzed.ip_addr.like("169.254.%")) & (~db.ipanalyzed.ip_addr.like("192.168.%")) & (~db.ipanalyzed.ip_addr.like("172.16.%")) & (db.ipanalyzed.username == auth.user.email)

    db.ipanalyzed.tcp_protocol.represent = lambda r, row: 'TCP' if (row.tcp_protocol == 6) else ('UDP' if (row.tcp_protocol == 17) else ('ICMP' if (row.tcp_protocol == 1) else ('IGMP' if (row.tcp_protocol == 2) else r)))
    db.ipanalyzed.ip_version.represent = lambda r, row: 'IP4' if (row.ip_version == 4) else ('IP6' if (row.ip_version == 6) else r)
    db.ipanalyzed.port.represent = lambda r, row: tryconvertport(row.port)

    links = [lambda row: trymakelinkToViewOnMap(row.ip_addr) if ((row.latitude + row.longitude) != 0) else 'CANNOT GEOLOC IP',
            lambda row: trymakelinkAddTrustee(row.ip_addr,row.id) if ((row.latitude + row.longitude) != 0) else 'CANNOT GEOLOC IP']

    gridIPANALYZED = SQLFORM.grid( query=myquery, headers=headers, fields=fields, links=links, showbuttontext=False, exportclasses=export_classes, orderby=~db.ipanalyzed.datetime, deletable=False, editable=False, details=False, selectable=False)
    return dict( gridIPANALYZED = gridIPANALYZED)

###########################################################################################################################################################
# def DisplayLOGANALYZEDDbGrid():
###########################################################################################################################################################
@auth.requires_login()
def DisplayLOGANALYZEDDbGrid():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)

        #Define headers as tuples/dictionaries
    headers = {'ipanalyzed.id':   'ID',
           'loganalyzed.datetime': 'datetime',
           'loganalyzed.protocol': 'protocol',
           'loganalyzed.ip_addr': 'IP_addr',
           'loganalyzed.port': 'port',
           'loganalyzed.status': 'status',
           'loganalyzed.longitude': 'longitude',
           'loganalyzed.latitude': 'latitude',
           'loganalyzed.conn_tries': 'SYNCH',
           'loganalyzed.auth_failure': 'RESET',
           'loganalyzed.banned': 'banned'
              }

    fields = (db.loganalyzed.id,
           db.loganalyzed.datetime,
           db.loganalyzed.protocol,
           db.loganalyzed.ip_addr,
           db.loganalyzed.port,
           db.loganalyzed.status,
           db.loganalyzed.longitude,
           db.loganalyzed.latitude,
           db.loganalyzed.conn_tries,
           db.loganalyzed.auth_failure,
           db.loganalyzed.banned)

    myquery = (db.loganalyzed.username == auth.user.email)

    db.loganalyzed.protocol.represent = lambda r, row: 'TCP' if (row.protocol == 6) else ('UDP' if (row.protocol == 17) else ('ICMP' if (row.protocol == 1) else ('IGMP' if (row.protocol == 2) else r)))
    db.loganalyzed.port.represent = lambda r, row: tryconvertport(row.port)

    links = [lambda row: trymakelinkToViewOnMap(row.ip_addr) if ((row.latitude + row.longitude) != 0) else 'CANNOT GEOLOC IP']

    myquery = (db.loganalyzed.idn != None)
    gridIPANALYZED = SQLFORM.grid(myquery, showbuttontext=False, exportclasses=export_classes, orderby=~db.loganalyzed.datetime, headers=headers, fields=fields, links=links, deletable=False, editable=False, details=False, selectable=False)
    return dict( gridIPANALYZED = gridIPANALYZED)
