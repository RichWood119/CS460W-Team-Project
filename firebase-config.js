// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAclDJzi50FBG8anJ_F_fvxar6HCkEKvLs",
  authDomain: "cs460w-project.firebaseapp.com",
  databaseURL: "https://cs460w-project-default-rtdb.firebaseio.com",
  projectId: "cs460w-project",
  storageBucket: "cs460w-project.appspot.com",
  messagingSenderId: "266537356483",
  appId: "1:266537356483:web:53846e1fecfee208a1a676"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
console.log("Firebase initialized successfully!", app);
