#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Carl
#

import json
import os
import re

class JsonParser(object):
	def __init__(self, jsonFile):

		if  not os.path.isfile(jsonFile):
			raise IOError('No Such file.')

		self.jf = jsonFile

	def jsonFileParser(self):
		with open(self.jf) as f:
			sMark, eMark = '{', '}'
			sMarkDict, eMarkDict = {sMark: 0}, {eMark: 0}
			pat = re.compile(r'{|}')
			lines = []
			for line in f:
				newline = line.strip('\n').strip('\t')
				lines.append(newline)

				ret = pat.findall(line)
				if ret:
					for i in ret:
						if i == sMark:
							sMarkDict[sMark] += 1
						elif i == eMark:
							eMarkDict[eMark] += 1

				if eMarkDict[eMark] != 0 and sMarkDict[sMark] == eMarkDict[eMark]:
					sMarkDict[sMark], eMarkDict[eMark] = 0, 0
#					print '\033[34m LINES(in jsonFileParser): %s \033[0m' % lines
					jobjs = self._returnJsonObj(lines)
					if jobjs:
						for js in jobjs:
							yield js
					else:
						yield False
					lines = []

	@staticmethod
	def _recurseParse(data):
		pat = re.compile(r'}\s*{')
		tmpList = []
#		print '\033[32mDATA(in _recurseParse): %s \033[0m' %data
		for v in data:
			tmpList.append(v)
			if pat.search(v):
				yield  ' '.join(tmpList)[:-1]
#				a = ' '.join(tmpList)[:-1]
#				print '\033[33mtmpList(in _recurseParse): %s\033[0m' %a
#				yield a
				tmpList = []
		yield ' '.join(tmpList)	
#		b = ' '.join(tmpList)	
#		print '\033[33mtmpList(in _recurseParse): %s\033[0m' %b
#		yield b
				
	@staticmethod
	def _returnJsonObj(lines):
		tmpResult = []
		idata = JsonParser._recurseParse(lines)
		for v in idata:
			v = v.strip().strip('\t')
			if not v.startswith('{'):
				v = '{' + v
			if not v.endswith('}'):
				v = v + '}'
			tmpResult.append(v)
			
#		print '\033[35mtmpResult(in _returnJsonObj): %s\033[0m' % tmpResult
		try:
			jobj = [json.loads(i) for i in tmpResult]
		except ValueError:
			return False
		return jobj

	def jsonFileCheck(self):
		ijson = self.jsonFileParser()
		for json in ijson:
			if not json:
				return False
		return True
			

if __name__ == '__main__':
	def test():	
		a = JsonParser(jsonFile='json.txt') 
		if a.jsonFileCheck():
			ijson = a.jsonFileParser()
			for i in ijson:
				print i
		else:
			print "The json file corrupt!"

	test()
