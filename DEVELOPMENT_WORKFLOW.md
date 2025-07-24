# วิธีทดสอบ QGIS Plugin อย่างรวดเร็วในระหว่างการพัฒนา

## วิธีที่ 1: ใช้ Plugin Reloader (แนะนำที่สุด)

### ติดตั้ง Plugin Reloader
1. เปิด QGIS
2. ไปที่ **Plugins → Manage and Install Plugins**
3. ค้นหา "**Plugin Reloader**"
4. กด **Install**

### การใช้งาน
1. แก้ไขโค้ด plugin ของคุณ
2. กด **F5** หรือไปที่ **Plugins → Plugin Reloader → Reload a plugin**
3. เลือก "QcomboLayer" จาก dropdown
4. กด **Reload**
5. Plugin จะถูก reload ใหม่ทันที!

### ข้อดี:
- ไม่ต้อง zip/unzip
- ไม่ต้อง restart QGIS
- กดปุ่มเดียวเสร็จ
- รองรับ hotkey F5

---

## วิธีที่ 2: Development Installation

### Setup ครั้งแรก
1. Copy folder plugin ไปยัง QGIS plugins directory:
```cmd
copy "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer" "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\qcombolayer"
```

2. สร้าง symbolic link (แนะนำ):
```cmd
mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\qcombolayer" "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
```

### การใช้งาน
1. แก้ไขโค้ดใน source directory
2. ใน QGIS: **Plugins → Plugin Reloader → Reload**
3. หรือ restart QGIS

### ข้อดี:
- แก้ไขใน source directory โดยตรง
- ไม่ต้อง copy ไฟล์
- Sync อัตโนมัติ

---

## วิธีที่ 3: QGIS Development Environment

### ใช้ Python Console ใน QGIS
```python
# ใน QGIS Python Console
import importlib
from qgis.utils import plugins

# Reload plugin module
if 'QcomboLayer' in plugins:
    # Unload plugin
    plugins['QcomboLayer'].unload()
    
    # Reload modules
    import QcomboLayer
    importlib.reload(QcomboLayer)
    
    # Reload plugin
    plugins['QcomboLayer'].__init__(iface)
    plugins['QcomboLayer'].initGui()
```

### Hotkey Setup
สร้าง macro ใน QGIS:
1. **Settings → Options → General → Variables**
2. เพิ่ม macro สำหรับ reload

---

## วิธีที่ 4: Command Line Development

### สร้าง Batch Script
```batch
@echo off
echo Reloading QcomboLayer Plugin...

REM Kill QGIS processes
taskkill /f /im qgis.exe 2>nul
timeout /t 2

REM Start QGIS with plugin
start "" "C:\Program Files\QGIS 3.x\bin\qgis.exe"

echo Plugin development environment ready!
pause
```

### สร้าง PowerShell Script
```powershell
# reload_plugin.ps1
Write-Host "Reloading QcomboLayer Plugin..." -ForegroundColor Green

# Function to reload plugin via QGIS Python API
$script = @"
from qgis.utils import plugins, reloadPlugin
if 'QcomboLayer' in plugins:
    reloadPlugin('QcomboLayer')
    print('Plugin reloaded successfully!')
"@

# Execute in QGIS
# (requires QGIS to be running with Python console access)
```

---

## วิธีที่ 5: Docker Development (สำหรับ Advanced)

### Docker Setup
```dockerfile
FROM qgis/qgis:latest
COPY ./qcombolayer /root/.local/share/QGIS/QGIS3/profiles/default/python/plugins/qcombolayer
```

---

## แนะนำสำหรับคุณ

### Setup แบบง่าย (ใช้เวลา 5 นาที):

1. **ติดตั้ง Plugin Reloader**:
```
Plugins → Manage and Install Plugins → ค้นหา "Plugin Reloader" → Install
```

2. **สร้าง Symbolic Link**:
```cmd
mklink /D "%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\QcomboLayer" "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
```

3. **Workflow การพัฒนา**:
   - แก้ไขโค้ดใน source directory
   - กด **F5** ใน QGIS
   - ทดสอบ feature ใหม่
   - ทำซ้ำ

### ข้อดีของวิธีนี้:
- ✅ ไม่ต้อง zip/unzip
- ✅ ไม่ต้อง restart QGIS
- ✅ ไม่ต้อง copy ไฟล์
- ✅ กดปุ่มเดียวเสร็จ
- ✅ รองรับ hotkey
- ✅ Debug ได้ง่าย

### การ Debug
```python
# เพิ่มใน plugin code
import traceback
try:
    # your code here
    pass
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()
```

---

## เมื่อพร้อม Release

### สร้าง Release Package
```cmd
cd "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS"
powershell Compress-Archive -Path "qcombolayer\*" -DestinationPath "QcomboLayer_v1.0.zip"
```

### หรือใช้ pb_tool (Plugin Builder Tool)
```cmd
cd "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
pb_tool zip
```
