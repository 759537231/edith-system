# Excel与SQL数据处理技巧

## 第一部分：Excel核心技能

### 一、核心函数

#### 1. VLOOKUP函数
**语法**：
```
=VLOOKUP(lookup_value, table_array, col_index_num, [range_lookup])
```
- `lookup_value`：要查找的值
- `table_array`：查找的数据区域
- `col_index_num`：返回第几列的值
- `range_lookup`：FALSE（精确匹配）或TRUE（近似匹配）

**示例**：
```excel
=VLOOKUP("张三", A2:D100, 3, FALSE)  // 在A2:D100区域查找"张三"，返回第3列的值
```

**适用场景**：
- 两个表格之间的数据关联匹配
- 根据员工ID查找员工姓名、部门等信息
- 商品编码对应商品名称和价格

**常见坑**：
- **#N/A错误**：查找不到值，检查查找值是否存在
- **#REF!错误**：列序号超出范围
- **从左到右限制**：只能查找返回右侧列的数据
- **不自动更新**：插入/删除列后列序号不会自动调整
- **性能问题**：大数据量时计算缓慢
- **区分大小写**：默认不区分大小写

---

#### 2. INDEX-MATCH组合
**语法**：
```
=INDEX(return_range, MATCH(lookup_value, lookup_range, [match_type]))
```
- `INDEX`：返回指定位置的值
- `MATCH`：查找值的位置

**示例**：
```excel
=INDEX(C2:C100, MATCH("张三", A2:A100, 0))  // 在A列查找张三，返回C列对应值
```

**适用场景**：
- VLOOKUP的替代方案，更灵活
- 可以向左查找（查找列在返回列右侧）
- 多条件查找
- 动态列引用

**常见坑**：
- **数组公式**：多条件时需要按Ctrl+Shift+Enter
- **MATCH类型**：0=精确匹配，1=小于，-1=大于
- **范围不一致**：INDEX和MATCH的范围大小需匹配

**优势**：
- 可以向左、向右、向上、向下查找
- 计算效率更高
- 插入/删除列时公式不会出错

---

#### 3. SUMIFS函数
**语法**：
```
=SUMIFS(sum_range, criteria_range1, criteria1, [criteria_range2, criteria2], ...)
```

**示例**：
```excel
=SUMIFS(D2:D100, A2:A100, "销售部", B2:B100, ">2024-01-01")  // 统计销售部2024年后的销售额
```

**适用场景**：
- 多条件求和
- 按部门、地区、时间等维度统计
- 带筛选条件的销售数据分析

**常见坑**：
- **参数顺序**：求和范围必须第一个参数
- **条件格式**：日期条件需用引号括起来
- **通配符**：`*`匹配任意字符，`?`匹配单个字符
- **空值处理**：空单元格不参与计算

---

#### 4. COUNTIFS函数
**语法**：
```
=COUNTIFS(criteria_range1, criteria1, [criteria_range2, criteria2], ...)
```

**示例**：
```excel
=COUNTIFS(A2:A100, "男", B2:B100, ">=30")  // 统计30岁以上男性人数
```

**适用场景**：
- 多条件计数
- 人员统计分析
- 产品分类统计

---

#### 5. IF嵌套函数
**语法**：
```
=IF(logical_test, value_if_true, value_if_false)
```

**示例**：
```excel
=IF(A2>=90, "优秀", IF(A2>=80, "良好", IF(A2>=60, "及格", "不及格")))
```

**适用场景**：
- 成绩等级评定
- 绩效评级
- 条件分类

**常见坑**：
- **嵌套层数限制**：Excel 2016+支持64层嵌套，但建议简化逻辑
- **逻辑顺序**：从大到小或从小到大顺序要正确
- **替代方案**：多条件可用IFS函数（Excel 2019+）
- **性能问题**：过多嵌套影响可读性和性能

**优化方案**：
```excel
=IFS(A2>=90, "优秀", A2>=80, "良好", A2>=60, "及格", TRUE, "不及格")
```

---

#### 6. TEXT函数
**语法**：
```
=TEXT(value, format_text)
```

**示例**：
```excel
=TEXT(A2, "yyyy-mm-dd")  // 日期格式化
=TEXT(B2, "0.00%")  // 百分比格式化
=TEXT(C2, "#,##0.00")  // 千分位格式化
```

**适用场景**：
- 日期格式转换
- 数字格式化显示
- 字符串拼接时的格式控制

**常见坑**：
- **返回文本**：结果是文本格式，不能直接计算
- **本地化差异**：格式代码在不同语言版本Excel中可能不同

---

#### 7. 日期函数
**核心函数**：
```excel
=TODAY()  // 当前日期
=NOW()    // 当前日期和时间
=YEAR(日期)  // 提取年份
=MONTH(日期) // 提取月份
=DAY(日期)   // 提取日
=WEEKDAY(日期, [type])  // 星期几
=DATEDIF(开始日期, 结束日期, "Y/M/D")  // 计算日期差
=EDATE(日期, 月数)  // 计算几个月后的日期
=EOMONTH(日期, 月数)  // 计算月末
```

**示例**：
```excel
=DATEDIF(A2, TODAY(), "Y") & "年" & DATEDIF(A2, TODAY(), "YM") & "个月"  // 计算工龄
```

**适用场景**：
- 工龄计算
- 账期管理
- 项目周期计算

---

### 二、高级功能

#### 1. 数据透视表
**创建步骤**：
1. 选择数据区域（必须有标题行）
2. 插入 → 数据透视表
3. 拖拽字段到行、列、值区域

**核心功能**：
- **值字段设置**：求和、计数、平均值、最大值、最小值
- **筛选器**：切片器、报表筛选
- **计算字段**：自定义公式
- **分组**：日期分组、数值区间分组

**适用场景**：
- 销售数据分析
- 财务报表汇总
- 用户行为分析

**常见坑**：
- **数据源格式**：不能有合并单元格、空行、空列
- **刷新问题**：数据源增加后需手动刷新
- **缓存问题**：多个透视表共享缓存可能导致数据不一致
- **性能问题**：大数据量时响应慢

**最佳实践**：
- 使用表格功能（Ctrl+T）作为数据源
- 定期刷新数据
- 使用切片器增强交互性

---

#### 2. 条件格式
**常用规则**：
- **突出显示单元格规则**：大于、小于、介于、等于
- **数据条**：可视化数值大小
- **色阶**：颜色渐变表示数值大小
- **图标集**：用图标表示数据状态
- **新建规则**：使用公式

**公式示例**：
```excel
=$A2>$B2  // A列大于B列时高亮
=AND($A2>100, $B2<50)  // 多条件
=WEEKDAY($A2,2)>5  // 周末高亮
```

**适用场景**：
- 异常数据标记
- 进度跟踪
- 数据可视化

**常见坑**：
- **相对引用**：公式中的列要绝对引用，行要相对引用
- **规则优先级**：多个规则冲突时按优先级执行
- **性能影响**：过多条件格式会降低性能

---

#### 3. 数据验证
**设置方法**：
数据 → 数据验证 → 允许条件

**常用类型**：
- **整数/小数**：限制输入数值范围
- **列表**：下拉选择框
- **日期**：限制日期范围
- **文本长度**：限制字符数
- **自定义公式**：复杂验证逻辑

**示例**：
```excel
// 下拉列表
=INDIRECT("部门列表")  // 引用命名区域
=A1:A10  // 直接引用区域

// 自定义公式：禁止输入重复值
=COUNTIF(A:A, A1)=1
```

**适用场景**：
- 防止数据录入错误
- 标准化数据格式
- 提高数据质量

**常见坑**：
- **复制粘贴绕过**：复制粘贴可绕过验证
- **引用范围**：动态范围需用OFFSET或表格
- **错误提示**：需设置输入信息和出错警告

---

#### 4. Power Query
**核心功能**：
- **数据获取**：Excel、CSV、数据库、网页、文件夹
- **数据清洗**：删除列、填充空值、替换值、拆分列
- **数据转换**：数据类型转换、透视/逆透视、合并查询
- **追加查询**：合并多个文件
- **分组依据**：聚合计算

**典型工作流**：
1. 数据 → 获取数据 → 选择数据源
2. 在Power Query编辑器中清洗转换
3. 关闭并上载到工作表或数据模型

**适用场景**：
- 多文件数据合并
- 复杂数据清洗
- 自动化数据处理

**常见坑**：
- **步骤依赖**：步骤顺序影响结果
- **数据类型**：自动识别可能错误
- **刷新失败**：数据源路径改变后需重新连接
- **性能问题**：大数据量需优化查询步骤

---

## 第二部分：SQL核心技能

### 一、核心语法

#### 1. JOIN操作
**语法**：
```sql
SELECT columns
FROM table1
JOIN_TYPE table2 ON table1.column = table2.column
```

**JOIN类型**：
- **INNER JOIN**：只返回匹配的记录
- **LEFT JOIN**：返回左表所有记录 + 右表匹配记录
- **RIGHT JOIN**：返回右表所有记录 + 左表匹配记录
- **FULL JOIN**：返回两表所有记录
- **CROSS JOIN**：笛卡尔积

**示例**：
```sql
-- 内连接
SELECT e.name, d.dept_name
FROM employees e
INNER JOIN departments d ON e.dept_id = d.id;

-- 左连接
SELECT e.name, d.dept_name
FROM employees e
LEFT JOIN departments d ON e.dept_id = d.id
WHERE d.id IS NULL;  -- 找出未分配部门的员工
```

**适用场景**：
- 多表关联查询
- 数据整合分析

**常见坑**：
- **重复记录**：连接键不唯一导致数据膨胀
- **性能问题**：大表连接需加索引
- **NULL处理**：LEFT JOIN时右表字段可能为NULL
- **连接顺序**：优化器可能调整顺序，但复杂查询需手动优化

---

#### 2. 子查询
**类型**：
- **单行子查询**：返回一行一列
- **多行子查询**：返回多行一列（用IN、ANY、ALL）
- **多列子查询**：返回多列
- **相关子查询**：引用外部查询的值
- **嵌套子查询**：多层嵌套

**示例**：
```sql
-- IN子查询
SELECT name, salary
FROM employees
WHERE dept_id IN (SELECT id FROM departments WHERE location = '北京');

-- EXISTS子查询
SELECT name
FROM employees e
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.emp_id = e.id AND o.amount > 10000);

-- 相关子查询
SELECT e.name, e.salary
FROM employees e
WHERE e.salary > (SELECT AVG(salary) FROM employees WHERE dept_id = e.dept_id);
```

**适用场景**：
- 复杂过滤条件
- 分步查询逻辑
- 存在性检查

**常见坑**：
- **性能差**：相关子查询效率低
- **NULL值**：IN子查询中NULL值的影响
- **重复值**：EXISTS比IN更适合去重
- **可读性**：过度嵌套降低可读性

---

#### 3. 窗口函数
**语法**：
```sql
SELECT 
    column,
    WINDOW_FUNCTION(column) OVER (
        [PARTITION BY partition_column]
        [ORDER BY sort_column]
        [FRAME_CLAUSE]
    )
FROM table
```

**常用函数**：
- **排名函数**：ROW_NUMBER(), RANK(), DENSE_RANK(), NTILE()
- **偏移函数**：LAG(), LEAD(), FIRST_VALUE(), LAST_VALUE()
- **聚合函数**：SUM() OVER(), AVG() OVER(), COUNT() OVER()

**示例**：
```sql
-- 排名
SELECT name, salary, dept,
       ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rn
FROM employees;

-- 累计求和
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date) as running_total
FROM sales;

-- 同比计算
SELECT month, revenue,
       LAG(revenue, 12) OVER (ORDER BY month) as last_year_same_month,
       revenue / LAG(revenue, 12) OVER (ORDER BY month) - 1 as yoy_growth
FROM monthly_sales;
```

**适用场景**：
- 分组排名
- 累计计算
- 同比环比分析
- 移动平均

**常见坑**：
- **MySQL版本**：8.0+才支持窗口函数
- **性能**：大数据量时需优化PARTITION BY和ORDER BY
- **框架子句**：默认RANGE BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW

---

#### 4. CTE（公用表表达式）
**语法**：
```sql
WITH cte_name AS (
    SELECT ...
),
cte_name2 AS (
    SELECT ... FROM cte_name
)
SELECT * FROM cte_name2;
```

**递归CTE**：
```sql
WITH RECURSIVE cte_name AS (
    -- 锚点成员
    SELECT ... WHERE ...
    UNION ALL
    -- 递归成员
    SELECT ... FROM cte_name WHERE ...
)
SELECT * FROM cte_name;
```

**示例**：
```sql
-- 多层查询简化
WITH sales_summary AS (
    SELECT dept, SUM(amount) as total
    FROM orders
    GROUP BY dept
),
top_depts AS (
    SELECT dept, total
    FROM sales_summary
    WHERE total > 1000000
)
SELECT * FROM top_depts;

-- 递归查询组织结构
WITH RECURSIVE org_hierarchy AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE manager_id IS NULL
    UNION ALL
    SELECT e.id, e.name, e.manager_id, oh.level + 1
    FROM employees e
    JOIN org_hierarchy oh ON e.manager_id = oh.id
)
SELECT * FROM org_hierarchy ORDER BY level, id;
```

**适用场景**：
- 复杂查询分解
- 递归数据处理
- 提高可读性
- 替代子查询

**常见坑**：
- **递归深度**：可能超出递归限制
- **性能**：递归CTE性能较差
- **多次引用**：CTE不物化，多次引用会重复执行

---

#### 5. 聚合函数与分组
**语法**：
```sql
SELECT 
    group_column,
    AGGREGATE_FUNCTION(column)
FROM table
WHERE condition
GROUP BY group_column
HAVING condition
ORDER BY sort_column;
```

**聚合函数**：
- COUNT(), SUM(), AVG(), MAX(), MIN()
- COUNT(DISTINCT column)
- GROUP_CONCAT()（MySQL）、STRING_AGG()（SQL Server）

**示例**：
```sql
-- 多维度分组
SELECT 
    dept, 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(*) as order_count,
    SUM(amount) as total_amount,
    AVG(amount) as avg_amount
FROM orders
WHERE order_date >= '2024-01-01'
GROUP BY dept, DATE_FORMAT(order_date, '%Y-%m')
HAVING SUM(amount) > 100000
ORDER BY month, total_amount DESC;
```

**适用场景**：
- 数据统计汇总
- 报表生成

**常见坑**：
- **ONLY_FULL_GROUP_BY**：MySQL严格模式下非聚合列必须在GROUP BY中
- **HAVING vs WHERE**：WHERE过滤行，HAVING过滤组
- **性能**：大数据量分组需索引支持
- **NULL值**：GROUP BY会将NULL分为一组

---

#### 6. 索引优化
**索引类型**：
- **单列索引**：普通索引
- **复合索引**：多列组合
- **唯一索引**：列值唯一
- **主键索引**：特殊唯一索引
- **全文索引**：文本搜索

**创建索引**：
```sql
CREATE INDEX idx_name ON table(column1, column2);
CREATE INDEX idx_name ON table(column1 DESC, column2 ASC);  -- 指定排序
```

**使用原则**：
- WHERE、JOIN、ORDER BY字段优先建索引
- 复合索引遵循最左前缀原则
- 高基数列（唯一值多）建索引效果更好
- 避免在索引列上使用函数或运算

**示例**：
```sql
-- 分析查询性能
EXPLAIN SELECT * FROM orders WHERE customer_id = 100 AND order_date > '2024-01-01';

-- 创建复合索引
CREATE INDEX idx_customer_date ON orders(customer_id, order_date);
```

**常见坑**：
- **索引失效**：LIKE以%开头、OR条件、类型转换
- **维护成本**：增删改操作需维护索引
- **存储空间**：索引占用额外空间
- **过度索引**：不是越多越好

---

### 二、常用查询模式

#### 1. 排名分析
```sql
-- TOP N问题
SELECT * FROM (
    SELECT 
        name, score,
        ROW_NUMBER() OVER (ORDER BY score DESC) as rn
    FROM students
) ranked
WHERE rn <= 10;

-- 分组TOP N
SELECT * FROM (
    SELECT 
        dept, name, salary,
        ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) as rn
    FROM employees
) ranked
WHERE rn <= 3;
```

---

#### 2. 累计计算
```sql
-- 累计求和
SELECT 
    date, amount,
    SUM(amount) OVER (ORDER BY date) as cumulative_sum
FROM daily_sales;

-- 移动平均（近7天）
SELECT 
    date, amount,
    AVG(amount) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as ma7
FROM daily_sales;
```

---

#### 3. 同比环比分析
```sql
-- 环比（月环比）
WITH monthly_data AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') as month,
        SUM(amount) as revenue
    FROM orders
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    month, revenue,
    LAG(revenue, 1) OVER (ORDER BY month) as prev_month,
    ROUND(revenue / LAG(revenue, 1) OVER (ORDER BY month) - 1, 4) as mom_growth
FROM monthly_data
ORDER BY month;

-- 同比（年同比）
SELECT 
    month, revenue,
    LAG(revenue, 12) OVER (ORDER BY month) as same_month_last_year,
    ROUND(revenue / LAG(revenue, 12) OVER (ORDER BY month) - 1, 4) as yoy_growth
FROM monthly_data
ORDER BY month;
```

---

#### 4. 留存分析
```sql
-- 用户留存率（次月留存）
WITH monthly_users AS (
    SELECT 
        DATE_FORMAT(first_login, '%Y-%m') as cohort_month,
        user_id
    FROM users
),
user_activity AS (
    SELECT DISTINCT
        DATE_FORMAT(login_date, '%Y-%m') as active_month,
        user_id
    FROM user_logs
)
SELECT 
    mu.cohort_month,
    COUNT(DISTINCT mu.user_id) as total_users,
    COUNT(DISTINCT CASE WHEN ua.active_month = DATE_ADD(mu.cohort_month, INTERVAL 1 MONTH) 
                        THEN mu.user_id END) as month1_retained,
    ROUND(COUNT(DISTINCT CASE WHEN ua.active_month = DATE_ADD(mu.cohort_month, INTERVAL 1 MONTH) 
                              THEN mu.user_id END) * 100.0 / COUNT(DISTINCT mu.user_id), 2) as month1_retention_rate
FROM monthly_users mu
LEFT JOIN user_activity ua ON mu.user_id = ua.user_id 
    AND ua.active_month BETWEEN mu.cohort_month AND DATE_ADD(mu.cohort_month, INTERVAL 12 MONTH)
GROUP BY mu.cohort_month
ORDER BY mu.cohort_month;
```

---

#### 5. 漏斗分析
```sql
-- 转化漏斗（浏览→加购→下单→支付）
WITH funnel_steps AS (
    SELECT 
        user_id,
        MAX(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END) as viewed,
        MAX(CASE WHEN event_type = 'cart' THEN 1 ELSE 0 END) as added_to_cart,
        MAX(CASE WHEN event_type = 'order' THEN 1 ELSE 0 END) as ordered,
        MAX(CASE WHEN event_type = 'pay' THEN 1 ELSE 0 END) as paid
    FROM user_events
    WHERE event_date = '2024-01-15'
    GROUP BY user_id
)
SELECT 
    '浏览' as step,
    COUNT(*) as users,
    100.0 as conversion_rate
FROM funnel_steps WHERE viewed = 1

UNION ALL

SELECT 
    '加购' as step,
    COUNT(*) as users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM funnel_steps WHERE viewed = 1), 2) as conversion_rate
FROM funnel_steps WHERE added_to_cart = 1

UNION ALL

SELECT 
    '下单' as step,
    COUNT(*) as users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM funnel_steps WHERE viewed = 1), 2) as conversion_rate
FROM funnel_steps WHERE ordered = 1

UNION ALL

SELECT 
    '支付' as step,
    COUNT(*) as users,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM funnel_steps WHERE viewed = 1), 2) as conversion_rate
FROM funnel_steps WHERE paid = 1;
```

---

## 最佳实践总结

### Excel最佳实践
1. **数据规范**：使用表格（Ctrl+T）管理数据
2. **备份习惯**：定期备份重要文件
3. **公式优化**：避免整列引用（如A:A），使用精确范围
4. **命名管理**：使用命名区域提高可读性
5. **版本兼容**：考虑低版本Excel兼容性

### SQL最佳实践
1. **索引优化**：关键查询字段建立索引
2. **分页处理**：大数据查询使用LIMIT分页
3. **事务控制**：合理使用事务保证数据一致性
4. **SQL注入**：使用参数化查询防止注入
5. **性能监控**：定期分析慢查询日志

### 综合建议
1. **工具选择**：简单数据处理用Excel，复杂大数据用SQL
2. **数据验证**：重要数据双重验证
3. **文档记录**：记录数据处理逻辑
4. **自动化**：重复工作使用Power Query或脚本自动化
5. **持续学习**：关注新功能和新特性

---

*本文档总结了Excel和SQL在日常数据处理中的核心技巧和最佳实践，适用于数据分析师、业务分析师等相关岗位。*