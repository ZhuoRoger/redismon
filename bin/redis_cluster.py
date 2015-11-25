#! /bin/env python
#-*- coding:utf8 -*-

import sys
import time
import commands

import logging
from  logging.config import logging

class RedisClusterInfo(object):
	"""Fetches the Redis Cluster metrice, "cluster info".
  
	Attributes:
                addr: Redis server hostname,as well as the Endpoint.
		port: Redis tcp port number.
                password: Redis require password, if not empty string.
 		logger: logging
          """	
	def __init__(self,addr,port,password):
                self.addr = addr
                self.port = port
                self.password = password
                self.tags = "redis="+ str(port)   

                logging.config.fileConfig("../conf/logging.ini")
                self.logger = logging.getLogger(__name__)

	def collect_cluster_info(self):
		"""Collect cluster info metrics.
			"The redis-cli must be in the command PATH!!!"		

		Returns:
			cluster_info_dict: redis cluster metrics dict.
		"""	
		cluster_command = "redis-cli -h " + self.addr + " -p " + str(self.port) + " --password " + self.password  + "cluster info"
		if (self.password == ""):	# If password is empty, replcate the password arg
			cluster_command = cluster_command.replace("--password"," ")
		cluster_info = commands.getoutput(cluster_command)	
		cluster_info_list =  cluster_info.replace("\r\n"," ").replace("\r","").split(" ")
		
		cluster_info_dict_all = {}	
		cluster_info_dict = {}
		for cluster_info_time in cluster_info_list:
			item_list = cluster_info_time.split(":")
			cluster_info_dict_all[item_list[0]] = item_list[1]
		# clear the cluster info 
		if cluster_info_dict_all.has_key("cluster_state"):
	
			if (cluster_info_dict_all["cluster_state"] == "ok" ):
		
				cluster_info_dict["cluster_state"] = 1
		else:
			 cluster_info_dict["cluster_state"] = 0
		cluster_info_dict["cluster_slots_assigned"] = cluster_info_dict_all["cluster_slots_assigned"]
		cluster_info_dict["cluster_slots_ok"] = cluster_info_dict_all["cluster_slots_ok"]
		cluster_info_dict["cluster_slots_pfail"] = cluster_info_dict_all["cluster_slots_pfail"]
		cluster_info_dict["cluster_slots_fail"] = cluster_info_dict_all["cluster_slots_fail"]
		cluster_info_dict["cluster_known_nodes"] = cluster_info_dict_all["cluster_known_nodes"]
		cluster_info_dict["cluster_size"] = cluster_info_dict_all["cluster_size"]		
	
		return cluster_info_dict

