set VAULT_ADDR=http://127.0.0.1:56748

vault login my_passwd

vault secrets enable -path=created_kv_store kv

vault kv put -format=json -mount=created_kv_store init/app/third-degree passwd=my-passwd

vault kv get -format=json -mount=created_kv_store init/app/third-degree

vault kv get -format=json -mount=created_kv_store -field=passwd init/app/third-degree