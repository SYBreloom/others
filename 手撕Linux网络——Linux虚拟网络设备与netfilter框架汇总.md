## 手撕Linux网络——Linux虚拟网络设备与netfilter框架汇总

https://zhuanlan.zhihu.com/p/223038075

### Linux 虚拟网络设备

### 1. TAP/TUN

TAP/TUN设备是一种让用户态程序向内核协议栈注入数据的设备，TAP等同于一个以太网设备，工作在二层；而TUN则是一个虚拟点对点设备，工作在三层。

### 2.veth

成对出现，用于连接两个network namespace

```
$ ip link add veth-a type veth peer name veth-b
```

删除的时候只需要删除其中一个就可以了

### 3.bridge

提供类似物理交换机设备的工作。默认工作再二层，可以分配IP地址，开启三层工作模式。

### 4.vlan

基本原理是在二层协议里插入VLAN协议数据，对物理上相互连接的设备进行逻辑网络切割

【todo】 这里有一个basic knowledge的文章



### 5.Netfilter框架分析

netfilter是linux内核中的一个数据包处理框架，它的功能包括数据包过滤，修改，SNAT/DNAT等

> 云计算底层技术-netfilter框架研究 
> https://opengers.github.io/openstack/openstack-base-netfilter-framework-overview/

