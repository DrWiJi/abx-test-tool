# ABX Audio Test Tool

A Python-based ABX testing tool for audio comparison, specifically designed for Windows with WASAPI support.

## Features

- ABX testing interface for audio comparison
- WASAPI audio output support
- Real-time statistics and p-value calculation
- Simple and intuitive user interface
- Support for multiple audio device selection

## Requirements

- Python 3.8 or higher
- Windows operating system
- WASAPI-compatible audio device

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/abx-test-tool.git
cd abx-test-tool
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Prepare your audio files:
   - Place your audio files in the `audio` directory
   - Name your files with `_A.wav` and `_B.wav` suffixes (e.g., `test1_A.wav`, `test1_B.wav`)

2. Run the application:
```bash
python main.py
```

3. Using the ABX Test:
   - Select your WASAPI output device from the dropdown
   - Use the "Play A", "Play B", and "Play X" buttons to listen to the samples
   - Choose "X = A" or "X = B" to indicate which sample you think X matches
   - The statistics will update automatically

## Project Structure

```
abx-test-tool/
├── src/
│   ├── __init__.py
│   ├── audio_player.py
│   ├── abx_test_app.py
│   └── main.py
├── audio/
│   └── (your audio files)
├── requirements.txt
├── LICENSE
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- [sounddevice](https://python-sounddevice.readthedocs.io/) for audio playback
- [soundfile](https://pysoundfile.readthedocs.io/) for audio file handling
- [scipy](https://www.scipy.org/) for statistical calculations 