# 伊迪丝工具函数

**位置**：`~/.hermes/utils/edith_utils.py`

**功能**：
1. `safe_delegate_task` - 安全的delegate_task封装，支持重试
2. `validate_output` - 验证子Agent输出是否符合规范
3. `extract_skill_info` - 从skill中提取关键信息
4. `build_optimized_context` - 构建优化后的context

**使用示例**：
```python
from edith_utils import safe_delegate_task, validate_output, extract_skill_info, build_optimized_context

# 安全调用delegate_task
result = safe_delegate_task(goal="...", context="...", toolsets=["web"], max_retries=3, timeout=300)

# 验证输出
is_valid, message = validate_output(result.get("summary", ""))

# 提取skill信息
skill_content = skill_view(name='tongshangbu')
info = extract_skill_info(skill_content)

# 构建优化后的context
context = build_optimized_context(info, output_format)
```

**依赖**：无外部依赖，纯Python实现
