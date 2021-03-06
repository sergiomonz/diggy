import pytest
import main
import json


class SQSMock:
    def send_message(self, QueueUrl, MessageBody):
        messagReceived = json.loads(MessageBody)
        messageExpeceted = {
            "user_id": "123",
            "user_name": "456",
            "reference_id": "789",
            "amount": 20000.0,
            "description": "Consignación a través de Payu"
        }

        assert messagReceived == messageExpeceted, "validate transaction message"
        assert QueueUrl == main.TRANSACTION_QUEUE

        return {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }


def test_handler():
    main.sqsClient = SQSMock()

    response = main.lambda_handler(
        {
            "Records": [
                {
                    "body": "cGF5bWVudF9tZXRob2RfdHlwZT0yJmRhdGU9MjAyMi4wNi4xMiUyQjA5JTI1M0E0MSUyNTNBMjImcHNlX3JlZmVyZW5jZTM9JnBzZV9yZWZlcmVuY2UyPSZmcmFuY2hpc2U9VklTQSZjb21taXNpb25fcG9sPTAuMDAmcHNlX3JlZmVyZW5jZTE9JnNoaXBwaW5nX2NpdHk9JmJhbmtfcmVmZXJlbmNlZF9uYW1lPSZzaWduPTZiNTY5M2M2NGJkN2MxMTE0Y2NmYjNhZTU3ZDY1NmJlJmV4dHJhMj0mZXh0cmEzPSZvcGVyYXRpb25fZGF0ZT0yMDIyLTA2LTEyJTJCMjElMjUzQTQxJTI1M0EyMiZiaWxsaW5nX2FkZHJlc3M9JnBheW1lbnRfcmVxdWVzdF9zdGF0ZT1BJmV4dHJhMT0mYmFua19pZD0xMCZuaWNrbmFtZV9idXllcj0mcGF5bWVudF9tZXRob2Q9MTAmYXR0ZW1wdHM9MSZ0cmFuc2FjdGlvbl9pZD0wOWIxNTY5Ny04MWViLTRhM2YtYmFmYi01OGQ3MzA0YWE1YjYmdHJhbnNhY3Rpb25fZGF0ZT0yMDIyLTA2LTEyJTJCMjElMjUzQTQxJTI1M0EyMiZ0ZXN0PTAmZXhjaGFuZ2VfcmF0ZT0xLjAwJmlwPTEwLjAuMC41JnJlZmVyZW5jZV9wb2w9MTQwNDAwNzI3MSZjY19ob2xkZXI9QVBQUk9WRUQmdGF4PTMxOTMuMDAmYW50aWZyYXVkTWVyY2hhbnRJZD0mcHNlX2Jhbms9JnRyYW5zYWN0aW9uX3R5cGU9QVVUSE9SSVpBVElPTl9BTkRfQ0FQVFVSRSZzdGF0ZV9wb2w9NCZiaWxsaW5nX2NpdHk9JnBob25lPSZlcnJvcl9tZXNzYWdlX2Jhbms9JnNoaXBwaW5nX2NvdW50cnk9Q08mZXJyb3JfY29kZV9iYW5rPTAwJmN1cz1hcHByb3ZlZCZjdXN0b21lcl9udW1iZXI9JmRlc2NyaXB0aW9uPVRlc3QlMkJQQVlVJm1lcmNoYW50X2lkPTUwODAyOSZhdXRob3JpemF0aW9uX2NvZGU9Nzg5OTE2JmN1cnJlbmN5PUNPUCZzaGlwcGluZ19hZGRyZXNzPSZjY19udW1iZXI9JTJBJTJBJTJBJTJBJTJBJTJBJTJBJTJBJTJBJTJBJTJBJTJBMDAwNCZpbnN0YWxsbWVudHNfbnVtYmVyPTEmbmlja25hbWVfc2VsbGVyPSZ2YWx1ZT0yMDAwMC4wMCZ0cmFuc2FjdGlvbl9iYW5rX2lkPTc4OTkxNiZiaWxsaW5nX2NvdW50cnk9Q08mY2FyZFR5cGU9Q1JFRElUJnJlc3BvbnNlX2NvZGVfcG9sPTEmcGF5bWVudF9tZXRob2RfbmFtZT1WSVNBJm9mZmljZV9waG9uZT0mZW1haWxfYnV5ZXI9anVhY2FnaXJpJTI1NDBnbWFpbC5jb20mcGF5bWVudF9tZXRob2RfaWQ9MiZyZXNwb25zZV9tZXNzYWdlX3BvbD1BUFBST1ZFRCZhY2NvdW50X2lkPTUxMjMyMSZiYW5rX3JlZmVyZW5jZWRfY29kZT1DUkVESVQmYWlybGluZV9jb2RlPSZwc2VDeWNsZT0mcmlzaz0mcmVmZXJlbmNlX3NhbGU9MTIzIzQ1NiM3ODkmYWRkaXRpb25hbF92YWx1ZT0wLjAwJTNB",
                }
            ]
        }, {})
    assert None == response, "Validate output"
