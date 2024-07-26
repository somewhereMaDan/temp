import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAqXcQ7lTZqD1sHxUNqy_udqTv2oHWF3AA",
  // apiKey: `${import.meta.env.FIREBASE_KEY}`,
  authDomain: "fileextraction-c0dfa.firebaseapp.com",
  // authDomain: `${import.meta.env.AUTH_DOMAIN}`,
  projectId: "fileextraction-c0dfa",
  // storageBucket: `${import.meta.env.StorageBucket}`,
  storageBucket : "fileextraction-c0dfa.appspot.com",
  // messagingSenderId: `${import.meta.env.Messaging_Sender_Id}`,
  messagingSenderId: "1060303250744",
  appId: "1:1060303250744:web:52346c1f86c757b9014dcd",
  // measurementId: `${import.meta.env.Measurement_Id}`
  measurementId: "G-K2LP9JX696"
};

const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);
// const analytics = getAnalytics(app);