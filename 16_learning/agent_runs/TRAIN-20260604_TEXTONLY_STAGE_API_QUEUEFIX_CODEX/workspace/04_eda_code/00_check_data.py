import os
import json

base = '03_data'
if os.path.exists(base):
    result = {'data_dir': base, 'files': []}
    for root, dirs, files in os.walk(base):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), base)
            result['files'].append(rel)
    print(json.dumps(result))
else:
    print('{}')
