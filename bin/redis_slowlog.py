#! /bin/env python
#-*- coding:utf8 -*-

import sys
import os
import time
import datetime
import redis

import logging
from  logging.config import logging

#import mysql.connector
#from mysql.connector import errorcode


class RedisSlowLog(object):
	"""Get the Redis slowlog size.
		if you want, please save the slowlog entries to database, then reset slowlog every 60 seconds. 

        Attributes:
                addr: Redis server hostname,as well as the Endpoint.
                port: Redis tcp port number.
                password: Redis require password, if not empty string.
                logger: logging	
	"""

	def __init__(self,addr,port,password,cluster_name,mysql_host,mysql_port,mysql_user,mysql_pass,mysql_database):

		self.addr = addr   
		self.port = port
		self.password = password

                logging.config.fileConfig("../conf/logging.ini")
                self.logger = logging.getLogger(__name__)
		
	"""	#记录redis slowlog的MySQL信息
                self.cluster_name = cluster_name
                self.mysql_host = mysql_host
                self.mysql_port = mysql_port
                self.mysql_user = mysql_user
                self.mysql_pass = mysql_pass
		self.mysql_database = mysql_database
	"""
	def get_slowlog_and_length(self):
		"""Get the Redis slowlog size.
		
		Returns:
			slowlog_len: The slowlog length.

		"""

		redis_cli = redis.StrictRedis(host=self.addr,port=self.port,password=self.password) 
		
		# get slowlog, SLOWLOG GET
		#self.redisSlowLog = redis_cli.slowlog_get()
	
		# get slowlog len
		slowlog_len = redis_cli.slowlog_len()   
		
		# reset slowlog , SLOWLOG RESET 
		#redis_cli.slowlog_reset()
	
		# retu slowlog length
		return (slowlog_len)

	"""def save_slowlog(self):
		#Store the redis slowlog entries in MySQL or MongoDB database.

		cnx = mysql.connector.connect(host=self.mysql_host, port=self.mysql_port, user=self.mysql_user, password=self.mysql_pass,database=self.mysql_database)
		cursor = cnx.cursor()
		add_slowlog = ("insert into t_slowlog(cluster_name,redis_host,f_port,slowlog_time,f_len,f_command) values(%s,%s,%s,%s, %s,%s) ")

		# 遍历slowlog 列表		
		for slowlog_item in self.redisSlowLog:
			
			run_time = slowlog_item["duration"]
			start_time = datetime.datetime.fromtimestamp(int(slowlog_item["start_time"])).strftime('%Y-%m-%d %H:%M:%S')
			slowlog_command = slowlog_item["command"]
			data_slowlog =(self.cluster_name,self.addr,self.port, start_time, run_time, slowlog_command)
			
			cursor.execute(add_slowlog,data_slowlog)
		cnx.commit()
		cursor.close()
		cnx.close() 
	"""
