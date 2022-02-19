import json
import uuid
from datetime import datetime

from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.contrib.hooks.mongo_hook import MongoHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from bson import json_util


class MongoToGCSOperator(BaseOperator):

    template_fields = ("dst", "mongo_query")

    @apply_defaults
    def __init__(
        self,
        mongo_conn_id,
        mongo_collection,
        mongo_query,
        bucket,
        filename,
        prefix="",
        mongo_db=None,
        tmp_file_location="/tmp/airflow-tmp",
        google_cloud_storage_conn_id="google_cloud_default",
        mime_type="application/octet-stream",
        delegate_to=None,
        gzip=False,
        replace=True,
        *args,
        **kwargs
    ):
        super(MongoToGCSOperator, self).__init__(*args, **kwargs)

        # Mongo Self
        self.mongo_conn_id = mongo_conn_id
        self.mongo_db = mongo_db
        self.mongo_collection = mongo_collection
        self.mongo_query = mongo_query
        self.is_pipeline = True if isinstance(self.mongo_query, list) else False
        self.tmp_file_location = tmp_file_location

        # Google Cloud Storage
        self.prefix = prefix
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.bucket = bucket
        self.mime_type = mime_type
        self.filename = filename
        self.delegate_to = delegate_to
        self.gzip = gzip
        self.replace = replace

        if not self.replace:
            dth = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.obj = "{}/{}/{}_{}.json".format(
                self.prefix, self.filename, self.filename, dth
            )
        else:
            self.obj = "{}/{}/{}.json".format(self.prefix, self.filename, self.filename)

    def execute(self, context):

        # Mongo DB Export
        if self.is_pipeline:
            results = MongoHook(self.mongo_conn_id).aggregate(
                mongo_collection=self.mongo_collection,
                aggregate_query=self.mongo_query,
                mongo_db=self.mongo_db,
            )
        else:
            results = MongoHook(self.mongo_conn_id).find(
                mongo_collection=self.mongo_collection,
                query=self.mongo_query,
                mongo_db=self.mongo_db,
            )
        docs_str = self._stringify(self.transform(results))
        with open(
            "{}/{}.tmp".format(self.tmp_file_location, self.filename), "w"
        ) as file:
            file.write(docs_str)

        # GCS Upload
        gcs_hook = GoogleCloudStorageHook(
            google_cloud_storage_conn_id=self.google_cloud_storage_conn_id,
            delegate_to=self.delegate_to,
        )

        gcs_hook.upload(
            bucket=self.bucket,
            object=self.obj,
            mime_type=self.mime_type,
            filename="{}/{}".format(self.tmp_file_location, self.filename),
            gzip=self.gzip,
        )

    @staticmethod
    def _stringify(iterable, joinable="\n"):
        """
        Takes an iterable (pymongo Cursor or Array) containing dictionaries and
        returns a stringified version using python join
        """
        return joinable.join(
            [json.dumps(doc, default=json_util.default) for doc in iterable]
        )

    @staticmethod
    def transform(docs):
        """
        Processes pyMongo cursor and returns an iterable with each element being
                a JSON serializable dictionary

        Base transform() assumes no processing is needed
        ie. docs is a pyMongo cursor of documents and cursor just
        needs to be passed through

        Override this method for custom transformations
        """
        return docs
