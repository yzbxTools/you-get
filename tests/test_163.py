#!/usr/bin/env python

import unittest
import os, sys

_srcdir = '%s/src/' % os.path.dirname(os.path.realpath(__file__))
_filepath = os.path.dirname(sys.argv[0])
sys.path.insert(1, os.path.join(_filepath, _srcdir))
sys.path.insert(1, os.path.abspath('src/'))

from you_get.extractors import (
    netease
)


class YouGetTests(unittest.TestCase):
    def test_netease(self):
        print(sys.path)
        netease.download('https://music.163.com/#/playlist?id=311692545', info_only=True)
                       
        netease.download('https://music.163.com/#/playlist?id=311692545', info_only=True)

if __name__ == '__main__':
    unittest.main()
