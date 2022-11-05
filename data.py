import sqlite3
import sql_service
from kivy.properties import ListProperty
import os

import sql_service as sql_service

from pygments.lexers.sql import PostgresLexer # SQL Oralce/Postgres
from pygments.lexers.jvm import JavaLexer
from pygments.lexers.sql import PlPgsqlLexer
from pygments.lexers.html import HtmlLexer
from pygments.lexers.css import CssLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.lexers.data import JsonLexer
from pygments.lexers.jvm import GroovyLexer
from pygments.lexers.templates import HtmlPhpLexer
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers.dotnet import CSharpAspxLexer
from pygments.lexers.foxpro import FoxProLexer
from pygments.lexers.basic import VBScriptLexer
from pygments.lexers.shell import BashLexer, BatchLexer, PowerShellLexer
from pygments.lexers.configs import DockerLexer
from pygments.lexers.python import CythonLexer
from pygments.lexers.special import TextLexer

class Data():

    dict_lang = {'SQL' : PostgresLexer(), 'JAVA':  JavaLexer(), 'PL/SQL':  PlPgsqlLexer(), 'HTML':HtmlLexer(), 'XML':  HtmlLexer(), 
            'CSS':  CssLexer(), 'JAVASCRIPT':  JavascriptLexer(), 'JSON':  JsonLexer(), 'Groovy':  GroovyLexer(), 'PHP':  HtmlPhpLexer(), 
            'C':  CLexer(), 'C++':  CppLexer(), 'C#':  CSharpAspxLexer(), 'FOXPRO':  FoxProLexer(), 'VISUAL BASIC':  VBScriptLexer(),
            'BASH':  BashLexer(), 'BATCH':  BatchLexer(), 'POWERSHELL':  PowerShellLexer(), 'DOCKER':  DockerLexer(),
            'PYTHON' :  CythonLexer(), 'TEXT' :  TextLexer()
        }

    def get_version():
        return '0.1.0'

    def get_speed_dial_items():
        return {
        "Undo":"undo",
        "Redo":"redo",
        "Cut":"content-cut",
        "Copy":"content-copy", 
        "Paste":"content-paste", 
        "Select All":"select-all",
        
        "Delete Version":"delete", 
        "Locate In Tree":"chart-tree",
        
        }

        # Future Version 1.0
        # "Find":"file-find",

    def create_db():
        # sql_service.create_db()
        sql_service.create_db()

    #####################################################
    #####################################################
    def delete_version(lang, cat, snip, version):
        return sql_service.delete_version(lang, cat, snip, version)

    #####################################################
    #####################################################
    def query_count_versions(lang, cat, snip):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT count(snip_detail.seq) 
            FROM snip_detail
            WHERE snip_detail.snip_mast = (SELECT DISTINCT snip_mast.row_id
                                            FROM node
                                            JOIN snip_mast ON node.row_id = snip_mast.node
                                            WHERE node.lang = :lang
                                            AND node.category = :cat
                                            AND snip_mast.description = :snip)	  
        """,
        {
            'lang':lang,
            'cat':cat,
            'snip':snip,
        })

        record = sql_cursor.fetchone()
        conn.close() 

        return record        


    #####################################################
    #####################################################    
    def query_last_session_open_nodes():
        data = {'lang':None, 'cat':None, 'snip':None}

        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            select key, value 
            FROM settings 
            WHERE settings.key LIKE 'last_open_node%'
        """)

        records = sql_cursor.fetchall()
        conn.close()  

        if records != None:
            if len(records) >= 3:
                for r in records:
                    if r[0] == 'last_open_node_lang':
                        data['lang'] = r[1]
                    if r[0] == 'last_open_node_cat':
                        data['cat'] = r[1]
                    if r[0] == 'last_open_node_snip':
                        data['snip'] = r[1]

        return data  

    def get_setting(key):

        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT value
            FROM settings
            WHERE key = :key;
        """,
        {
            'key':key,
        })

        record = sql_cursor.fetchone()
        conn.close()   

        return record[0]
        

    #####################################################
    #####################################################    
    def set_setting(key, value):

        # Be sure the key exist first.
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            INSERT INTO settings  (key)
            SELECT  :key
            WHERE :key NOT IN (SELECT  key from settings where key = :key);
        """,
        {
            'key':key,
        })

        conn.commit()
        conn.close()       

        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            UPDATE settings SET value = :value
            WHERE settings.key = :key
        """,
        {
            'key':key,
            'value':value
        })

        conn.commit()
        conn.close()          


    #####################################################
    ##################################################### 
    def query_lang_cat_exist(lang, cat):
        return sql_service.query_lang_cat_exist(lang, cat)


    #####################################################
    ##################################################### 
    def insert_into_node(lang, cat):
         sql_service.insert_into_node(lang, cat)                       


    #####################################################
    ##################################################### 
    def insert_into_snip_mast(lang, cat, snip, seq=0):
        sql_service.insert_into_snip_mast(lang, cat, snip, seq=0)

    #####################################################
    ##################################################### 
    def query_duplicate(lang, cat, snip):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT DISTINCT 'Y'
            FROM node
            JOIN snip_mast ON node.row_id = snip_mast.node
            WHERE node.lang = :lang
            AND node.category = :category
            AND snip_mast.description = :snippet
        """,
        {
            'lang':lang,
            'category':cat,
            'snippet':snip
        })
        record = sql_cursor.fetchone()
        conn.close()   

        return record


    #####################################################
    ##################################################### 
    def query_snip_detail_code(length, seq, lang, cat, snip_desc):
        return sql_service.query_snip_detail_code(length, seq, lang, cat, snip_desc)                


    #####################################################
    ##################################################### 
    def query_node_detail(lang, cat, snip):
        return sql_service.query_node_detail(lang, cat, snip)


    #####################################################
    ##################################################### 
    def query_version(snip_id):
        return sql_service.query_version(snip_id)


    #####################################################
    ##################################################### 
    def query_tree(filter='N', filter_value=''):
        return sql_service.query_tree(filter='N', filter_value='')


    #####################################################
    ##################################################### 
    def update_delete_snip_mast(lang, cat, snip):
        sql_service.update_delete_snip_mast(lang, cat, snip)

    #####################################################
    ##################################################### 
    def insert_snip_detail(lang, cat, snip, snip_text):
        sql_service.insert_snip_detail(lang, cat, snip, snip_text)