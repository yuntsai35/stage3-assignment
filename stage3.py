from fastapi import * 
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse

import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector

con = mysql.connector.connect(
  host="share.cav8g6cg8pxy.us-east-1.rds.amazonaws.com",
  user="admin",
  password=os.getenv("DB_PASSWORD"),

)
print("database ready")

import boto3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION_NAME=os.getenv("AWS_REGION_NAME")
S3_BUCKET_NAME=os.getenv("S3_BUCKET_NAME")

def check_db():
    cursor=con.cursor(dictionary=True)
    cursor.execute("CREATE DATABASE IF NOT EXISTS share_db")
    cursor.execute("USE share_db")
    cursor.execute("CREATE TABLE IF NOT EXISTS share (id int not null auto_increment, content text not null, picture text not null, PRIMARY KEY (id))")

check_db()

app=FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/stage3.html", media_type="text/html")



@app.post("/files")
async def upload_info(text: str=Form(...), file:UploadFile=File(...)):
    
    if file and text:
        s3_client= boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=AWS_REGION_NAME)
        s3_client.upload_fileobj(
             file.file,
             S3_BUCKET_NAME,
             Key=file.filename,
             ExtraArgs={
        "ContentType": file.content_type 
    }
        )

        image_url = "https://dlw5pmuk2nt8j.cloudfront.net/"+file.filename
        
        cursor=con.cursor(dictionary=True)
        cursor.execute("insert into share (content, picture) value (%s,%s)", [text, image_url])

        con.commit()
        cursor.close()
        return {"ok": True}
    
	
@app.get("/files")
async def render_info(request: Request):
	
    cursor=con.cursor(dictionary=True)
    cursor.execute("select * from share order by id desc")
    results=cursor.fetchall()
    cursor.close()

    data_list=[]
    for result in results:
         data_list.append({
                     "id": result['id'],
                     "content": result['content'],
                     "picture": result['picture'],
                    })
    
    return {"data":data_list}



