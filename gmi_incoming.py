import config
import os
import re
import shutil

shutil.copytree(os.getcwd(), './site_output')
os.chdir('site_output')
cwd = os.getcwd()

def get_list_of_gmis():
    list = []
    for r, d, f in os.walk(cwd):
        for file in f:
            if file.endswith(".gmi") and not (r == cwd and file.startswith("index")):
                # provide relative links
                list.append(os.path.join(r, file)[len(cwd) + 1:])
    return list

gmi_files = get_list_of_gmis()
incoming_links = {}
link_re = re.compile(r'=> (\.*)?([a-z0-9/~-]*?(\.gmi)?) (([a-z0-9:_./~-]*)*( )?)*', re.I)

for gmi in gmi_files:
    file = open(gmi).read().splitlines()
    for line in file:
        match = link_re.search(line)
        if match:
            dest = match.group(2)
            # python doesn't like leading slashes
            if dest.startswith('/'):
                dest = dest[1:]
            # Absolute paths need to be modified.
            if dest.startswith(config.gemdocs_root):
                dest = dest[len(config.gemdocs_root) + 1:]
            # resolve relative paths into root of site dir
            if dest.startswith('..'):
                dest = os.path.abspath(dest)[len(cwd) + 1:]
            # assume directory links are to their indexes
            if not match.group(3):
                dest = dest + '/index.gmi'
            if dest in incoming_links:
                incoming_links[dest].append(gmi)
            else:
                incoming_links[dest] = [gmi]

for dest in incoming_links.keys():
    if os.path.exists(dest) and dest.endswith(".gmi"):
        incoming = incoming_links.get(dest)
        incoming = list(map((lambda x: '=> /' + config.gemdocs_root + x), incoming))
        with open(dest, 'a') as file:
            file.write('\n' + '## Incoming links' + '\n\n')
            file.writelines(incoming)
            file.close()
