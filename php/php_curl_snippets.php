<?php
$url = "http://nj02.nlpc.baidu.com/nlpc_depparser_query_107?username=songxin02&app=nlpc_201508121509570";
$data = '{"sentence":"��ðٶ�","grain_size":1,"sentence_segmented":false}';
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CUROPT_POST, true);
#���������ʽ��Ĭ���������׼���
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
$result = curl_exec($ch);
curl_close($ch);
print_r($result);
?>
