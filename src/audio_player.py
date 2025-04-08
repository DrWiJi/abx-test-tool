import sounddevice as sd
import numpy as np
from tkinter import messagebox

class AudioPlayer:
    def __init__(self):
        self.stream = None
        self.current_data = None
        self.pos = 0
        self.is_playing = False
        self.device_id = None
        self.device_info = None
        
        # Find WASAPI API index
        self.wasapi_api = None
        for i, api in enumerate(sd.query_hostapis()):
            if api['name'] == 'Windows WASAPI':
                self.wasapi_api = i
                break
        
        if self.wasapi_api is None:
            raise RuntimeError("WASAPI API not found")
            
        # Find WASAPI devices
        self.wasapi_devices = [idx for idx, dev in enumerate(sd.query_devices()) 
                             if dev['hostapi'] == self.wasapi_api and dev['max_output_channels'] > 0]
        
        if not self.wasapi_devices:
            raise RuntimeError("No WASAPI output devices found.")
        
        # Use the first WASAPI device by default
        self.set_device(self.wasapi_devices[0])

    @staticmethod
    def get_available_devices(wasapi_only=False):
        devices = []
        for i, dev in enumerate(sd.query_devices()):
            if dev['max_output_channels'] > 0:  # Only output devices
                if wasapi_only:
                    hostapi = sd.query_hostapis(dev['hostapi'])
                    if hostapi['name'] != 'Windows WASAPI':
                        continue
                devices.append({
                    'id': i,
                    'name': dev['name'],
                    'hostapi': sd.query_hostapis(dev['hostapi'])['name']
                })
        return devices

    @staticmethod
    def get_wasapi_devices():
        return AudioPlayer.get_available_devices(wasapi_only=True)

    def set_device(self, device_id):
        self.device_id = device_id
        self.device_info = sd.query_devices(device_id)
        print(f"\nUsing device: {self.device_info['name']}")
        print(f"Device details: {self.device_info}")

    def callback(self, outdata, frames, time, status):
        if status:
            print(status)
        chunk = self.current_data[self.pos:self.pos + frames]
        if len(chunk) < frames:
            chunk = np.pad(chunk, (0, frames - len(chunk)), mode='constant')
            self.pos += frames
            raise sd.CallbackStop
        outdata[:] = chunk
        self.pos += frames

    def play(self, data, fs):
        self.stop()
        self.current_data = data
        self.pos = 0
        try:
            self.stream = sd.OutputStream(
                device=self.device_id,
                samplerate=fs,
                channels=1 if len(data.shape) == 1 else data.shape[1],
                callback=self.callback,
                finished_callback=self.play_finished,
                blocksize=1024,
                latency='low'
            )
            self.stream.start()
            self.is_playing = True
        except sd.PortAudioError as e:
            error_msg = f"Error playing audio: {str(e)}"
            messagebox.showerror("Playback Error", error_msg)
            self.is_playing = False

    def stop(self):
        if self.stream and self.stream.active:
            self.stream.stop()
            self.stream.close()
        self.is_playing = False

    def play_finished(self):
        self.is_playing = False