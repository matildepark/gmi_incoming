import config
import os
import re
import shutil

shutil.copytree(os.getcwd(), './site_output')
os.chdir('/site_output')
cwd = os.getcwd()

def get_list_of_gmis():
    list = []
    for r, f in os.walk(cwd):
        for file in f:
            if file.endswith(".gmi") and not file.startswith("/index"):
                # provide relative links
                list.append(os.path.join(r, file)[len(cwd) + 1:])
    return list

gmi_files = get_list_of_gmis()
incoming_links = {}
link_re = re.compile(r'=> (\.*)?([a-z0-9/~]*?)(\.gmi)?( [a-z0-9:_./~-]*)*?( )*?', re.I)

for gmi in gmi_files:
    file = open(gmi).read().splitlines()
    for line in file:
        match = link_re.search(line)
        if match:
            dest = match.group(2)
            if not dest.startswith('/'):
                dest = '/' + dest
            if not match.group(3):
                dest = dest + '/index.gmi'
            if incoming_links[dest]:
                incoming_links[dest].append(gmi)
            else:
                incoming_links[dest] = [gmi]

for dest in incoming_links.keys():
    if os.path.exists(dest):
        incoming = incoming_links.get(dest)
        incoming = list(map((lambda x: '=> /' + config.gemdocs_root + x), incoming))
        with open(dest, 'w') as file:
            file.write('\n' + '## Incoming links' + '\n')
            file.writelines(incoming)
            file.close()