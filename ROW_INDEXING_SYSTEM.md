# Row-Based Indexing System Implementation

## Problem Identified
The previous implementation was trying to use unique values as indices, which caused issues because:
1. Unique values don't have consistent indexing
2. Sorting unique values doesn't match the actual row order in the data
3. Index movement wasn't predictable or reliable

## Solution: Row-Based Indexing (0-based)

### **New System Overview**
- **Index 0**: First row/feature in the layer
- **Index 1**: Second row/feature in the layer  
- **Index 2**: Third row/feature in the layer
- **And so on...**

### **Key Changes Made**

#### 1. **Updated `get_value_at_index()` Method**
```python
def get_value_at_index(self, layer, fields, index):
    """หาค่าที่ index ที่กำหนดจาก field โดยใช้ row number (0-based indexing)"""
    # ดึงค่าทั้งหมดจาก field ตามลำดับ feature (row number)
    values = []
    for feature in layer.getFeatures():
        value = feature[field_name]
        values.append(value)
    
    # ตรวจสอบว่า index อยู่ในช่วงที่ถูกต้อง
    if 0 <= index < len(values):
        return str(values[index]) if values[index] is not None else None
```

**Before**: Used unique values + sorting
**Now**: Uses actual row order from layer.getFeatures()

#### 2. **Added `get_total_rows_for_field()` Method**
```python
def get_total_rows_for_field(self, layer, field_name):
    """หาจำนวน rows ทั้งหมดใน field"""
    # Counts all non-null values in the field
```

#### 3. **Enhanced `fetch_min_value()` Method**
- Always fetches value at index 0 (first row)
- Shows total row count for user reference
- Clear messaging: "ดึงค่าที่ index 0: [value] (จากทั้งหมด [total] แถว)"

#### 4. **Improved `modify_filter_index()` Method**
- **Better Boundary Checking**: Validates index against actual row count
- **Multi-layer Support**: Checks boundaries for all Flex configurations
- **Clear Error Messages**: Shows which layers have how many rows
- **Safer Index Updates**: Only updates if all validations pass

#### 5. **Enhanced User Feedback**
- Shows current index position
- Shows total available rows
- Clear messages for boundary conditions
- Better error handling and rollback

### **How It Works Now**

#### **Setup Phase**:
1. User selects layer and field
2. Clicks "Fetch Min" → Gets value from row 0 (first row)
3. Sets action mode to "Flex (View&Move)"
4. Adds filter configuration

#### **Application Phase**:
1. Click "Apply All Filters" → Filters using the exact value
2. Sets current_filter_index = 0

#### **Navigation Phase** (Flex mode only):
1. **Right Arrow (→)**: current_index + 1
   - Gets value from next row
   - Updates filter to show features with that value
2. **Left Arrow (←)**: current_index - 1
   - Gets value from previous row  
   - Updates filter to show features with that value

#### **Boundary Protection**:
- Cannot go below index 0
- Cannot exceed total row count
- Shows warning messages for boundaries
- Automatic rollback if index is invalid

### **Example Workflow**

**Layer Data Example**:
```
Row 0: field_value = "A"
Row 1: field_value = "B"  
Row 2: field_value = "A"
Row 3: field_value = "C"
Row 4: field_value = "B"
```

**User Actions**:
1. **Fetch Min**: Gets "A" (from row 0)
2. **Apply Filter**: Shows features where field_value = "A" (rows 0, 2)
3. **Right Arrow**: Goes to index 1, gets "B", shows features where field_value = "B" (rows 1, 4)
4. **Right Arrow**: Goes to index 2, gets "A", shows features where field_value = "A" (rows 0, 2)
5. **And so on...**

### **Benefits**

1. **Predictable Navigation**: Index 0, 1, 2, 3... follows actual data order
2. **Reliable Boundaries**: Always knows exactly how many rows exist
3. **Intuitive Behavior**: Users can navigate through data in order
4. **Better Error Handling**: Clear feedback about current position and limits
5. **Multi-layer Support**: Each layer can have different row counts

### **Files Modified**

1. **QcomboLayer_dialog.py**:
   - `get_value_at_index()`: Row-based indexing
   - `get_total_rows_for_field()`: New method for row counting
   - `fetch_min_value()`: Enhanced with row count display
   - `modify_filter_index()`: Better boundary checking
   - `apply_all_filters()`: Enhanced user feedback

### **Testing Checklist**

- [ ] **Fetch Min**: Gets value from first row (index 0)
- [ ] **Row Count**: Displays correct total row count
- [ ] **Navigation**: Arrow buttons move through actual row indices
- [ ] **Boundaries**: Cannot go below 0 or above row count
- [ ] **Multi-layer**: Works correctly with multiple layers having different row counts
- [ ] **Error Messages**: Clear feedback for all boundary conditions
- [ ] **Rollback**: Index reverts if navigation fails

---

**The plugin now has a proper, reliable indexing system that matches user expectations!**
