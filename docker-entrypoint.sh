#!/bin/bash
set -e

if [ ! -s ${QR_JDC}/config/config.json ]; then
  echo "检测到config配置目录下不存在config.json，从示例文件复制一份用于初始化...\n"
  cp -fv ${QR_JDC}/sample/config.json ${QR_JDC}/config/config.json
fi

if [ -s ${QR_JDC}/config/config.json ]; then
  echo "检测到config配置目录下存在config.json，即将启动...\n"

  python ${QR_JDC}/app.py

fi

exec "$@"
