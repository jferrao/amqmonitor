import sys
from xml.dom.minidom import parse, parseString


relevant_keys = {
    'broker': [
        'consumerCount',
        'enqueueCount',
        'dequeueCount',
        'averageEnqueueTime',
        'minEnqueueTime',
        'maxEnqueueTime',
        'storeUsage',
        'storePercentUsage',
        'memoryUsage',
        'memoryPercentUsage'
    ],
    'queue': [
        'destinationName',
        'size',
        'consumerCount',
        'enqueueCount',
        'dequeueCount',
        'averageEnqueueTime',
        'maxEnqueueTime']
}


dom = parse('queue.xml')
stats = dict()

# Parse message into a dictionary
for entry in dom.getElementsByTagName('entry'):
    stats[entry.childNodes[1].childNodes[0].data] = entry.childNodes[3].childNodes[0].data if entry.childNodes[3].childNodes else None

# Identify the stats type
if 'vm' in stats:
    stats_type = 'broker'
elif 'selector' in stats:
    # not implemented
    stats_type = 'subscription'
elif 'size' in stats:
    stats_type = 'queue'
else:
    stats_type = None

stats = {key: stats[key] for key in relevant_keys.get(stats_type)}

for key, value in stats.iteritems():
    print key, value

