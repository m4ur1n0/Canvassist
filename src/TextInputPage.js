import React, { useState } from 'react';
import './styles.css';

export default function TextInputPage() {
  const [inputText, setInputText] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Save the input text to a local text file
    saveTextToFile(inputText);

    // Call the local Python script
    callPythonScript();
  };

  const saveTextToFile = (text) => {
    const fileContent = new Blob([text], { type: 'text/plain' });
    const file = new File([fileContent], 'input.txt');

    // Create a URL for the file
    const fileURL = URL.createObjectURL(file);

    // Automatically download the file
    const link = document.createElement('a');
    link.href = fileURL;
    link.setAttribute('download', 'input.txt');
    document.body.appendChild(link);
    link.click();
  };

  const callPythonScript = () => {
    // Use JavaScript to call the Python script
    // Example: require('child_process').execSync('python run.py');
    // Or use another method that fits your requirements
  };

  return (
    <div className="container">
      <form onSubmit={handleSubmit}>
        <label>
          Enter Text:
          <textarea value={inputText} onChange={(e) => setInputText(e.target.value)} />
        </label>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}
