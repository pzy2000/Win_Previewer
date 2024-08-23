# Win_Previewer

[中文](README_CN.md)

Win_Previewer is a Python-based tool that allows you to monitor and manage multiple running Windows applications by displaying real-time thumbnails of active windows. This tool is designed for developers and power users who need to keep track of multiple applications simultaneously, with features such as blacklist management and window activation.

## Features

- **Real-Time Thumbnails**: Displays live thumbnails of all active windows.
- **Window Activation**: Click on a thumbnail to bring the corresponding window to the foreground.
- **Blacklist Management**: Exclude specific windows from being displayed by adding them to a blacklist.
- **Dynamic Updates**: Automatically updates the blacklist every 5 seconds to reflect changes.
- **Custom Refresh Rate**: Set a custom refresh rate for updating thumbnails (default is 100 ms).
- **Effect Diagram**:
- ![img.png](res%2Fimg.png)

## Installation

To install the required dependencies, run:

```bash
pip install pillow pywin32 numpy
```

## Usage

1. Clone the repository and navigate to the directory.
2. Run the `main.py` script:
   ```bash
   python main.py
   ```
3. Set the refresh rate in the prompt (default is 100 ms).
4. The application will display thumbnails of active windows. Click on a thumbnail to activate the corresponding window.
5. Manage the blacklist by clicking the "Blacklist Management" button at the bottom of the window.

## Configuration

- **Blacklist**: The `blacklist.txt` file in the same directory allows you to predefine windows that should be excluded from the thumbnails. The file is updated automatically when you manage the blacklist through the GUI.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

This README provides an overview of the project, including its features, installation instructions, usage guidelines, and how to contribute.