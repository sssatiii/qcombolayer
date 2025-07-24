# วิธีแก้ปัญหา Icon ไม่แสดงใน QGIS Plugin

## สาเหตุที่เป็นไปได้

1. **ไฟล์ resources.py มีปัญหา** (เกิดจาก script ที่ generate ไม่ถูกต้อง)
2. **Path ไปยัง icon ไม่ถูกต้อง**
3. **ขนาดหรือรูปแบบของ icon ไม่เหมาะสม**
4. **QGIS ไม่ได้ restart หลังจากเปลี่ยน icon**

## วิธีแก้ไขแบบ Step-by-Step

### ขั้นตอนที่ 1: ใช้ Direct Path (ทำแล้ว)
แก้ไขไฟล์ `QcomboLayer.py` ให้ใช้ direct path แทน resource path:

```python
# แทนที่บรรทัดนี้:
icon_path = ':/plugins/QcomboLayer/icon.png'

# ด้วยบรรทัดนี้:
icon_path = os.path.join(self.plugin_dir, 'icon.png')
```

### ขั้นตอนที่ 2: ตรวจสอบไฟล์ icon
1. **ขนาด**: ควรเป็น 24x24 หรือ 32x32 pixels
2. **รูปแบบ**: PNG เท่านั้น
3. **ชื่อไฟล์**: `icon.png` (case-sensitive)
4. **ตำแหน่ง**: อยู่ใน root directory ของ plugin

### ขั้นตอนที่ 3: ทดสอบ Plugin
1. **Restart QGIS** อย่างสมบูรณ์ (ปิดแล้วเปิดใหม่)
2. ไปที่ **Plugins → Manage and Install Plugins**
3. เช็คว่า QcomboLayer plugin ยัง enable อยู่หรือไม่
4. ถ้าไม่เห็น icon ให้ disable แล้ว enable ใหม่

### ขั้นตอนที่ 4: Debug เพิ่มเติม
ถ้ายังไม่แสดง ให้เพิ่ม debug code ใน `initGui()`:

```python
def initGui(self):
    # Use direct path to icon file
    icon_path = os.path.join(self.plugin_dir, 'icon.png')
    
    # Debug: ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
    if os.path.exists(icon_path):
        print(f"Icon found at: {icon_path}")
    else:
        print(f"Icon NOT found at: {icon_path}")
        # ใช้ default icon ถ้าไม่เจอ
        icon_path = ""
    
    self.add_action(
        icon_path,
        text=self.tr(u'QcomboLayer'),
        callback=self.run,
        parent=self.iface.mainWindow())
```

## วิธีทดสอบการแก้ไข

### 1. ตรวจสอบไฟล์
```cmd
cd "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
dir icon.png
```

### 2. ตรวจสอบใน QGIS
1. เปิด QGIS
2. ไปที่ **Plugins → Python Console**
3. รันคำสั่ง:
```python
import os
plugin_dir = r"c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
icon_path = os.path.join(plugin_dir, "icon.png")
print(f"Icon exists: {os.path.exists(icon_path)}")
print(f"File size: {os.path.getsize(icon_path) if os.path.exists(icon_path) else 'N/A'} bytes")
```

### 3. ตรวจสอบ Plugin Loading
ใน **Plugins → Python Console**:
```python
from qgis.utils import plugins
if 'QcomboLayer' in plugins:
    print("Plugin loaded successfully")
    plugin = plugins['QcomboLayer']
    print(f"Plugin directory: {plugin.plugin_dir}")
else:
    print("Plugin not loaded")
```

## Fallback Solutions

### วิธีที่ 1: ใช้ Built-in Icon
ถ้ายังไม่ได้ผล ให้ใช้ icon จาก QGIS:
```python
from qgis.PyQt.QtGui import QIcon
from qgis.core import QgsApplication

# ใช้ built-in icon
icon = QgsApplication.getThemeIcon("/mActionOpenTable.svg")
```

### วิธีที่ 2: ไม่ใช้ Icon
comment บรรทัด icon ออกไปชั่วคราว:
```python
def initGui(self):
    # icon_path = os.path.join(self.plugin_dir, 'icon.png')
    self.add_action(
        "",  # ไม่ใช้ icon
        text=self.tr(u'QcomboLayer'),
        callback=self.run,
        parent=self.iface.mainWindow())
```

## ขั้นตอนถัดไป

1. **Restart QGIS** ก่อนอื่น
2. ตรวจสอบว่า icon file มีอยู่จริง
3. ถ้ายังไม่ได้ ให้ใช้ debug code เพื่อดูว่าเกิดอะไรขึ้น
4. ถ้ายังไม่ได้ ให้ลองใช้ fallback solutions

## หมายเหตุ

- การเปลี่ยนจาก resource path เป็น direct path ควรจะแก้ปัญหาได้
- ถ้ายังไม่ได้ อาจเป็นเพราะไฟล์ icon มีปัญหา หรือ QGIS ต้อง restart
- Plugin จะยังทำงานได้ปกติแม้ไม่มี icon
