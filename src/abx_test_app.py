import tkinter as tk
from tkinter import ttk, messagebox
import soundfile as sf
import random
from scipy.stats import binomtest
import os
from collections import defaultdict
from .audio_player import AudioPlayer
import sounddevice as sd

class ABXTestApp:
    def __init__(self, master, audio_pairs):
        self.master = master
        self.audio_pairs = audio_pairs
        self.player = AudioPlayer()
        self.current_x_path = None
        self.current_x_is_a = None
        self.total_tests = 0
        self.correct_answers = 0
        
        self.setup_ui()
        self.new_test()
        self.update_playback_status()

    def setup_ui(self):
        self.master.title("ABX Audio Test")
        
        # Device selection
        device_frame = ttk.LabelFrame(self.master, text="WASAPI Output Device")
        device_frame.grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky="ew")
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(device_frame, textvariable=self.device_var, state="readonly")
        self.device_combo.grid(column=0, row=0, padx=5, pady=5, sticky="ew")
        
        # Populate devices (WASAPI only)
        devices = AudioPlayer.get_wasapi_devices()
        device_names = [dev['name'] for dev in devices]  # Only show device names for WASAPI
        self.device_combo['values'] = device_names
        
        # Set current device
        current_device = self.player.device_info['name']
        self.device_combo.set(current_device)
        
        # Bind device change event
        self.device_combo.bind('<<ComboboxSelected>>', self.on_device_change)
        
        # Playback controls
        controls_frame = ttk.Frame(self.master)
        controls_frame.grid(column=0, row=1, columnspan=3, padx=5, pady=5)
        
        self.btn_play_a = ttk.Button(controls_frame, text="Play A", command=lambda: self.play('A'))
        self.btn_play_a.grid(column=0, row=0, padx=5)
        
        self.btn_play_x = ttk.Button(controls_frame, text="Play X", command=lambda: self.play('X'))
        self.btn_play_x.grid(column=1, row=0, padx=5)

        self.btn_play_b = ttk.Button(controls_frame, text="Play B", command=lambda: self.play('B'))
        self.btn_play_b.grid(column=2, row=0, padx=5)          

        self.btn_stop = ttk.Button(controls_frame, text="Stop", command=lambda: self.stop())
        self.btn_stop.grid(column=1, row=1, pady=5)

        # Response buttons
        response_frame = ttk.Frame(self.master)
        response_frame.grid(column=0, row=2, columnspan=3, padx=5, pady=5)
        
        self.btn_a = ttk.Button(response_frame, text="X = A", command=lambda: self.respond(True), width=10)
        self.btn_a.grid(column=0, row=0, padx=5)  
        
        self.btn_b = ttk.Button(response_frame, text="X = B", command=lambda: self.respond(False), width=10)
        self.btn_b.grid(column=2, row=0, padx=5)  

        # Statistics
        stats_frame = ttk.Frame(self.master)
        stats_frame.grid(column=0, row=3, columnspan=3, padx=5, pady=5)
        
        self.stats_label = ttk.Label(stats_frame, text="Правильных ответов: 0/0")
        self.stats_label.grid(column=0, row=0, pady=2)  
        
        self.pval_label = ttk.Label(stats_frame, text="p-value: N/A")
        self.pval_label.grid(column=0, row=1, pady=2)  

    def on_device_change(self, event):
        selected_device = self.device_var.get()
        devices = AudioPlayer.get_wasapi_devices()
        for dev in devices:
            if dev['name'] == selected_device:
                self.player.set_device(dev['id'])
                break

    def new_test(self):
        pair = random.choice(self.audio_pairs)
        self.current_pair = pair
        self.current_x_is_a = random.choice([True, False])
        self.current_x_path = pair['A'] if self.current_x_is_a else pair['B']

    def stop(self):
        if self.player.is_playing:
            self.player.stop()

    def play(self, target):
        try:
            if target == 'A':
                file_path = self.current_pair['A']
            elif target == 'B':
                file_path = self.current_pair['B']
            else:
                file_path = self.current_x_path

            self.btn_stop.config(text=f"Stop {target}")
            
            data, fs = sf.read(file_path, always_2d=True)
            self.player.play(data, fs)
            self.toggle_buttons(False)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка воспроизведения: {str(e)}")
            self.toggle_buttons(True)

    def update_playback_status(self):
        if not self.player.is_playing:
            self.toggle_buttons(True)
        self.master.after(100, self.update_playback_status)

    def toggle_buttons(self, enabled):
        state = tk.NORMAL if enabled else tk.DISABLED
        for btn in [self.btn_play_a, self.btn_play_b, self.btn_play_x, self.btn_a, self.btn_b]:
            btn.config(state=state)

    def respond(self, user_choice):
        if self.player.is_playing:
            return
            
        is_correct = (user_choice == self.current_x_is_a)
        self.total_tests += 1
        self.correct_answers += 1 if is_correct else 0
        
        self.update_stats()
        self.new_test()

    def update_stats(self):
        self.stats_label.config(text=f"Правильных ответов: {self.correct_answers}/{self.total_tests}")
        
        if self.total_tests > 0:
            pval = binomtest(self.correct_answers, self.total_tests, 0.5, alternative='greater')
            self.pval_label.config(text=f"p-value: {pval.pvalue:.4f}")

def find_audio_pairs(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.wav')]
    pairs = defaultdict(dict)
    
    for f in files:
        if '_A.wav' in f:
            base = f.split('_A.wav')[0]
            pairs[base]['A'] = os.path.join(folder_path, f)
        elif '_B.wav' in f:
            base = f.split('_B.wav')[0]
            pairs[base]['B'] = os.path.join(folder_path, f)
    
    return [v for v in pairs.values() if 'A' in v and 'B' in v] 