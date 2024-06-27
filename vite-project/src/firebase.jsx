// import { initializeApp } from "firebase/app";
// import { getStorage } from "firebase/storage";
// import { getAnalytics } from "firebase/analytics";

// const firebaseConfig = {
//   apiKey: "AIzaSyBLXCFAvQej9tJI6HCa_BDzxPx5Qs2jhoE",
//   authDomain: "pdfextraction-671cd.firebaseapp.com",
//   projectId: "pdfextraction-671cd",
//   storageBucket: "pdfextraction-671cd.appspot.com",
//   messagingSenderId: "459111462789",
//   appId: "1:459111462789:web:66de143592d9ba39a536ec",
//   measurementId: "G-P7YW504LMM"
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);
// export const storage = getStorage(app);
// const analytics = getAnalytics(app);


import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyAqXcQ7lTZqD1sHxUNqy_udqTv2oHWF3AA",
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