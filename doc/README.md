# CCTV Multi-Camera Viewer

A modern, cross-platform application for viewing multiple CCTV camera streams simultaneously. Built with PySide6 and OpenCV, featuring a clean interface with light/dark theme support.

## Features

- **Multi-Camera Support**: View multiple camera streams in a customizable grid layout
- **Modern GUI**: Clean, responsive interface built with PySide6
- **Theme Support**: Switch between light and dark themes
- **Stream Protocols**: Support for RTSP, HTTP, MJPEG, and USB cameras
- **Real-time Streaming**: Low-latency video streaming with OpenCV
- **Camera Management**: Easy add, edit, and remove cameras
- **Settings**: Comprehensive settings for appearance, display, network, and general preferences
- **Connection Testing**: Test camera connections before adding them
- **Auto-reconnect**: Automatic reconnection on stream failures

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd cctv-viewer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

## Requirements

- Python 3.8+
- PySide6 6.5.0+
- OpenCV 4.8.0+
- Requests 2.31.0+

## Supported Camera Types

### RTSP Cameras
```
rtsp://username:password@192.168.1.100:554/stream1
```

### HTTP/MJPEG Streams
```
http://192.168.1.100:8080/video
http://192.168.1.100/mjpg/video.mjpg
```

### USB Cameras
```
0  (for first USB camera)
1  (for second USB camera)
```

## Usage

1. **Adding Cameras**:
   - Click "Add Camera" in the toolbar or use File → Add Camera
   - Enter camera name and stream URL
   - Test the connection before saving
   - Configure timeout and retry settings

2. **Managing Cameras**:
   - Right-click on any camera for context menu
   - Edit camera settings or remove cameras
   - Start/stop individual streams

3. **Settings**:
   - Access via Settings → Preferences
   - Configure appearance (light/dark theme)
   - Adjust display settings (grid columns, aspect ratio)
   - Set network parameters (timeouts, retries)
   - General preferences (auto-start, logging)

4. **Keyboard Shortcuts**:
   - `Ctrl+N`: Add new camera
   - `F11`: Toggle fullscreen
   - `Ctrl+,`: Open settings
   - `Ctrl+Q`: Quit application

## Configuration

Camera configurations are automatically saved to `cameras_config.json` in the application directory. Application settings are stored using Qt's QSettings system.

## Troubleshooting

### Common Issues

1. **Camera won't connect**:
   - Verify the stream URL is correct
   - Check network connectivity
   - Ensure camera supports the protocol
   - Try different timeout values

2. **Poor performance**:
   - Reduce FPS limit in display settings
   - Lower buffer size
   - Enable hardware acceleration if available

3. **Stream keeps disconnecting**:
   - Increase connection timeout
   - Adjust reconnect interval
   - Check network stability

## Development

The application is structured as follows:

```
src/
├── main_window.py      # Main application window
├── camera_grid.py      # Grid layout for cameras
├── camera_widget.py    # Individual camera display widget
├── camera_manager.py   # Camera management logic
├── settings_manager.py # Settings persistence
├── theme_manager.py    # Theme management
├── settings_dialog.py  # Settings configuration dialog
└── add_camera_dialog.py # Add/edit camera dialog
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and feature requests, please use the GitHub issue tracker.