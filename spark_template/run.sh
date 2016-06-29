#!/bin/bash
export HADOOP_CONF_DIR="${SPARK_HOME}/hadoop-conf"
export HADOOP_USER_NAME='${USER_NAME}'
spark-submit \
    --master local \
    --deploy-mode client \
    --queue default \
    --driver-memory 3G \
    --executor-memory 4G \
    --executor-cores 1 \
    --num-executors 16 \
    spark_script.py
