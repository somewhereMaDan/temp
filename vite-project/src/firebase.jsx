import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyBLXCFAvQej9tJI6HCa_BDzxPx5Qs2jhoE",
  authDomain: "pdfextraction-671cd.firebaseapp.com",
  projectId: "pdfextraction-671cd",
  storageBucket: "pdfextraction-671cd.appspot.com",
  messagingSenderId: "459111462789",
  appId: "1:459111462789:web:66de143592d9ba39a536ec",
  measurementId: "G-P7YW504LMM"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const storage = getStorage(app);
const analytics = getAnalytics(app);