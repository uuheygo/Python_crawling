import re

def url_processing(filename):
    all_urls = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip().split('\t')
            all_urls.append(line[2])
    
    sites = []
    pattern = re.compile('\.(^[\.\/]+\.edu)')
    for entry in all_urls:
        if 'edu' in entry:
            target = re.findall(r'([^\./]+\.edu)', entry)
            sites.append(target[0])
        else:
            sites.append(" ")
    for entry in sites:
        print entry
    
if __name__ == '__main__':
    url_processing('school_url.txt')