# 常用命令参考

## 项目结构分析

### 查看目录结构
```bash
# 基本列表
ls -la

# 递归查看
find . -type f -name "*.py" | head -20

# 树形结构
tree -L 2 -I node_modules

# 统计文件
find . -name "*.py" | wc -l
```

### 查看文件内容
```bash
# 查看文件
cat README.md

# 查看前10行
head -10 main.py

# 查看后10行
tail -10 app.log

# 搜索内容
grep -r "function" --include="*.js"
```

## 代码分析

### Python
```bash
# 语法检查
python -m py_compile script.py

# 代码风格
flake8 src/

# 类型检查
mypy src/

# 代码复杂度
radon cc src/ -a
```

### JavaScript/TypeScript
```bash
# 语法检查
eslint src/

# 类型检查
tsc --noEmit

# 代码风格
prettier --check src/
```

## 测试

### Python
```bash
# 运行测试
pytest

# 运行特定测试
pytest tests/test_main.py

# 带覆盖率
pytest --cov=src

# 详细输出
pytest -v
```

### JavaScript/TypeScript
```bash
# 运行测试
npm test

# 运行特定测试
npm test -- --grep "test name"

# 带覆盖率
npm test -- --coverage

# 监听模式
npm test -- --watch
```

## Git操作

### 基本操作
```bash
# 查看状态
git status

# 查看差异
git diff

# 添加文件
git add .

# 提交
git commit -m "message"

# 推送
git push

# 拉取
git pull
```

### 分支操作
```bash
# 查看分支
git branch

# 创建分支
git branch feature-xxx

# 切换分支
git checkout feature-xxx

# 合并分支
git merge feature-xxx

# 删除分支
git branch -d feature-xxx
```

### 查看历史
```bash
# 查看日志
git log --oneline

# 查看特定文件历史
git log --follow -p -- main.py

# 查看差异
git diff HEAD~3
```

## 调试

### Python
```bash
# 使用pdb
python -m pdb script.py

# 使用ipdb
ipdb script.py

# 打印调试
print(f"DEBUG: {variable}")

# 日志调试
import logging
logging.debug(f"DEBUG: {variable}")
```

### JavaScript/TypeScript
```bash
# 使用Node debugger
node --inspect script.js

# 使用Chrome DevTools
node --inspect-brk script.js

# 打印调试
console.log('DEBUG:', variable)
```

## 包管理

### Python
```bash
# 安装包
pip install package

# 安装依赖
pip install -r requirements.txt

# 查看已安装
pip list

# 生成依赖
pip freeze > requirements.txt
```

### JavaScript/TypeScript
```bash
# 安装包
npm install package

# 安装依赖
npm install

# 查看已安装
npm list

# 生成依赖
npm shrinkwrap
```

## 性能分析

### Python
```bash
# 使用cProfile
python -m cProfile -s cumulative script.py

# 使用line_profiler
kernprof -l -v script.py

# 使用memory_profiler
python -m memory_profiler script.py
```

### JavaScript/TypeScript
```bash
# 使用Node profiler
node --prof script.js

# 分析结果
node --prof-process isolate-*.log

# 使用Chrome DevTools
node --inspect script.js
```

## 代码格式化

### Python
```bash
# 使用black
black src/

# 使用isort
isort src/

# 使用autopep8
autopep8 --in-place src/
```

### JavaScript/TypeScript
```bash
# 使用prettier
prettier --write src/

# 使用eslint --fix
eslint --fix src/
```

## 文档生成

### Python
```bash
# 使用sphinx
sphinx-quickstart docs
make html

# 使用pdoc
pdoc --html src/
```

### JavaScript/TypeScript
```bash
# 使用jsdoc
jsdoc src/

# 使用typedoc
typedoc src/
```
