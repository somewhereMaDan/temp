import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { toast, Toaster } from "sonner";

const UploadPDF = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [extractedText, setExtractedText] = useState('');
  const [summary, setSummary] = useState('');
  const [prompt, setPrompt] = useState('');
  const [answer, setAnswer] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleInputSubmit = async (e) => {
    e.preventDefault();
    toast.info("Generating Answer...")
    try {
      const response = await axios.post('http://localhost:5000/promptAnswer', {
        prompt: prompt
      });
      toast.success("Answer Generated")
      setAnswer(response.data); // Updated to set the answer
    } catch (err) {
      console.log(err);
    }
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      alert('Please select a file');
      return;
    }
    toast.info("Generating a summary while upload the file")

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      toast.success("PDF Uploaded Successfully, also Summary Got Generated")
      setExtractedText(response.data.extracted_text);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div className='mainpage'>
      <Toaster richColors />
      <div>
        <h1>Upload a PDF File</h1>
        <form onSubmit={handleSubmit}>
          <input type="file" onChange={handleFileChange} />
          <button type="submit">Upload</button>
        </form>
        {extractedText && (
          <div>
            <h2>Extracted Text:</h2>
            <p>{extractedText}</p>
          </div>
        )}

        {summary && (
          <div>
            <h2>Summary by AI:</h2>
            <p>{summary}</p>
          </div>
        )}
      </div>
      <div>
        <form style={{ marginTop: '20px' }} onSubmit={handleInputSubmit}>
          <input onChange={(e) => setPrompt(e.target.value)} type="textarea" />
          <button style={{ marginLeft: '20px' }} type="submit">Ask</button>
          <div>
            <p>{answer}</p> {/* Display the answer here */}
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadPDF;
