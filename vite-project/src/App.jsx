import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { toast, Toaster } from "sonner";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { storage } from './firebase.jsx';
import { v4 } from "uuid";

const UploadPDF = () => {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [extractedText, setExtractedText] = useState([]);
  const [summary, setSummary] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [answer, setAnswer] = useState('');

  const [TotalFileNames, setTotalFileNames] = useState([])

  const handleFileChange = (event) => {
    setSelectedFiles(prevFiles => [...prevFiles, ...Array.from(event.target.files)]);
  };


  const handleSubmit = async (event) => {
    event.preventDefault();
    if (selectedFiles.length === 0) {
      alert('Please select at least one file');
      return;
    }

    toast.info("Uploading the files and generating summaries...");
    const fileURLs = [];

    for (const file of selectedFiles) {
      const fileRef = ref(storage, `Files/${file.name + v4()}`);
      setTotalFileNames(prevFileNames => [...prevFileNames, file.name]);
      try {
        const snapshot = await uploadBytes(fileRef, file);
        const url = await getDownloadURL(snapshot.ref);
        fileURLs.push(url);
      } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file');
        return;
      }
    }

    try {
      const response = await axios.post('http://localhost:5000/upload', { fileURLs });

      toast.success("PDFs Uploaded Successfully, summaries generated.");
      setExtractedText(response.data.extracted_texts);
      setSummary(response.data.summaries);
    } catch (error) {
      console.error('Error uploading files:', error);
      alert('Error uploading files');
    }
  };

  const handleInputSubmit = async (e) => {
    e.preventDefault();
    toast.info("Generating Answer...")
    try {
      const response = await axios.post('http://localhost:5000/promptAnswer', {
        prompt: prompt,
        TotalFileNames: TotalFileNames
      });
      toast.success("Answer Generated")
      setAnswer(response.data); // Updated to set the answer
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className='mainpage'>
      <Toaster richColors />
      <div>
        <h1>Upload PDF Files</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} multiple />
          <button type="submit">Upload</button>
        </form>
        {/* {extractedText.length > 0 && extractedText.map((text, index) => (
          <div key={index}>
            <h2>Extracted Text {index + 1}:</h2>
            <p>{text}</p>
          </div>
        ))} */}
        {summary.length > 0 && summary.map((sum, index) => (
          <div key={index}>
            <h2>Summary by AI For PDF {index + 1}, PDF Name: {TotalFileNames[index]}:</h2>
            <p>{sum}</p>
          </div>
        ))}
      </div>

      <div>
        <h2>Generate a Question-Based Answer from the PDFs</h2>
        <form className='Generate_Answer_Form' onSubmit={handleInputSubmit}>
          <div>
            <input type="text" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Enter your prompt here" />
          </div>
          <div>
            <button type="submit">Generate Answer</button>
          </div>
        </form>
        {answer && (
          <div>
            <h2>Answer by AI:</h2>
            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default UploadPDF;
