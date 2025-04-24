import os

def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
#from PIL import ImageTk, Image
import subprocess

class MonitorMasterApp:
    def __init__(self, master):
        self.master = master
        master.title("Blam Monitor Master")
        master.configure(background='#000f24')
        self.font_style = ("Conduit ITC", 20)
        
        # WINDOW SIZE
        self.window_width = 580
        self.window_height = 610
        
        self.text_color_unavailable = '#60646e'
        self.text_color_standby = '#7eb3de'
        self.text_color_running = '#73de9a'
        self.text_color_err = '#de7373'
        
        self.text_unavailable = 'Unavailable in this engine'
        self.text_standby = 'Standing by...'
        self.text_running = 'RUNNING'
        self.text_err = 'ERROR (printed to console)'
        
        self.button_bg_color = '#26394f'
        self.button_fg_color = '#8eaec4'
        self.button_disabled_bg_color = '#171f29'
        self.button_disabled_fg_color = '#37454f'

        self.processes = {}

        self.buttons = [
            ("Bitmaps", "tool monitor-bitmaps"),
            ("Bitmaps (Data and Tags)", "tool monitor-data-and-tags-bitmaps"),
            ("Models", "tool monitor-models"),
            ("Models (Draft)", "tool monitor-models-draft"),
            ("Strings", "tool monitor-strings"),
            ("Structure (BSP)", "tool monitor-structures")
        ]

        # Not bothering with BG image anymore, if you want this added back ask me
        #background_image = Image.open(resource_path("res_BMM/bg.png"))
        #background_image = background_image.resize((self.window_width, self.window_height))
        #self.bg_image = ImageTk.PhotoImage(background_image)
        #self.bg_label = tk.Label(master, image=self.bg_image)
        #self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # TITLE
        title_label = tk.Label(master, text="Blam Monitor Master", font=("Denmark", 24, 'bold'), fg='#8eaec4', bg='#000f24')
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10), sticky="n")
        
        # LABEL - Engine
        title_label_engine = tk.Label(master, text="Engine:", font=("Conduit ITC", 20, 'bold'), fg='#8eaec4', bg='#000f24')
        title_label_engine.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="e")
        
        # COMBO - Engine
        engines = ["Halo 2", "Halo 3/ODST", "Halo: Reach", "Halo 4"]
        self.combo_engine = ttk.Combobox(master, values=engines, width=10, state="readonly", font=("Conduit ITC", 16))
        self.combo_engine.set("<SELECT>")
        self.combo_engine.grid(row=1, column=1, padx=(0, 20), pady=10, sticky="w")
        #Style
        combostyle = ttk.Style()
        combostyle.theme_create('combostyle', parent='alt',
                                settings = {'TCombobox':
                                            {'configure':
                                            {'selectbackground': '#000f24',
                                            'fieldbackground': '#000f24',
                                            'background': '#000f24',
                                            'foreground': self.text_color_standby,
                                            'text': '#FFFFFF'
                                            }}}
                                )
        combostyle.theme_use('combostyle')
        self.combo_engine.bind('<<ComboboxSelected>>', self.engine_selected)
        
        
        # BUTTONS
        '''button_widgets = []
        for i, (text, command) in enumerate(self.buttons):
            button = tk.Button(master, text=text, command=lambda cmd=command: self.toggle_process(cmd),
                               bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
            button.grid(row=i+2, column=0, padx=(20, 10), pady=10, sticky="e")
            status_label = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
            status_label.grid(row=i+2, column=1, padx=(0, 20), pady=10, sticky="w")
            self.buttons[i] = (text, command, button, status_label)'''
            
        self.button_bitmaps = tk.Button(master, text="Bitmaps", command=lambda cmd="tool monitor-bitmaps": self.toggle_process(cmd, self.status_label_bitmaps), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_bitmaps.grid(row=0+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_bitmaps = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_bitmaps.grid(row=0+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[0] = ("Bitmaps", "tool monitor-bitmaps", self.button_bitmaps, self.status_label_bitmaps)
        
        self.button_bitmaps_data_and_tags = tk.Button(master, text="Bitmaps (Data and Tags)", command=lambda cmd="tool monitor-data-and-tags-bitmaps": self.toggle_process(cmd, self.status_label_bitmaps_data_and_tags), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_bitmaps_data_and_tags.grid(row=1+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_bitmaps_data_and_tags = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_bitmaps_data_and_tags.grid(row=1+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[1] = ("Bitmaps (Data and Tags)", "tool monitor-data-and-tags-bitmaps", self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
        
        self.button_models = tk.Button(master, text="Models", command=lambda cmd="tool monitor-models": self.toggle_process(cmd, self.status_label_models), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_models.grid(row=2+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_models = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_models.grid(row=2+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[2] = ("Models", "tool monitor-models", self.button_models, self.status_label_models)
        
        self.button_models_draft = tk.Button(master, text="Models (Draft)", command=lambda cmd="tool monitor-models-draft": self.toggle_process(cmd, self.status_label_models_draft), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_models_draft.grid(row=3+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_models_draft = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_models_draft.grid(row=3+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[3] = ("Models (Draft)", "tool monitor-models-draft", self.button_models_draft, self.status_label_models_draft)
        
        self.button_strings = tk.Button(master, text="Strings", command=lambda cmd="tool monitor-strings": self.toggle_process(cmd, self.status_label_strings), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_strings.grid(row=4+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_strings = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_strings.grid(row=4+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[4] = ("Strings", "tool monitor-strings", self.button_strings, self.status_label_strings)
        
        self.button_structures = tk.Button(master, text="Structures (BSP)", command=lambda cmd="tool monitor-structures": self.toggle_process(cmd, self.status_label_structures), bg=self.button_bg_color, fg=self.button_fg_color, font=self.font_style)
        self.button_structures.grid(row=5+2, column=0, padx=(20, 10), pady=10, sticky="e")
        self.status_label_structures = tk.Label(master, text=self.text_standby, fg=self.text_color_standby, bg='#000f24', font=("Conduit ITC", 16))
        self.status_label_structures.grid(row=5+2, column=1, padx=(0, 20), pady=10, sticky="w")
        self.buttons[5] = ("Structures", "tool monitor-structures", self.button_structures, self.status_label_structures)


        master.geometry(str(self.window_width) + "x" + str(self.window_height))
        
        # Initially set all buttons to disabled (so user can select engine)
        self.disable_button(self.button_bitmaps, self.status_label_bitmaps)
        self.disable_button(self.button_bitmaps_data_and_tags, self.status_label_bitmaps_data_and_tags)
        self.disable_button(self.button_models, self.status_label_models)
        self.disable_button(self.button_models_draft, self.status_label_models_draft)
        self.disable_button(self.button_strings, self.status_label_strings)
        self.disable_button(self.button_structures, self.status_label_structures)

    def disable_button(self, button, label):
        # Disable given button
        button.config(bg=self.button_disabled_bg_color)
        button.config(fg=self.button_disabled_fg_color)
        button.config(state="disabled")
        #Set label text
        label.config(text=self.text_unavailable, fg=self.text_color_unavailable)
        
        
    def enable_button(self, button, label):
        # Enable given button
        button.config(bg=self.button_bg_color)
        button.config(fg=self.button_fg_color)
        button.config(state="normal")
        label.config(text=self.text_standby, fg=self.text_color_standby)

    def engine_selected(self, event):
       # self.combo_engine - ttk.Combobox()
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
            self.log_to_console(f"Stopping process: {command}")
            self.processes[command].terminate()
            del self.processes[command]
            label.config(text=self.text_standby, fg=self.text_color_standby)
            # TODO: Enable engine combobox if no processes are running
            if not self.processes:
                self.combo_engine.config(state="readonly")
            
        else:
            self.log_to_console(f"Starting process: {command}")
            try:
                process = subprocess.Popen(command.split())
                self.processes[command] = process
                label.config(text=self.text_running, fg=self.text_color_running)
                # Disable engine combobox
                self.combo_engine.config(state="disabled")
            except OSError as e:
                label.config(text=self.text_err, fg=self.text_color_err)
                print(e)

    def log_to_console(self, message):
        print (message)
        pass

    def close_processes(self):
        for command, process in self.processes.items():
            process.terminate()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MonitorMasterApp(root)
    
    def on_closing():
        app.close_processes()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.resizable(width=False, height=False)
    root.mainloop()
