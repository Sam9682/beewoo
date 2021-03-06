# -*- coding: utf-8 -*-
@auth.requires_login()

def index():
    export_classes = dict(csv=True, json=False, html=False,
                          tsv=False, xml=False, csv_with_hidden_cols=False,
                          tsv_with_hidden_cols=False)
    myquery = (db.ipligence2.id != None) | (db.ipligence2.id < 10)
    grid = SQLFORM.grid(myquery, showbuttontext=False, exportclasses=export_classes)
    return dict( grid = grid)
