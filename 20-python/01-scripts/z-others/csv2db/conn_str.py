# 同步 csv 到 mysql demo
"""
/home/admin/yovole_ml_dev/sync2mysql.py \
  --conn_str 'jdbc:mysql://localhost:3306/bigdata_dmp_rpt' \
  --username 'root' \
  --password 'Root123' \
  --table 'rpt_storage_pool_summary_list' \
  --csvpath '/home/admin/ml-datas/prj_pool_fullday/output/result.csv' \
  --colunms 'region_flag,az_flag,cluster_flag,pool_name,available_day,score,op_date,update_time' \
  --pk 'region_flag,az_flag,cluster_flag,pool_name,op_date' \
  --sep ','

"""
# create_engine 连接字符串示例
mysql_conn = 'mysql+pymysql://root:Root123@10.4.15.121:3306/bigdata_dmp_rpt?charset=utf8'
impala_conn = 'impala://10.4.15.120:21051/yovole_dm_dmp_prod'
ck_conn = 'clickhouse+native://10.4.15.105:7777/yovole_dm_clickhouse_prod'
