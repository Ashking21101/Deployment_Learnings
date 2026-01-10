Mac: Cmd + /


# fastapi (in respective folder)
uvicorn app.main:app --reload
# react  (in respective folder)
npm run dev
# after creating image docker command
docker run -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" chatbot-backend2




# IAM user Credentials
User name,Password,Console sign-in URL


# Important
Access key ID,Secret access key



```bash
# .env (iam user)
BACKEND .env ->
OPENAI_API_KEY=""
CLERK_JWKS_URL=
DEFAULT_AWS_REGION=
AWS_ACCOUNT_ID=

FRONTEND .env ->
VITE_CLERK_PUBLISHABLE_KEY=

# testing locally
load environment variavle = 
export $(cat .env | grep -v '^#' | xargs)

create a local image for demo
docker build -t chatbot-backend2 .

run below command for demo testing
docker run -p 8000:8000 -e OPENAI_API_KEY="$OPENAI_API_KEY" chatbot-backend2 (later need to make linux image for aws)


========================================================================
         For backend deplyment on AWS
1. create an ECR registry named chatbot-backend in AI_engineer

2. in my cd backend terminal vscode below command
aws configure = 
provide above keys(these are of IAM user AI_engineer)

3. Authenticate Docker to ECR (using your .env values!) run below command =
aws ecr get-login-password --region $DEFAULT_AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$DEFAULT_AWS_REGION.amazonaws.com

4. make a new image for aws  using following command = 
docker build --platform linux/amd64 -t chatbot-backend .

5. go to APPRUNNER->service->create
image repo = chatbot-backend, tag = latest, use Existingrule
service name = chatbot-backend
set minimum cpu
Add envirnemnt varaibel = OPENAI_API_KEY and its value
port 8000 for fastapi
autoscalling min = 1, max=1
Health check configuration: Protocol: HTTP, Path: /health, Interval: 20 seconds (maximum allowed)
                            Timeout: 5 seconds, Healthy threshold: 2, Unhealthy threshold: 5
create

========================================================================
         For frontend deplyment on AWS
 1. change the url in         
src/services/api.js:
const BASE_URL = "https://innx5kfubm.ap-south-1.awsapprunner.com";

2. npm run build ================ hosting-below =============
3. create s3 bucket name is chatbot-frontend-ashish-2026, same region
4. go inside s3 bucket-> static website hosting ->edit=enable 
    put index.html in both (mandatory for react router)
5. go to its permision and do Block pulic access = OFF (all uncheck)
6. add public policy add it  , and check the buckey name should be clear in the RESOURCE below
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::chatbot-frontend-ashish-2026/*"
    }
  ]
}
7. now upload the content from inside my-react-app/dist (do not uplaod dist, upload only its content)
8. to access website, go to s3 propertis->static website hosting->link



====================================new update after i did hosting====================================
        Adding User authentication
go to clerk -> create app -> name:chatbot-app -> google+github -> create
choose react 
1. dont copy 1st command, copy 2nd command and run in my-react-app folder (npm install @clerk/clerk-react)
    to check clerk version = npm list @clerk/clerk-react
2. create .env in my-react-app and paste the clerkpublishablekey here -> npm run dev
3. add clerk wrapper code in src/main.jsx -> npm run dev
4. add clerk signin in src/app.jsx (login page first)-> npm run dev
4. add cleark code in scr/components/header.jsx -> npm run dev (this is for signup page to appear first before home)
5. add clerk auth token code in src/pages/Home.jsx -> npm run dev (add clerk auth token) 
6. add clerk bearer code in src/services/api.js -> npm run dev  (add auth token)
------------------------------------------------------------------------
        Below is backend authentication
7. To Verify Clerk JWT in FastAPI, use fastapi_clerk_auth


main.jsx → App.jsx → Home.jsx → api.js → FastAPI (main.py) → back again


┌──────────────┐
│   User       │
│ (Browser)    │
└──────┬───────┘
       │
       │ Types message + clicks "Send"
       ▼
┌────────────────────┐
│ Home.jsx (React)   │
│ sendMessage()      │
└──────┬─────────────┘
       │
       │ getToken()
       │ (Clerk SDK)
       ▼
┌────────────────────┐
│ Clerk (Frontend)   │
│ Issues JWT         │
└──────┬─────────────┘
       │
       │ JWT returned
       ▼
┌──────────────────────────┐
│ api.js (fetch wrapper)   │
│ POST /chat               │
│ Authorization: Bearer JWT│
└──────┬───────────────────┘
       │
       │ HTTP request
       ▼
┌─────────────────────────────┐
│ FastAPI /chat endpoint      │
│ Depends(clerk_guard)        │
└──────┬──────────────────────┘
       │
       │ JWT verification
       │ (signature, expiry)
       ▼
┌─────────────────────────────┐
│ Clerk JWKS (Public Keys)    │
│ Token verified              │
└──────┬──────────────────────┘
       │
       │ ✔ Valid token
       ▼
┌─────────────────────────────┐
│ FastAPI business logic      │
│ user_id = creds.decoded[sub]│
└──────┬──────────────────────┘
       │
       │ Prompt to LLM
       ▼
┌─────────────────────────────┐
│ OpenAI API                  │
│ Generates response          │
└──────┬──────────────────────┘
       │
       │ Reply text
       ▼
┌─────────────────────────────┐
│ FastAPI response            │
│ { reply: "..." }            │
└──────┬──────────────────────┘
       │
       │ JSON response
       ▼
┌─────────────────────────────┐
│ Home.jsx                    │
│ setReply()                  │
└─────────────────────────────┘
       │
       ▼
┌──────────────┐
│ UI updates   │
│ User sees    │
│ message      │
└──────────────┘
