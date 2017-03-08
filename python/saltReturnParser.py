#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Charles
#

import json
import re
import os
import sys


# color define
class ColorDefine:
    RED_DARK = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    RED = '\033[35m'
    CYAN = '\033[36m'
    CLOSE_COLOR = '\033[0m'


class JsonFileParser(object):
    def __init__(self, jsonfile):
        if not os.path.isfile(jsonfile):
            raise IOError('No Such file.')

        self.jf = jsonfile
        self.left_bracket = re.compile(r'{')
        self.right_bracket = re.compile(r'}')

    def _parse_file(self):
        lb_length, rb_length = 0, 0
        tmplines = []
        with open(self.jf) as f:
            for line in f:
                tmplines.append(line)
                lb_length += len(self.left_bracket.findall(line))
                rb_length += len(self.right_bracket.findall(line))
                if lb_length - rb_length == 0:
                    yield ' '.join(tmplines)
                    tmplines = []
                    lb_length, rb_length = 0, 0
            if lb_length - rb_length != 0:
                raise Exception('corrupt json file')

    # @staticmethod
    # def _repl(match_obj):
    #     mstr = match_obj.group()
    #     if mstr == "'":
    #         return '"'
    #     elif mstr == '"':
    #         return "'"
    #     elif mstr == "\\":
    #         return '\\\\'
    #     else:
    #         return '\"{0}\"'.format(mstr)

    def iparse(self):
        for json_string in self._parse_file():
            # strs = re.sub(r'\'|"|(?<=: )[a-zA-Z]+(?=,)|\\|(?<=: )[a-zA-Z]+(?=})',
            #               self._repl, json_string)
            data = json.loads(json_string)
            yield data


def change_color(chars, color):
    return '{0}{1}{2}'.format(getattr(ColorDefine, color.upper()), chars, ColorDefine.CLOSE_COLOR)


def output_result(jfile):
    parser = JsonFileParser(jfile)
    hostnum, failed_task_num = 0, 0
    for js in parser.iparse():
        hostnum += 1
        for host in js:
            if not isinstance(js[host], dict):
                print('Host {0}:\n\tresult: {1}'.format(change_color(host, 'yellow'),
                                                        change_color(js[host], 'red')))
                failed_task_num += 1
                continue
            else:
                print('Host {0}:'.format(change_color(host, 'yellow')))

            for task in js[host]:
                result = js[host][task]['result']
                if result is True:
                    print('\ttask: {0}  result: {1}'.format(task, change_color(result, 'green')))
                else:
                    failed_task_num += 1
                    print('\ttask: {0}  result: {1}'.format(task, change_color(result, 'red')))

    print('\nSummary:'
          '\n\t有返回值的主机数: {0}'
          '\n\t执行失败的任务数: {1}'.format(hostnum, failed_task_num))

if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print('Usage: {0} {1}'.format(sys.argv[0], 'filename'))
    #     exit(1)

    jfile = os.path.abspath('result.txt')
    output_result(jfile)
