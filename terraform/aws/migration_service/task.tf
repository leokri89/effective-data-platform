resource "aws_dms_replication_task" "sqlserver_redshift_migration_task" {
  cdc_start_time            = 1484346880 #Unix timestamp
  migration_type            = "cdc"
  replication_instance_arn  = aws_dms_replication_instance.ec2_replication_instance.arn
  replication_task_id       = "sqlserver-redshift-replication-task"
  replication_task_settings = "..."
  source_endpoint_arn       = aws_dms_endpoint.sqlserver_source.arn
  table_mappings            = "{\"rules\":[{\"rule-type\":\"selection\",\"rule-id\":\"1\",\"rule-name\":\"replicate_all\",\"object-locator\":{\"schema-name\":\"%\",\"table-name\":\"%\"},\"rule-action\":\"include\"}]}"

  tags = {
    Name = "test"
  }

  target_endpoint_arn = aws_dms_endpoint.redshift_target.arn
}