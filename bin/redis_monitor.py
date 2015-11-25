#! /bin/env python
#-*- coding:utf8 -*
import json
import time
import socket
import re
import yaml
import requests
import redis
import logging
from  logging.config import logging

from redis_server import RedisServer
from redis_cluster import RedisClusterInfo
from redis_slowlog import RedisSlowLog


falcon_client = "http://127.0.0.1:1988/v1/push"
upload_ts = int(time.time())
calculate_metric_dict = {
		"total_connections_received" : "COUNTER",
		"rejected_connections" : "COUNTER",
		"keyspace_hits" : "COUNTER",
		"keyspace_misses" : "COUNTER",
		"total_commands_processed" : "COUNTER",
		"total_net_input_bytes" : "COUNTER",              
		"total_net_output_bytes" : "COUNTER",
		"expired_keys" : "COUNTER",
		"evicted_keys" : "COUNTER",
		"used_cpu_sys" : "COUNTER",
		"used_cpu_user" : "COUNTER",
		"slowlog_len" : "COUNTER"
		}

class RedisFalconMonitor(object):
	"""

	"""	
	def __init__(self,addr,port,password,cluster_name):
		self.addr = addr
		self.port = port
		self.password = password
		self.tags = "redis=" + str(port) + "_" + cluster_name  
		self.cluster_name = cluster_name
		logging.config.fileConfig("../conf/logging.ini")
		self.logger = logging.getLogger(__name__)

	def ping_redis(self):
		redis_is_alive = 0
		try:
			redis_cli = redis.StrictRedis(host=self.addr ,port=self.port,password=self.password,socket_timeout=0.5)
                        ping_res = redis_cli.ping()
                        if(ping_res):
                        	redis_is_alive = 1
		except redis.exceptions.ConnectionError,ex:
                       	self.logger.error(ex)
		except redis.exceptions.AuthenticationError,ex:
			self.logger.error(ex)
		except redis.exceptions.ResponseError,ex:
			self.logger.error(ex)
		except Exception,ex:
                	self.logger.error(ex)
		if  redis_is_alive == 0 : # If redis is dead, update the alive metrice here.
			redis_alive_data = [{"endpoint":self.addr, "metric": "redis_alive", "tags":self.tags , "timestamp":upload_ts, "value":redis_is_alive, "step": 60, "counterType": "GAUGE"}]        
        		r = requests.post(falcon_client,data=json.dumps(redis_alive_data))
			self.logger.debug(r.text)
		return redis_is_alive 
			
	def send_data(self):
		#创建实例	
		redis_server_info = RedisServer(self.addr,self.port,self.password)
	
		#处理后的info dict		
		redis_server_info_dict = redis_server_info.collect_info_data() 
		
		# redis server info dict  
		redis_info_dict = redis_server_info_dict

		#Redis slowlog len
		redis_slowlog = RedisSlowLog(self.addr,self.port,self.password,self.cluster_name,"","","","","")
		redis_slowlog_len = redis_slowlog.get_slowlog_and_length()
		redis_info_dict["slowlog_len"] = redis_slowlog_len	
	
		#redis cluster info信息采集	
		if (redis_server_info_dict.has_key("cluster_enabled") ):	
			if ( redis_server_info_dict["cluster_enabled"] == 1 ):
				redis_cluster_info = RedisClusterInfo(self.addr,self.port,self.password)
				redis_cluser_info_dict = redis_cluster_info.collect_cluster_info()
				redis_info_dict.update(redis_cluser_info_dict)
                redis_update_list = []  # The upload info list
	
		# Redis is Alive
		redis_info_dict["redis_alive"] = 1 
	       
		for info_key in redis_info_dict.keys():
			# 计算的key, 采用COUNTER, 注意cmdstat开头的命令
			calculate_keys = calculate_metric_dict.keys()
			if ( info_key in calculate_keys or re.match("^cmdstat",info_key)):
				key_item_dict = {"endpoint": self.addr, "metric": info_key, "tags": self.tags, "timestamp":upload_ts, "value": redis_info_dict[info_key], "step": 60, "counterType": "COUNTER"}
			else:
                       		key_item_dict = {"endpoint": self.addr, "metric": info_key, "tags": self.tags, "timestamp":upload_ts, "value": redis_info_dict[info_key], "step": 60, "counterType": "GAUGE"}
		        redis_update_list.append(key_item_dict)
		r = requests.post(falcon_client,data=json.dumps(redis_update_list))

def main():
	redis_hostname = socket.gethostname()
	f=open("../conf/redismon.conf")
	y = yaml.load(f)
	f.close()
	redis_items = y["items"]
	for redis_ins in redis_items:
		redis_clusterName = redis_ins["cluster_name"]
		redis_port = redis_ins["port"]
		redis_password = redis_ins["password"]
		redis_falcon_monitor = RedisFalconMonitor(redis_hostname, redis_port,redis_password,redis_clusterName)
		redis_is_alive = redis_falcon_monitor.ping_redis()
		if(redis_is_alive == 0):
			continue
		redis_falcon_monitor.send_data()

if __name__ == '__main__':
	main()
