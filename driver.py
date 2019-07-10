#! /usr/bin/env python
# -*- coding: utf-8 -

import time
import sys

# python driver.py ls
if 'ls' in sys.argv[1]:
    from ls_dir import Demo
# python driver.py system httpd
elif 'system' in sys.argv[1]:
    from system_status import Demo 
else:
    raise IndexError(
        "Cannot open the file: {arg}".format(arg=sys.argv[0])
    )



start = time.time()
obj = Demo()
import pdb; pdb.set_trace()
outputs = obj.main()
print('outputs:{outputs}'.format(outputs=outputs))
end = time.time()
print("process {timedelta} ms".format(
    timedelta = (end - start) * 1000
))