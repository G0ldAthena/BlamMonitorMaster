import os
import sys
import threading
import re
import shutil

import customtkinter as ctk
import win32api
from PIL import Image
import subprocess

def resourcePath(relativePath):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        basePath = sys._MEIPASS
    except Exception:
        basePath = os.path.abspath(".")

    return os.path.join(basePath, relativePath)


class MonitorMasterApp:
    def __init__(self, master):
        self.master = master
        master.title("Blam Monitor Master")
        master.configure(fg_color='#000f24')
        master.columnconfigure(0, weight=1)  # Left column
        master.columnconfigure(1, weight=1)  # Right column
        
        self.font_small = ctk.CTkFont(family="Arial", size=12, weight="bold")
        self.font_big = ctk.CTkFont(family="Arial", size=16, weight="bold")
        
        self.font_style = self.font_big
        
        # WINDOW SIZE
        self.window_width = 500
        self.window_height = 722
        
        self.text_color_unavailable = '#60646e'
        self.text_color_standby = '#7eb3de'
        self.text_color_running = '#73de9a'
        self.text_color_err = '#de7373'
        
        self.text_unavailable = 'Unavailable in this engine'
        self.text_standby = 'Standing by...'
        self.text_running = 'RUNNING'
        self.text_wrongdir = 'ERROR (Tool not found!)'
        self.text_err = 'ERROR (printed to console)'
        
        self.button_fg_color = '#26394f'
        self.button_text_color = '#8eaec4'
        self.button_disabled_fg_color = '#171f29'
        self.button_disabled_text_color = '#37454f'

        self.processes = {}
        self.string_monitor_active = 0

        self.buttons = [
            ("Bitmaps", "tool monitor-bitmaps"),
            ("Bitmaps (Data and Tags)", "tool monitor-data-and-tags-bitmaps"),
            ("Models", "tool monitor-models"),
            ("Models (Draft)", "tool monitor-models-draft"),
            ("Strings", "tool monitor-strings"),
            ("Structure (BSP)", "tool monitor-structures")
        ]

        # Background image
        self.bg_image_initial = Image.open(resourcePath("bg.tif"))
        self.bg_image = ctk.CTkImage(light_image = self.bg_image_initial, dark_image = self.bg_image_initial, size = (self.window_width, self.window_height))
        self.bg_label = ctk.CTkLabel(master, image=self.bg_image, text= "")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # SIZE RETAINER
        #size_retainer = ctk.CTkButton(master, text= "", width = self.window_width/1.80, fg_color="transparent")
        #size_retainer.grid(row=0, column=0, columnspan=1, pady=(10, 0), sticky="n")

        # TITLE
        self.logo_image_initial = Image.open(resourcePath("logo.png")).convert("RGBA")
        self.logo_image = ctk.CTkImage(light_image = self.logo_image_initial, dark_image = self.logo_image_initial, size = (self.window_width * 0.78, 153))
        title_label = ctk.CTkLabel(master, image=self.logo_image, text= "", fg_color="transparent")
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 0), sticky="n")
        
        # CURRENT PATH
        running_in_label = ctk.CTkLabel(master, text= "Running in: ", font=self.font_small, text_color='#8eaec4', fg_color="transparent")
        running_in_label.grid(row=1, column=0, padx=(0,5), pady=3, sticky="e")
        directory_label = ctk.CTkLabel(master, text= "/" + os.path.split(os.getcwd())[1], font=self.font_small, text_color='#8eaec4', fg_color="transparent")
        directory_label.grid(row=1, column=1, padx=(5,0), pady=3, sticky="w")
        
        # LABEL - Engine
        title_label_engine = ctk.CTkLabel(master, text="Engine:", font=("Conduit ITC", 20, 'bold'), text_color='#8eaec4', fg_color="transparent")
        title_label_engine.grid(row=2, column=0, padx=(0, 5), pady=5, sticky="e")
        # COMBO - Engine
        engines = ["Halo 2", "Halo 3/ODST", "Halo: Reach", "Halo 4"]
        self.combo_engine = ctk.CTkComboBox(master, values=engines, state="readonly", font=self.font_small, command = self.engine_selected)
        self.combo_engine.set("<SELECT>")
        self.combo_engine.grid(row=2, column=1, padx=(5, 0), pady=5, sticky="w")
        #Style
        '''combostyle = tctk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox':
                                            {'configure':
                                            {'selectbackground': "transparent",
                                            'fieldbackground': "transparent",
                                            'background': "transparent",
                                            'foreground': self.text_color_standby,
                                            'text': '#FFFFFF'
                                            }}}
                                )
        combostyle.theme_use('combostyle')'''
        #self.combo_engine.bind('<<ComboboxSelected>>', self.engine_selected)
        
        
        # BUTTONS AND LABELS
        self.button_bitmaps = ctk.CTkButton(master, text="Bitmaps", command=lambda cmd="tool monitor-bitmaps": self.toggle_process(cmd, self.status_label_bitmaps), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_bitmaps.grid(row=0+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_bitmaps = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_bitmaps.grid(row=0+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[0] = ("Bitmaps", "tool monitor-bitmaps", self.button_bitmaps, self.status_label_bitmaps)
        
        self.button_bitmaps_data_and_tags = ctk.CTkButton(master, text="Bitmaps (Tags)", command=lambda cmd="tool monitor-data-and-tags-bitmaps": self.toggle_process(cmd, self.status_label_bitmaps_data_and_tags), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_bitmaps_data_and_tags.grid(row=1+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_bitmaps_data_and_tags = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_bitmaps_data_and_tags.grid(row=1+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[1] = ("Bitmaps (Data and Tags)", "tool monitor-data-and-tags-bitmaps", self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
        
        self.button_models = ctk.CTkButton(master, text="Models", command=lambda cmd="tool monitor-models": self.toggle_process(cmd, self.status_label_models), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_models.grid(row=2+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_models = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_models.grid(row=2+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[2] = ("Models", "tool monitor-models", self.button_models, self.status_label_models)
        
        self.button_models_draft = ctk.CTkButton(master, text="Models (Draft)", command=lambda cmd="tool monitor-models-draft": self.toggle_process(cmd, self.status_label_models_draft), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_models_draft.grid(row=3+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_models_draft = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_models_draft.grid(row=3+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[3] = ("Models (Draft)", "tool monitor-models-draft", self.button_models_draft, self.status_label_models_draft)
        
        self.button_strings = ctk.CTkButton(master, text="Strings", command=lambda cmd="tool monitor-strings": self.toggle_string(cmd, self.status_label_strings), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_strings.grid(row=4+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_strings = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_strings.grid(row=4+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[4] = ("Strings", "tool monitor-strings", self.button_strings, self.status_label_strings)
        
        self.button_structures = ctk.CTkButton(master, text="Structures (BSP)", command=lambda cmd="tool monitor-structures": self.toggle_process(cmd, self.status_label_structures), fg_color=self.button_fg_color, text_color=self.button_text_color, font=self.font_style)
        self.button_structures.grid(row=5+3, column=0, padx=(0, 5), pady=10, sticky="e")
        self.status_label_structures = ctk.CTkLabel(master, text=self.text_standby, text_color=self.text_color_standby, fg_color="transparent", font=self.font_small)
        self.status_label_structures.grid(row=5+3, column=1, padx=(5, 0), pady=10, sticky="w")
        self.buttons[5] = ("Structures", "tool monitor-structures", self.button_structures, self.status_label_structures)


        # CONSOLE
        self.textbox_console = ctk.CTkTextbox(
            master,
            height= 125,
            width = self.window_height - 320,
            fg_color="transparent",
            font=self.font_small,
            text_color=self.text_color_standby,
            wrap="none",
            scrollbar_button_color=self.button_fg_color,
            scrollbar_button_hover_color=self.button_text_color
            )
        self.textbox_console.grid(row=6+3, column=0, columnspan=2, pady=(40), sticky="n")
        #self.textbox_console.insert("0.0", "Standing by...")

        # Redirect stdout
        sys.stdout = TextRedirector(self.textbox_console)
        sys.stderr = TextRedirector(self.textbox_console)

        master.geometry(str(self.window_width) + "x" + str(self.window_height))
        
        # Initially set all buttons to disabled (so user can select engine)
        self.disable_button(self.button_bitmaps, self.status_label_bitmaps)
        self.disable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
        self.disable_button(self.button_models, self.status_label_models)
        self.disable_button(self.button_models_draft, self.status_label_models_draft)
        self.disable_button(self.button_strings, self.status_label_strings)
        self.disable_button(self.button_structures, self.status_label_structures)
        
        # AUTO SET ENGINE
        if not (os.path.exists("tool.exe")):
            # Tool not found, set error stuff
            print("Tool not found!")
            self.status_label_bitmaps.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.status_label_bitmaps_data_and_tags.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.status_label_models.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.status_label_models_draft.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.status_label_strings.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.status_label_structures.configure(text=self.text_wrongdir, text_color=self.text_color_err)
            self.combo_engine.configure(state="disabled")
        else:
            print("Tool found, detecting game version...")
            # Automatically detect which engine via tool.exe
            tool_properties = self.getFileProperties("tool.exe")
            match tool_properties['StringFileInfo']['FileDescription']:
                case "H2 Game Asset Compiler":
                    self.combo_engine.set("Halo 2")
                    self.engine_selected(self)
                case "H3 Game Asset Compiler":
                    self.combo_engine.set("Halo 3/ODST")
                    self.engine_selected(self)
                case "H3ODST Game Asset Compiler":
                    self.combo_engine.set("Halo 3/ODST")
                    self.engine_selected(self)
                case "HR Game Asset Compiler":
                    self.combo_engine.set("Halo: Reach")
                    self.engine_selected(self)
                case "H4 Game Asset Compiler":
                    self.combo_engine.set("Halo 4")
                    self.engine_selected(self)
        
        # Done! now waiting for user input
        print("Standing by...")
                
                    
            

    # Get file properties on windows (credit to Helmut N.)
    #==============================================================================
    def getFileProperties(self, fname):
    #==============================================================================
        """
        Read all properties of the given file return them as a dictionary.
        """
        propNames = ('Comments', 'InternalName', 'ProductName',
            'CompanyName', 'LegalCopyright', 'ProductVersion',
            'FileDescription', 'LegalTrademarks', 'PrivateBuild',
            'FileVersion', 'OriginalFilename', 'SpecialBuild')

        props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

        try:
            # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
            fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
            props['FixedFileInfo'] = fixedInfo
            props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                    fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                    fixedInfo['FileVersionLS'] % 65536)

            # \VarFileInfo\Translation returns list of available (language, codepage)
            # pairs that can be used to retreive string info. We are using only the first pair.
            lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

            # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
            # two are language/codepage pair returned from above

            strInfo = {}
            for propName in propNames:
                strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
                ## print str_info
                strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

            props['StringFileInfo'] = strInfo
        except:
            pass

        return props


    def disable_button(self, button, label):
        # Disable given button
        button.configure(fg_color=self.button_disabled_fg_color)
        button.configure(text_color=self.button_disabled_text_color)
        button.configure(state="disabled")
        #Set label text
        label.configure(text=self.text_unavailable, text_color=self.text_color_unavailable)
        
        
    def enable_button(self, button, label):
        # Enable given button
        button.configure(fg_color=self.button_fg_color)
        button.configure(text_color=self.button_text_color)
        button.configure(state="normal")
        label.configure(text=self.text_standby, text_color=self.text_color_standby)

    def engine_selected(self, event):
        value = self.combo_engine.get()
        print("Engine selected: ", value)
        
        if value == "Halo 2":
            ## Set Halo 2 available buttons
            # bitmaps               - YES
            # data and tags bitmaps - YES
            # models                - YES
            # models draft          - x
            # strings               - x
            # structures            - YES
            self.enable_button(self.button_bitmaps, self.status_label_bitmaps)
            self.enable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
            self.enable_button(self.button_models, self.status_label_models)
            self.disable_button(self.button_models_draft, self.status_label_models_draft)
            self.disable_button(self.button_strings, self.status_label_strings)
            self.enable_button(self.button_structures, self.status_label_structures)

        elif value == "Halo 3/ODST":
            # Set Halo 3/ODST available buttons
            # bitmaps               - YES
            # data and tags bitmaps - x
            # models                - YES
            # models draft          - YES
            # strings               - YES
            # structures            - YES
            self.enable_button(self.button_bitmaps, self.status_label_bitmaps)
            self.disable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
            self.enable_button(self.button_models, self.status_label_models)
            self.enable_button(self.button_models_draft, self.status_label_models_draft)
            self.enable_button(self.button_strings, self.status_label_strings)
            self.enable_button(self.button_structures, self.status_label_structures)

            
        elif value == "Halo: Reach":
            # Set Halo: Reach available buttons
            # bitmaps               - YES
            # data and tags bitmaps - x
            # models                - YES
            # models draft          - YES
            # strings               - YES
            # structures            - x
            self.enable_button(self.button_bitmaps, self.status_label_bitmaps)
            self.disable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
            self.enable_button(self.button_models, self.status_label_models)
            self.enable_button(self.button_models_draft, self.status_label_models_draft)
            self.enable_button(self.button_strings, self.status_label_strings)
            self.disable_button(self.button_structures, self.status_label_structures)

            
        elif value == "Halo 4":
            # Set Halo 4 available buttons
            # bitmaps               - YES
            # data and tags bitmaps - x
            # models                - x
            # models draft          - x
            # strings               - YES
            # structures            - x
            self.enable_button(self.button_bitmaps, self.status_label_bitmaps)
            self.disable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
            self.disable_button(self.button_models, self.status_label_models)
            self.disable_button(self.button_models_draft, self.status_label_models_draft)
            self.enable_button(self.button_strings, self.status_label_strings)
            self.disable_button(self.button_structures, self.status_label_structures)
            
        else:
            print("ERROR: No engine selected")

    def toggle_process(self, command, label):
        button_index = None
        for i, (_, cmd, _, _) in enumerate(self.buttons):
            if cmd == command:
                button_index = i
                break

        if button_index is None:
            return

        if command in self.processes:
            print(f"Stopping process: {command}")
            self.processes[command].terminate()
            del self.processes[command]
            label.configure(text=self.text_standby, text_color=self.text_color_standby)
            # Enable engine combobox if no processes are running
            if not self.processes:
                self.combo_engine.configure(state="readonly")
            
        else:
            print(f"Starting process: {command}")
            try:
                startupinfo = None
                if os.name == 'nt': # If on windows, hide subprocess windows
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,  stderr=subprocess.PIPE, startupinfo=startupinfo, text=True)
                self.processes[command] = process
                
                # Start mover process in another thread
                new_thread = threading.Thread(target=self.subprocess_console_write, name = command + " thread", args=(process,))
                new_thread.daemon = True
                new_thread.start()
                
                label.configure(text=self.text_running, text_color=self.text_color_running)
                # Disable engine combobox
                self.combo_engine.configure(state="disabled")
            except OSError as e:
                label.configure(text=self.text_err, text_color=self.text_color_err)
                print(e)
    
    def subprocess_console_write(self, process):
        if process.stdout is None:
            raise ValueError("Subprocess must be created with stdout=subprocess.PIPE")
        while True:
            line = process.stdout.readline()
            print(line)
    
    def toggle_string(self, command, label):
        button_index = None
        for i, (_, cmd, _, _) in enumerate(self.buttons):
            if cmd == command:
                button_index = i
                break

        if button_index is None:
            return

        if command in self.processes:
            
            # Stop process
            print(f"Stopping process: tool monitor-strings")
            self.processes[command].terminate()
            del self.processes[command]
            self.string_monitor_active = 0
            
            # Set label text
            label.configure(text=self.text_standby, text_color=self.text_color_standby)
            
            # Enable engine combobox if no processes are running
            if not self.processes:
                self.combo_engine.configure(state="readonly")
            
        else:
            print(f"Starting process: tool monitor-strings")
            try:
                startupinfo = None
                if os.name == 'nt': # If on windows, hide subprocess windows
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                # Start process
                process = subprocess.Popen("tool monitor-strings", stdout=subprocess.PIPE,  stderr=subprocess.PIPE, startupinfo=startupinfo, text=True)
                self.processes[command] = process
                self.string_monitor_active = 1
                
                # Start mover process in another thread
                string_thread = threading.Thread(target=self.string_mover, name = "string_mover_thread", args=(process,))
                string_thread.daemon = True
                string_thread.start()
                #self.string_mover(process)
                
                # Set label text
                label.configure(text=self.text_running, text_color=self.text_color_running)
                # Disable engine combobox
                self.combo_engine.configure(state="disabled")
            except OSError as e:
                label.configure(text=self.text_err, text_color=self.text_color_err)
                print(e)
                
    def string_mover(self, proc):

        if proc.stdout is None:
            raise ValueError("Subprocess must be created with stdout=subprocess.PIPE")

        print("string mover active...")

        # init vars
        source_string_file = ""

        while self.string_monitor_active == 1:
            line = proc.stdout.readline()
            print(line)
            if not line:
                break  # EOF
            decoded_line = line.strip()
            #if "importing" in decoded_line:
            if "importing" in decoded_line and ".txt" in decoded_line:
            
                # store Tool's print output into a variable for use later
                source_string_file = decoded_line
                #print("DEBUG:" + source_string_file)

            # Wait until import is finished
            if "Import time:" in decoded_line and source_string_file != "":
                self.move_multilingual_file(source_string_file)
                source_string_file = ""

            continue
        
            
    def move_multilingual_file(self, input_string):
        # Extract the file path within single quotes
        match = re.search(r"'([^']+)'", input_string)
        if not match:
            print("No valid file path found in input.")
            return

        relative_txt_path = match.group(1)
        txt_filename = os.path.basename(relative_txt_path)
        name_without_ext = os.path.splitext(txt_filename)[0]

        # Construct source and destination paths
        source_path = os.path.join("tags", name_without_ext + ".multilingual_unicode_string_list")
        
        # Replace "data" with "tags" in the directory path and append the new file name
        destination_dir = os.path.dirname(relative_txt_path).replace("data", "tags", 1)
        destination_path = os.path.join(destination_dir, name_without_ext + ".multilingual_unicode_string_list")

        # Create destination directory if it doesn't exist
        os.makedirs(destination_dir, exist_ok=True)

        # Move (overwrite) the file
        try:
            shutil.move(source_path, destination_path)
            print(f"Moved to {destination_path}")
        except FileNotFoundError:
            print(f"Source file does not exist: {source_path}")
        except Exception as e:
            print(f"Error moving file: {e}")
            


    def close_processes(self):
        for command, process in self.processes.items():
            process.terminate()
        #subprocess.Popen("tool monitor-strings").terminate()
        self.master.destroy()

class TextRedirector(object):
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert("end", message)
        self.remove_consecutive_newlines()
        self.text_widget.see("end")
        
    def remove_consecutive_newlines(self):
        content = self.text_widget.get("1.0", "end-1c")     # Get all text, excluding the final newline
        cleaned = re.sub(r'\n{2,}', '\n', content)          # Replace 2+ newlines with a single newline

        self.text_widget.delete("1.0", "end")               # Clear the widget
        self.text_widget.insert("1.0", cleaned)             # Insert cleaned text

    def flush(self):
        pass

if __name__ == "__main__":
    root = ctk.CTk()
    app = MonitorMasterApp(root)

    
    def on_closing():
        app.close_processes()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.resizable(width=False, height=False)
    root.mainloop()
