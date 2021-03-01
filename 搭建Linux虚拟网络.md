在Linux里用namespace, veth pair, bridge, NAT搭建虚拟网络

原网址：https://zhuanlan.zhihu.com/p/199298498

### 1. ip netns的基本操作

ip netns 创建network namespace 

```sh
$ sudo ip netns add red # 创建namespace
```

```sh
$ sudo ip netns ls  # 查看现有namespace
$ sudo ip netns del red  # 删除namespace
```

### 2. namespace之间通信，用veth pair创建虚拟的网线和网卡

使用linxu提供的`veth pair`  创建网线

```shell
$ ip link add veth-red type veth peer name veth-blue
```

两端网卡安装到netns中

```sh
$ ip link set veth-blue netns blue
$ ip link set veth-red netns red
```

赋予IP地址，然后up

```shell
$ ip netns exec red ip addr add 192.168.15.1/24 dev veth-red
$ ip netns exec red ip link set veth-red up
# 同样的对blue也需要进行操作
```

ip netns exec (name) 是选择具体的net namespace

删除方法：

```sh
$ sudo ip netns exec red ip link del veth-red # 只需要删除一端就可以了
```

### 3. 使用bridge连接不同的namespace

Linux 提供的虚拟交换机bridge.

```shell
$ ip link add vbridge-0 type bridge
$ ip link set dev vbridge-0 up   # 启动vbridge
```

同上，使用veth pair连接red和vbridge-0， blue和vbridge-0

```sh
$ ip link add veth-red type veth peer name veth-red-br
$ ip link add veth-blue type veth peer name veth blue-br
$ ip link set veth-red netns red
$ ip link set veth-red-br master vbridge-0
$ ip link set veth-blue netns blue
$ ip link set veth-blue-br master vbridge-0
```

然后同上配置ip地址，启动四个网卡（bridge的两个，两个veth分别一个）

默认情况下需要修改iptables, 修改对于bridge的禁用。

### 4. 使用bridge的路由模式连通namespace与host

启动bridge的路由功能，连接主机和网络空间的blue和red.

```shell
$ ip addr add 192.168.15.5/24 dev vbridge-0
```

如果要让red和blue可以ping通主机，需要给vbridge-0添加一条gateway的路由

```shell
$ ip netns exec red ip route add default via 192.168.15.5
```

总结：①配置vbridge的IP地址，使其具有路由功能；②设置ns的gateway

### 5.使用NAT连通namespace和公网

为了ping通8.8.8.8（Google提供的免费DNS地址），需要为Linux系统的eth0开通IP forward功能。

```shell
# 查看是否已经开启ip forward，0为关闭，1为开启
$ sysctl net.ipv4.ip_forward
net.ipv4.ip_forward = 0

# 开启ip forward
$ sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
```

通过iptables增加SNAT规则，将源ip为192.168.15.0/24内的数据包的源ip修改为eth0的ip：

```shell
$ iptables -t nat -A POSTROUTING -s 192.168.15.0/24 -j MASQUERADE
```

这样就可以让namespace连接到公网了

但是公网走到namesapce，比如ping 192.168.15.1 需要端口转发port-forwarding： DNAT

比如通过访问3.113.17.15:8083来访问192.168.15.1:80 其中3.113.17.15是公网IP， 192.168.15.1是namespace的IP

```shell
$ iptables -t nat -A PREROUTING -p tcp --dport 8083 -j DNAT --to-destination 192.168.15.1:80
```

### 总结

本文从network namespace出发，使用veth pair，bridge，NAT等虚拟网络设备和技术在一个Linux主机中搭建了一个虚拟网络，并实现了如下效果：

- 虚拟网络的设备直接可以互相访问；
- 虚拟网络的设备与主机之间可以互相访问；
- 虚拟网络的设备可以访问公网。