while true
do
  python journal_spider.py #执行抓取
  python ../parse_item.py  #转换格式
  sleep 30m                #30分钟执行一次
done