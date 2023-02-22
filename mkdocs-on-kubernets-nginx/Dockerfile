#FROM repo.intranet.pags/corpplatform-docker/squidfunk/mkdocs-material:8.5.11 AS build
FROM squidfunk/mkdocs-material as build

COPY . /docs

WORKDIR /docs

RUN mkdocs build

FROM nginxinc/nginx-unprivileged:1.23-alpine-perl

COPY --from=build /docs/site /usr/share/nginx/html

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf