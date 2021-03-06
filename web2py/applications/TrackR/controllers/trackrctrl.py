# -*- coding: utf-8 -*-
# try something like
import re
import numpy as np
import pandas as pd
from numpy import genfromtxt
from scipy.stats import multivariate_normal
from sklearn.metrics import f1_score
from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import accuracy_score
import pygeoip
from sklearn import svm
from pydal import *
from ipaddress import *
import matplotlib as mpl
from matplotlib.colors import ListedColormap
import os
if os.environ.get('DISPLAY','') == '':
    print('no display found. Using non-interactive Agg backend')
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pylab import stem, setp, grid, savefig, show, gca, subplot, subplots_adjust
import datetime as dt
from sklearn.preprocessing import normalize
#from gluon.contrib.websocket_messaging import websocket_send
from gluon.validators import *
import struct, socket

MAX_NB_LINE_TO_READ = 99999
longitude = 0.0
latitude = 0.0
ip_collection = dict()


###########################################################################################################################################################
# def lookup_addr(addr):
###########################################################################################################################################################
def lookup_addr(addr):
     try:
         return socket.gethostbyaddr(addr)
     except socket.herror:
         return addr, None, None


###########################################################################################################################################################
# def ipLocator(ipData, ip):
###########################################################################################################################################################
def ipLocator(ipData, ip):
    loc = {}
    for i, anip in enumerate(ip):
        record = ipData.record_by_name(anip)
        if (record):
            loc[i]=(record['latitude'], record['longitude'])
        else:
            loc[i]=(0, 0)
    return loc

###########################################################################################################################################################
# def index():
###########################################################################################################################################################
@auth.requires_login()
def index():
    return(DisplayTrackRList())

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

def ip2int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]


def int2ip(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))

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
      if (vlat + vlon > 0): break
  return([vlon, vlat])

###########################################################################################################################################################
# def AnalyzeIP(an_ip):
###########################################################################################################################################################
def AnalyzeIP(an_ip):
     if (an_ip != None):
         ip_collection.setdefault(an_ip,[]).append([an_ip])
     ip_collection[an_ip].insert(0,LocalizeIpAddress(an_ip))
     return(ip_collection)

###########################################################################################################################################################
# def AnalyzeFail2BanFile(filename):
###########################################################################################################################################################
def AnalyzeFail2BanFile(filename):
    # Apache
    GeoIPDatabase = '/home/phan/trackr/modules/GeoLiteCity.dat'
    ipData = pygeoip.GeoIP(GeoIPDatabase)

    ban_data = pd.read_csv(filename, delim_whitespace=True, header=None, names=['date','time','S1','S2','S3','program','action', 'ip','rest'])

    zFilteredBan1 = ban_data[ban_data['S1'].apply(lambda x: "actions" in x)]
    if not zFilteredBan1.empty:
        zFilteredBan2 = zFilteredBan1[zFilteredBan1['action'].apply(lambda x: "Ban" in x)]

        if not zFilteredBan2.empty:
            zBan = zFilteredBan2.groupby(['ip']).size().reset_index(name='count')
            logger.debug('AnalyzeFail2BanFile(): zBan size = %d ' % ( len(zBan.index)))
            nb = 0
            bangeo = {}
            bangeo = ipLocator(ipData, zBan['ip'])
            BansXlat = [bangeo[row][0] for row in bangeo]
            BansXlong = [bangeo[row][1] for row in bangeo]
            theDateTime = dt.datetime.now().strftime('%Y-%m-%d %X')
            elem = 1
            LOGANALYZED1 = []
            for zBanIP, elemLat, elemLong, zBanCount, in zip(zBan['ip'],BansXlat,BansXlong, zBan['count']):
                ip_collection[zBanIP]=(elemLat, elemLong, zBanCount)
                #LOGANALYZED1= 'username': str(auth.user.email), 'ip_addr': str(zBanIP), 'port': '0', 'latitude': elemLat, 'longitude': elemLong, 'banned':  zBanCount, 'datetime': theDateTime "
                logger.debug('AnalyzeFail2BanFile(): LOGANALYZED1 = %s ' % ( LOGANALYZED1))
                elem = elem + 1
                db.loganalyzed.update_or_insert( (db.loganalyzed.username==str(auth.user.email)) & (db.loganalyzed.ip_addr==str(zBanIP)) & (db.loganalyzed.port==0) & (db.loganalyzed.latitude==elemLat) & (db.loganalyzed.longitude==elemLong), username=auth.user.email, ip_addr=zBanIP, port=0, latitude=elemLat, longitude=elemLong, banned=zBanCount, datetime=theDateTime)
            #if LOGANALYZED1: db.loganalyzed.bulk_insert(LOGANALYZED1)
            return(ip_collection)

###########################################################################################################################################################
# def AnalyzeLogFile(filename):
###########################################################################################################################################################
def AnalyzeLogFile(filename):
    # Apache
    # 2015-03-05 10:11:09 213.162.49.205 GET /index.html - 200 500000003 1219 7 88525 HTTP/1.1 "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:32.0) Gecko/20100101 Firefox/32.0" "-"
    # Odoo
    # 2016-04-21 16:48:03,506 1528 INFO IST werkzeug: 10.237.6.168 - - [21/Apr/2016 16:48:03] "POST /longpolling/poll HTTP/1.1" 200 -

    # Apache
    #preg_match[1] = '/(\S+) (\S+) (\S+) (\S+) (.*?\-) (\S+)/'

    # Odoo
    #preg_match[2] = '/(\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (\S+) (.*?\-) (\S+) (.*)$/'

    # ip_collection[('@IP',nb_hit,nb_ok,nb_error,'URL')]
    # ip_collection.setdefault('127.0.0.1',[]).append(['127.0.0.1', 0, 0, 0,'URL'])

     file = open(filename,'r')
     nb = 0
     for line in file:
        an_ip = re.search('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',line)
        if (an_ip != None):
            ip_collection.setdefault(an_ip.group(0),[]).append([an_ip.group(0), re.findall(r'\"(.*?)\"|\[(.*?)\]|(\S+)', line)])
       	nb+=1
       	if nb > MAX_NB_LINE_TO_READ: break
     for ip_key in ip_collection.keys():
        ip_collection[ip_key].insert(0,LocalizeIpAddress(ip_key))
     return(ip_collection)

###########################################################################################################################################################
# def DisplayTrackRForm():
###########################################################################################################################################################
@auth.requires_login()
def DisplayTrackRForm():
    import os
    form=SQLFORM.factory(Field('name'), Field('file', 'upload', uploadfolder=os.path.join(request.folder,'uploads')))
    if form.process().accepted:
            request.flash='file uploaded !'
    return(dict(AnalyzeLogFile=AnalyzeLogFile,form=form,ip_collection=ip_collection))

###########################################################################################################################################################
# def DisplayTrackRFormFail2Ban():
###########################################################################################################################################################
@auth.requires_login()
def DisplayTrackRFormFail2Ban():
    import os
    form=SQLFORM.factory(Field('name'), Field('file', 'upload', uploadfolder=os.path.join(request.folder,'uploads')))
    if form.process().accepted:
            request.flash='file uploaded !'
    return(dict(AnalyzeFail2BanFile=AnalyzeFail2BanFile,form=form,ip_collection=ip_collection))

###########################################################################################################################################################
# def read_dataset(filePath,delimiter=','):
###########################################################################################################################################################
def read_dataset(filePath,delimiter=','):
    return genfromtxt(filePath, delimiter=delimiter)

###########################################################################################################################################################
# def feature_normalize(dataset):
###########################################################################################################################################################
def feature_normalize(dataset):
    mu = np.mean(dataset,axis=0)
    sigma = np.std(dataset,axis=0)
    return (dataset - mu)/sigma

###########################################################################################################################################################
# def estimateGaussian(dataset):
###########################################################################################################################################################
def estimateGaussian(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.cov(dataset.T)
    return mu, sigma

###########################################################################################################################################################
# def multivariateGaussian(dataset,mu,sigma):
###########################################################################################################################################################
def multivariateGaussian(dataset,mu,sigma):
    p = multivariate_normal(mean=mu, cov=sigma)
    return p.pdf(dataset)

###########################################################################################################################################################
# def selectThresholdByCV(probs,gt):
###########################################################################################################################################################
def selectThresholdByCV(probs,gt):
    best_epsilon = 0
    best_f1 = 0
    f = 0
    stepsize = (max(probs) - min(probs)) / 1000;
    epsilons = np.arange(min(probs),max(probs),stepsize)
    for epsilon in np.nditer(epsilons):
        predictions = (probs < epsilon)
        f = f1_score(gt, predictions,average='binary')
        if f > best_f1:
            best_f1 = f
            best_epsilon = epsilon
    return best_f1, best_epsilon

def optimize_training_parameters(self, n):
        # data
        from_timestamp = self.min_timestamp
        to_timestamp = self.min_timestamp + datetime.timedelta(days=365) + datetime.timedelta(hours=1)
        train_timestamps, train_values = self.load_monitor_data(from_timestamp, to_timestamp, "1")
        train_data = np.array(train_values)[:, 0:5]

        # parameters
        nu = np.linspace(start=1e-5, stop=1e-2, num=n)
        gamma = np.linspace(start=1e-6, stop=1e-3, num=n)
        opt_diff = 1.0
        opt_nu = None
        opt_gamma = None
        fw = open("training_param.csv", "w")
        fw.write("nu,gamma,diff\n")
        for i in range(len(nu)):
            for j in range(len(gamma)):
                classifier = svm.OneClassSVM(kernel="rbf", nu=nu[i], gamma=gamma[j])
                classifier.fit(train_data)
                label = classifier.predict(train_data)
                p = 1 - float(sum(label == 1.0)) / len(label)
                diff = math.fabs(p-nu[i])
                if diff < opt_diff:
                    opt_diff = diff
                    opt_nu = nu[i]
                    opt_gamma = gamma[j]
                fw.write(",".join([str(nu[i]), str(gamma[j]), str(diff)]) + "\n")
        fw.close()
        return opt_nu, opt_gamma

###########################################################################################################################################################
# def DisplayMachLearnUnsup_IPANALYZED():
###########################################################################################################################################################
@auth.requires_login()
def DisplayMachLearnUnsup_IPANALYZED():
    nameOfImage = ''

    if (request.vars.nu_value is not None) & (request.vars.gamma_value is not None) & (request.vars.kernel_value is not None):
        SQLstr = "select latitude, longitude, sum(tcph_syn), sum(tcph_rst) from ipanalyzed group by latitude, longitude;"
        rows = db.executesql(SQLstr)
        num_rows = len(rows)

        table_matrix = np.zeros((num_rows,4))
        table_ip = []

        i = 0
        for row in rows:
            rowsIP = []
            if row[0] == '': row[0] = 0
            if row[1] == '': row[1] = 0
            XlatLong = [row[0], row[1]]
            if ((float(row[0]) != 0) & (float(row[1]) != 0)):
                table_matrix[i] = [row[0], row[1], row[2], row[3]]
                i = i + 1
                SQLstrIP = "select ip_addr from ipanalyzed where latitude=" + str(row[0]) + " and " + "longitude=" + str(row[1]) + ";"
                rowsIP = db.executesql(SQLstrIP)
                logger.debug("select ip_addr from ipanalyzed where latitude=" + str(row[0]) + " and " + "longitude=" + str(row[1]) + ";")
            if (rowsIP != []):
                table_ip.append(str(rowsIP[0][0]))
            else:
                table_ip.append('IP Inconnu')

        #max_abs_scaler = preprocessing.MaxAbsScaler()
        #norm1 = max_abs_scaler.fit_transform(table_matrix)
        #norm1 = preprocessing.normalize(table_matrix[:,np.newaxis])
        clf = svm.OneClassSVM(nu=float(request.vars.nu_value), kernel=request.vars.kernel_value, gamma=float(request.vars.gamma_value))
        clf.fit(table_matrix)
        #clf.fit(norm1)

        pred = clf.predict(table_matrix)

        # inliers are labeled 1, outliers are labeled -1
        normal = table_matrix[pred == 1]
        abnormal = table_matrix[pred == -1]
        plt.figure()
        plt.plot(normal[:,0],normal[:,1],'bx')
        plt.plot(abnormal[:,0],abnormal[:,1],'ro')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        name = str(response.session_db_unique_key) + '_ipanalyzed.png'
        #nameOfImage = os.path.join(request.folder, 'static','images', name)
        nameOfImage = URL('static','images', name)
        logger.debug('DisplayMachLearnUnsup_IPANALYZED(): save result filename = %s' % nameOfImage)
        dateFmt = mpl.dates.DateFormatter('%Y')
        plt.savefig(os.path.join(request.folder, 'static','images', name))
        plt.close()
        request.flash='SMV executé !'

        return dict(nameOfImage=nameOfImage, table_matrix=table_matrix, table_ip=table_ip, normal=normal,abnormal=abnormal)
    else:
        return dict(nameOfImage=nameOfImage)

    ###########################################################################################################################################################
# def DisplayMachLearnUnsup_OTHSEC():
###########################################################################################################################################################
@auth.requires_login()
def DisplayMachLearnUnsup_OTHSEC():
    nameOfImage = ''

    if (request.vars.nu_value is not None) & (request.vars.gamma_value is not None) & (request.vars.kernel_value is not None):

        db.ipanalyzed.ip_addr.represent = lambda row: int(ipaddress.IPv4Address(row.ip_addr))

        SQLstr = "select addr_from, addr_to, sum(case when tcph_syn='T' then 1 else 0 end), sum(case when tcph_rst='T' then 1 else 0 end) from othsec group by addr_from, addr_to;"
        rows = db.executesql(SQLstr)
        num_rows = len(rows)

        table_matrix = np.zeros((num_rows+1,4))
        table_ip = np.chararray((num_rows+1,1))

        i = 0
        for row in rows:
            if (not str(row[0]).startswith("192.")):
                aRow = str(row[0])
                Xlat, Xlong = LocalizeIpAddress(row[0])
            elif (not str(row[1]).startswith("192.")):
                aRow = str(row[1])
                Xlat, Xlong = LocalizeIpAddress(row[1])
            if (Xlat != 0) & (Xlong != 0):
                table_ip[i] = row[1]
                table_matrix[i] = [Xlat, Xlong, row[2], row[3]]
            #norm1 = normalize(table_matrix[:,np.newaxis], axis=0).ravel()
            i = i + 1

        norm1 = table_matrix #/ np.linalg.norm(table_matrix)

        #clf = svm.OneClassSVM(nu=0.01, kernel="rbf", gamma=0.0000001) 2%
        #clf = svm.OneClassSVM(nu=0.02, kernel="rbf", gamma=0.0000001) 10%
        #clf = svm.OneClassSVM(nu=0.009, kernel="rbf", gamma=0.0000001) 12%
        #clf = svm.OneClassSVM(nu=0.01, kernel="rbf", gamma=0.000001) 0.7%
        #clf = svm.OneClassSVM(nu=0.01, kernel="rbf", gamma=0.0001) 0.96
        #clf = svm.OneClassSVM(nu=0.01, kernel="rbf", gamma=0.00001)
        clf = svm.OneClassSVM(nu=float(request.vars.nu_value), kernel=request.vars.kernel_value, gamma=float(request.vars.gamma_value))

        clf.fit(norm1)

        pred = clf.predict(norm1)

        # inliers are labeled 1, outliers are labeled -1
        normal = norm1[pred == 1]
        abnormal = norm1[pred == -1]
        plt.figure()
        plt.plot(normal[:,0],normal[:,1],'bx')
        plt.plot(abnormal[:,0],abnormal[:,1],'ro')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        name = str(response.session_db_unique_key) + '_ipanalyzed.png'
        #nameOfImage = os.path.join(request.folder, 'static','images', name)
        nameOfImage = URL('static','images', name)
        logger.debug('DisplayMachLearnUnsup_OTHSEC(): save result filename = %s' % nameOfImage)
        dateFmt = mpl.dates.DateFormatter('%Y')
        plt.savefig(os.path.join(request.folder, 'static','images', name))
        plt.close()

        return dict(nameOfImage=nameOfImage, table_matrix=table_matrix, table_ip=table_ip, normal=normal,abnormal=abnormal)
    else:
        return dict(nameOfImage=nameOfImage)

###########################################################################################################################################################
# def DisplayMachLearnKNN_OTHSEC():
###########################################################################################################################################################
@auth.requires_login()
def DisplayMachLearnKNN_OTHSEC():
    nameOfImage = ''

    if (request.vars.n_neighbors_value is not None) & (request.vars.h_value is not None):

        db.ipanalyzed.ip_addr.represent = lambda row: int(ipaddress.IPv4Address(row.ip_addr))

        SQLstr = "select addr_from, addr_to, sum(case when tcph_syn='T' then 1 else 0 end), sum(case when tcph_rst='T' then 1 else 0 end) from othsec group by addr_from, addr_to;"
        rows = db.executesql(SQLstr)
        num_rows = len(rows)

        SQLstr = "select IP_addr, longitude, latitude, conn_tries, auth_failure, banned from loganalyzed;"
        rowsB = db.executesql(SQLstr)
        num_rowsB = len(rowsB)

        SQLstr = "select longitude, latitude, sum(tcph_syn), sum(tcph_rst) from ipanalyzed group by longitude, latitude;"
        rowsC = db.executesql(SQLstr)
        num_rowsC = len(rowsC)

        table_matrix = np.zeros((num_rows+1,4))
        table_ip = np.chararray((num_rows+1,1))
        X, y = np.zeros((num_rows+1,4)), np.zeros((num_rows+1,1))
        X_train, y_train = np.zeros((num_rowsB+num_rowsC+1,4)), np.zeros((num_rowsB+num_rowsC+1,1))

        i = 0
        for row in rows:
            if (not str(row[0]).startswith("192.")):
                aRow = str(row[0])
                Xlat, Xlong = LocalizeIpAddress(row[0])
            elif (not str(row[1]).startswith("192.")):
                aRow = str(row[1])
                Xlat, Xlong = LocalizeIpAddress(row[1])
            if (Xlat != 0) & (Xlong != 0):
                table_ip[i] = row[1]
                table_matrix[i] = [Xlat, Xlong, row[2], row[3]]
            #norm1 = normalize(table_matrix[:,np.newaxis], axis=0).ravel()
            i = i + 1

        j = 0
        f = lambda x: 0 if (x is None) else (0 if (str(x) == "") else x)
        for row in rowsB:
            y_train[j] = 0
            r0, r1, r2, r3, r4, r5 = f(row[0]), f(row[1]), f(row[2]), f(row[3]), f(row[4]), f(row[5])
            y_train[j] = int(r5>0)
            X_train[j] = [r1,r2,r3,r4]
            j = j + 1
        for row in rowsC:
            r0, r1, r2, r3 = f(row[0]), f(row[1]), f(row[2]), f(row[3])
            y_train[j] = r3>(r2*0.8)
            X_train[j] = [r0,r1,r2,r3]
            j = j + 1

        X = np.array(table_matrix[:, 0:4])
        y = np.array(table_matrix[:,3]>(table_matrix[:,2]*0.8))

        #X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

        n_neighbors = int(request.vars.n_neighbors_value)
        h = float(request.vars.h_value)

        # Create color maps
        cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA','#00AAFF'])
        cmap_bold = ListedColormap(['#FF0000', '#00FF00','#00AAFF'])

        knn = KNeighborsClassifier(n_neighbors, weights='distance')

        knn.fit(X_train, y_train)

        logger.debug('DisplayMachLearnKNN_OTHSEC(): Précision du Classifier K-NN sur le training set: %d' % knn.score(X_train, y_train))

        # calculate min, max and limits
        x_min, x_max = X_train[:, 0].min() - 1, X_train[:, 0].max() + 1
        y_min, y_max = X_train[:, 1].min() - 1, X_train[:, 1].max() + 1
        #xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
        #Z = knn.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = pred = knn.predict(X)

        normal = X[pred == 1]
        abnormal = X[pred == -1]
        logger.debug('DisplayMachLearnKNN_OTHSEC(): accuracy_score = %d' % accuracy_score(y, pred))

        # inliers are labeled 1, outliers are labeled -1
        #Z = Z.reshape(xx.shape)
        plt.figure()
        #plt.pcolormesh(xx, yy, Z, cmap=cmap_light)

        # Plot also the training points
        plt.scatter(X_train[:, 0], X_train[:, 1], c=y_train, cmap=cmap_bold)
        #plt.xlim(xx.min(), xx.max())
        #plt.ylim(yy.min(), yy.max())
        plt.title("3-Class classification (k = %i)" % (n_neighbors))
        plt.show()

        name = str(response.session_db_unique_key) + '_ipanalyzed.png'
        nameOfImage = URL('static','images', name)
        logger.debug('DisplayMachLearnKNN_OTHSEC(): save result filename = %s' % nameOfImage)
        dateFmt = mpl.dates.DateFormatter('%Y')
        plt.savefig(os.path.join(request.folder, 'static','images', name))
        plt.close()

        return dict(nameOfImage=nameOfImage, table_matrix=table_matrix, table_ip=table_ip, normal=normal, abnormal=abnormal)
    else:
        return dict(nameOfImage=nameOfImage)



###########################################################################################################################################################
# def DisplayMachLearnADA_OTHSEC():
###########################################################################################################################################################
@auth.requires_login()
def DisplayMachLearnADA_OTHSEC():
    nameOfImage = ''

    if (request.vars.n_neighbors_value is not None) & (request.vars.h_value is not None):

        db.ipanalyzed.ip_addr.represent = lambda row: int(ipaddress.IPv4Address(row.ip_addr))

        SQLstr = "select addr_from, addr_to, sum(case when tcph_syn='T' then 1 else 0 end), sum(case when tcph_rst='T' then 1 else 0 end) from othsec group by addr_from, addr_to;"
        rows = db.executesql(SQLstr)
        num_rows = len(rows)

        SQLstr = "select IP_addr, longitude, latitude, banned from loganalyzed;"
        rowsB = db.executesql(SQLstr)
        num_rowsB = len(rowsB)

        table_matrix = np.zeros((num_rows+1,4))
        table_ip = np.chararray((num_rows+1,1))

        i = 0
        for row in rows:
            if (not str(row[0]).startswith("192.")):
                aRow = str(row[0])
                Xlat, Xlong = LocalizeIpAddress(row[0])
            elif (not str(row[1]).startswith("192.")):
                aRow = str(row[1])
                Xlat, Xlong = LocalizeIpAddress(row[1])
            if (Xlat != 0) & (Xlong != 0):
                table_ip[i] = row[1]
                table_matrix[i] = [Xlat, Xlong, row[2], row[3]]
            #norm1 = normalize(table_matrix[:,np.newaxis], axis=0).ravel()
            i = i + 1

        X_train = np.zeros((num_rows,4))
        y_train = np.zeros((num_rows))

        X_train = table_matrix
        y_train = table_matrix[:,[2]]<(table_matrix[:,[3]]/0.8)
        #j = 0
        #for row in rowsB:
        #    X_train[j] = [ip2int(row[0]),row[1],row[2],row[3]]
        #    y_train[j] = int(row[3])>0
        #    j = j + 1

        # Example settings
        n_samples = 300
        outliers_fraction = 0.15
        n_outliers = int(outliers_fraction * n_samples)
        n_inliers = n_samples - n_outliers

        # define outlier/anomaly detection methods to be compared
        anomaly_algorithms = [
            ("Robust covariance", EllipticEnvelope(contamination=outliers_fraction)),
            ("One-Class SVM", svm.OneClassSVM(nu=outliers_fraction, kernel="rbf",
                                              gamma=0.1)),
            ("Isolation Forest", IsolationForest(behaviour='new',
                                                 contamination=outliers_fraction,
                                                 random_state=42)),
            ("Local Outlier Factor", LocalOutlierFactor(
                n_neighbors=35, contamination=outliers_fraction))]

        # Define datasets
        blobs_params = dict(random_state=0, n_samples=n_inliers, n_features=2)
        datasets = [
            make_blobs(centers=[[0, 0], [0, 0]], cluster_std=0.5,
                       **blobs_params)[0],
            make_blobs(centers=[[2, 2], [-2, -2]], cluster_std=[0.5, 0.5],
                       **blobs_params)[0],
            make_blobs(centers=[[2, 2], [-2, -2]], cluster_std=[1.5, .3],
                       **blobs_params)[0],
            4. * (make_moons(n_samples=n_samples, noise=.05, random_state=0)[0] -
                  np.array([0.5, 0.25])),
            14. * (np.random.RandomState(42).rand(n_samples, 2) - 0.5)]

        # Compare given classifiers under given settings
        xx, yy = np.meshgrid(np.linspace(-7, 7, 150),
                             np.linspace(-7, 7, 150))

        plt.figure(figsize=(len(anomaly_algorithms) * 2 + 3, 12.5))
        plt.subplots_adjust(left=.02, right=.98, bottom=.001, top=.96, wspace=.05,
                            hspace=.01)

        plot_num = 1
        rng = np.random.RandomState(42)

        for i_dataset, X in enumerate(datasets):
            # Add outliers
            X = np.concatenate([X, rng.uniform(low=-6, high=6,
                               size=(n_outliers, 2))], axis=0)

            for name, algorithm in anomaly_algorithms:
                t0 = time.time()
                algorithm.fit(X)
                t1 = time.time()
                plt.subplot(len(datasets), len(anomaly_algorithms), plot_num)
                if i_dataset == 0:
                    plt.title(name, size=18)

                # fit the data and tag outliers
                if name == "Local Outlier Factor":
                    y_pred = algorithm.fit_predict(X)
                else:
                    y_pred = algorithm.fit(X).predict(X)

                # plot the levels lines and the points
                if name != "Local Outlier Factor":  # LOF does not implement predict
                    Z = algorithm.predict(np.c_[xx.ravel(), yy.ravel()])
                    Z = Z.reshape(xx.shape)
                    plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black')

                colors = np.array(['#377eb8', '#ff7f00'])
                plt.scatter(X[:, 0], X[:, 1], s=10, color=colors[(y_pred + 1) // 2])

                plt.xlim(-7, 7)
                plt.ylim(-7, 7)
                plt.xticks(())
                plt.yticks(())
                plt.text(.99, .01, ('%.2fs' % (t1 - t0)).lstrip('0'),
                         transform=plt.gca().transAxes, size=15,
                         horizontalalignment='right')
                plot_num += 1

                plt.show()

        return dict(nameOfImage=nameOfImage, table_matrix=table_matrix, table_ip=table_ip, normal=normal,abnormal=abnormal)
    else:
        return dict(nameOfImage=nameOfImage)



###########################################################################################################################################################
# def DisplayMachLearnSup_IPANALYZED():
###########################################################################################################################################################
@auth.requires_login()
def DisplayMachLearnSup_IPANALYZED():
    db.define_table('othsec',
          Field('idn', 'string',20,''),
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
          Field('idn', 'string',20,''),
          Field('origin', 'string',20,'IP'),
          Field('datetime', 'string',12,'00:00:00'),
          Field('tcp_protocol', 'string',8,'IP'),
          Field('ip_addr', 'string',40,'aa.aa.aa.aa'),
          Field('port', 'string',10,'0000'),
          Field('mac', 'string',12,''),
          Field('status', 'string',10),
          Field('risk', 'integer',0),
          Field('hits', 'integer',0),
          Field('longitude', 'double',0),
          Field('latitude', 'double',0))

    db.ipanalyzed.ip_addr.represent = lambda row: int(ipaddress.IPv4Address(row.ip_addr))

    myquery = (db.ipanalyzed.latitude != 0) & (db.ipanalyzed.longitude != 0) & (db.ipanalyzed.tcp_protocol != 17) & (~db.ipanalyzed.ip_addr.like("127.%")) & (~db.ipanalyzed.ip_addr.like("169.254.%")) & (~db.ipanalyzed.ip_addr.like("192.168.%")) & (~db.ipanalyzed.ip_addr.like("172.16.%"))

    counter = db.ipanalyzed.latitude.count()
    rows = db(query=myquery).select(db.ipanalyzed.latitude,db.ipanalyzed.longitude,counter,groupby=[db.ipanalyzed.latitude,db.ipanalyzed.longitude])
    num_rows = len(db(query=myquery).select(db.ipanalyzed.latitude,db.ipanalyzed.longitude,counter,groupby=[db.ipanalyzed.latitude,db.ipanalyzed.longitude]))

    #print "Nombre d'enregistrements à traiter = %d" % (num_rows)

    table_matrix = np.zeros((num_rows+1,3))

    i = 0
    for row in rows:
        table_matrix[i] = [row.ipanalyzed.latitude, row.ipanalyzed.longitude, row[counter]]
        i = i + 1

    clf = svm.OneClassSVM(nu=0.05, kernel="rbf", gamma=0.1)
    clf.fit(table_matrix)

    pred = clf.predict(table_matrix)

    # inliers are labeled 1, outliers are labeled -1
    normal = table_matrix[pred == 1]
    abnormal = table_matrix[pred == -1]
    plt.figure()
    plt.plot(normal[:,0],normal[:,1],'bx')
    plt.plot(abnormal[:,0],abnormal[:,1],'ro')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    name = str(response.session_db_unique_key) + '_ipanalyzed.png'
    #nameOfImage = os.path.join(request.folder, 'static','images', name)
    nameOfImage = URL('static','images', name)
    logger.debug('DisplayTrackRList(): filename = %s' % nameOfImage)
    dateFmt = mpl.dates.DateFormatter('%Y')
    plt.savefig(os.path.join(request.folder, 'static','images', name))
    plt.close()

    return dict(nameOfImage=nameOfImage, table_matrix=table_matrix)

###########################################################################################################################################################
# def DisplayTrackRIP():
###########################################################################################################################################################
@auth.requires_login()
def DisplayTrackRIP():
    import os
    form = SQLFORM.factory( Field('Enter_IP_Address', requires=IS_NOT_EMPTY()))
    if form.process().accepted:
            pass
    return(dict(AnalyzeIP=AnalyzeIP,form=form,ip_collection=ip_collection))

###########################################################################################################################################################
# def DisplayTrackRIPGeo():
###########################################################################################################################################################
@auth.requires_login()
def DisplayTrackRIPGeo():
    import os
    form = SQLFORM.factory( Field('Enter_IP_Address', requires=IS_NOT_EMPTY()), buttons = [A("Go to another page",_class='btn',_href=URL("default","anotherpage"))]
)
    if form.process().accepted:
            pass
    return(dict(AnalyzeIP=AnalyzeIP,form=form,ip_collection=ip_collection))

###########################################################################################################################################################
# def DisplayGeolocDb():
###########################################################################################################################################################
@auth.requires_login()
def DisplayGeolocDb():
    return dict()

###########################################################################################################################################################
# def DisplayGeolocDbRT():
###########################################################################################################################################################
@auth.requires_login()
def DisplayGeolocDbRT():
    return dict()

###########################################################################################################################################################
# def DisplayGeolocDbRTAno():
###########################################################################################################################################################
@auth.requires_login()
def DisplayGeolocDbRTAno():
    return dict()


###########################################################################################################################################################
# def DisplayTrackRClientIPGeo():
###########################################################################################################################################################
@auth.requires_login()
def DisplayTrackRClientIPGeo():
    import os
    form = SQLFORM.factory( Field('Enter_IP_Address', requires=IS_NOT_EMPTY()))
    #form.add_button('Ajouter aux IP autorisées', URL('trackrctrl', 'AddTrusteeIPInDB'))

    if form.process().accepted:
            pass
    return(dict(AnalyzeIP=AnalyzeIP,form=form,ip_collection=ip_collection))

################
# def AddTrusteeIPInDB():
###########################################################################################################################################################
@auth.requires_login()
def AddTrusteeIPInDB():
    if (request.vars['Enter_ID'] is not None):
        an_ID = request.vars['Enter_ID']
        SQLstr = "select username, ip_addr, longitude, latitude, port from ipanalyzed where id =" + str(an_ID) + ";"
        rowsB = db.executesql(SQLstr)
        num_rowsB = len(rowsB)

        theDateTime = dt.datetime.now().strftime('%Y-%m-%d %X')
        for rowB in rowsB:
            db.loganalyzed.update_or_insert( (db.loganalyzed.username==str(auth.user.email)) & (db.loganalyzed.ip_addr==rowB[1]) & (db.loganalyzed.port==rowB[4]), username=str(auth.user.email), ip_addr=rowB[1], port=rowB[4], latitude=rowB[3], longitude=rowB[2], banned=-1, datetime=str(theDateTime))

            logger.debug('AddTrusteeIPInDB(): for ID = %s' % str(an_ID))



################
# def AddBannedeIPInDB():
###########################################################################################################################################################
@auth.requires_login()
def AddBannedeIPInDB():
    if (request.vars['Enter_LAT'] is not None) & (request.vars['Enter_LONG'] is not None):
        an_LAT, an_LONG = request.vars['Enter_LAT'], request.vars['Enter_LONG']
        SQLstr = "select username, ip_addr, longitude, latitude, port from ipanalyzed where latitude=" + str(an_LAT) + " and longitude=" + str(an_LONG) + ";"
        rowsB = db.executesql(SQLstr)
        num_rowsB = len(rowsB)

        theDateTime = dt.datetime.now().strftime('%Y-%m-%d %X')
        for rowB in rowsB:
            db.loganalyzed.update_or_insert( (db.loganalyzed.username==str(auth.user.email)) & (db.loganalyzed.ip_addr==rowB[1]) & (db.loganalyzed.port==rowB[4]), username=str(auth.user.email), ip_addr=rowB[1], port=rowB[4], latitude=rowB[3], longitude=rowB[2], banned=1, datetime=str(theDateTime))

            logger.debug('AddBannedeIPInDB(): for ID = %s' % str(an_ID))
