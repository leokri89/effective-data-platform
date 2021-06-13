
seen = set()

flist = ['/path/to/file/dataset_{}.json'.format(x) for x in range(8)]

with open('/path/to/file/result_0.json','w') as fout:
    for file in flist:
        with open(file) as fin:
            for line in fin:
                id = hash(line)
                if id not in seen:
                    fout.write(line)
                    seen.add(id)
