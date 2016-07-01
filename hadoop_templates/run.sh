#!/bin/bash

INPUT_PATH='/user/bigdata/profiling/customer_20160630/part-00000'
OUTPUT_PATH='/user/sogxin/unified_user_behaviour/offline_data/20160630/'
HADOOP_HOME='/home/work/bin/hadoop'
BEGIN_DATE='20140601'
CITY_ID='110000'
PYTHON_HDFS_PATH='/user/songxin/tools/python.tgz'

${HADOOP_HOME}/bin/hadoop fs -rm -r ${OUTPUT_PATH}
$HADOOP_HOME/bin/hadoop  jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.4.1.jar \
    -D mapreduce.job.name='offline_data_extraction_20160630' \
    -D mapreduce.job.queuename='highPriority' \
    -D mapreduce.job.priority=NORMAL \
    -D stream.num.map.output.key.fields=2 \
    -D num.key.fields.for.partition=1 \
    -D mapreduce.job.maps=64 \
    -D mapreduce.job.reduces=10 \
    -D mapreduce.map.memory.mb=2000 \
    -partitioner org.apache.hadoop.mapred.lib.KeyFieldBasedPartitioner \
    -cacheArchive "${PYTHON_HDFS_PATH}#python" \
    -input ${INPUT_PATH} \
    -output ${OUTPUT_PATH} \
    -mapper "./python/bin/python mapper.py ${BEGIN_DATE} ${CITY_ID}" \
    -reducer "cat" \
    -file mapper.py 

