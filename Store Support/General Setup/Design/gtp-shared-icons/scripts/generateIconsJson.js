/* This JavaScript code snippet is reading SVG files from a specified folder, converting them to base64 strings, and then saving the base64 strings along with the file names into a JSON file. */
const fs = require('fs');
const path = require('path');
const base64 = require('base64-js');

// Path to the folder containing the SVG files
const folderPath = path.resolve(__dirname, '../images/icons');

// Initialize an empty object to store the base64 strings
const svgObj = {};

// Read the directory
fs.readdir(folderPath, (err, files) => {
  if (err) {
    console.error(err);
    return;
  }

  // Iterate over each file in the folder
  files.forEach((file) => {
    // Check if the file is an SVG
    if (path.extname(file).toLowerCase() === '.svg') {
      // Read the SVG file as binary data
      const filePath = path.join(folderPath, file);
      const data = fs.readFileSync(filePath);

      // Convert the binary data to base64 string
      const base64Data = base64.fromByteArray(data);

      // Add the base64 string to the object with the filename as key
      let filename = path.basename(file, path.extname(file));
      svgObj[filename] = base64Data;
    }
  });

  // Convert the object to JSON
  const json = JSON.stringify(svgObj, null, 2);
  const outputFilePath = path.resolve(__dirname, '../assets/icons.json');
  // Write the JSON data to a file
  fs.writeFile(outputFilePath, json, 'utf8', (err) => {
    if (err) {
      console.error(err);
      return;
    }
    console.log('Conversion complete. JSON file saved.');
  });
});
