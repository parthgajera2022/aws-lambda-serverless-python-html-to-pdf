import json
import os
import pdfkit
from io import StringIO
import base64
import boto3
import uuid


def htmltopdf(event, context):
    objbody = json.loads(event['body'])

    File64 = objbody['File64']
    pagesize = objbody['page-size']
    orientation = objbody['orientation']
    base64_file_bytes = File64.encode('utf-8')

    with open('/tmp/temp.html', 'wb') as file_to_save:
        decoded_file_data = base64.decodebytes(base64_file_bytes)
        file_to_save.write(decoded_file_data)

    options = {
        'page-size': pagesize,
        'orientation': orientation
    }

    config = pdfkit.configuration(wkhtmltopdf='/opt/bin/wkhtmltopdf')
    pdfkit.from_file('/tmp/temp.html', '/tmp/outr.pdf', options=options, configuration=config)

    #html = """<html><body style='color:red;'>This is a test <br/>सरल</body></html>"""
    #pdfkit.from_string(html, '/tmp/outr.pdf',options=options, configuration=config)
    #pdfkit.from_url('http://google.com', '/tmp/outr.pdf',options=options, configuration=config)
    file_name = "pdf-" + str(uuid.uuid4())[:12] + ".pdf"
    s3 = boto3.client('s3')
    with open("/tmp/outr.pdf", "rb") as f:
        s3.upload_fileobj(f, "s3-repo", file_name)

    os.remove("/tmp/outr.pdf")
    os.remove("/tmp/temp.html")

    params = {'Bucket': "s3-repo", 'Key': file_name}
    SignedURL = boto3.client('s3').generate_presigned_url(
                    'get_object',
                    Params=params,
                    ExpiresIn=(60*60*24*7)  # 7days
                )

    response = {
        'headers': { "Content-Type": "application/json" },
        'statusCode': 200,
        'body': json.dumps({ "message": "Successfully converted","file_name": SignedURL}),
        'isBase64Encoded': True
    }

    return response
