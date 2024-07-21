chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === "getTranscript") {
      fetch('http://127.0.0.1:5000/get_transcript', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ link: message.link })
      })
      .then(response => response.text())
      .then(data => sendResponse({ transcript: data }))
      .catch(error => sendResponse({ error: error }));
      return true;
    }
  });
  