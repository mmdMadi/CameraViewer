# UI Files for CCTV Multi-Camera Viewer

This directory contains Qt Designer (.ui) files for the CCTV Multi-Camera Viewer application.

## 📁 **UI Files Included**

### **main_window.ui**
- Main application window layout
- Menu bar with File, View, Settings menus
- Toolbar with camera control actions
- Central widget with scroll area for camera grid
- Status bar for application feedback

### **add_camera_dialog.ui**
- Dialog for adding/editing cameras
- Basic settings: Name, URL, Description
- Video settings: FPS, Resolution, Stream Mode
- Connection settings: Timeout, Retry Count, Auto-start
- URL examples and test connection button

### **settings_dialog.ui**
- Comprehensive settings dialog with tabs
- Appearance: Theme, UI options, window opacity
- Display: Grid layout, video performance settings
- Network: Connection timeouts, advanced options
- General: Startup behavior, system tray integration

### **camera_widget.ui**
- Individual camera display widget
- Header with camera name and control buttons
- Video display area with fullscreen support
- Status and performance information labels

### **fullscreen_viewer.ui**
- Fullscreen video viewer window
- Overlay control bar with camera controls
- Full-screen video display
- Status overlay with keyboard shortcuts

## 🛠️ **Using Qt Designer**

### **Opening Files**
1. Install Qt Designer (comes with Qt or PySide6 development tools)
2. Open Qt Designer
3. File → Open → Select any .ui file from this directory
4. Edit the interface visually

### **Key Features to Edit**
- **Layouts**: Modify spacing, margins, alignment
- **Widgets**: Add/remove buttons, labels, inputs
- **Properties**: Change text, tooltips, size constraints
- **Stylesheets**: Modify appearance and colors
- **Connections**: Link signals to slots

## 🔄 **Converting to Python**

### **Automatic Conversion**
Run the conversion script:
```bash
python convert_ui.py
```

### **Manual Conversion**
Convert individual files:
```bash
pyside6-uic ui/main_window.ui -o src/ui/main_window_ui.py
pyside6-uic ui/add_camera_dialog.ui -o src/ui/add_camera_dialog_ui.py
```

### **Using Converted Files**
```python
from src.ui.main_window_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
```

## 📐 **Design Guidelines**

### **Layout Principles**
- Use proper layouts (QVBoxLayout, QHBoxLayout, QGridLayout)
- Set appropriate spacing and margins
- Use size policies and constraints
- Maintain consistent alignment

### **Widget Naming**
- Use descriptive names: `cameraNameEdit`, `startButton`
- Follow camelCase convention
- Include widget type in name: `Button`, `Label`, `Edit`

### **Responsive Design**
- Set minimum/maximum sizes where appropriate
- Use stretch factors in layouts
- Consider different screen sizes
- Test with various window sizes

### **Accessibility**
- Set proper tab order
- Add tooltips for buttons and controls
- Use clear, descriptive labels
- Ensure keyboard navigation works

## 🎨 **Styling**

### **Theme Support**
The UI files include basic styling that works with both light and dark themes:
- Neutral colors that adapt to theme
- Proper contrast ratios
- Consistent spacing and sizing

### **Custom Stylesheets**
Some widgets include inline stylesheets for:
- Video display areas (black background)
- Status labels (smaller font, muted colors)
- Control buttons (consistent sizing)

## 🔧 **Customization Tips**

### **Adding New Widgets**
1. Drag widget from toolbox
2. Set object name and properties
3. Add to appropriate layout
4. Connect signals if needed

### **Modifying Layouts**
1. Select layout in Object Inspector
2. Adjust spacing, margins in Property Editor
3. Change layout type if needed
4. Test with different content

### **Creating Dialogs**
1. Start with QDialog base
2. Add QVBoxLayout as main layout
3. Group related controls in QGroupBox
4. Add button box at bottom
5. Set up accept/reject connections

## 📱 **Responsive Features**

### **Main Window**
- Resizable with minimum size constraints
- Scroll area for camera grid overflow
- Toolbar can be hidden/shown
- Status bar provides feedback

### **Dialogs**
- Modal dialogs with proper sizing
- Scroll areas for long content
- Tab widgets for organization
- Consistent button layouts

### **Camera Widgets**
- Fixed aspect ratios
- Scalable video display
- Overlay controls
- Performance indicators

The UI files provide a solid foundation for the CCTV viewer interface and can be easily customized using Qt Designer!