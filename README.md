Redis monitor plugin for Open-Falcon
------------------------------------
------------------------------------
功能支持
------------------
已测试的Redis版本2.2.15, 2.4.16, 2.6.14, 2.8.23, 3.0.0.

采集Redis基础状态信息, Redis复制,Redis Cluster, slowlog,所有cmdstat_xx命令执行频率等; 支持单机多实例;

暂不支持Sentinel(哨兵)的监控

环境需求
-----------------
操作系统: Linux

Python > 2.6

PyYAML > 3.10

redis-py > 2.10

python-requests > 0.11

redismon部署
--------------------------
1 目录解压到/path/to/redismon 

2 配置当前服务器的Redis多实例信息,/path/to/redismon/conf/redismon.conf 每行记录一个实例: 集群名，密码，端口

- {cluster_name: cluster_1, password: '', port: 6379}

3 配置crontab, 修改redismon_cron文件中redismon安装path; cp redismon_cron /etc/cron.d/ 

4 查看日志文件/path/to/redismon/log/redismon.log, 如无异常信息，表示采集正常；几分钟后，可从open-falcon的dashboard中查看redis metric

5 endpoint默认是hostname

采集的Redis指标
----------------------------------------

--------------------------------
| Counters | Type | Notes|
|-----|------|------|
|aof_current_rewrite_time_sec  |GAUGE|当前AOF重写持续的耗时|
|aof_enabled                   |GAUGE| appenonly是否开启,appendonly为yes则为1,no则为0|
|aof_last_bgrewrite_status     |GAUGE|最近一次AOF重写操作是否成功|
|aof_last_rewrite_time_sec     |GAUGE|最近一次AOF重写操作耗时|
|aof_last_write_status         |GAUGE|最近一次AOF写入操作是否成功|
|aof_rewrite_in_progress       |GAUGE|AOF重写是否正在进行|
|aof_rewrite_scheduled         |GAUGE|AOF重写是否被RDB save操作阻塞等待|
|blocked_clients               |GAUGE|正在等待阻塞命令（BLPOP、BRPOP、BRPOPLPUSH）的客户端的数量|
|client_biggest_input_buf      |GAUGE|当前客户端连接中，最大输入缓存|
|client_longest_output_list    |GAUGE|当前客户端连接中，最长的输出列表|
|cluster_enabled               |GAUGE|是否启用Redis集群模式，cluster_enabled|
|cluster_known_nodes           |GAUGE|集群中节点的个数|
|cluster_size                  |GAUGE|集群的大小，即集群的分区数个数|
|cluster_slots_assigned        |GAUGE|集群中已被指派slot个数，正常是16385个|
|cluster_slots_fail            |GAUGE|集群中已下线（客观失效）的slot个数|
|cluster_slots_ok              |GAUGE|集群中正常slots个数|
|cluster_slots_pfail           |GAUGE|集群中疑似下线（主观失效）的slot个数|
|cluster_state                 |GAUGE|集群的状态是否正常|
|cmdstat_auth                  |COUNTER|auth命令每秒执行次数|
|cmdstat_config                |COUNTER|config命令每秒执行次数|
|cmdstat_get                   |COUNTER|get命令每秒执行次数|
|cmdstat_info                  |COUNTER|info命令每秒执行次数|
|cmdstat_ping                  |COUNTER|ping命令每秒执行次数|
|cmdstat_set                   |COUNTER|set命令每秒执行次数|
|cmdstat_slowlog               |COUNTER|slowlog命令每秒执行次数|
|connected_clients             |GAUGE|当前已连接的客户端个数|
|connected_clients_pct         |GAUGE|已使用的连接数百分比，connected_clients/maxclients |
|connected_slaves              |GAUGE|已连接的Redis从库个数|
|evicted_keys                  |COUNTER|因内存used_memory达到maxmemory后，每秒被驱逐的key个数|
|expired_keys                  |COUNTER|因键过期后，被惰性和主动删除清理key的每秒个数|
|hz			       |GAUGE|serverCron执行的频率，默认10，表示100ms执行一次，建议不要大于120|
|instantaneous_input_kbps      |GAUGE|瞬间的Redis输入网络流量(kbps)|
|instantaneous_ops_per_sec     |GAUGE|瞬间的Redis操作QPS|
|instantaneous_output_kbps     |GAUGE|瞬间的Redis输出网络流量(kbps)|
|keys                          |GAUGE|当前Redis实例的key总数|
|keyspace_hit_ratio            |GAUGE|查找键的命中率（每个周期60sec精确计算)|
|keyspace_hits                 |COUNTER|查找键命中的次数|
|keyspace_misses               |COUNTER|查找键未命中的次数|
|latest_fork_usec              |GAUGE|最近一次fork操作的耗时的微秒数(BGREWRITEAOF,BGSAVE,SYNC等都会触发fork),当并发场景fork耗时过长对服务影响较大|
|loading		       |GAUGE|标志位，是否在载入数据文件|
|master_repl_offset            |GAUGE|master复制的偏移量，除了写入aof外，Redis定期为自动增加|
|mem_fragmentation_ratio       |GAUGE|内存碎片率，used_memory_rss/used_memory|
|pubsub_channels               |GAUGE|目前被订阅的频道数量|
|pubsub_patterns               |GAUGE|目前被订阅的模式数量|
|rdb_bgsave_in_progress        |GAUGE|标志位，记录当前是否在创建RDB快照|
|rdb_current_bgsave_time_sec   |GAUGE|当前bgsave执行耗时秒数|
|rdb_last_bgsave_status        |GAUGE|标志位，记录最近一次bgsave操作是否创建成功|
|rdb_last_bgsave_time_sec      |GAUGE|最近一次bgsave操作耗时秒数|
|rdb_last_save_time            |GAUGE|最近一次创建RDB快照文件的Unix时间戳|
|rdb_changes_since_last_save   |GAUGE|从最近一次dump快照后，未被dump的变更次数(和save里变更计数器类似)|
|redis_alive                   |GAUGE|当前Redis是否存活，ping监控socket_time默认500ms|
|rejected_connections          |COUNTER|因连接数达到maxclients上限后，被拒绝的连接个数|
|repl_backlog_active           |GAUGE|标志位，master是否开启了repl_backlog,有效地psync(2.8+)|
|repl_backlog_first_byte_offset|GAUGE|repl_backlog中首字节的复制偏移位|
|repl_backlog_histlen          |GAUGE|repl_backlog当前使用的字节数|
|repl_backlog_size             |GAUGE|repl_backlog的长度(repl-backlog-size)，网络环境不稳定的，建议调整大些
|role                          |GAUGE|当前实例的角色：master 1， slave 0|
|master_link_status            |GAUGE|标志位,从库复制是否正常，正常1，断开0|
|master_link_down_since_seconds|GAUGE|从库断开复制的秒数|
|slave_read_only	       |GAUGE|从库是否设置为只读状态，避免写入|
|slowlog_len                   |COUNTER|slowlog的个数(因未转存slowlog实例，每次采集不会slowlog reset，所以当slowlog占满后，此值无意义)|
|sync_full                     |GAUGE|累计Master full sync的次数;如果值比较大，说明常常出现全量复制，就得分析原因，或调整repl-backlog-size|
|sync_partial_err              |GAUGE|累计Master pysync 出错失败的次数|
|sync_partial_ok               |GAUGE|累计Master psync成功的次数|
|total_commands_processed      |COUNTER|每秒执行的命令数，比较准确的QPS|
|total_connections_received    |COUNTER|每秒新创建的客户端连接数|
|total_net_input_bytes         |COUNTER|Redis每秒网络输入的字节数|
|total_net_output_bytes        |COUNTER|Redis每秒网络输出的字节数|
|uptime_in_days                |GAUGE|Redis运行时长天数|
|uptime_in_seconds	       |GAUGE|Redis运行时长的秒数|
|used_cpu_sys                  |COUNTER|Redis进程消耗的sys cpu|
|used_cpu_user                 |COUNTER|Redis进程消耗的user cpu|
|used_memory                   |GAUGE|由Redis分配的内存的总量，字节数|
|used_memory_lua               |GAUGE|lua引擎使用的内存总量，字节数；有使用lua脚本的注意监控|
|used_memory_pct               |GAUGE|最大内存已使用百分比,used_memory/maxmemory; 存储场景无淘汰key注意监控.(如果maxmemory=0表示未设置限制,pct永远为0)|
|used_memory_peak              |GAUGE|Redis使用内存的峰值，字节数|
|used_memory_rss               |GAUGE|Redis进程从OS角度分配的物理内存，如key被删除后，malloc不一定把内存归还给OS,但可以Redis进程复用|

建议设置监控告警项
-----------------------------
说明:系统级监控项由falcon agent提供；监控触发条件根据场景自行调整
--------------------------------
| 告警项 | 触发条件 | 备注|
|-----|------|------|
|load.1min|all(#3)>10|Redis服务器过载，处理能力下降|
|cpu.idle |all(#3)<10|CPU idle过低，处理能力下降|
|df.bytes.free.percent|all(#3)<20|磁盘可用空间百分比低于20%，影响从库RDB和AOF持久化|
|mem.memfree.percent|all(#3)<15|内存剩余低于15%，Redis有OOM killer和使用swap的风险|
|mem.swapfree.percent|all(#3)<80|使用20% swap,Redis性能下降或OOM风险|
|net.if.out.bytes|all(#3)>94371840|网络出口流量超90MB,影响Redis响应|
|net.if.in.bytes|all(#3)>94371840|网络入口流量超90MB,影响Redis响应|
|disk.io.util|all(#3)>90|磁盘IO可能存负载，影响从库持久化和阻塞写|
|redis.alive|all(#2)=0|Redis实例存活有问题，可能不可用|
|used_memory|all(#2)>32212254720|单实例使用30G，建议拆分扩容；对fork卡停，full_sync时长都有明显性能影响|
|used_memory_pct|all(#3)>85|(存储场景)使用内存达85%,存储场景会写入失败|
|mem_fragmentation_ratio|all(#3)>2|内存碎片过高(如果实例比较小，这个指标可能比较大，不实用)|
|connected_clients|all(#3)>5000|客户端连接数超5000|
|connected_clients_pct|all(#3)>85|客户端连接数占最大连接数超85%|
|rejected_connections|all(#1)>0|连接数达到maxclients后，创建新连接失败|
|total_connections_received|每秒新创建连接数超5000，对Redis性能有明显影响，常见于PHP短连接场景|
|master_link_status>|all(#1)=0|主从同步断开；会全量同步，HA/备份/读写分离数据最终一致性受影响|
|slave_read_only|all(#1)=0|从库非只读状态|
|repl_backlog_active|all(#1)=0|repl_backlog关闭，对网络闪断场景不能psync|
|keys|all(#1)>50000000|keyspace key总数5千万，建议拆分扩容|
|instantaneous_ops_per_sec|all(#2)>30000|整体QPS 30000,建议拆分扩容|
|slowlog_len|all(#1)>10|1分钟中内，出现慢查询个数(一般Redis命令响应大于1ms，记录为slowlog)|
|latest_fork_usec|all(#1)>1000000|最近一次fork耗时超1秒(其间Redis不能响应任何请求)|
|keyspace_hit_ratio|all(#2)<80|命中率低于80%|
|cluster_state|all(#1)=0|Redis集群处理于FAIL状态，不能提供读写|
|cluster_slots_assigned|all(#1)<16384|keyspace的所有数据槽未被全部指派，集群处理于FAIL状态|
|cluster_slots_fail|all(#1)>0|集群中有槽处于失败，集群处理于FAIL状态|

Contributors
------------------------------------------
- 卓汝林: QQ:570923416; weibo: http://weibo.com/u/2540962412
