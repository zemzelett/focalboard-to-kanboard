import json
import csv
import argparse
import zipfile

argumentParser = argparse.ArgumentParser(
    prog='focal-to-kan',
    description='Converts Focalboard archive export to Kanboard import CSV'
)
argumentParser.add_argument(
    'inFile',
    help='Focalboard archive to convert',
    nargs=1,
)
argumentParser.add_argument(
    '-o',
    help='output file name',
    nargs=1
)

args = argumentParser.parse_args()
if not args.inFile:
    print('inFile has to be supplied!')
    exit(1)

root = zipfile.Path(args.inFile[0])

boardDir = None
for part in root.iterdir():
    if part.is_dir():
        boardDir = part
        break
boardDirPath = root.joinpath(boardDir.name)

boardFile = None
for part in boardDirPath.iterdir():
    if part.is_file():
        boardFile = part
        break

focalJsonl = boardFile.open()

tags = {}
tagsId = ''
status = {}
statusId = ''
tasks = {}
descriptions = []

while line := focalJsonl.readline():
    o = json.loads(line)
    data = o['data']
    if o['type'] == 'board':
        for o in data['cardProperties']:
            if o['name'] == 'Status':
                statusId = o['id']
                status = {v['id']: v['value'] for v in o['options']}
            elif o['name'] == 'Tags':
                tagsId = o['id']
                tags = {v['id']: v['value'] for v in o['options']}
    elif data['type'] == 'card':
        tasks[data['id']] = data
    elif data['type'] == 'text':
        descriptions.append(data)

rows = [[
    'Reference',
    'Title',
    'Description',
    'Assignee Username',
    'Creator Username',
    'Color Name',
    'Column Name',
    'Category Name',
    'Swimlane Name',
    'Complexity',
    'Time Estimated',
    'Time Spent',
    'Start Date',
    'Due Date',
    'Priority',
    'Status',
    'Tags',
    'External Link'
]]

for d in descriptions:
    if d['parentId'] in tasks:
        tasks[d['parentId']]['description'] = d['title']

for task in tasks.values():
    props = task['fields']['properties']
    rows.append(
        [
            'focalboard import',
            task['title'],
            task.get('description', ''),
            'your_user_here',
            'your_user_here',
            'Grey',
            status[props[statusId]],
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            ','.join(map(lambda v: tags.get(v, ''), props.get(tagsId, [])))
        ]
    )

outFilename = args.o[0] if args.o else f'{args.inFile[0]}.csv'
csvFile = open(outFilename, 'w', newline='')
csv.writer(csvFile).writerows(rows)