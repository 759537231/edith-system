# 语言特定指南

## Python

### 项目结构
```
project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   └── test_utils/
│       ├── __init__.py
│       └── test_helpers.py
├── requirements.txt
├── setup.py
└── README.md
```

### 常用工具
```bash
# 虚拟环境
python -m venv venv
source venv/bin/activate

# 包管理
pip install package
pip install -r requirements.txt

# 代码质量
flake8 src/
mypy src/
black src/
isort src/

# 测试
pytest
pytest --cov=src
```

### 最佳实践
```python
# 类型注解
def greet(name: str) -> str:
    return f"Hello, {name}!"

# 文档字符串
def calculate(a: int, b: int) -> int:
    """
    计算两数之和
    
    Args:
        a: 第一个数
        b: 第二个数
        
    Returns:
        两数之和
    """
    return a + b

# 异常处理
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

## JavaScript/TypeScript

### 项目结构
```
project/
├── src/
│   ├── index.ts
│   ├── utils/
│   │   └── helpers.ts
│   └── types/
│       └── index.ts
├── tests/
│   ├── index.test.ts
│   └── utils/
│       └── helpers.test.ts
├── package.json
├── tsconfig.json
└── README.md
```

### 常用工具
```bash
# 包管理
npm install package
npm install

# 代码质量
eslint src/
prettier --check src/
tsc --noEmit

# 测试
npm test
npm test -- --coverage
```

### 最佳实践
```typescript
// 类型定义
interface User {
  id: number;
  name: string;
  email: string;
}

// 函数
function greet(name: string): string {
  return `Hello, ${name}!`;
}

// 异步操作
async function fetchData(url: string): Promise<User> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}
```

## Go

### 项目结构
```
project/
├── cmd/
│   └── main.go
├── internal/
│   ├── handler/
│   │   └── handler.go
│   └── service/
│       └── service.go
├── pkg/
│   └── utils/
│       └── utils.go
├── go.mod
├── go.sum
└── README.md
```

### 常用工具
```bash
# 包管理
go mod init
go get package

# 代码质量
golangci-lint run
go vet ./...

# 测试
go test ./...
go test -cover ./...
```

### 最佳实践
```go
// 包命名
package main

// 函数
func Greet(name string) string {
    return fmt.Sprintf("Hello, %s!", name)
}

// 错误处理
func ReadFile(path string) ([]byte, error) {
    data, err := os.ReadFile(path)
    if err != nil {
        return nil, fmt.Errorf("failed to read file: %w", err)
    }
    return data, nil
}
```

## Rust

### 项目结构
```
project/
├── src/
│   ├── main.rs
│   └── lib.rs
├── tests/
│   └── integration_test.rs
├── Cargo.toml
└── README.md
```

### 常用工具
```bash
# 包管理
cargo add package
cargo build

# 代码质量
cargo clippy
cargo fmt --check

# 测试
cargo test
cargo test -- --nocapture
```

### 最佳实践
```rust
// 函数
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}

// 错误处理
fn read_file(path: &str) -> Result<String, std::io::Error> {
    std::fs::read_to_string(path)
}

// 所有权
fn process(data: Vec<u8>) -> Vec<u8> {
    // 处理数据
    data
}
```

## Java

### 项目结构
```
project/
├── src/
│   ├── main/
│   │   └── java/
│   │       └── com/
│   │           └── example/
│   │               └── Main.java
│   └── test/
│       └── java/
│           └── com/
│               └── example/
│                   └── MainTest.java
├── pom.xml
└── README.md
```

### 常用工具
```bash
# 构建
mvn clean install
mvn package

# 测试
mvn test
mvn test -Dtest=MainTest

# 代码质量
mvn checkstyle:check
mvn spotbugs:check
```

### 最佳实践
```java
// 类
public class User {
    private final String name;
    private final String email;
    
    public User(String name, String email) {
        this.name = name;
        this.email = email;
    }
    
    public String getName() {
        return name;
    }
    
    public String getEmail() {
        return email;
    }
}

// 异常处理
public void process() {
    try {
        riskyOperation();
    } catch (SpecificException e) {
        logger.error("Operation failed: " + e.getMessage());
        throw e;
    }
}
```

## PHP

### 项目结构
```
project/
├── src/
│   ├── Controller/
│   ├── Service/
│   └── Entity/
├── tests/
│   ├── Controller/
│   └── Service/
├── composer.json
└── README.md
```

### 常用工具
```bash
# 包管理
composer install
composer require package

# 代码质量
phpcs src/
phpstan analyse src/

# 测试
phpunit
phpunit --coverage-html coverage/
```

### 最佳实践
```php
<?php

// 类
class User
{
    private string $name;
    private string $email;
    
    public function __construct(string $name, string $email)
    {
        $this->name = $name;
        $this->email = $email;
    }
    
    public function getName(): string
    {
        return $this->name;
    }
    
    public function getEmail(): string
    {
        return $this->email;
    }
}

// 异常处理
function process(): void
{
    try {
        riskyOperation();
    } catch (SpecificException $e) {
        logger()->error('Operation failed: ' . $e->getMessage());
        throw $e;
    }
}
```
