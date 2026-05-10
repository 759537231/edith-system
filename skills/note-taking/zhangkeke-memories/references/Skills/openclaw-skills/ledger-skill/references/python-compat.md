# Python 版本兼容性问题

## 问题

`ledger.py` 使用了 Python 3.10+ 语法 `bool | None`，在 Python 3.9 上会报错：

```
TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'
```

## 解决方案

将所有 `X | None` 改为 `Optional[X]`，并在文件开头添加：
```python
from typing import Optional
```

需要修改的位置（截至 2026-05-04）：
- `_infer_in_budget()` 返回值
- `_record_correction()` 参数
- `add_entry()` 参数 `in_budget`, `reimburse_pair_id`
- `correct_entry()` 返回值
- `add_expense_with_reimburse()` 参数 `reimburse_amount_yuan`
- `add_reimburse_pair()` 返回值
- `get_pair_status()` 返回值
- `get_entries()` 参数
- `get_summary()` 参数
- `export_csv()` 参数
- `save_csv()` 参数
- `confirm_pending()` 返回值
- `reject_pending()` 返回值

## 调用方式（Python 3.9 系统自带）

```bash
/opt/homebrew/bin/python3 -c "
import sys
sys.path.insert(0, '/Users/qianmo/Desktop/张壳壳/Skills/openclaw-skills/ledger-skill/scripts')
import ledger
result = ledger.add_entry(...)
"
```

如果用系统自带 Python 3.9，必须先修复类型注解。
如果用 Homebrew 安装的 Python 3.14+，无需修改。
