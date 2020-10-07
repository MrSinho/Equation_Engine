import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys, re, ast, os, shutil, concurrent.futures, traceback

from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDIconButton, MDFloatingActionButton
from kivymd.uix.textfield import MDTextField, MDTextFieldRect, MDTextFieldRound
from kivy.lang import Builder
from kivy_ import *
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.list import ThreeLineListItem, ThreeLineIconListItem, IconLeftWidget
from kivy.uix.scrollview import ScrollView
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog

class App(MDApp): 
    def call_exec_algorithm(self,obj):
        print(self.algorithm_builder.text)     
        print(self.points_x_builder.text, self.points_y_builder.text, self.points_z_builder.text)  
        ln = "\n"
        self.entire_class = f"""
class Simulation(object):
    def __init__({self._class}, *args):
        self.app = QtGui.QApplication(sys.argv)
        self.window = gl.GLViewWidget() #create a window
        self.window.setGeometry(480, 270, 800, 600) #set the geometry of the window(padding x, padding y, scale x, scale y)
        self.window.setWindowTitle("Simulation")    #set the window title
        self.window.setCameraPosition(distance=30, elevation=100) #set the camera position
        self.window.show() #show the window
        {str(["self."+str(name) for name in self.names_list]).replace("[", "").replace("]", "").replace("'", "")} = {str([str(name) for name in self.names_list]).replace("[", "").replace("]", "").replace("'", "")}
        self.how = how
        self.points_list = [] #create an empty points_list
        self.point_mesh = np.array([
            [0, 0, 0],
            [2, 0, 0],
            [1, 2, 0],
            [1, 1, 1]
        ])
        self.faces = np.array([
            [0, 1, 2],
            [0, 1, 3],
            [0, 2, 3],
            [1, 2, 3]
        ])

        {(self.start_builder.text).replace(ln, (ln+"        "))}

    #Update is called once per frame
    def Update(self):
        #here ends the algorithm 
        {self.algorithm_builder.text.replace(ln, (ln+"        "))}
        self.newpoint = (self.{self.points_x_builder.text}, self.{self.points_y_builder.text}, self.{self.points_z_builder.text}) # create a newpoint tuple
        #add the new point to the points list
        self.points_list.append(self.newpoint) #add the tuple to the points_list
        self.points = np.array(self.points_list) #convert the points list to an array of tuples
        self.draw()
    def draw(self):
        if self.how == 1:
            self._point_mesh = gl.GLMeshItem(vertexes = self.point_mesh, faces = self.faces, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))
            self._point_mesh.scale(.001, .001, .001)
            self._point_mesh.translate(self.newpoint[0], self.newpoint[1], self.newpoint[2])
            self.window.addItem(self._point_mesh)
        elif self.how == 2:
            try: 
                self.window.removeItem(self.drawpoints)
                #print("removed")
            except Exception: pass
            self.drawpoints = gl.GLLinePlotItem(pos=self.points, width=1, antialias=True) #make a variable to store drawing data(specify the points, set antialiasing)
            self.window.addItem(self.drawpoints) #draw the item
  
    #start properly
    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
                QtGui.QApplication.instance().exec_()
    #animate and update
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.Update)
        timer.start(10)
        self.start()

if __name__ == "__main__":
    {str(self.call)}
"""
        try:
            print(self.entire_class)
            #Clock.schedule_interval(self.execute_class, 0.1)
            App().stop()
            exec(self.entire_class)
        except Exception: traceback.print_exc()
        #exec(self.entire_class)
    
    #def execute_class(self, *args):
    #    try: exec(self.entire_class)
    #    except Exception: traceback.print_exc()

    def confirm_variable(self, obj):
        self.can_add_var = True
        self.screen.remove_widget(self.confirm_button)
        self.screen.remove_widget(self.variable_builder)
        self.screen.remove_widget(self.var_table)
        try: 
            self.variable = self.variable_builder.text.split()
            print(self.variable)
            if(self.variable[0] == "remove"):
                    try:
                        i=0
                        for _ in self.names_list: 
                            if _ == self.variable[1]: 
                                self.types_list.pop(i)
                                self.names_list.pop(i)
                                self.values_list.pop(i)
                                self.variables_list.pop(i)
                                print(self.types_list, self.names_list, self.values_list)
                            i+=1
                        self.update_variables()
                        print("variable has been removed")
                    except Exception: 
                        traceback.print_exc()
                        print("cannot remove variable")
                        self.update_all_widgets()
            
            elif((self.variable[0] == "rename") or (self.variable[0] == "type") or (self.variable[0] == "value")):
                try:
                    i = 0
                    for _ in self.names_list: 
                        if _ == self.variable[1]:
                            if self.variable[0]   == "rename": self.names_list[i]  = self.variable[-1]
                            elif self.variable[0] == "type"  : self.types_list[i]  = self.variable[-1]
                            elif self.variable[0] == "value" : self.values_list[i] = self.variable[-1]
                        i+=1
                    print (self.variables_list)
                    self.update_variables()
                    print("variable has been updated")
                except Exception: 
                    traceback.print_exc()
                    print("cannot update variable")
                    self.update_all_widgets()

            else:
                try: float(self.variable[-1])
                except Exception: 
                    traceback.print_exc()
                    print("Invalid syntax!")
                    self.update_all_widgets()
                if(self.variable[0].isalpha() and self.variable[1].isalpha()): #(self.variable[-1].isalpha() or self.variable[-1].isdigit())):
                    #if(self.variable[0] == "rename"):
                    #    try:
                    #    except Exception: print("cannot rename variable")
                    self.variables_list.append(self.variable_builder.text)
                    print(self.variables_list)
                    self.types_list.append(self.variable[0])
                    print(self.types_list)
                    self.names_list.append(self.variable[1])
                    self.values_list.append(self.variable[-1])
                    self.update_variables()
                else: 
                    print("Invalid syntax!!")
                    self.update_all_widgets()
                    return
        except Exception: 
            traceback.print_exc()
            print("Invalid syntax!")

    def update_variables(self):
        i = 0
        var_lines = [] 
        for _ in self.variables_list:
            var_line = "("+'"'+str(self.names_list[i])+'"'+", "+'"'+str(self.types_list[i])+'"'+", "+'"'+str(self.values_list[i])+'"'+")"
            if i < (len(var_lines)-1): var_line+","
            var_lines.append(var_line)
            i += 1
        var_lines = (str(var_lines)).replace("'", "").replace("[", "").replace("]", "")
        print(var_lines)
        self.dinamic_table = 'self.var_table = MDDataTable(pos_hint={"center_x":0.7, "center_y":0.575}, rows_num = 20, size_hint=(0.2,0.55), column_data=[("Name", dp(15)), ("Type", dp(15)),("Value", dp(15))], row_data=['+var_lines+'])'
        #print(self.dinamic_table)
        self.screen.remove_widget(self.var_table)
        exec(self.dinamic_table)
        self.var_table.bind(on_check_press = self.add_check_press)
        self.call = f"Simulation({str([str(value) for value in self.values_list])}, {str(self.how)}).animation()".replace("[", "").replace("]", "").replace("'", "")
        self._class = f"self, {str([str(name) for name in self.names_list])}, how".replace("[", "").replace("]", "").replace("'", "")      
        print("variable has been loaded successfully!")  
        print(self.call)
        print(self._class)
        self.update_all_widgets()

    def update_all_widgets(self):
        self.screen.remove_widget(self.algorithm_builder)
        self.screen.remove_widget(self.run_button)
        self.screen.remove_widget(self.add_var_button)
        #self.screen.remove_widget(self.remv_var_button)
        self.screen.remove_widget(self.start_builder)
        self.screen.remove_widget(self.points_x_builder)
        self.screen.remove_widget(self.points_y_builder)
        self.screen.remove_widget(self.points_z_builder)
        self.screen.remove_widget(self.var_table)

        self.screen.add_widget(self.var_table)
        self.screen.add_widget(self.algorithm_builder)
        self.screen.add_widget(self.start_builder)
        self.screen.add_widget(self.run_button)
        self.screen.add_widget(self.add_var_button)
        #self.screen.add_widget(self.remv_var_button)
        self.screen.add_widget(self.points_x_builder)
        self.screen.add_widget(self.points_y_builder)
        self.screen.add_widget(self.points_z_builder)
        self.update_checkbox()

    def add_variable(self, obj):
        if self.can_add_var:
            self.variable_builder = Builder.load_string(variable_helper)
            self.confirm_button = MDRectangleFlatButton(text = "Add", pos_hint={"center_x":0.9,"center_y":0.47+.025},
                                                   on_release=self.confirm_variable)
            self.can_add_var = False
            self.screen.add_widget(self.variable_builder)
            self.screen.add_widget(self.confirm_button)
    
    def add_check_press(self, instance_table, instance_row):
        if(self.can_remv_var == False):
            self.can_remv_var = True
            print(instance_row)
        elif(self.can_remv_var == True):
            self.can_remv_var = False
            print("deselected ", str(instance_row))

    def draw_edges(self):
        if ((not self.edges) or self.points):
            print("edges")
            self.edges = True
            self.points = False
            self.how = "2"
        elif(self.edges or (not self.points)):
            self.draw_points()
        self.update_checkbox()
        

    def draw_points(self):
        if (self.edges or (not self.points)):
            print("points")
            self.points = True
            self.edges = False
            self.how = "1"
        elif((not self.edges) or self.points):
            self.draw_edges()
        self.update_checkbox()

    def update_checkbox(self):
        self.screen.remove_widget(self.toolbar)
        self.screen.remove_widget(self.edges_checkbox_builder)
        self.screen.remove_widget(self.points_checkbox_builder)
        self.edges_checkbox_builder = Builder.load_string(edges_checkbox)
        self.points_checkbox_builder = Builder.load_string(points_checkbox)
        self.screen.add_widget(self.edges_checkbox_builder)
        self.screen.add_widget(self.points_checkbox_builder)
        self.screen.add_widget(self.toolbar)

    def save(self, obj):
        try:
            if os.path.exists(f"Saved/{self.directory_builder.text}"): shutil.rmtree(f"Saved/{self.directory_builder.text}")
            os.makedirs(f"Saved/{self.directory_builder.text}")

            saved_start = open(f"Saved/{self.directory_builder.text}/start.start", "w")
            saved_start.write(self.start_builder.text)
            saved_start.flush()
            saved_start.close()

            saved_eq = open(f"Saved/{self.directory_builder.text}/equation.alg", "w")
            saved_eq.write(self.algorithm_builder.text)
            saved_eq.flush()
            saved_eq.close()

            saved_variables = open(f"Saved/{self.directory_builder.text}/variables.var", "w")
            saved_variables.write(str(self.variables_list))
            saved_variables.flush()
            saved_variables.close()

            print("File has been saved successfully")
            self.save_dialog.dismiss()
        except Exception:
            traceback.print_exc()
            print("could not save")
        
        
        
    def close_save_popup(self, obj):
        self.save_dialog.dismiss()
    def close_load_popup(self, obj):
        self.load_dialog.dismiss()

    def save_popup(self):
        self.directory_builder = Builder.load_string(directory_helper)
        cancel_button = MDRectangleFlatButton(text = "Cancel", on_release = self.close_save_popup)
        save_button = MDRectangleFlatButton(text = "Save", on_release = self.save)
        
        self.save_dialog = MDDialog(title = "Save file as", 
                                    size_hint = (0.6, 1), type = "custom", 
                                    content_cls = self.directory_builder,
                                    buttons = [cancel_button, save_button])
        #self.screen.add_widget(self.save_helper)
        self.save_dialog.open()
    
    def load_popup(self):
        self.directory_builder = Builder.load_string(directory_helper)
        cancel_button = MDRectangleFlatButton(text = "Cancel", on_release = self.close_load_popup)
        load_button = MDRectangleFlatButton(text = "Load", on_release = self.load)
        
        self.load_dialog = MDDialog(title = "Load file", 
                                    size_hint = (0.6, 1), type = "custom", 
                                    content_cls = self.directory_builder,
                                    buttons = [cancel_button, load_button])
        #self.screen.add_widget(self.save_helper)
        self.load_dialog.open()

    def load(self, obj):
        try:
            self.file_start = open(f"Saved/{self.directory_builder.text}/start.start", "r").read()
            self.screen.remove_widget(self.start_builder)
            self.start_builder = Builder.load_string(start_helper)
            self.screen.add_widget(self.start_builder)
        except Exception: 
            traceback.print_exc()
            print("could not load Start function")

        try:
            self.file_eq  = open(f"Saved/{self.directory_builder.text}/equation.alg", "r" ).read()
            self.screen.remove_widget(self.algorithm_builder)   
            self.algorithm_builder = Builder.load_string(algorithm_helper)
            self.screen.add_widget(self.algorithm_builder)
            print(self.file_eq)
        except Exception: 
            traceback.print_exc()
            print("could not load Update function")

        try:
            self.file_var = open(f"Saved/{self.directory_builder.text}/variables.var", "r").read()
            self.variables_list = list(ast.literal_eval(self.file_var)) #convert string of list to a list
            print(type(self.variables_list))
            print(self.variables_list)
            for i in self.variables_list:
                i =i.split()
                print(i)
                self.types_list.append(i[0])
                self.names_list.append(i[1])
                self.values_list.append(i[-1])
            self.update_variables()     
            self.load_dialog.dismiss()
          
        except Exception: 
            traceback.print_exc()
            print("could not load variables") 
        

    def imports(self):
        print("import settings")

    def build(self):
        self.how = "2"

        self.can_add_var = True
        self.can_remv_var = False
        self.edges = True
        self.points = False
        self.file_eq = ""
        self.file_start = ""

        Window.size=(1400, 700)
        self.title = "Algorithm Engine"
        self.variables_list = []#"float x = 0.5", "float yy = 3.0", "float z 0", "float c 1", "float y = 0"]
        self.types_list     = []#"float", "float", "float", "float", "float"                               ]
        self.values_list    = []#"0.5", "3.0", "0", "1", "0"                                               ]
        self.names_list     = []#"x", "yy", "z", "c","y"                                                   ]

        #theme
        self.theme_cls.primary_palette = "Yellow"
        self.theme_cls.primary_hue = "500"
        self.theme_cls.theme_style = "Dark"

        self.screen = Screen()

        self.toolbar = Builder.load_string(toolbar)
        

        self.run_button = MDRectangleFlatButton(text = "Run", 
                                       pos_hint={"center_x": 0.086-.025, "center_y": 0.217},
                                       on_release = self.call_exec_algorithm)
        #self.save_button = MDRectangleFlatButton(text = "Save", 
        #                               pos_hint={"center_x": 0.086, "center_y": 0.317},
        #                               on_release = self.call_exec_algorithm)
        #self.load_button = MDRectangleFlatButton(text = "Load", 
        #                               pos_hint={"center_x": 0.086, "center_y": 0.317},
        #                               on_release = self.call_exec_algorithm)

        self.add_var_button = MDIconButton(icon = "plus", pos_hint={"center_x":0.9, "center_y": 0.61+.025},
                                      on_release = self.add_variable)

        #self.remv_var_button = MDIconButton(icon = "minus", pos_hint={"center_x":0.912, "center_y":0.61+.025}) 
            
        self.var_table = MDDataTable(#check = True,
                                pos_hint={"center_x":0.7, "center_y":0.575},
                                rows_num = 10,
                                size_hint=(.2,0.55),
                                column_data=[
                                ("Name", dp(15)), 
                                ("Type", dp(15)), 
                                ("Value", dp(15)), 
        ],
                                row_data=[

        ])
        
        self.points_x_builder = Builder.load_string(point_x_helper)
        self.points_y_builder = Builder.load_string(point_y_helper)
        self.points_z_builder = Builder.load_string(point_z_helper)

        #script_builder
        self.algorithm_builder = Builder.load_string(algorithm_helper)
        self.start_builder = Builder.load_string(start_helper)
        self.edges_checkbox_builder = Builder.load_string(edges_checkbox)
        self.points_checkbox_builder = Builder.load_string(points_checkbox)


        #var_table
        self.screen.add_widget(self.var_table)
        #script_builder
        self.screen.add_widget(self.algorithm_builder)
        self.screen.add_widget(self.start_builder)
        self.screen.add_widget(self.edges_checkbox_builder)
        self.screen.add_widget(self.points_checkbox_builder)
        #run_button
        self.screen.add_widget(self.run_button)
        #toolbar
        self.screen.add_widget(self.toolbar)
        #save button
        #self.screen.add_widget(self.save_button)
        ##load button
        #self.screen.add_widget(self.load_button)
        ##imports button

        #plus_button
        self.screen.add_widget(self.add_var_button)
        #minus_button
        #self.screen.add_widget(self.remv_var_button)
        #points_input
        self.screen.add_widget(self.points_x_builder)
        self.screen.add_widget(self.points_y_builder)
        self.screen.add_widget(self.points_z_builder)
        
        return self.screen

while True:
    if __name__ == "__main__":
        app = App()
        app.run()
        

