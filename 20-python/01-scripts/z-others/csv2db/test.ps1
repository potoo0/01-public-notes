python .\sync2mysql.py `
  --conn_str 'mysql://root:root@localhost:3306/testdb?charset=utf8' `
  --table 'rpt_oss_capacity_summary' `
  --csvpath 'test/output/oss_capacity_summary.csv' `
  --colunms 'region_flag,total_tbytes,avail_tbytes,used_tbytes,yesterday_inc,twodaybefore_inc,week_inc_avg,available_day,op_date,update_time' `
  --pk 'op_date,region_flag' `
  --sep '|'


python .\sync2mysql.py `
  --conn_str 'mysql://root:root@localhost:3306/testdb?charset=utf8' `
  --table 'rpt_computes_hour_cpu_load' `
  --csvpath 'test/output/node.csv' `
  --colunms 'pie,flow,op_date,update_time' `
  --pk 'op_date' `
  --sep '|'
