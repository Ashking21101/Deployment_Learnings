/*==================================================
This file is the SINGLE communication layer
between React frontend and FastAPI backend.
==================================================*/

const BASE_URL = "http://localhost:8000";

// Production (AWS App Runner)
// const BASE_URL = "https://innx5kfubm.ap-south-1.awsapprunner.com";


// no auth required
export async function apiGet(path) {
  const res = await fetch(`${BASE_URL}${path}`);
  if (!res.ok) {
    throw new Error("GET request failed");
  }
  return res.json(); // convert json response to js object
}


// This function expects a Clerk JWT token
// which proves the identity of the logged-in user
export async function apiPost(path, body, token) {
  // Send POST request to backend
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    // Headers sent to FastAPI : {Required so FastAPI can parse JSON, Clerk JWT (WHO is calling) token sent to backend}, body =Convert JavaScript object → JSON string
    headers: {"Content-Type": "application/json", Authorization: `Bearer ${token}`, }, body: JSON.stringify(body),
  });

  if (!res.ok) {
    throw new Error("POST request failed");
  }
  return res.json();
}






