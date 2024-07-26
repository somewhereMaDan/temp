import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  // apiKey: "AIzaSyAqXcQ7lTZqD1sHxUNqy_udqTv2oHWF3AA",
  apiKey: `${import.meta.env.FIREBASE_KEY}`,
  authDomain: "fileextraction-c0dfa.firebaseapp.com",
  projectId: "fileextraction-c0dfa",
  storageBucket: "fileextraction-c0dfa.appspot.com",
  messagingSenderId: "1060303250744",
  appId: "1:1060303250744:web:52346c1f86c757b9014dcd",
  measurementId: "G-K2LP9JX696"
};

const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);
const analytics = getAnalytics(app);