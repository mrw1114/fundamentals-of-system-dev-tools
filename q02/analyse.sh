#!/bin/bash
# 判断是否传入1个参数
if [ $# -ne 1 ]; then
    echo "Usage: $0 <csv_file>" >&2
    exit 1
fi
# 判断是否存在文件
if [ ! -e $1 ]
then
  echo "$1 doesn't exist" >&2
  exit 2
fi

# 排序并输出5xx次数最多的 path
awk -F',' 'NR!=1&&$4>=500 {cnt[$3]++} END {for(i in cnt)print cnt[i],i}' $1 | sort -t',' -k1,1nr -k2,2 | awk -F' ' '{print $2}' | head -n 2

# 计算平均路径
awk -F',' 'NR!=1 {sum+=$5; n++} END {if(n != 0) printf "%.2f\n", sum / n; else print "0.00"}' $1
