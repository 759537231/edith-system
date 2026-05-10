# 腾讯位置服务 Skill

## 功能
- POI 关键词搜索
- 周边搜索
- 智能旅游规划
- 轨迹可视化

## 使用方法

### 1. 搜索地点
用户：搜索「关键词」
生成链接：`https://map.qq.com/m/place/search?keyword=关键词`

### 2. 周边搜索
用户：「位置」周边「类别」
生成链接：`https://map.qq.com/m/place/search?keyword=类别&center=纬度,经度&radius=1000`

### 3. 旅游规划
用户：规划「城市」旅游，想去「景点列表」
生成链接：`https://map.qq.com/m/place/search?keyword=景点`

### 4. 坐标转地址
调用腾讯逆地理编码 API（需要 Key）：
`https://apis.map.qq.com/ws/geocoder/v1/?location=纬度,经度&key=你的Key`

## API Key 配置
如需完整功能，需要：
1. 访问 https://lbs.qq.com/dev/console/key/manage
2. 申请 Web Service Key
3. 将 Key 存入配置

## 示例
- 用户：「搜索附近的餐厅」→ 生成腾讯地图搜索链接
- 用户：「西直门周边美食」→ 生成带坐标的搜索链接
- 用户：「去北京旅游，故宫、颐和园」→ 生成旅游路线链接