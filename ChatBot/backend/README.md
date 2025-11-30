--------------BACKEND

vector.py = embeding and db creation
app.py = rag logic

to run fastapi app
go to your folder
type = uvicorn app:app --reload --port 8000

to end it : control+c


--------------FRONTEND
folder name is frontend
npx create-react-app frontend
cd frontend
npm start
http://localhost:3000




---------------Dockerfile
make Dockerfile and .dockerignore
docker build -t chatbot-backend .
docker run -p 8000:8000 chatbot-backend
(i deleted all images and conatiners)











_________________________________________________________________________________________________
my question is why there is no __main__ in my code?
(note below code is not to be used it is to show that , if we want to wirte the uvicorn directly in code to run the app, and the reason we dont have __main__ in our code is we run the app by command line) 
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

and when we use above way , we run as "Fastapi run app.py"