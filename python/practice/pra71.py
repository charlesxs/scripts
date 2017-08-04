#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import pymysql
import re
import readline
from functools import wraps

DEBUG = False

class ExitingError(Exception):
	pass

class DB(object):
	def __init__(self, host, 
				user, 
				password, 
				database='test', 
				port=3306, 
				charset='utf8', debug=DEBUG):
		if debug:
			print_color("yellow", "Debug: Connect Args %s %s %s %s %s %s"
						% (host, user, password, database, port, charset))

		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.port = port
		self.charset = charset

		self._conn = self.__connect()
		self._conn.autocommit(1)
		self._pat = re.compile(r'insert|update|delete', re.I)
	
	def __connect(self, debug=DEBUG):
		try:
			conn = pymysql.connect(self.host, 
								   self.user, 
								   self.password, 
								   self.database, 
								   self.port, 
								   charset=self.charset)
		except pymysql.Error as e:
			if debug:
				print_color("yellow", "Debug: Mysql connect Exception, %s" % e)
				return 1
			return 1
		return conn
	
	def query(self, sql, args=None, close=True, debug=DEBUG):
		if args: sql = sql % args

		if debug: print_color("yellow", "Debug: Query SQL, %s" % sql)

		cursor = self._conn.cursor()
		try:
			cursor.execute(sql)
			data = cursor.fetchall()	
		except pymysql.Error as e:
			self._conn.close()
			print("Error: %s" %e)
			return 1
		finally:
			cursor.close()
			if close: self._conn.close()

		if not self._pat.findall(sql):
			return data

#def check_value(func):
#	@wraps(func)
#	def wrapper(fn, *args, **kwargs):
#		if fn == "gender":
#			v = func(fn, *args, **kwargs)
#			if v not in (0, 1):
#				raise ValueError("Gender's valid values is 0 or 1.")
#		elif fn == "age":
#			v = func(fn, *args, **kwargs)
#			if v >= 100:
#				raise ValueError("Age's valid values less than 100.")
#		else:
#			v = func(fn, *args, **kwargs)
#		return v
#	return wrapper

def print_color(color, msg):
	if color == "red":
		print("\033[31m%s\033[0m" % msg)
	elif color == "green":
		print("\033[32m%s\033[0m" % msg)
	elif color == "yellow":
		print("\033[33m%s\033[0m" % msg)
	elif color == "bule":
		print("\033[34m%s\033[0m" % msg)
	else:
		print("Unknown Color.")

def check_value(fn, value):
	if fn == "gender":
		if value not in ('0', '1'):
			raise ValueError("Gender's valid values is 0(Female) or 1(Male).")
	elif fn == "age":
		if int(value) >= 100:
			raise ValueError("Age's valid values less than 100.")
	
#@check_value
def loop_input(fn, imsg, emsg):
	while True:
		v = input("%s: " % imsg)	

		if not v:
			print("%s" % emsg)
			continue
		elif v in ['exit', 'q', 'quit']:
			raise ExitingError("Exiting.")

		try:
			check_value(fn, v)
		except ValueError as e:
			print_color('red', "Error: %s" %e)
			continue
		else:
			return v
			break
	
def InputSu():
	while True:
		try:
			name = loop_input("name", "Enter the student's name", "Student's name not allow None.")
			gender = loop_input("gender", "Enter the student's gender", "Student's gender not allow None.")
			age = loop_input("age", "Enter the student's age", "Student's age not allow None.")
			sql = '''insert into student (sname, sgender, sage) values ("%s", "%s", %s)'''
			ret = db.query(sql, (name, gender, int(age)), close=False)
		except ExitingError as e:
			print_color("red", "System Exiting ...")
			db.query('select "exit";')
			break

		if ret != 1:
			print_color("green", "Student's infomation entering over ...")


def QuerySu():
	Gender = {'0': 'Female', '1': 'Male'}
	while True:
		name = input("Enter the student's name for query: ")
		sql = '''select * from test.student where sname = "%s";''' 
	
		if name in ["exit", "quit", "q", "Q"]:
			print_color("red", "System Exiting ...")
			break

		ret = db.query(sql, name, close=False)

		if not ret:
			print_color("red", "Not found this student from enter name.")
			continue

		for info in ret:
			sid, sname, sgender, sage = info
			sinfo = '''Student's ID: %s
Student's Name: %s
Sutdent's Gender: %s
Student's Age: %s ''' % (sid, sname, Gender[sgender], sage)
			print_color("yellow","Display students infomation." )
			print(sinfo)
			print_color("green", "="*30)
		
def main():
		cmdList = {'1': InputSu, '2': QuerySu}
		print("\033[1;38mWelcome to School Infomation Network\033[0m".center(100))
		print_color("yellow", "-"*100)
		resp = input('''		Press 1 for entering student's information
		Press 2 for query student's information

		Your Choice: ''')

		try:
			print()
			cmdList[resp]()
		except KeyError as e:
			print("Invalid input, Exiting...")
		
if __name__ == '__main__':
	dbinfo = ('127.0.0.1', 'root', '')			
	db = DB(*dbinfo)
	try:
		main()
	except KeyboardInterrupt:
		print()
		print_color("red", "System Exiting ...")

