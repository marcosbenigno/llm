"use client"
import React, { useState, useRef } from 'react';
import styles from './page.module.css';

const UploadForm = () => {
  const [file, setFile] = useState({
    string: null,
    form: null,
    selection: null,
  });
  const [isLoading, setIsLoading] = useState({
    string: false,
    form: false,
    selection: false,
  });
  const [results, setResults] = useState({
    string: '',
    form: '',
    selection: '',
  });
  const fileInputRef1 = useRef(null);
  const fileInputRef2 = useRef(null);
  const fileInputRef3 = useRef(null);

  const handleFileChange = (e, endpoint) => {
    const selectedFile = e.target.files[0];
    
    setFile((item) => ({ ...item, [endpoint]: selectedFile }));
   
    if (selectedFile) {
      handleSubmit(selectedFile, endpoint);
    }
  };

  function beautifyPythonJson(jsonString) {
    try {
     
      const cleanedJsonString = jsonString.replace(/\\/g, '');
  
      const jsonObject = JSON.parse(cleanedJsonString);
      return JSON.stringify(jsonObject, null, 2); 
    } catch (error) {
      console.error('Invalid JSON:', error);
      return null;
    }
  }

  const handleSubmit = async (selectedFile, endpoint) => {

    if (!selectedFile) {
      return;
    }
    const formData = new FormData();
    formData.append('jsonFile', selectedFile);
    
    try {
      setIsLoading((item) => ({ ...item, [endpoint]: true }));
      const response = await fetch(`http://127.0.0.1:5000/protocol/${endpoint}`, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const jsonData = await response.json();
        let stringResult;
        if (endpoint == 'string') {
          stringResult = JSON.stringify(jsonData.success).replaceAll('\\', '');
        } else {
          stringResult = beautifyPythonJson(jsonData.success);
        }
        setResults((item) => ({ ...item, [endpoint]: stringResult }));

        //alert(JSON.stringify(jsonData.success).replaceAll('\\', ''));
      } else {
        console.error('Failed to upload the file.');
      }
    } catch (error) {
      console.error('An error occurred:', error);
    } finally {
      setIsLoading((item) => ({ ...item, [endpoint]: false }));
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Systematic Review Assistant</h1>
      <h3 className={styles.title}>String Generator</h3>
      <form className={styles.form} encType="multipart/form-data" onSubmit={(e) => e.preventDefault()}>
        
        <input
          type="file"
          ref={fileInputRef1}
          style={{ display: 'none' }}
          name="jsonFile"
          onChange={(e) => {handleFileChange(e, 'string')}}
        />
        <div>
         
          <label
            htmlFor="file-input"
            style={{
              cursor: 'pointer',
              backgroundColor: 'grey',
              color: 'white',
              padding: '10px',
              borderRadius: '5px',
            }}
            onClick={() => fileInputRef1.current.click()}
          >
            Select JSON Protocol File
          </label>
         
          {file.string && <span style={{ marginLeft: '10px' }}>{isLoading.string ? `Working on ${file.string.name}...` : 'Done! '}</span>}
        </div>

        <button type="submit" style={{ display: 'none' }} />
      </form>
      <span className={styles.results}>{results.string && `Your string: ${results.string}`}</span>

      <h3 className={styles.title}>Forms Generator</h3>
      <form className={styles.form} encType="multipart/form-data" onSubmit={(e) => e.preventDefault()}>
        
        <input
          type="file"
          ref={fileInputRef2}
          style={{ display: 'none' }}
          name="jsonFile"
          onChange={(e) => {handleFileChange(e, 'form')}}
        />
        <div>
         
          <label
            htmlFor="file-input"
            style={{
              cursor: 'pointer',
              backgroundColor: 'grey',
              color: 'white',
              padding: '10px',
              borderRadius: '5px',
            }}
            onClick={() => fileInputRef2.current.click()}
          >
            Select JSON Protocol File
          </label>
          
          {file.form && <span style={{ marginLeft: '10px' }}>{isLoading.form ? `Working on ${file.form.name}...` : 'Done! '}</span>}
        </div>
   
        <button type="submit" style={{ display: 'none' }} />
      </form>
      <span className={styles.results}>{results.form && `Fields for your form: ${results.form}`}</span>


      <h3 className={styles.title}>Articles Selection</h3>
      <form className={styles.form} encType="multipart/form-data" onSubmit={(e) => e.preventDefault()}>
        
        <input
          type="file"
          ref={fileInputRef3}
          style={{ display: 'none' }}
          name="jsonFile"
          onChange={(e) => {handleFileChange(e, 'selection')}}
        />
        <div>

          <label
            htmlFor="file-input"
            style={{
              cursor: 'pointer',
              backgroundColor: 'grey',
              color: 'white',
              padding: '10px',
              borderRadius: '5px',
            }}
            onClick={() => fileInputRef3.current.click()}
          >
            Select JSON Protocol File
          </label>
     
          {file.selection && <span style={{ marginLeft: '10px' }}>{isLoading.selection ? `Working on ${file.selection.name}...` : 'Done! '}</span>}
        </div>

      </form>
      <span className={styles.results}>{results.selection && `Your selection data: ${results.selection}`}</span>
    </div>
  );
};

export default UploadForm;
