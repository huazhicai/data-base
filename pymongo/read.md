### 连接数据库

1. 简写, 默认的 localhost, 27017
client = MongoClient()

2. 指定端口和地址
client = MongoClient('localhost', 27017)

3. 使用URI
client = MongoClient('mongodb://localhost:27017/')