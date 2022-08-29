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
         return sql_service.query_count_versions(lang, cat, snip) 


    #####################################################
    #####################################################    
    def query_last_session_open_nodes():
        return sql_service.query_last_session_open_nodes()


    #####################################################
    #####################################################    
    def insert_setting(key, value):
        sql_service.insert_setting(key, value)


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
       return sql_service.query_duplicate(lang, cat, snip)

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