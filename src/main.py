import tkinter as tk
from tkinter import messagebox
import os
from .abx_test_app import ABXTestApp, find_audio_pairs

def main():
    samples_folder = 'samples'
    
    # Check if the samples folder exists
    if not os.path.exists(samples_folder):
        # Create root window to show error message
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Error", f"The '{samples_folder}' folder is missing. Please create it and add audio files.")
        return
    
    try:
        audio_pairs = find_audio_pairs(samples_folder)
        
        if not audio_pairs:
            # Create root window to show error message
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            messagebox.showerror("Error", f"No valid audio pairs found in '{samples_folder}' folder.\nPlease add audio files with '_A.wav' and '_B.wav' suffixes.")
            return
        
        root = tk.Tk()
        app = ABXTestApp(root, audio_pairs)
        root.geometry("300x400")
        root.mainloop()
    except Exception as e:
        # Handle any other unexpected errors
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main() 