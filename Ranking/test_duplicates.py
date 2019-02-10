import json

with open('frequency_counts.json') as f:
    data = json.load(f)

keep_values = []
keep_keys = []
duplicates = []
indizes = {}

for key,val in data.items():
    if val in keep_values:
        duplicates.append(key)
        i = keep_values.index(val)
        indizes[keep_keys[i]].append(key)
    else:
        keep_keys.append(key)
        keep_values.append(val)
        indizes[key] = []

print(keep_keys)
print(duplicates)
for key,val in indizes.items():
    if val != []:
        print(key + ': ' + str(indizes[key]))