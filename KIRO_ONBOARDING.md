- Refactor existing “Hello World” Python Lambda into a photo upload & sharing backend  
- Serverless architecture using AWS Lambda, API Gateway, Amazon Cognito, S3 & DynamoDB  

- **Key Requirements:**  
  - Support a `GET /login` endpoint that redirects to Cognito Hosted UI  
  - Protect routes so only authenticated users can access upload functionality  
  - Provide `POST /upload` endpoint that returns a pre‑signed S3 upload URL (client handles actual upload)  
  - Serve `GET /photos` (base path) to return a random selection of top 10 photos with cursor‑based pagination  
  - On successful upload, persist photo metadata in DynamoDB  

- **Architecture Overview:**  
  - Client ↔ API Gateway ↔ Lambda functions  
  - Cognito User Pool for signup/signin & JWT authorizer in API Gateway  
  - S3 bucket for photo storage with pre‑signed URLs  
  - DynamoDB table for storing photo metadata  

- **Authentication Flow (`/login`):**  
  - Method: `GET /login`  
  - Redirects user to Cognito Hosted UI  
  - Handles OAuth callback, exchanges code for JWT tokens  
  - API Gateway uses Cognito JWT authorizer for protected endpoints  

- **Upload Endpoint (`POST /upload`):**  
  - Authorization: required (`Authorization: Bearer <JWT>`)  
  - Request body: `{ "filename": "...", "contentType": "image/..." }`  
  - Generates UUID for photo, constructs S3 key (`{userId}/{photoId}/{filename}`)  
  - Returns JSON: `{ "uploadUrl": "...", "photoId": "..." }`  
  - Client uploads directly to S3 using the signed URL  

- **Photo Listing (`GET /photos`):**  
  - Query params: `limit` (default 10), `lastKey` (pagination token)  
  - Optionally public or user‑specific based on auth  
  - Returns JSON:  
    - `items`: list of `{ photoId, s3Key, uploadedAt, userId }`  
    - `lastKey`: opaque token or `null`  

- **Data Model (DynamoDB “PhotoMetadata” Table):**  
  - `photoId` (String) – partition key (UUID)  
  - `uploadedAt` (String, ISO‑8601) – sort key  
  - `userId` (String) – Cognito sub of uploader  
  - `s3Key` (String) – S3 object key  
  - `contentType` (String) – MIME type  
  - `metadata` (Map) – optional captions, tags, etc.  

- **Deployment & Configuration:**  
  - Use AWS SAM (or Serverless Framework) with a `template.yaml` defining:  
    - REST API resource (`PhotoApi`) with Cognito authorizer  
    - Lambda functions for `/login`, `/upload`, `/photos`  
  - Environment variables: `BUCKET_NAME`, `TABLE_NAME`, `USER_POOL_ID`, etc.  
  - IAM roles granting Lambda:  
    - S3 `PutObject` & `GetObject`  
    - DynamoDB `PutItem`, `Query`, `Scan`  

- **Next Steps:**  
  - Scaffold project with AWS SAM  
  - Configure Cognito User Pool & App Client  
  - Implement & test `/login` OAuth flow  
  - Build & secure `/upload` endpoint (signed URLs)  
  - Add logic to persist metadata in DynamoDB after upload confirmation  
  - Implement `/photos` listing with randomness & pagination  
  - Write unit & integration tests  
  - Deploy to AWS and perform end‑to‑end verification  
  - Set up monitoring & performance tuning  
