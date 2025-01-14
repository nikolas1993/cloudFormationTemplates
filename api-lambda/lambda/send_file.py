import json
import boto3
import jwt
import os
from datetime import datetime
from io import StringIO


s3_client = boto3.client("s3")

JwtKey = os.environ["JwtKey"]
DestBucket = os.environ["DestBucket"]
DestPath = os.environ["DestPath"]
SourceBucket = os.environ["SourceBucket"]
SourcePath = os.environ["SourcePath"]
FileName = os.environ["FileName"]

CSV_SEPARATOR = ";"
NEW_LINE_SEPARATOR = "\n"
FILE_EXTENSION = ".csv"

headers = {
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
}


def lambda_handler(event, context):
    print("Send file POST " + json.dumps(event))
    try:
        token = "" + event["headers"]["Authorization"]
        token = token.replace("Bearer ", "")
        print(token)
        decoded = jwt.decode(token, JwtKey, algorithms=["HS256"])
    except Exception as e:
        print(e)
        print("JWT Error")
        return {"body": "", "headers": headers, "statusCode": 403}

    # from body to list
    listString_body = event["body"]
    listString = json.loads(listString_body)
    listString_body = ""

    listString_body = NEW_LINE_SEPARATOR.join(
        CSV_SEPARATOR.join(campo for campo in riga) for riga in listString
    )

    # I write the file on DestBucket and SourceBucket
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%Y%m%d")  # %H%M
    FileNameOUT = FileName + timestampStr + FILE_EXTENSION
    OUT_string_encoded = listString_body.encode("utf-8")
    print(
        "Send file DestBucket="
        + DestBucket
        + " DestPath="
        + DestPath
        + " FileNameOUT="
        + FileNameOUT
    )
    s3_client.put_object(
        Bucket=DestBucket, Key=DestPath + "/" + FileNameOUT, Body=OUT_string_encoded
    )
    s3_client.put_object(
        Bucket=SourceBucket, Key=SourcePath + "/" + FileNameOUT, Body=OUT_string_encoded
    )
    return {"statusCode": 200, "headers": headers, "body": json.dumps(FileNameOUT)}


def lambda_handler_dir(event, context):
    print("File List GET " + json.dumps(event))
    try:
        token = "" + event["headers"]["Authorization"]
        token = token.replace("Bearer ", "")
        print(token)
        decoded = jwt.decode(token, JwtKey, algorithms=["HS256"])
    except Exception as e:
        print(e)
        print("Errore JWT")
        return {"body": "", "headers": headers, "statusCode": 403}

    lista = []
    s3_paginator = boto3.client("s3").get_paginator("list_objects_v2")
    for page in s3_paginator.paginate(
        Bucket=SourceBucket, Prefix=SourcePath
    ):  # , StartAfter=start_after):
        for key in page.get("Contents", ()):
            fileName = str(key["Key"]).replace(SourcePath + "/", "")
            lastModified = key["LastModified"].strftime("%d-%m-%Y %H:%M:%S")
            if fileName != "":
                lista.append(
                    {
                        "fileName": fileName,
                        "lastModified": lastModified,
                        "size": key["Size"],
                    }
                )
    return {"statusCode": 200, "headers": headers, "body": json.dumps(lista)}


def lambda_handler_file(event, context):
    print("Get list GET " + json.dumps(event))
    try:
        token = "" + event["headers"]["Authorization"]
        token = token.replace("Bearer ", "")
        print(token)
        decoded = jwt.decode(token, JwtKey, algorithms=["HS256"])
    except Exception as e:
        print(e)
        print("Errore JWT")
        return {"body": "", "headers": headers, "statusCode": 403}
    if ("queryStringParameters" not in event) or (
        "fileName" not in event["queryStringParameters"]
    ):
        return {"statusCode": 400, "headers": headers, "body": "Missing fileName"}
    fileName = event["queryStringParameters"]["fileName"]
    s3_client_p = boto3.client(
        "s3",
        region_name="eu-west-1",
        config=boto3.session.Config(
            signature_version="s3v4",
        ),
    )

    response = s3_client_p.generate_presigned_url(
        "get_object",
        Params={"Bucket": SourceBucket, "Key": SourcePath + "/" + fileName},
        ExpiresIn=3600,
    )
    return {"statusCode": 200, "headers": headers, "body": json.dumps(response)}
