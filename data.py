import sqlite3
from kivy.properties import ListProperty
import os

class Data():

    def get_version():
        return '0.1.0'

    def get_db_file():
        return os.path.join(os.getcwd(), "snippet_db.db")

    def get_languages():
        return list([
            "BASH",
            "BATCH",
            "C",
            "C#",
            "C++",
            "CSS",
            "DOCKER",
            "FOXPRO",
            "Groovy",
            "HTML/XML",
            "JAVA",
            "JAVASCRIPT",
            "JSON",
            "PHP",
            "PL/SQL",
            "POWERSHELL",
            "PYTHON",
            "SQL",
            "VISUAL BASIC"
        ])

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
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""CREATE TABLE if not exists node
        (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            lang TEXT NOT NULL,
            category TEXT
        )
        """)
        conn.commit()

        sql_cursor.execute("""CREATE TABLE if not exists 
        snip_mast
        (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            node INTEGER  NOT NULL,
            description TEXT,
            deleted INTEGER
        )
        """)        
        conn.commit()

        sql_cursor.execute("""CREATE TABLE if not exists 
        snip_detail
        (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            snip_mast INTEGER  NOT NULL,
            seq INTEGER NOT NULL,
            code TEXT,
            create_date INTEGER DEFAULT CURRENT_TIMESTAMP
        )
        """)        
        conn.commit()
        
        sql_cursor.execute("""CREATE TABLE if not exists 
        settings
        (
            row_id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT,
            value TEXT
        )
        """)        
        conn.commit()
        conn.close()   


    #####################################################
    #####################################################
    def delete_version(lang, cat, snip, version):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            DELETE FROM snip_detail
            WHERE snip_detail.seq = :version
            AND snip_detail.snip_mast = (SELECT DISTINCT snip_mast.row_id
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
            'version':version
        })

        conn.commit()
        conn.close()  

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


    #####################################################
    #####################################################    
    def insert_setting(key, value):
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
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT DISTINCT 'Y'
            FROM node
            WHERE node.lang = :lang
            AND node.category = :cat
        """,
        {
            'lang':lang,
            'cat':cat
        })
        record = sql_cursor.fetchone()
        conn.close()   
        
        return record  


    #####################################################
    ##################################################### 
    def insert_into_node(lang, cat):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            INSERT INTO node (lang, category) values (:lang, :category)        
        """,
        {
            'lang':lang,
            'category':cat
        })
        conn.commit()
        conn.close()                                  


    #####################################################
    ##################################################### 
    def insert_into_snip_mast(lang, cat, snip, seq=0):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            INSERT INTO snip_mast (node, description, deleted) 
            SELECT	node.row_id,
                    :snippet, 
                    :seq
            FROM node
            WHERE node.lang = :lang
            AND UPPER(node.category) = UPPER(:category)
        """,
        {
            'seq':seq,
            'snippet':snip,
            'lang':lang,
            'category':cat
        })
        conn.commit()
        conn.close()   


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
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT DISTINCT snip_detail.code,
                snip_detail.seq
              FROM node
              JOIN snip_mast ON node.row_id = snip_mast.node
              JOIN snip_detail snip_detail ON snip_mast.row_id = snip_detail.snip_mast
             WHERE snip_detail.seq = (:len - :seq)
               AND node.lang = :lang
               AND node.category = :cat
               AND snip_mast.description = :snip_desc
        """,
        {
            'len':length,
            'seq':seq,
            'lang':lang,
            'cat':cat,
            'snip_desc':snip_desc
        })

        record = sql_cursor.fetchone()
        conn.close() 

        return record                   


    #####################################################
    ##################################################### 
    def query_node_detail(lang, cat, snip):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT DISTINCT
                    node.lang,
                    node.category AS category,
                    snip_mast.description AS snippet,
                    snip_detail.code,
                    snip_mast.deleted,
                    snip_detail.code,
                    snip_detail.seq,
                    snip_detail.create_date,
                    snip_detail.snip_mast
            FROM node
            JOIN snip_mast ON node.row_id = snip_mast.node
            JOIN snip_detail snip_detail ON snip_mast.row_id = snip_detail.snip_mast
                AND snip_detail.seq = (SELECT MAX(sd2.seq)
                                        FROM snip_detail sd2
                                        WHERE sd2.snip_mast = snip_detail.snip_mast)
            AND node.lang = :lang
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
    def query_version(snip_id):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            SELECT DISTINCT
                    'Version: ' || (snip_detail.seq ) || ' - ' || 
                    strftime('%m.%d.%Y',snip_detail.create_date) as snippet_date     
            FROM snip_detail
            WHERE snip_detail.snip_mast = :snip_id
            ORDER BY seq desc
        """,
        {
            'snip_id':snip_id
        })

        records = sql_cursor.fetchall()
        conn.close() 

        return records   


    #####################################################
    ##################################################### 
    def query_tree(filter='N', filter_value=''):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
                SELECT DISTINCT
                node.lang,
                node.category AS category,
                snip_mast.description AS snippet,
                snip_detail.code,
                snip_mast.deleted
        FROM node
        JOIN snip_mast ON node.row_id = snip_mast.node
        LEFT JOIN snip_detail snip_detail ON snip_mast.row_id = snip_detail.snip_mast
                    and snip_detail.seq = (SELECT MAX(sd2.seq)
                                    FROM snip_detail sd2
                                    WHERE sd2.snip_mast = snip_detail.snip_mast) 
        WHERE ((:filter = 'Y' AND upper(snip_detail.code) like '%' || :filter_value || '%') 
                OR :filter = 'N')                                   
        ORDER BY snip_mast.deleted, node.lang, node.category, snip_mast.description;
        """,
        {
            'filter':filter,
            'filter_value':filter_value
        })

        records = sql_cursor.fetchall()
        conn.close() 
        
        return records


    #####################################################
    ##################################################### 
    def update_delete_snip_mast(lang, cat, snip):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""UPDATE snip_mast SET deleted = 1
                WHERE row_id IN 
                (SELECT s2.row_id FROM snip_mast s2
                    JOIN node ON s2.node = node.row_id
                    WHERE node.lang = :lang
                    AND node.category = :category
                    AND s2.description = :snippet)
        """,
        {
            'lang':lang,
            'category':cat,
            'snippet':snip
        })
        conn.commit()
        conn.close()        


    def insert_snip_detail(lang, cat, snip, snip_text):
        conn = sqlite3.connect(Data.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""INSERT INTO snip_detail (snip_mast, seq, code) 
            SELECT DISTINCT
                snip_mast.row_id,
                IFNULL((SELECT MAX(sd2.seq)
                    FROM snip_detail sd2
                    WHERE sd2.snip_mast = snip_mast.row_id),0)+1,						
                    :snip_text
            FROM node
            JOIN snip_mast ON node.row_id = snip_mast.node
            AND node.lang = :lang
            AND node.category = :category
            AND snip_mast.description = :snippet
        """,
        {
            'lang':lang,
            'category':cat,
            'snippet':snip,
            'snip_text':snip_text
        })
        conn.commit()
        conn.close() 