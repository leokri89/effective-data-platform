set container_name=glue_devenv
set image_version=amazon/aws-glue-libs:glue_libs_3.0.0_image_01
set host_workspace_dir=/c/Users/pve_lkrivickas/repositorio/
set aws_profile_dir=/c/Users/pve_lkrivickas/.aws/
set disable_ssl=true

docker run -it --rm -p 8888:8888 -p 4040:4040 -v "%host_workspace_dir%:/home/glue_user/workspace/jupyter_workspace/repositorio/" -v "%aws_profile_dir%:/home/glue_user/.aws/" -e DISABLE_SSL="%disable_ssl%" --name %container_name% %image_version% /home/glue_user/jupyter/jupyter_start.sh
