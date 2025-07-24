# วิธีการเปลี่ยน Icon ของ QGIS Plugin

## ขั้นตอนการเปลี่ยน Icon

### 1. แทนที่ไฟล์ icon.png
- **ที่อยู่ไฟล์**: `c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer\icon.png`
- **ข้อกำหนด**:
  - รูปแบบ: PNG
  - ขนาด: 24x24 หรือ 32x32 pixels
  - ชื่อไฟล์: `icon.png` (ต้องเป็นชื่อเดิม)

### 2. Compile Resources ใหม่
เปิด Command Prompt/PowerShell ใน directory ของ plugin และรันคำสั่ง:

```powershell
cd "c:\iNFRA\proj-infra\DOH AI\Data\QGIS-proj\pyQGIS\qcombolayer"
pyrcc5 resources.qrc -o resources.py
```

### 3. Restart QGIS
- ปิด QGIS
- เปิด QGIS ใหม่
- Icon ใหม่จะปรากฏใน toolbar

## ไฟล์ที่เกี่ยวข้อง

### resources.qrc
```xml
<RCC>
    <qresource prefix="/plugins/QcomboLayer" >
        <file>icon.png</file>
    </qresource>
</RCC>
```

### QcomboLayer.py (บรรทัด 161)
```python
icon_path = ':/plugins/QcomboLayer/icon.png'
self.add_action(
    icon_path,
    text=self.tr(u'QcomboLayer'),
    callback=self.run,
    parent=self.iface.mainWindow())
```

## หมายเหตุ

1. **ไม่ต้องแก้ไขโค้ด** - ถ้าคุณใช้ชื่อไฟล์ `icon.png` เหมือนเดิม
2. **Compile Resources** - จำเป็นต้องทำเพื่อให้ QGIS รู้จัก icon ใหม่
3. **Restart QGIS** - ต้องเริ่มใหม่เพื่อให้ plugin โหลด icon ใหม่

## การ Troubleshoot

ถ้า icon ไม่เปลี่ยน:
1. ตรวจสอบว่าไฟล์ `icon.png` มีขนาดและรูปแบบถูกต้อง
2. ตรวจสอบว่า compile resources สำเร็จ (ไฟล์ `resources.py` อัพเดทแล้ว)
3. Restart QGIS อีกครั้ง
4. ลองปิด/เปิด plugin ใน Plugin Manager
