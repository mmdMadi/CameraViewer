# CameraViewer — Multi-Camera CCTV Viewer / نمایشگر چند دوربین مداربسته

| 🇬🇧 English | 🇮🇷 فارسی |
| :--- | :--- |
| [English](#english) | [فارسی](#persian) |

---

## English

A modern, cross-platform desktop application for viewing multiple CCTV camera streams simultaneously. Built with **PySide6** and **OpenCV**, featuring a clean interface with light/dark theme support.

### Features

- **Multi-Camera Support** — view multiple camera streams in a customizable grid layout
- **Modern GUI** — clean, responsive interface built with PySide6
- **Theme Support** — switch between light and dark themes
- **Stream Protocols** — RTSP, HTTP, MJPEG, and USB cameras
- **Real-time Streaming** — low-latency video streaming with OpenCV
- **Camera Management** — easily add, edit, and remove cameras
- **Connection Testing** — test a camera connection before adding it
- **Auto-reconnect** — automatic reconnection on stream failures
- **Snapshots & Recording** — save still images and record streams
- **System Tray** — minimize to tray and keep watching

### Requirements

- Python 3.8+ (developed and tested with 3.12.13)
- PySide6 6.5.0+
- OpenCV 4.8.0+
- Requests 2.31.0+

### Installation

```bash
# 1. Clone the repository
git clone git@github.com:mmdMadi/CameraViewer.git
cd CameraViewer

# 2. Create and activate a virtual environment (Python 3.12.13 recommended)
python3.12 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

### Usage

1. **Adding cameras** — click **Add Camera** in the toolbar (or `Ctrl+N`), enter a name and stream URL, and test the connection before saving.
2. **Managing cameras** — right-click any camera tile for a context menu; edit, remove, or start/stop individual streams.
3. **Fullscreen** — press `F11` (or double-click a tile) to view a single camera fullscreen.
4. **Settings** — `Ctrl+,` opens preferences: appearance (theme), display (grid columns, aspect ratio), network (timeouts, retries), and general options (auto-start, logging).
5. **Shortcuts** — `Ctrl+N` add camera · `F11` fullscreen · `Ctrl+,` settings · `Ctrl+Q` quit.

### Supported Camera URLs

```
# RTSP
rtsp://username:password@192.168.1.100:554/stream1

# HTTP / MJPEG
http://192.168.1.100:8080/video
http://192.168.1.100/mjpg/video.mjpg

# USB camera (device index)
0   # first USB camera
1   # second USB camera
```

### Configuration

- **Camera list** — saved in `cameras_config.json` in the project directory.
- **Application settings** — stored via Qt's `QSettings` system.

### Project Structure

```
src/
├── main_window.py        # Main application window
├── camera_grid.py        # Grid layout for cameras
├── camera_widget.py      # Individual camera display widget
├── camera_manager.py     # Camera management logic
├── settings_manager.py   # Settings persistence
├── theme_manager.py      # Theme management
├── settings_dialog.py    # Settings configuration dialog
├── add_camera_dialog.py  # Add/edit camera dialog
├── snapshot_manager.py   # Snapshot capture
├── recording_manager.py  # Stream recording
└── stream_optimizer.py   # Stream performance tuning
```

More details: [doc/README.md](doc/README.md) · [doc/STREAM_OPTIMIZATION_GUIDE.md](doc/STREAM_OPTIMIZATION_GUIDE.md)

---

## فارسی

اپلیکیشن رومیزی مدرن و چندسکویی برای مشاهدهٔ همزمان چند جریان ویدیویی دوربین مداربسته. این برنامه با **PySide6** و **OpenCV** ساخته شده و رابط کاربری تمیزی با پشتیبانی از تم روشن/تاریک دارد.

### امکانات

- **پشتیبانی از چند دوربین** — مشاهدهٔ همزمان چند دوربین در چیدمان شبکه‌ای قابل تنظیم
- **رابط کاربری مدرن** — رابط تمیز و واکنش‌گرا مبتنی بر PySide6
- **پشتیبانی از تم** — جابه‌جایی بین تم روشن و تاریک
- **پروتکل‌های استریم** — پشتیبانی از RTSP، HTTP، MJPEG و دوربین‌های USB
- **استریم بی‌درنگ** — پخش ویدیو با تأخیر پایین با OpenCV
- **مدیریت دوربین** — افزودن، ویرایش و حذف آسان دوربین‌ها
- **آزمایش اتصال** — تست اتصال دوربین پیش از ذخیره
- **اتصال مجدد خودکار** — اتصال مجدد خودکار هنگام قطعی
- **عکس فوری و ضبط** — ذخیرهٔ قاب و ضبط جریان‌ها
- **سینی سیستم (System Tray)** — کوچک‌سازی به سینی و ادامهٔ پایش

### پیش‌نیازها

- پایتون 3.8 به بالا (توسعه و تست با 3.12.13)
- PySide6 نسخهٔ 6.5.0 به بالا
- OpenCV نسخهٔ 4.8.0 به بالا
- Requests نسخهٔ 2.31.0 به بالا

### نصب

```bash
# 1. کلون کردن مخزن
git clone git@github.com:mmdMadi/CameraViewer.git
cd CameraViewer

# 2. ساخت و فعال‌سازی محیط مجازی (پایتون 3.12.13 پیشنهاد می‌شود)
python3.12 -m venv .venv
source .venv/bin/activate

# 3. نصب وابستگی‌ها
pip install -r requirements.txt

# 4. اجرای برنامه
python main.py
```

### نحوهٔ استفاده

1. **افزودن دوربین** — روی **Add Camera** در نوار ابزار کلیک کنید (یا `Ctrl+N`)، نام و آدرس استریم را وارد کنید و پیش از ذخیره، اتصال را تست کنید.
2. **مدیریت دوربین‌ها** — روی هر کاشی دوربین کلیک راست کنید؛ ویرایش، حذف یا شروع/توقف استریم هر دوربین.
3. **تمام‌صفحه** — برای مشاهدهٔ یک دوربین به‌صورت تمام‌صفحه، `F11` را بزنید (یا روی کاشی دوبار کلیک کنید).
4. **تنظیمات** — با `Ctrl+,` به تنظیمات بروید: ظاهر (تم)، نمایش (تعداد ستون‌ها، نسبت ابعاد)، شبکه (مهلت زمانی، تلاش مجدد) و گزینه‌های عمومی (شروع خودکار، ورودنگاری).
5. **میان‌برهای صفحه‌کلید** — `Ctrl+N` افزودن دوربین · `F11` تمام‌صفحه · `Ctrl+,` تنظیمات · `Ctrl+Q` خروج.

### آدرس‌های پشتیبانی‌شدهٔ دوربین

```
# RTSP
rtsp://username:password@192.168.1.100:554/stream1

# HTTP / MJPEG
http://192.168.1.100:8080/video
http://192.168.1.100/mjpg/video.mjpg

# دوربین USB (شاخص دستگاه)
0   # اولین دوربین USB
1   # دومین دوربین USB
```

### پیکربندی

- **فهرست دوربین‌ها** — در فایل `cameras_config.json` در پوشهٔ پروژه ذخیره می‌شود.
- **تنظیمات برنامه** — از طریق سامانهٔ `QSettings` کیوت ذخیره می‌شود.

### ساختار پروژه

```
src/
├── main_window.py        # پنجرهٔ اصلی برنامه
├── camera_grid.py        # چیدمان شبکه‌ای دوربین‌ها
├── camera_widget.py      # ویجت نمایش هر دوربین
├── camera_manager.py     # منطق مدیریت دوربین‌ها
├── settings_manager.py   # ذخیرهٔ تنظیمات
├── theme_manager.py      # مدیریت تم
├── settings_dialog.py    # گفت‌وگوی تنظیمات
├── add_camera_dialog.py  # گفت‌وگوی افزودن/ویرایش دوربین
├── snapshot_manager.py   # عکس فوری
├── recording_manager.py  # ضبط استریم
└── stream_optimizer.py   # بهینه‌سازی کارایی استریم
```

جزئیات بیشتر: [doc/README.md](doc/README.md) · [doc/STREAM_OPTIMIZATION_GUIDE.md](doc/STREAM_OPTIMIZATION_GUIDE.md)
