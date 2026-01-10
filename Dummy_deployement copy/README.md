# Dummy Deployment (React + FastAPI)

This project demonstrates a **basic full-stack setup** using:

- **Frontend**: React (Vite)
- **Backend**: FastAPI
- **Deployment**:
  - Frontend → AWS Amplify (Static)
  - Backend → AWS App Runner (Containerized)

---

## 🚀 Frontend Setup (React + Vite)

Create a new React project using Vite:

```bash
Below are some basic commands
npm create vite@latest my-react-app
ctrl + c   =>    means end
cd my-react-app
npm run dev   => means start
npm install react-router-dom (this should be done inside my-react-app)


# Folder structue that i created/modified/alredy present important

Dummy_deployement/
│
├── backend/
│   ├── app/
│   │   └── main.py
│   ├── requirements.txt   # Run backend from this folder
│   └── .env
│
├── dummyenv/               # Python virtual environment
│
└── my-react-app/
    └── src/
        ├── components/
        │   └── Header.jsx
        │
        ├── pages/
        │   ├── About.jsx
        │   └── Home.jsx
        │
        ├── services/
        │   └── api.js      # React ↔ FastAPI communication
        │
        ├── App.css
        ├── App.jsx
        ├── index.css
        └── main.jsx





