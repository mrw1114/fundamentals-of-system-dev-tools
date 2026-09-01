#!/bin/bash
# 判断是否传入1个参数
if [ $# -ne 1 ]; then
    echo "Usage: $0 <csv_file>" >&2
    exit 1
fi
# 不存在文件时
if [ ! -e $1 ]
then
  echo "$1 doesn't exist" >&2
  exit 2
fi
# 存在文件时
echo "$1 exists."

