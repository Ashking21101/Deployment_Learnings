// Below code is to be used if we are using FETCH in service/api.js file instead of AXIOS API. 
// Base URL of FastAPI backend
// const BASE_URL = "http://localhost:8000";
const BASE_URL = "https://innx5kfubm.ap-south-1.awsapprunner.com";

// Helper function for GET requests
export async function apiGet(path) {
  // Send GET request to backend
  const res = await fetch(`${BASE_URL}${path}`);

  // fetch does NOT throw errors automatically
  if (!res.ok) {
    throw new Error("Request failed");
  }

  // Convert response JSON → JavaScript object
  return res.json();
}

// Helper function for POST requests
export async function apiPost(path, body) {
  // Send POST request with JSON body.                                   
  const res = await fetch(`${BASE_URL}${path}`, //below "application/json" required for FastAPI
    {method: "POST",headers: {"Content-Type": "application/json", }, body: JSON.stringify(body), // JS → JSON
    });

  // Manual error handling
  if (!res.ok) {
    throw new Error("Request failed");
  }

  // Convert response JSON → JavaScript object
  return res.json();
}










/* below code is to be used if we are using AXIOS in service/api.js file instead of fetch API. 
import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000",
});

// here 'api.' will used in .jsx file, and our fastapi "app" name is changed here to "api."
// app = FastAPI(title="Demo Backend") == api
// api.get("/message") == @app.get("/message")
// 👉 This file is the only place React talks to backend.    

*/