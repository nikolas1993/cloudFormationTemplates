import json


def entrypoint(event, context):
    print(event)
    hello_string: str = str("Hello from {} !").format(event["who"])
    print(hello_string)
    return {"statusCode": 200, "body": json.dumps(hello_string)}
