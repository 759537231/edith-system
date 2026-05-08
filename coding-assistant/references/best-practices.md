# 编程最佳实践

## 1. 代码质量

### 命名规范
```python
# 好
def calculate_total_price(items):
    total_price = 0
    for item in items:
        total_price += item.price
    return total_price

# 坏
def calc(i):
    t = 0
    for x in i:
        t += x.p
    return t
```

### 函数设计
```python
# 好：单一职责
def get_user(user_id):
    return database.get_user(user_id)

def send_email(user, message):
    email_service.send(user.email, message)

# 坏：多重职责
def process_user(user_id):
    user = database.get_user(user_id)
    email_service.send(user.email, "Welcome!")
    return user
```

### 错误处理
```python
# 好：具体异常
try:
    result = database.query(sql)
except DatabaseConnectionError:
    logger.error("Database connection failed")
    raise
except QueryError as e:
    logger.error(f"Query failed: {e}")
    raise

# 坏：通用异常
try:
    result = database.query(sql)
except Exception:
    pass
```

### 类型注解
```python
# 好
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 坏
def greet(name):
    return f"Hello, {name}!"
```

## 2. 测试规范

### 测试命名
```python
# 好
def test_calculate_total_price_with_empty_list():
    assert calculate_total_price([]) == 0

def test_calculate_total_price_with_multiple_items():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total_price(items) == 30

# 坏
def test1():
    assert calculate_total_price([]) == 0

def test2():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total_price(items) == 30
```

### 测试结构
```python
# Arrange-Act-Assert模式
def test_calculate_total_price():
    # Arrange
    items = [Item(price=10), Item(price=20)]
    
    # Act
    result = calculate_total_price(items)
    
    # Assert
    assert result == 30
```

### 测试覆盖
```python
# 测试边界情况
def test_calculate_total_price_with_negative_price():
    items = [Item(price=-10)]
    with pytest.raises(ValueError):
        calculate_total_price(items)

# 测试异常情况
def test_calculate_total_price_with_invalid_input():
    with pytest.raises(TypeError):
        calculate_total_price("invalid")
```

## 3. Git规范

### 提交信息
```bash
# 好
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login bug"
git commit -m "docs: update README"

# 坏
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

### 分支命名
```bash
# 好
git branch feature/user-auth
git branch bugfix/login-error
git branch docs/readme-update

# 坏
git branch new-feature
git branch fix
git branch update
```

### 原子提交
```bash
# 好：每个提交只做一件事
git commit -m "feat: add user model"
git commit -m "feat: add user API"
git commit -m "feat: add user tests"

# 坏：一个提交做多件事
git commit -m "feat: add user system"
```

## 4. 文档规范

### README结构
```markdown
# 项目名称

简短描述

## 安装

安装步骤

## 使用

使用示例

## API

API文档

## 贡献

贡献指南

## 许可证

许可证信息
```

### 代码注释
```python
# 好
def calculate_total_price(items):
    """
    计算商品总价
    
    Args:
        items: 商品列表
        
    Returns:
        总价
        
    Raises:
        ValueError: 如果价格为负数
    """
    total_price = 0
    for item in items:
        if item.price < 0:
            raise ValueError("Price cannot be negative")
        total_price += item.price
    return total_price

# 坏
def calculate_total_price(items):
    # 计算总价
    total_price = 0
    for item in items:
        total_price += item.price
    return total_price
```

## 5. 性能优化

### 算法优化
```python
# 坏：O(n²)
def find_duplicates_slow(lst):
    duplicates = []
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if lst[i] == lst[j]:
                duplicates.append(lst[i])
    return duplicates

# 好：O(n)
def find_duplicates_fast(lst):
    seen = set()
    duplicates = []
    for item in lst:
        if item in seen:
            duplicates.append(item)
        seen.add(item)
    return duplicates
```

### 缓存使用
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### 异步处理
```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    urls = ["http://example.com/1", "http://example.com/2"]
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
```

## 6. 安全规范

### 输入验证
```python
# 好
def process_input(user_input):
    if not isinstance(user_input, str):
        raise TypeError("Input must be a string")
    if len(user_input) > 100:
        raise ValueError("Input too long")
    return user_input.strip()

# 坏
def process_input(user_input):
    return user_input
```

### 密码处理
```python
import hashlib
import os

def hash_password(password):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt + key

def verify_password(stored_password, provided_password):
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    new_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
    return new_key == stored_key
```

### SQL注入防护
```python
# 好
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# 坏
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
```

## 7. 代码审查清单

### 功能检查
- [ ] 代码是否符合需求
- [ ] 边界情况是否处理
- [ ] 错误处理是否完善
- [ ] 性能是否可接受

### 代码质量
- [ ] 命名是否清晰
- [ ] 函数是否单一职责
- [ ] 是否有重复代码
- [ ] 是否有类型注解

### 测试覆盖
- [ ] 是否有单元测试
- [ ] 测试是否覆盖边界情况
- [ ] 测试是否独立
- [ ] 测试是否可读

### 安全性
- [ ] 输入是否验证
- [ ] 敏感数据是否加密
- [ ] 是否有SQL注入风险
- [ ] 是否有XSS风险

### 文档
- [ ] 是否有README
- [ ] 是否有代码注释
- [ ] 是否有API文档
- [ ] 是否有使用示例
