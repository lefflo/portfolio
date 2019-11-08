import json
import boto3
import zipfile
import StringIO
import mimetypes

s3 = boto3.resource('s3')

portfolio_bucket = s3.Bucket('mathieu.portfolio')
build_bucket = s3.Bucket('mathieu.portfoliobuild')

portfolio_zip = StringIO.StringIO()
build_bucket.download_fileobj('portfoliobuild.zip', portfolio_zip)

with zipfile.ZipFile(portfolio_zip) as myzip:
    for nm in myzip.namelist():
        obj = myzip.open(nm)
        portfolio_bucket.upload_fileobj(obj, nm,
         ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
        portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
