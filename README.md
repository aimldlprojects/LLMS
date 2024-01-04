"""
aa


@app.get("/view/{document_key:path}")
async def view_document(document_key: str):
    try:
        # Decode URL-encoded characters
        document_key = unquote(document_key)

        # Assuming the document_key is the S3 object key
        response = s3_connector().get_object(Bucket=bucket_name, Key=document_key)

        # Log additional details about the S3 request
        print(f"S3 Request Details: {response}")

        file_content = response['Body'].read()
        filename = document_key.split("/")[-1]

        # Encode the file content to base64
        encoded_content = base64.b64encode(file_content).decode('utf-8')

        # If you want the document to be viewed in the browser
        media_type, _ = mimetypes.guess_type(filename)
        headers = {"Content-Disposition": f"inline; filename={filename}"}

        return StreamingResponse(content=iter([encoded_content]), media_type=media_type, headers=headers)

    except Exception as e:
        # Add logging to print the error and relevant information
        print(f"Error viewing document - Document Key: {document_key}, Error: {str(e)}")
        raise HTTPException(status_code=404, detail="Document not found")
Collapse
has context menu
