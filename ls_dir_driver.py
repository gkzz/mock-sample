#! /usr/bin/env python
# -*- coding: utf-8 -

import time

from ls_dir import Demo

start = time.time()
obj = Demo()
outputs = obj.main()
print('outputs:{outputs}'.format(outputs=outputs))
end = time.time()
print("process {timedelta} ms".format(
    timedelta = (end - start) * 1000
))