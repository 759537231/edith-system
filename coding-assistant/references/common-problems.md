# 常见问题和解决方案

## 1. 代码运行报错

### 问题：ImportError
**原因**：模块不存在或路径错误
**解决**：
```bash
# 检查模块是否存在
pip list | grep module_name

# 检查Python路径
python -c "import sys; print(sys.path)"

# 安装模块
pip install module_name
```

### 问题：SyntaxError
**原因**：语法错误
**解决**：
1. 检查错误行号
2. 检查括号、引号是否匹配
3. 检查缩进
4. 使用语法检查工具

### 问题：TypeError
**原因**：类型不匹配
**解决**：
1. 检查变量类型
2. 添加类型转换
3. 使用类型注解

### 问题：IndexError
**原因**：索引超出范围
**解决**：
1. 检查数组长度
2. 添加边界检查
3. 使用try-except

### 问题：KeyError
**原因**：字典键不存在
**解决**：
1. 检查键是否存在
2. 使用get()方法
3. 使用defaultdict

## 2. 测试失败

### 问题：测试找不到
**原因**：测试文件命名不规范
**解决**：
```bash
# pytest
pytest tests/test_*.py

# jest
npm test -- --testPathPattern="test"
```

### 问题：测试依赖缺失
**原因**：测试需要的模块未安装
**解决**：
```bash
# 安装测试依赖
pip install pytest pytest-cov
npm install --save-dev jest
```

### 问题：测试数据问题
**原因**：测试数据不正确
**解决**：
1. 使用fixtures
2. 使用工厂模式
3. 使用mock

### 问题：测试环境问题
**原因**：环境变量未设置
**解决**：
1. 使用.env文件
2. 使用pytest-env
3. 设置环境变量

## 3. Git问题

### 问题：冲突
**原因**：多人修改同一文件
**解决**：
1. git status查看冲突
2. 手动解决冲突
3. git add添加解决
4. git commit提交

### 问题：提交信息错误
**原因**：提交信息不清晰
**解决**：
```bash
# 修改最后一次提交信息
git commit --amend -m "新的提交信息"
```

### 问题：误删文件
**原因**：不小心删除了文件
**解决**：
```bash
# 恢复文件
git checkout HEAD -- file.txt

# 恢复所有文件
git checkout HEAD -- .
```

### 问题：分支混乱
**原因**：分支管理不当
**解决**：
```bash
# 查看分支
git branch

# 切换分支
git checkout main

# 删除分支
git branch -d feature-xxx
```

## 4. 性能问题

### 问题：程序运行慢
**原因**：算法效率低
**解决**：
1. 分析性能瓶颈
2. 优化算法
3. 使用缓存
4. 异步处理

### 问题：内存泄漏
**原因**：资源未释放
**解决**：
1. 使用with语句
2. 及时释放资源
3. 使用弱引用
4. 分析内存使用

### 问题：数据库慢
**原因**：查询效率低
**解决**：
1. 添加索引
2. 优化查询
3. 使用缓存
4. 分页查询

## 5. 依赖问题

### 问题：版本冲突
**原因**：依赖版本不兼容
**解决**：
```bash
# Python
pip install package==version

# JavaScript
npm install package@version
```

### 问题：依赖缺失
**原因**：依赖未安装
**解决**：
```bash
# Python
pip install -r requirements.txt

# JavaScript
npm install
```

### 问题：依赖过多
**原因**：依赖管理不当
**解决**：
```bash
# Python
pip install pipreqs
pipreqs ./

# JavaScript
npm prune
```

## 6. 环境问题

### 问题：Python版本不对
**原因**：使用了错误的Python版本
**解决**：
```bash
# 检查版本
python --version

# 使用特定版本
python3.11 script.py

# 使用pyenv
pyenv install 3.11.0
pyenv local 3.11.0
```

### 问题：Node版本不对
**原因**：使用了错误的Node版本
**解决**：
```bash
# 检查版本
node --version

# 使用nvm
nvm install 18
nvm use 18
```

### 问题：虚拟环境问题
**原因**：虚拟环境未激活
**解决**：
```bash
# Python
python -m venv venv
source venv/bin/activate

# JavaScript
npx vite
```

## 7. 部署问题

### 问题：部署失败
**原因**：配置错误
**解决**：
1. 检查配置文件
2. 检查环境变量
3. 检查日志
4. 本地测试

### 问题：权限问题
**原因**：文件权限不对
**解决**：
```bash
# 修改权限
chmod +x script.sh

# 修改所有者
chown user:group file
```

### 问题：端口占用
**原因**：端口已被占用
**解决**：
```bash
# 查看端口占用
lsof -i :8000

# 杀死进程
kill -9 PID

# 使用其他端口
python -m http.server 8001
```

## 8. 调试技巧

### 使用print调试
```python
print(f"DEBUG: variable = {variable}")
print(f"DEBUG: type = {type(variable)}")
```

### 使用logging调试
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logging.debug(f"DEBUG: {variable}")
```

### 使用pdb调试
```python
import pdb; pdb.set_trace()
```

### 使用断点调试
```python
# VS Code
# 在行号前点击添加断点
# 按F5启动调试
```

### 使用Chrome DevTools
```javascript
// 在代码中添加
debugger;

// 打开Chrome DevTools
// Sources面板查看代码
// 在debugger处暂停
```
