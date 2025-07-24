# UI File XML Syntax Fix

## Issue
Qt Designer reported XML syntax error at line 308, column 30:
- Expected ';', but got ')'
- Error was in the action mode dropdown text "Flex (View&Move)"

## Root Cause
The ampersand character (&) in XML must be escaped as `&amp;` according to XML standards.

## Fix Applied
**Before:**
```xml
<string>Flex (View&Move)</string>
```

**After:**
```xml
<string>Flex (View&amp;Move)</string>
```

## Additional Update
Updated the Python code in `QcomboLayer_dialog.py` to handle both the escaped and unescaped versions:
```python
flex_configs = [config for config in self.filter_configurations 
               if config['action_mode'].startswith("Flex (View&") or 
                  config['action_mode'].startswith("Flex (View&amp;")]
```

## Result
- UI file should now load properly in Qt Designer
- Plugin functionality remains unchanged
- XML validation passes

## Files Modified
1. `QcomboLayer_dialog_base.ui` - Fixed XML escape sequence
2. `QcomboLayer_dialog.py` - Updated string matching logic

The UI file should now open without errors in Qt Designer.
