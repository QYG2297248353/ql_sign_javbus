### JavBus论坛签到脚本

#### 青龙面板配置

###### 依赖安装
Python
```bash
requests
beautifulsoup4
```

###### 环境变量准备

| 变量名             | 变量值获取方式                             | 必选 | 描述                                   |
|-----------------| ------------------------------------------ | ---- | -------------------------------------- |
| CLIENT_ID       | 系统设置>>应用设置>>创建应用(环境变量权限) | YES  | 青龙面板用户权限，用于添加修改环境变量 |
| CLIENT_SECRET   | 系统设置>>应用设置>>创建应用(环境变量权限) | YES  | 青龙面板用户权限，用于添加修改环境变量 |
| javbus_saltkey  | 请登录站点查看                             | YES  | 服务器加密                             |
| javbus_auth     | 请登录站点查看                             | YES  | 加密密钥                               |
| javbus_username | 用户名                                     | YES  | 效验签到用户                           |
| javbus_sign     | 签到记录                                   | 可选 | 自动生成记录                           |
| javbus_cookie   | 自动续期                                   | 可选 | 自动生成刷新记录                       |
| proxies_enable  | 开启代理                                   | 可选 | 默认 false，可选 true,false            |
| proxies_host    | 代理主机                                   | 可选 | ip 示例：127.0.0.1                     |
| proxies_port    | 代理端口                                   | 可选 | 7890                                   |
| javbus_sign_url | 签到地址                                   | 可选 | https://{{镜像地址}}.com/forum/        |

+ 获取加密盐

> javbus_saltkey
>
> F12 唤出开发者控制台 >> 应用 >> Cookie >> 获取 `xxx_xxx_saltkey`

![Snipaste_2023-11-09_17-55-46](readme.assets/Snipaste_2023-11-09_17-55-46.png)

+ 获取授权密钥

> javbus_auth
>
> 可参考上方 ：`xxx_xxx_auth`

```sh
# 方案一(获取并复制)：
copy(document.cookie.match(/4fJN_2132_auth=([^;]+)/)[1]); console.log(document.cookie.match(/4fJN_2132_auth=([^;]+)/)[1]);

# 方案二(仅输出)
document.cookie.match(/4fJN_2132_auth=([^;]+)/)[1];
```



###### 一键订阅
```bash
ql repo https://github.com/QYG2297248353/ql_sign_javbus.git "auto_sign_javbus" "" "qlApi"
```
