# 包含可信第三方的部署

**声明**：一切以[隐语官方文档](https://www.secretflow.org.cn/zh-CN/docs/scql/0.5.0b2/topics)为准

官方部署文档有的地方说的不太清楚，我把自己的一点个人理解和自己的部署流程写在下面作为参考（）

## scql系统基本架构

![image](https://github.com/DINOREXNB/dinorexnb.github.io/blob/main/docs/images/xxaq1-1.png?raw=true){width=400}

简单来说就是两个参与方想要用双方的数据进行一些“操作”，于是他们将自己的数据放进scql系统当中取进行计算从而得到他们想要的查询结果

在这个查询过程当中，`scql`系统中的`SCDB`负责转化用户的查询语句转化“执行图”(我把他理解为一种计算任务)；然后把计算任务下发给各个参与查询的`SCQLEngine`。而`SCQLEngine`则会执行下发的计算任务，在本机进行计算后将计算结果发送给`SCDB`

## 部署流程（多机部署）

这里的话大部分和[官方部署文档](https://www.secretflow.org.cn/zh-CN/docs/scql/0.5.0b2/topics/deployment/how-to-deploy-centralized-cluster#step-1-deploy-scqlengine)步骤大同小异，主要在配置本地的数据集，还有用户注册上做了一些说明

### 配置引擎

```
--listen_port=8080
--datasource_router=embed
--enable_driver_authorization=false
--server_enable_ssl=false
--driver_enable_ssl_as_client=false
--peer_engine_enable_ssl_as_client=false
--embed_router_conf={"datasources":[{"id":"ds001","name":"mysql db","kind":"MYSQL","connection_str":"db=alice;user=root;password=__MYSQL_ROOT_PASSWORD__;host=mysql;auto-reconnect=true"}],"rules":[{"db":"*","table":"*","datasource_id":"ds001"}]}
# party authentication flags
--enable_self_auth=true
--enable_peer_auth=true
--private_key_pem_path=/home/admin/engine/conf/ed25519key.pem
--authorized_profile_path=/home/admin/engine/conf/authorized_profile.json
```

如果要在使用本地mysql的数据集需要修改`embed_router_conf`项

```
"datasources": [
  {
    "id": "ds001",
    "name": "mysql db for scql",
    "kind": "MYSQL",
    "connection_str": "${connection_str}"
  }
],
"rules":[
  {
    "db": "*",
    "table": "*",
    "datasource_id": "ds001"
  }
]
```

- `connection_str`一项可以参考如下配置，其中`db`为你的数据库名称，`user`是你的数据库的用户名（一般为`root`），`password`是连接数据库的密码，`host`是主机名称/IP地址（一般为`localhost:3306`）

```
db=${db};user=${user};password=${password};host=${host}
```

### 身份验证文件

> scql 0.3.0b1版本重构去除了GRM，使用公私钥验证来保证安全，因此engine、scdb都需要依赖额外的公私钥

```bash
# 生成私钥
openssl genpkey -algorithm ed25519 -out ed25519key.pem

# 从私钥文件中提取公钥，并将其输出为DER格式，然后对DER格式的公钥进行Base64编码
openssl pkey -in ed25519key.pem  -pubout -outform DER | base64

# 链接疑似失效（）
wget https://raw.githubusercontent.com/secretflow/scql/main/examples/scdb-tutorial/engine/alice/conf/authorized_profile.json
```

官方文档在这里用[`openssl`](https://zh.wikipedia.org/wiki/OpenSSL)生成了一个私钥存储在`ed25519key.pem`文件里，文档的意思应该是要让你手动把非己方的公钥放到`authorized_profile.json`这个文件里面作为参与方身份验证；这个配置文件的`parties`数组内应该是可以添加多个参与方，如果有新用户(比如`carol`)进来，就在每个旧用户的这个配置文件后面添加新用户的公钥即可（新用户的配置文件内也要添加所有旧用户的公钥）

- alice方的`authorized_json.profile`内容如下

```
{
    "parties": [
        {
            "party_code": "bob",
            "public_key": "__BOB_PUBLIC_KEY__"
        }
    ]
}
```

- bob方的`authorized_json.profile`内容如下

```
{
    "parties": [
        {
            "party_code": "alice",
            "public_key": "__ALICE_PUBLIC_KEY__"
        }
    ]
}
```

## 客户端上的用户创建

https://github.com/secretflow/scql/blob/3d1294a93a54f291485f91ba32e1abf55b9e93f0/cmd/scqltool/main.go