#!/bin/bash

INPUT_PATH=""
OUTPUT_PATH=""
HADOOP_HOME=''
PYTHON_HDFS_PATH='/user/XXXX/tools/python.tgz'

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='JOB_NAME' \
    -D mapreduce.job.queuename='QUEUE_NAME' \
    -D mapredude.job.priority=NORMAL \
    -D stream.map.output.field.separator="\t" \
    -D stream.num.map.output.key.fields=2 \
    -D org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -D num.key.fields.for.partition=1 \
    -D mapredude.job.tasks=32 \
    -D mapreduce.map.memory.mb=6000 \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper './python/bin/python mapper.py' \
    -reducer 'cat' \
    -file mapper.py

