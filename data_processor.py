import sys

class DataProcessor:
    
    def processingData(fileName, cocomoCode=1):
        with open(fileName, 'r') as file:
            rawDataset = file.readlines()
    
        data = [line.strip().split(',') for line in rawDataset]
        cocomoCode = 1
        columnNames = [ 
                       ['rely', 'data', 'cplx', 'time', 'stor', 'virt', 'turn', 'acap', 'aexp', 'pcap', 'vexp', 'lexp', 'modp', 'tool', 'sced', 'kloc', 'actualEffort'],
                       
                       ['prec', 'flex', 'resl', 'team', 'pmat', 'rely', 'data', 'cplx', 'ruse', 'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'apex', 'plex', 'ltex', 'tool', 'site', 'sced', 'kloc', 'actualEffort', 'defects', 'months'],
                       
                       ['rely', 'data', 'cplx', 'time', 'stor', 'virt', 'turn', 'acap', 'aexp', 'pcap', 'vexp', 'lexp', 'modp', 'tool', 'sced', 'kloc', 'actualEffort'],                       
        ]
        
        for key, val in enumerate(data):
            indexedTuple = {key: value for key, value in zip(columnNames[cocomoCode], val)}
            for indexName in indexedTuple:
                if indexName in ['kloc', 'actualEffort', 'defects', 'months']:
                    indexedTuple[indexName] = float(indexedTuple[indexName])
            data[key] = indexedTuple
        return data