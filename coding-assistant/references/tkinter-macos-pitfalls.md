# tkinter on macOS: Pitfalls & Fixes

## Problem: label.config() and StringVar silently fail

**Symptoms:**
- `root.title("new title")` works
- `lambda: root.title("...")` works  
- `label.config(text="new text")` does NOT update display
- `StringVar.set("new text")` does NOT update linked label

**Environment that fails:**
- macOS system Python 3.9.6 + tkinter 8.5 (Tcl 8.5)
- Path: `/usr/bin/python3`
- From: `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/`

**Environment that works:**
- Homebrew Python 3.14 + tkinter 9.0 (Tcl 9.0)
- Path: `/opt/homebrew/bin/python3`
- Install: `brew install python@3.14 python-tk@3.14 tcl-tk`

## Root Cause

macOS system Python ships with an old Tcl/Tk 8.5 framework that has known display-update bugs on modern macOS (aqua windowing system). The label widget's display refresh is broken — changes to text/textvariable don't trigger a redraw.

## Workarounds

### Option 1: Use root.title() for display (no install needed)
```python
# Instead of label.config(text="value"), use:
root.title(str(value))
```

### Option 2: Switch to Homebrew Python (recommended)
```bash
brew install tcl-tk python@3.14 python-tk@3.14
/opt/homebrew/bin/python3 your_script.py
```

### Option 3: Use PyQt/wxPython instead
If tkinter compatibility is unreliable, consider PyQt5/6 or wxPython.

## Diagnosis Commands

```bash
# Check current tkinter version
python3 -c "import tkinter; print('tkinter:', tkinter.TkVersion, 'Tcl:', tkinter.TclVersion)"

# Check which Python you're using
which python3
python3 --version

# Check Homebrew Python tkinter
/opt/homebrew/bin/python3 -c "import tkinter; print('tkinter:', tkinter.TkVersion)"
```

## Key Finding (2026-05-07)

This is NOT a code bug. The same code works with Homebrew Python but fails with system Python. The issue is the Tcl/Tk framework version bundled with macOS system Python.

## Troubleshooting: Background GUI Process Not Appearing

**Symptom:** User says "窗口在哪里" / "I don't see the window"
**Diagnosis:** Check process status with `process(action='poll')` — likely the script crashed on startup.
**Common cause:** Python syntax/attribute error at launch (e.g., referencing a method that doesn't exist).

**Lesson:** Always do a quick syntax check or at minimum launch the process and immediately poll it to catch startup crashes. Don't assume "process started" means "window is visible".

## ✅ Verified (2026-05-08)

**Test file:** `~/Desktop/calculator/test_homebrew3.py`
**Test command:** `/opt/homebrew/bin/python3 ~/Desktop/calculator/test_homebrew3.py`
**Result:** Button click successfully updates label from "未点击" to "点击了！"

**Conclusion:** Homebrew Python + tcl-tk solution confirmed working. The tkinter GUI display update issue is resolved.
