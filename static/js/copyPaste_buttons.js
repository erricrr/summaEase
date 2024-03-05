// var isRecording = false;
// var recognition;
// const lang = 'en-US';


// Copy Transcription Text
function copyToClipboardTrans() {
  var textareaElement = document.querySelector('textarea');
  var textareaText = textareaElement.value;

  navigator.clipboard.writeText(textareaText)
    .then(function() {
      alert('Copied to clipboard!');
    })
    .catch(function(error) {
      console.error('Failed to copy to clipboard: ', error);
    });
};


function copyToClipboardSum() {
  var summaryElement = document.getElementById('summaryBlock');
  var summaryText = summaryElement.innerHTML;
  var tempDiv = document.createElement('div');

  tempDiv.style.position = 'fixed';
  tempDiv.style.opacity = '0';
  tempDiv.innerHTML = summaryText;
  document.body.appendChild(tempDiv);

  var range = document.createRange();
  range.selectNodeContents(tempDiv);
  var selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);

  try {
    document.execCommand('copy');
    alert('Copied to clipboard!');
  } catch (error) {
    console.error('Copy failed: ', error);
  }

  selection.removeAllRanges();
  document.body.removeChild(tempDiv);
}


// Disable TRANSCRIBE button
function enableTranscribeButton(buttonId, fileId) {
  // Get the file input element
  const fileInput = document.querySelector(`input[name="${fileId}"]`);

  // Get the transcribe button element
  const transcribeButton = document.getElementById(buttonId);

  // Enable the transcribe button if a file is selected, otherwise disable it
  if (fileInput.files.length > 0) {
    transcribeButton.disabled = false;

  } else {
    transcribeButton.disabled = true;

  }
}

// WORKS FOR CUT AND PASTE ENTIRES
var textarea = document.getElementById("textInput");
var summarizeButton = document.getElementById("submitButton");

// Add an event listener to the textarea for input changes
textarea.addEventListener("input", function () {
  // Check if the textarea has any text
  if (textarea.value.trim() !== "") {
    // Enable the Summarize button
    summarizeButton.disabled = false;
  } else {
    // Disable the Summarize button
    summarizeButton.disabled = true;
  }
});






