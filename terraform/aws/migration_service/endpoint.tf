resource "aws_dms_endpoint" "sqlserver_source" {
  database_name               = "sql_database"
  endpoint_id                 = "sqlserver-source-dms-endpoint"
  endpoint_type               = "source"
  engine_name                 = "sqlserver"
  username                    = "sql-user"
  password                    = "********"
  port                        = 1433
  server_name                 = "sql-server-hostname"

  tags = {
    Name = "test"
  }

}

resource "aws_dms_endpoint" "redshift_target" {
  database_name               = "stage"
  endpoint_id                 = "redshift-target-dms-endpoint"
  endpoint_type               = "target"
  engine_name                 = "redshift"
  username                    = "redshift-user"
  password                    = "********"
  port                        = 5432
  server_name                 = "dw-stage"

  tags = {
    Name = "test"
  }

}