import tkinter as tk
from .abx_test_app import ABXTestApp, find_audio_pairs

def main():
    samples_folder = 'samples'
    audio_pairs = find_audio_pairs(samples_folder)
    
    if not audio_pairs:
        raise ValueError(f"No valid audio pairs found in {samples_folder}")
    
    root = tk.Tk()
    app = ABXTestApp(root, audio_pairs)
    root.geometry("300x400")
    root.mainloop()

if __name__ == "__main__":
    main() 