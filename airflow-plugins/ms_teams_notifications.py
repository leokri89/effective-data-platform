
import json
import requests
from datetime import datetime

class HomebrewNotifications:

    @staticmethod
    def success_teams_notification(context):

        url = ""
        task_instance = context.get('task_instance_key_str').split('__')[0]
        run_id = context.get('run_id')
        execution_date = context.get('ts')
        last_execution_date = context.get('prev_execution_date_success').isoformat()

        if len(url) < 10:
            return 504
        else:
            msg_template = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "summary": "Dag Succeeded",
                "sections": [{
                    "activityTitle": "Alert",
                    "activitySubtitle": "Dag Succeeded",
                    "activityImage": "https://cwiki.apache.org/confluence/download/attachments/62693171/AIRFLOW?version=2&modificationDate=1567414976000&api=v2",
                    "facts": [{
                        "name": "Dag",
                        "value": task_instance
                    }, {
                        "name": "Run ID",
                        "value": run_id
                    }, {
                        "name": "Ocurrance date",
                        "value": execution_date
                    }, {
                        "name": "Last success execution date",
                        "value": last_execution_date
                    }],
                    "markdown": True
                }],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "Go to DAG",
                    "targets": [{
                        "os": "default",
                        "uri": "http://airflow.dadosbpc.com:8080/tree?dag_id={}".format(task_instance)
                    }]
                }]
            }
            r = requests.post(url, json=msg_template)
            print(r.status_code)

    @staticmethod
    def failed_teams_notification(context):

        url = ""
        task_instance = context.get('task_instance_key_str').split('__')[0]
        run_id = context.get('run_id')
        execution_date = context.get('ts')
        last_execution_date = context.get('prev_execution_date_success').isoformat()

        if len(url) < 10:
            return 504
        else:
            msg_template = {
                "@type": "MessageCard",
                "@context": "http://schema.org/extensions",
                "themeColor": "0076D7",
                "summary": "Dag Failed",
                "sections": [{
                    "activityTitle": "Alert",
                    "activitySubtitle": "Dag Failed after all retries",
                    "activityImage": "https://cwiki.apache.org/confluence/download/attachments/62693171/AIRFLOW?version=2&modificationDate=1567414976000&api=v2",
                    "facts": [{
                        "name": "Dag",
                        "value": task_instance
                    }, {
                        "name": "Run ID",
                        "value": run_id
                    }, {
                        "name": "Ocurrance date",
                        "value": execution_date
                    }, {
                        "name": "Last success execution date",
                        "value": last_execution_date
                    }],
                    "markdown": True
                }],
                "potentialAction": [{
                    "@type": "OpenUri",
                    "name": "Go to DAG",
                    "targets": [{
                        "os": "default",
                        "uri": "http://airflow.dadosbpc.com:8080/tree?dag_id={}".format(task_instance)
                    }]
                }]
            }
            r = requests.post(url, json=msg_template)
            print(r.status_code)
