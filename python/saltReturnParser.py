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


def get_salt_hots(hostsfile):
    if not os.path.isfile(hostsfile):
        raise IOError('not found hostsfile')
    with open(hostsfile) as f:
        return [line.strip() for line in f.readlines()]


def output_result(jfile, hostslist):
    parser = JsonFileParser(jfile)
    hostnum, failed_task_num = 0, 0
    return_hosts = []
    for js in parser.iparse():
        hostnum += 1
        host = js.keys()[0]
        return_hosts.append(host)

        if not isinstance(js[host], dict):
            print('Host {0}:\n\tresult: {1}'.format(change_color(host, 'yellow'),
                                                    change_color(js[host], 'red')))
            if js[host] is not True:
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
          '\n\tAll the hosts number: {0}'
          '\n\tReturned hosts number: {1}'
          '\n\tFailed tasks number: {2}'
          '\n\tNot Returned hosts:'.format(len(hostslist), hostnum, failed_task_num))
    no_return_hosts = set(hostslist).difference(set(return_hosts))
    for h in no_return_hosts:
        print('\t\t{0}'.format(change_color(h, 'red_dark')))

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} {1} {2}'.format(sys.argv[0], 'filename', 'hostsfile'))
        exit(1)

    output_result(os.path.abspath(sys.argv[1]),
                  get_salt_hots(os.path.abspath(sys.argv[2])))
