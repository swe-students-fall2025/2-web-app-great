class Config:
    # 用于 session / flash 消息的密钥
    SECRET_KEY = "dev-secret-change-me"

    # 本地 MongoDB
    MONGO_URI = "mongodb://localhost:27017/loopu"

    # 如果要改成 Atlas，就换下面这个：
    # MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/loopu?retryWrites=true&w=majority"
