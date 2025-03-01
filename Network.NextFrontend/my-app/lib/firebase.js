import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyD1D5jm3lbhqA3aYftLtAGCXCEYVRNmS0k",
  authDomain: "next-app-18c2d.firebaseapp.com",
  projectId: "next-app-18c2d",
  storageBucket: "next-app-18c2d.appspot.com",
  messagingSenderId: "314945170574",
  appId: "1:314945170574:web:0190154b827fbe2a3feddf",
  measurementId: "G-LGRP468TS5"
};

// Ensure Firebase is initialized only once
const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();

const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { auth, provider };
