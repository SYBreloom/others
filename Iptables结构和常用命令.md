## Iptables

### iptables处理传输数据包的过程

![img](https://upload-images.jianshu.io/upload_images/7775566-d1ad7de240451282.png?imageMogr2/auto-orient/strip|imageView2/2/w/729/format/webp)



进入网卡后，先prerouting，根据destination address判断是否把这个packet转发出去。



### iptables中的链 （5个）

PREROUTING，forward， Input，  Output ， POSTROUTING

#### 工作流程

- 到本机的报文： PREROUTING -> Input -> 用户空间
- 本机转发的报文： PREROUTING -> Forward -> POSTROUTING
- 本机发出的报文： Output -> POSTROUTING

### iptables 主要的表 （4个）

Filter表: 过滤

NAT表: 就是NAT.

Mangle表： 修改服务类型，配置TTL，实现QoS

Raw表：决定数据包是否被状态跟踪机制处理（用的很少）

### 表和链的关系

> 我们在实际的使用过程中，往往是通过"表"作为操作入口，对规则进行定义的

filter表只存在于input, output和forward三个链里面。

raw表 只有 PREROUTING, output

mangle每个都有

nat表三个链：PREROUTING、POSTROUTING、output

**只有output这个链里面，会有所有4个表的存在**

执行优先级： raw --> mangle --> nat --> filter

------

### 数据经过防火墙的流程

![iptables详解（1）：iptables概念](http://www.zsythink.net/wp-content/uploads/2017/02/021217_0051_6.png)

> 我们在写Iptables规则的时候，要时刻牢记这张路由次序图，灵活配置规则。

------

### 常用的处理动作

**ACCEPT**：允许数据包通过。

**DROP**：直接丢弃数据包，不给任何回应信息，这时候客户端会感觉自己的请求泥牛入海了，过了超时时间才会有反应。

**REJECT**：拒绝数据包通过，必要时会给数据发送端一个响应的信息，客户端刚请求就会收到拒绝的信息。

**SNAT**：源地址转换，解决内网用户用同一个公网地址上网的问题。

**MASQUERADE**：是SNAT的一种特殊形式，适用于动态的、临时会变的ip上。

**DNAT**：目标地址转换。

**REDIRECT**：在本机做端口映射。

**LOG**：在/var/log/messages文件中记录日志信息，然后将数据包传递给下一条规则，也就是说除了记录以外不对数据包做任何其他操作，仍然让下一条规则去匹配。

------

### 管理和设置iptables规则

![img](https://upload-images.jianshu.io/upload_images/7775566-fb35d0a138063159.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/690/format/webp)

![img](https://upload-images.jianshu.io/upload_images/7775566-736f5a5882a69420.jpg?imageMogr2/auto-orient/strip|imageView2/2/w/690/format/webp)

iptables [-t 表名] 命令选项 ［链名］ ［条件匹配］ ［-j 目标动作或跳转］


### 一些栗子

1.拒绝进入防火墙的所有ICMP协议数据包

```shell
$ iptables -I INPUT -p icmp -j REJECT
```

-I 表示insert，默认插入到最前面。-A表示append。
--insert -I chain [rulenum] default=1 

2.允许防火墙转发除ICMP协议以外的所有数据包

```shell
$ iptables -A FORWARD -p ! icmp -j ACCEPT
```

说明：使用“！”可以将条件取反。

3.拒绝转发来自192.168.1.10主机的数据，允许转发来自192.168.0.0/24网段的数据

```sh
$ iptables -A FORWARD -s 192.168.1.11 -j REJECT

$ iptables -A FORWARD -s 192.168.0.0/24 -j ACCEPT
```

说明：注意要把拒绝的放在前面不然就不起作用了啊。

10.禁止转发来自MAC地址为00：0C：29：27：55：3F的和主机的数据包

```shell
$ iptables -A FORWARD -m mac --mac-source 00:0c:29:27:55:3F -j DROP
```

说明：iptables中使用“-m 模块关键字”的形式调用显示匹配。咱们这里用“-m mac –mac-source”来表示数据包的源MAC地址。

- -m 模块关键字的形式出现的还是比较多的，需要查一下

23. 防止 DoS 攻击

```shell
$ iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT
```

例子转载自https://www.jianshu.com/p/ee4ee15d3658

### 更多栗子

https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html

里面包括了一些-m扩展字段的说明，比如--mac-source, --mac-d, --limit-burst

（其中--limit和--limit-burst用于to lessen the effects of DoS syn flood attack）

### iptables防火墙规则的保存与恢复

iptables-save把规则保存到文件中，再由目录rc.d下的脚本（/etc/rc.d/init.d/iptables）自动装载

使用命令iptables-save来保存规则。一般用c

```
iptables-save > /etc/sysconfig/iptables
```

生成保存规则的文件 /etc/sysconfig/iptables，

也可以用

```
service iptables save
```

它能把规则自动保存在/etc/sysconfig/iptables中。

当计算机启动时，rc.d下的脚本将用命令iptables-restore调用这个文件，从而就自动恢复了规则。



