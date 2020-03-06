#-*- coding: utf-8 -*-
'''
MySQLDataDictionary: documents a MySQL model as html
Copyright (C) 2018  Ashton Lamont
Copyright (C) 2020  Bruno Gonçalves

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

import os
from wb import *
import grt
from mforms import Utilities, FileChooser, OpenDirectory

# Global vars
filePath = ""
newPath = ""
docProject = ""
scriptVersion = "0.2.1"


def mysqldatadictionary():
    #print(grt.root.wb.doc)
    global filePath
    filePath = chooseFolder()

    global docProject
    docProject = grt.root.wb.doc.info.project

    global newPath
    newPath = filePath + "\%s" % (docProject)
    print(newPath)

    if os.path.exists(newPath):
        #maybe delete and recreate here
        print("Folder Exists")
    else:    
        os.makedirs(newPath)
        os.makedirs(newPath + "\_assets")

    _createStyleFile()
    _createLandingPage()
    
    indexPath=newPath + "\index.html"
    textStart ="""<!DOCTYPE html>
    <html lang="en">
        <head>
            <title>Schema Report</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" type="text/css" href="./_assets/style.css">
        </head>
        <body>
            <div class="page-header"><b>MySQL Database Documenter</b></div>
            <div class="page-body">
                <div class="sidenav">
                    <b>Schema and Table List (schema.table):</b>
                    <br/>"""
    writeToFile(indexPath,textStart,"w")
    findModels(grt.root.wb.doc.physicalModels,newPath)
    #print(filePath)
    textEnd = """                </div>
                <div class="content">
                    <iframe id="tableFrame" src="./_assets/main.html"></iframe>
                </div>
            </div>
        </body>
    </html>"""
    writeToFile(indexPath,textEnd,"a")
    pass


def _createStyleFile():
    exportPath = newPath + "\_assets\style.css"
    css = """/*Style Sheet*/
    @import url('https://fonts.googleapis.com/css?family=Orbitron:900|Poppins&display=swap');

    * {
        box-sizing: border-box;
    }

    html, body {
        width: 100%;
        height: 100%;
        margin: 0px;
        font-family: 'Poppins', 'Arial', 'Helvetica', 'sans-serif';
        font-size: 1em;
    }

    .page-header {
        top: 0px;
        left: 0px;
        margin-top: 0px;
        margin-bottom: 0px;
        background: navy;
        width: 100%;
        height: 6%;
        float: left;
        font-family: 'Orbitron', 'sans-serif';
        text-shadow: 3px 3px 3px #EC0000;
        color: #FFFFFF;
        font-size: 1.95vw;
        text-align: left;
    }
    
    .page-body {
        height: 94%;
    }
    .page-body::after {
        content: "";
        clear: both;
        display: table;
    }

    /* Style the side navigation */
    .sidenav {
        top: 0px;
        left: 0px;
        background: navy;
        width: 20%;
        height: 100%;
        float: left;
        color: white;
        font-size: 1.1vw;
        z-index: 1;
        overflow-x: hidden;
        overflow-y: scroll;
    }
    /* Side navigation links */
    .sidenav a {
        color: white;
        padding: 5px;
        text-decoration: none;
        display: block;
    }
    /* Change color on hover */
    .sidenav a:hover {
        background-color: #ddd;
        color: black;
    }
    
    /* Style the content */
    .content {
        height: 100%;
        width: 80%;
        float: left;
        padding: 5px;
    }
    iframe {
        height: 100%;
        width: 100%;
        overflow-x: scroll;
        overflow-y: scroll;
    }
    
    /*##############################*/
    /* Landing page specific styles */
    /*##############################*/
    .landing-header{
        font-family: 'Orbitron', 'sans-serif';
        color: navy;
    }
    .landing-version {
        font-size: 14px;
    }
    .landing-footer {
        font-family: 'Consolas', 'Courier New', 'monospace';
        background: transparent;
        color: navy;
        font-size: 10px;
        position: fixed;
        bottom: 0;
        text-align: left
    }

    /*##############################*/
    /* Child pages specific styles  */
    /*##############################*/
	table {
		width: 100%;
		color: white;
		font-weight: bold;
	}
    .table-title, .columns-title, .indexes-title {
		background-color: navy;
	} 
	.table-header, .columns-header, .indexes-header {
		background-color: #3498DB;
		width: 25%
	}
	.table-data, .columns-data, .indexes-data {
		background-color: #D4EEFF ;
		color: black;
		font-weight: normal;
    }"""
    writeToFile(exportPath, css, "w")


def _createLandingPage():
    exportPath = newPath + "\_assets\main.html"
    html = """<!DOCTYPE html>
    <html lang="en">
        <head>
            <title>MySQL Database Documenter</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" type="text/css" href="style.css">
        </head>
        <body>
            <div class="landing-header">
                <h1>MySQL Database Documenter</h1>
                <div class="landing-version">%s</div>
            </div>
            <div class="landing-footer">
                Copyright (C) 2018 Ashton Lamont<br/>Copyright (C) 2020  Bruno Gonçalves
            </div>
        </body>
    </html>""" % scriptVersion
    writeToFile(exportPath, html, "w")

def connection():
    pass


def findModels(models,path):
    for m in models:
        findSchemas(m.catalog.schemata,path)
        #print(m)
    pass


def findSchemas(schemata, path):
    for s in schemata:
        newPath=""
        sn = s.name
        print(sn)
        newPath = path + "\%s" % (sn)
        print(newPath)
        if os.path.exists(newPath):
            #maybe delete and recreate here
            print("Folder Exists")
        else:
            os.makedirs(newPath)
        htmlSchemaFiles(s,newPath)
    pass


def chooseFolder():
    # Put plugin contents here
    path= ""
    filechooser = FileChooser(OpenDirectory)
    if filechooser.run_modal():
		path = filechooser.get_path()
    print "HTML File: %s" % (path)

    if len(path) >= 1:
        #print(path)
        return path
    pass


def writeToFile(path,text,mode):
    print(path)
    if mode == "a":
        tFile = open(path, "a") # a - append, w - overwrite
    elif mode == "w":
        tFile = open(path, "w")
    print >>tFile, text
    tFile.close()

def _isUnsignedColumn(column):
    un = "n.a."
    if "INT" in column.formattedType:
        un = "No"
        for f in column.flags:
            if f == "UNSIGNED":
                un = "Yes"
    return un
    

def htmlSchemaFiles(schema,path):
    # iterate through columns from each table of the schema
    sn = schema.name

    for table in schema.tables:
        text=""
        text="""<!DOCTYPE html>
    <html lang="en">
        <head>
			<title>tables</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" type="text/css" href="../_assets/style.css">
        </head>
        <body>"""
        tn = table.name
        childPath=path + "\%s.html" % (tn)
        link = "                    <a href=\"#\" onclick=\"javascript:document.getElementById('tableFrame').src='./%s/%s.html'\">%s.%s </a>" % (sn,tn,sn,tn)
        listPath = newPath + "\index.html"
        writeToFile(listPath,link,"a")


		# tables information
        text += """
            <a id="%s.%s"></a>
            <table>
                <tr class="table-title"><td colspan="2" >Table</td></tr>
                <tr><td class="table-header">Schema</td><td class="table-data">%s</td></tr>
                <tr><td class="table-header">Table Name</td><td class="table-data">%s</td></tr>
                <tr><td class="table-header">DB Engine</td><td class="table-data">%s</td></tr>
                <tr><td class="table-header">Last Change</td><td class="table-data">%s</td></tr>
                <tr><td class="table-header">Table Comments</td><td class="table-data">%s</td></tr>
            </table>"""  % (sn, tn, sn, tn, table.tableEngine, table.lastChangeDate, table.comment)


		# columns information
        text += """
            <table>
                <tr class="columns-title"><td colspan="9">Columns</td></tr>
                <tr class="columns-header"><th>Name</th><th>Data Type</th><th>PK</th><th>NN</th><th>FK</th><th>AI</th><th>UN</th><th>Default</th><th>Comment</th></tr>"""
        for column in table.columns:
            pk = ('No', 'Yes')[bool(table.isPrimaryKeyColumn(column))]
            fk = ('No', 'Yes')[bool(table.isForeignKeyColumn(column))]
            nn = ('No', 'Yes')[bool(column.isNotNull)]
            ai = ('No', 'Yes')[bool(column.autoIncrement)]
            un = _isUnsignedColumn(column)
            text += """
                <tr class="columns-data"><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (column.name,column.formattedType,pk,nn,fk,ai,un,column.defaultValue,column.comment)


		#indexes information
        text += """
            </table>
            <table>
                <tr class="indexes-title"><td colspan="4">Indexes</td></tr>
                <tr class="indexes-header"><th>Name</th><th>Type</th><th>Columns</th><th>Comment</th></tr>"""
        for index in table.indices:
            # index name
            idn = index.name

			# index columns
            ic = ""
            ic = ", ".join(str(c.referencedColumn.name) for c in index.columns)

			# index type
            it = index.indexType

			# index description
            id = index.comment
            text += """
                <tr class="indexes-data"><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (idn, it, ic, id)
        text += """
            </table>
        </body>
    </html>"""
        writeToFile(childPath,text,"w")
    #Utilities.show_message("Report generated", "HTML Report format from current model generated", "OK","","")
    return 0


mysqldatadictionary()
