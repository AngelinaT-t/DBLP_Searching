
author_file = "data/mauthor.txt"
title_file = 'data/mtitle.txt'
year_file = 'data/myear.txt'
journal_file = "data/mjournal.txt"
link_file = 'data/mlink.txt'




with open("jounal_info.data") as f:
    items = filter(None,f.read().split('\n'))

with open(author_file, 'w') as auf, open(title_file, 'w') as titf, open(year_file, 'w') as yeaf, open(journal_file, 'w') as jourf, open(link_file, 'w') as linkf:
    for item in items:
        split_items = item.split(' --- ')
        auf.write(split_items[0]+'\n')
        titf.write(split_items[1]+'\n')
        yeaf.write(split_items[2]+'\n')
        jourf.write(split_items[3]+'\n')
        linkf.write(split_items[4]+'\n')
