# plugin.py

from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QComboBox, QPushButton, QLabel, QLineEdit, QHBoxLayout
from qgis.core import QgsProject, QgsExpression, QgsFeatureRequest, QgsVectorLayer
from qgis.utils import iface

class QcomboLayerPlugin(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QcomboLayer Plugin")
        
        # สร้าง Layout
        layout = QVBoxLayout()

        # เลือก Layer
        self.layer_combo = QComboBox()
        self.layer_combo.addItems([layer.name() for layer in QgsProject.instance().mapLayers().values()])
        layout.addWidget(QLabel("Select Layer:"))
        layout.addWidget(self.layer_combo)

        # เลือก Field
        self.field_combo = QComboBox()
        layout.addWidget(QLabel("Select Field:"))
        layout.addWidget(self.field_combo)

        # กรอกข้อมูลที่จะ Filter
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Enter filter value...")
        layout.addWidget(QLabel("Enter filter value:"))
        layout.addWidget(self.filter_input)

        # สร้างปุ่มสำหรับ Action (Fix หรือ Flex)
        self.action_button = QComboBox()
        self.action_button.addItems(["Fix", "Flex"])
        layout.addWidget(QLabel("Set action:"))
        layout.addWidget(self.action_button)

        # กดปุ่ม Ok เพื่อยืนยัน
        self.ok_button = QPushButton("Ok")
        self.ok_button.clicked.connect(self.apply_filter)
        layout.addWidget(self.ok_button)

        # ปุ่มลูกศร (เพิ่มหรือลดข้อมูล)
        self.arrow_layout = QHBoxLayout()
        self.left_arrow = QPushButton("←")
        self.right_arrow = QPushButton("→")
        self.arrow_layout.addWidget(self.left_arrow)
        self.arrow_layout.addWidget(self.right_arrow)
        layout.addLayout(self.arrow_layout)

        self.setLayout(layout)

        # เชื่อมโยงการเลือก Layer กับ Field
        self.layer_combo.currentIndexChanged.connect(self.update_fields)

    def update_fields(self):
        layer_name = self.layer_combo.currentText()
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        
        # ดึงฟิลด์จาก Layer
        fields = layer.fields()
        self.field_combo.clear()
        self.field_combo.addItems([field.name() for field in fields])

    def apply_filter(self):
        layer_name = self.layer_combo.currentText()
        field_name = self.field_combo.currentText()
        filter_value = self.filter_input.text()
        action = self.action_button.currentText()

        # ดึง Layer จากชื่อ
        layer = QgsProject.instance().mapLayersByName(layer_name)[0]

        # สร้าง Expression สำหรับการกรองข้อมูล
        expr = QgsExpression(f'"{field_name}" = \'{filter_value}\'')
        request = QgsFeatureRequest(expr)

        # เลือกฟีเจอร์ที่ตรงกับเงื่อนไข
        features = layer.getFeatures(request)

        # แสดงผลลัพธ์
        for feature in features:
            print(f"ID: {feature.id()}, {field_name}: {feature[field_name]}")

        iface.messageBar().pushMessage("Filtered Data", f"Data filtered for {field_name}: {filter_value}", level=Qgis.Info)

        # กรองข้อมูลใน layer
        self.filter_layer(layer, field_name, filter_value, action)

    def filter_layer(self, layer, field_name, filter_value, action):
        expr = QgsExpression(f'"{field_name}" = \'{filter_value}\'')
        request = QgsFeatureRequest(expr)
        
        # หากเป็น Flex, ให้สามารถเพิ่มหรือลดข้อมูลได้
        if action == "Flex":
            features = layer.getFeatures(request)
            for feature in features:
                # คำนวณการเลื่อนข้อมูล
                feature[field_name] = int(feature[field_name]) + 1  # เพิ่มข้อมูล +1
                print(f"Updated ID: {feature.id()}, {field_name}: {feature[field_name]}")

            iface.mapCanvas().refresh()

# คำสั่งในการเปิด Dialog ของ Plugin
plugin_dialog = QcomboLayerPlugin()
plugin_dialog.exec_()
