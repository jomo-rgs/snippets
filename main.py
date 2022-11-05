from ast import Num
from data import Data
import re
import sys
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivymd.uix.snackbar import Snackbar
from kivymd.app import MDApp
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ListProperty, StringProperty, ObjectProperty, NumericProperty, DictProperty
from kivy.uix.treeview import TreeView, TreeViewNode
from kivy.uix.button import Label
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard

# Window.size = (1000,1000)


#######################  #######################  #######################  
#######################    CLASS-TreeViewLabel    #######################  
#######################  #######################  #######################  
class TreeViewLabel(Label, TreeViewNode):
    pass        


#######################  #######################  #######################  
#######################     CLASS-ConfirmPopup    #######################  
#######################  #######################  #######################  
class ConfirmPopup(GridLayout):
	text = StringProperty()
	
	def __init__(self,**kwargs):
		self.register_event_type('on_answer')
		super(ConfirmPopup,self).__init__(**kwargs)
		
	def on_answer(self, *args):
		pass	

#######################  #######################  #######################  
#######################    CLASS-SearchPopup      #######################  
#######################  #######################  #######################  
class SearchPopup(Popup):

    my_layout_instance = ObjectProperty()

    ###################################################
    ## SearchPopup: Default Constructor 
    ###################################################
    def __init__(self, my_layout_instance): 
        super(SearchPopup, self).__init__()
        self.my_layout_instance = my_layout_instance

    ###################################################
    ## BTN SEARCH : Search Btn Clicked
    ###################################################
    def btn_search(self):
        self.my_layout_instance.btn_search(self.ids.text_search.text)    
        self.dismiss()




#######################  #######################  #######################  
#######################    CLASS-NewSnipPopup     #######################  
#######################  #######################  #######################  
class NewSnipPopup(Popup):

    languages = ListProperty([])
    category = StringProperty('')
    language = StringProperty('')
    my_layout_instance = ObjectProperty()

    ###################################################
    ## NewSnipPopup: Default Constructor 
    ###################################################
    def __init__(self, my_layout_instance): 
        super(NewSnipPopup, self).__init__()  
        self.my_layout_instance = my_layout_instance
        tree_list = my_layout_instance.tree_list
        if len(tree_list) == 2:
            self.language = tree_list[0]
        elif len(tree_list) == 3:
            self.language = tree_list[1]
            self.category = tree_list[0]
        elif len(tree_list) == 4:
            self.language = tree_list[2]
            self.category = tree_list[1]
        else:
            self.language = "Text" 
              
        self.languages = list(Data.dict_lang.keys())  


    ####################################################
    ## NewSnipPopup : Create New Snippet
    ####################################################    
    def btn_create(self):
        lang = self.ids.spinner_lang.text
        category = self.ids.text_cat.text
        snippet = self.ids.text_snip_name.text

        self.ids.lbl_category_error.text = ""
        self.ids.lbl_snip_name_error.text = ""

        # Validate Form
        if len(category) < 1:
            self.ids.lbl_category_error.text = "*Category Required"
        if len(snippet) < 1:
            self.ids.lbl_snip_name_error.text = "*Name Required"
        if len(category) < 1 or len(snippet) < 1:
            return None

        if Data.query_duplicate(lang, category, snippet) != None:            
            self.ids.lbl_snip_name_error.text = f"{lang} > {category} > {snippet} : already exists."
            return None  

        self.my_layout_instance.create(lang, category, snippet)                     

        self.dismiss()




#######################  #######################  #######################  
#######################      CLASS-MyLayout       #######################  
#######################  #######################  #######################  
class MyLayout(Widget):
    tree_list = ListProperty([])
    old_code = StringProperty('')           # Save old value to check for changes
    old_version = NumericProperty()         # Save old value to check for changes
    old_tree_list = ListProperty([])        # Save old value to check for changes
    last_selected_text_value = StringProperty('')   # Used for copy function
    last_selected_start = NumericProperty()         # Used for copy function
    last_selected_end = NumericProperty()           # Used for copy function
    filter_value = StringProperty('')

    data = Data.get_speed_dial_items()

    # dict_lang = DictProperty({'SQL' : PostgresLexer(), 'JAVA':  JavaLexer(), 'PL/SQL':  PlPgsqlLexer(), 'HTML' or lang == 'XML':  HtmlLexer(), 
    #         'CSS':  CssLexer(), 'JAVASCRIPT':  JavascriptLexer(), 'JSON':  JsonLexer(), 'Groovy':  GroovyLexer(), 'PHP':  HtmlPhpLexer(), 
    #         'C':  CLexer(), 'C++':  CppLexer(), 'C#':  CSharpAspxLexer(), 'FOXPRO':  FoxProLexer(), 'VISUAL BASIC':  VBScriptLexer(),
    #         'BASH':  BashLexer(), 'BATCH':  BatchLexer(), 'POWERSHELL':  PowerShellLexer(), 'DOCKER':  DockerLexer(),
    #         'PYTHON' :  CythonLexer(), 'TEXT' :  TextLexer()
    #     } ) 
    
    #####################################################
    ## INIT SCREEN - Initialize Stuff
    #####################################################    
    def init_screen(self):  
        # Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
        Config.set('input', 'mouse', 'mouse,disable_multitouch')

        Data.create_db()
        self.load_tree()

        # Reload Nodes Open From Last Session
        node_dict = Data.query_last_session_open_nodes()
        self.find_and_open_nodes(node_dict['lang'], node_dict['cat'], node_dict['snip'])

        print(f"Split Width Value = {Data.get_setting('split_width')}")
        
        if Data.get_setting('split_width') != None:
            self.ids.split_2.width = Data.get_setting('split_width')


        # I don't like the way this looks on the screen...
        # self.ids.db_location.text = Data.get_db_file() + "  "

    #####################################################
    ## BTN SEARCH - Search Snippets Popup
    ##################################################### 
    def btn_search(self, value):
        self.filter_value = value
        self.load_tree()
        self.ids.code.text = "" 
        self.ids.spinner_history.opacity = 0
        self.ids.spinner_history.disabled = True 

        self.ids.btn_filter.height = 35
        self.ids.btn_filter.opacity = 1
        self.ids.btn_filter.disabled = False

    #####################################################
    ## CLEAR FILTER - Clear Search Filter in Tree
    #####################################################    
    def clear_filter(self):
        print("clear filter")
        self.filter_value = ""
        self.load_tree()

        self.ids.btn_filter.height = 0
        self.ids.btn_filter.opacity = 0
        self.ids.btn_filter.disabled = True        

    #####################################################
    ## BTN SPEED DIAL - Actions for Speed Dial Menu
    #####################################################    
    def btn_speed_dial(self, instance):
        if instance.icon == 'select-all':
            self.ids.code.select_all()
            self.ids.code.copy()
        if instance.icon == 'content-copy':
            Clipboard.copy(self.last_selected_text_value)
        if instance.icon == 'content-cut':
            self.ids.code.cut()
        if instance.icon == 'content-paste':
            self.ids.code.paste()
        if instance.icon == 'chart-tree':
            if len(self.old_tree_list) == 4:
                snip, cat, lang, not_used = self.old_tree_list
                self.find_and_open_nodes(lang, cat, snip)
        if instance.icon == 'undo':
            self.ids.code.do_undo()
        if instance.icon == 'redo':
            self.ids.code.do_redo()
        if instance.icon == 'delete':
            self.delete_version_check()

    #####################################################
    ## HOLD LAST TEXT SELECTION (Function 1)
    ## Keep text highlighted when focus is lost
    #####################################################    
    def hold_last_text_selected(self):
        if self.ids.code.selection_text.strip() != "":
            self.last_selected_text_value = self.ids.code.selection_text
            begin, end = sorted([self.ids.code.selection_from, self.ids.code.selection_to])
            self.last_selected_start = begin
            self.last_selected_end = end
            
    #####################################################
    ## CODE FOCUS (Function 2)
    ## Keep text highlighted when focus is lost
    ######################################################             
    def code_focus(self):
        if self.last_selected_start != None and self.last_selected_end != None:
            self.ids.code.select_text(self.last_selected_start, self.last_selected_end)

    #####################################################
    ## DELETE VERSION - Prompt User Before Delete
    #####################################################    
    def delete_version_check(self):
        if len(self.get_tree_list()) != 4:
            print('No snippet selected')
            return

        content = ConfirmPopup(text=f'Delete History version: {self.old_version}?')
        content.bind(on_answer=self.delete_version)
        self.popup = Popup(title="Confirm Delete",
                            content=content,
                            size_hint=(None, None),
                            size=(480,150),
                            auto_dismiss= False)
        self.popup.open()

    #####################################################
    ## DELETE VERSION - Delete the Current Code Version 
    #####################################################    
    def delete_version(self, instance, answer):
        self.popup.dismiss()  
        if answer.upper() != 'YES':
             return

        snip, cat, lang, not_used = self.get_tree_list()
        count = Data.query_count_versions(lang, cat, snip)

        if count[0] <= 1:
            Snackbar(text="Must leave at least one version. Cannot delete").open() 
            return 

        snip, cat, lang, not_used = self.get_tree_list()
        Data.delete_version(lang, cat, snip, self.old_version)
        self.select_node()

    #####################################################
    ## FIND AND OPEN NODE - Find Node in Tree and Open
    #####################################################    
    def find_and_open_nodes(self, lang, cat, snip):
        tree = self.ids.tree
        lang_found = False
        category_found = False
        snip_found = False
        for node in tree.iterate_all_nodes():

            if node.text == lang and lang_found == False:
                lang_found = True
                if node.is_open == False:
                    tree.toggle_node(node)

            # Expand Cat Node
            if node.text == cat and lang_found == True and category_found == False:
                lang_found = False # Only fire one time.
                category_found = True
                if node.is_open == False:
                    tree.toggle_node(node) 

            if node.text == snip and category_found == True and snip_found == False:
                snip_found = True #Only fire 1 time
                tree.select_node(node)
                self.select_node()                
            
    #####################################################
    ### get_tree_list : List with selected tree values
    #####################################################
    def get_tree_list(self):
        tree = []
        if self.ids.tree.selected_node != None:
            tree.append(self.ids.tree.selected_node.text)
            pn = self.ids.tree.selected_node.parent_node
            if pn != None:
                tree.append(pn.text)
                pn_base = pn.parent_node
                if pn_base != None:
                    tree.append(pn_base.text)
                    pn_root = pn_base.parent_node
                    if pn_root != None:
                        tree.append(pn_root.text)

        return tree

    #####################################################
    ## CREATE - Create New Snippet
    #####################################################    
    def create(self, lang, category, snippet):
        self.ids.spinner_history.opacity = 0
        self.ids.spinner_history.disabled = True             
 
        if Data.query_lang_cat_exist(lang, category) == None:
            Data.insert_into_node(lang, category)
         
        Data.insert_into_snip_mast(lang, category, snippet)

        self.load_tree() 
        self.find_and_open_nodes(lang, category, snippet)

    #####################################################
    ## SPINNER CHANGE - Version Spinner Value Changed
    #####################################################    
    def spinner_change(self):
        seq = self.ids.spinner_history.values.index(self.ids.spinner_history.text)
        length = len(self.ids.spinner_history.values)

        tree_list = self.get_tree_list()
        if tree_list == None:
            return None

        if len(tree_list) < 4:
            return None

        record = Data.query_snip_detail_code(length, seq, tree_list[2], tree_list[1], tree_list[0])

        if record != None:
            if len(record) >= 1:
                self.ids.code.text = record[0]
                self.old_code = record[0]
                self.ids.current_snippet.text = f"  {tree_list[2]} ->  {tree_list[1]} ->  {tree_list[0]} : {record[1]}"
                self.old_version = record[1]

    #####################################################
    ### SELECT NODE
    #####################################################
    def select_node(self):
        tree = self.get_tree_list()
        self.tree_list = tree
        self.old_tree_list = tree

        self.ids.current_snippet.text = "" 
        self.ids.code.text = ""
        self.old_code = ""
        self.ids.spinner_history.opacity = 0
        self.ids.spinner_history.disabled = True       

        ## >>> Exit Function ********************
        if len(tree) < 4: return     

        snippet, category, lang, not_used = tree

        record = Data.query_node_detail(lang, category, snippet) 

        if record is not None:
            self.ids.code.text = record[3]
            self.old_code = record[3]

        self.ids.code.lexer = Data.dict_lang[lang]    

        snip_id = -1
        if record != None:
            if len(record) >= 8:
                snip_id = record[8]

        records = Data.query_version(snip_id)  

        if len(records) > 0:
            versions = []
            for r in records:
                versions.append(r[0])

            self.ids.spinner_history.values = versions    
            self.ids.spinner_history.text = versions[0] 
            self.ids.spinner_history.opacity = 1
            self.ids.spinner_history.disabled = False  
            self.ids.current_snippet.text = f"  {lang} ->  {category} ->  {snippet} : {record[6]}"
            self.old_version = record[6]
                                  

    #################################################
    ## NODE CLICKED - Node In Tree Has Been Clicked
    #################################################
    def node_clicked(self, Label, MouseEvent):
        if self.ids.code.text != self.old_code:
            self.auto_save_on_tree_change()
        self.select_node()
                
    #################################################
    ### LOAD TREE - Populate Tree With Values
    #################################################
    def load_tree(self):
        for node in [i for i in self.ids.tree.iterate_all_nodes()]:         # Clear All Nodes 
            self.ids.tree.remove_node(node)

        filter = 'N'
        filter_value = ""
        if self.filter_value is not None:
            if self.filter_value.strip() != "":
                filter = 'Y'
                filter_value = self.filter_value.strip()
        
        records = Data.query_tree(filter, filter_value)

        node = None
        node2 = None
        last_lang = None
        last_category = None
        for record in records:
            lang = record[0]

            if record[4] == 1:
                continue
                       
            if last_lang != lang:
                lbl1 = TreeViewLabel(text=lang)
                lbl1.bind(on_touch_down=self.node_clicked)
                node = self.ids.tree.add_node(lbl1)

            if last_category != record[1]:
                lbl2 = TreeViewLabel(text=record[1])
                lbl2.bind(on_touch_down=self.node_clicked)
                node2 = self.ids.tree.add_node(lbl2, node)

            lbl = TreeViewLabel(text=record[2])
            lbl.bind(on_touch_down=self.node_clicked)
            self.ids.tree.add_node(lbl, node2)

            last_lang = record[0]
            last_category = record[1]

    #######################################
    ## DELETE BTN - Delete Btn Event
    #######################################    
    def delete_btn(self, button):
        if len(self.get_tree_list()) == 4:
            content = ConfirmPopup(text='Delete Snippet?')
            content.bind(on_answer=self.delete_confirm)
            self.popup = Popup(title="Confirm Delete",
                                content=content,
                                size_hint=(None, None),
                                size=(480,150),
                                auto_dismiss= False)
            self.popup.open()
        else:
            Snackbar(text="Nothing Selected to Delete").open() 

    #######################################
    ## DELETE CONFIRM - Verify with user
    #######################################
    def delete_confirm(self, instance, answer):
        self.popup.dismiss()        
        if answer.upper() == ('YES'):
            self.delete()

    #######################################
    ## DELETE BUTTON - Mark as deleted
    #######################################
    def delete(self):
        tree = self.get_tree_list()
        lang = tree[2]
        category = tree[1]
        snippet = tree[0]

        self.ids.tree.remove_node(self.ids.tree.selected_node)

        Snackbar(text="Delete Document").open()
        snip_text = self.ids.code.text               
        
        Data.update_delete_snip_mast(lang, category, snippet)

        self.ids.code.text = "" 
        self.ids.spinner_history.opacity = 0
        self.ids.spinner_history.disabled = True 

    #####################################################
    ## TOGGLE TREE - Hide/Display Tree Control
    #####################################################    
    def toggle_tree(self, button):
        if self.ids.split_2.width == 0:
            self.ids.split_2.width = self.tree_width
        else:
            self.tree_width = self.ids.split_2.width
            self.ids.split_2.width = 0

    #####################################################
    ## ON REQUEST CLOSE - Stuff To Do Before Close
    #####################################################     
    def on_request_close(self, *args):
        if self.old_code != self.ids.code.text:
            self.save(0)

        l = len(self.tree_list)
        if l >= 2:
            Data.set_setting('last_open_node_lang', self.tree_list[l-2])
        else:
            Data.set_setting('last_open_node_lang', '')
        if l >= 3:
            Data.set_setting('last_open_node_cat', self.tree_list[l-3])    
        else:
            Data.set_setting('last_open_node_cat', '')            
        if l >= 4:
            Data.set_setting('last_open_node_snip', self.tree_list[l-4])
        else:
            Data.set_setting('last_open_node_snip', '')

        # Save split window position
        Data.set_setting('split_width',self.ids.split_2.width)
      
        #quit()
        sys.exit()
        return True

    #####################################################
    ## AUTO SAVE ON TREE CHANGE 
    ## - Save snippet if user clicks out of field
    #####################################################    
    def auto_save_on_tree_change(self):
        self.save(1) # 1 = Previous snippet

    #######################################
    ## SAVE BUTTON
    #######################################
    def save(self, *args):
        if args[0] == 1:
            tree = self.old_tree_list
        else:
            tree = self.get_tree_list()

        if len(tree) == 4:                        
            lang = tree[2]
            category = tree[1]
            snippet = tree[0]
            
            snip_text = self.ids.code.text    

            if self.ids.code.text != self.old_code and self.ids.code.text != "":
                Data.insert_snip_detail(lang, category, snippet, snip_text)

                self.select_node()
                self.old_code = self.ids.code.text
                Snackbar(text="Snippet Saved").open()
            else:
                print("No Change made...")
                Snackbar(text="Nothing to Save").open()  
        else:
            if args[0] != 1: # Suppress message if auto save from tree 
                Snackbar(text="Nothing Selected to Save").open()           


    # def settings(self, button):
    #     Snackbar(text="Show Settings").open()      


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'BlueGray'
        myLayout = MyLayout()
        myLayout.init_screen()
        Window.bind(on_request_close=myLayout.on_request_close)
        self.title = 'Snippet ' + Data.get_version()
        self.icon = 'icon.png'
        Window.maximize()
        return myLayout

MainApp().run()         