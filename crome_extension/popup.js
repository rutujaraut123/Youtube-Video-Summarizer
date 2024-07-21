document.getElementById('fetchTranscript').addEventListener('click', function() {
    var link = document.getElementById('videoLink').value;
    chrome.runtime.sendMessage({ action: "getTranscript", link: link }, function(response) {
      if (response.transcript) {
        document.getElementById('transcript').textContent = response.transcript;
      } else {
        console.error('Error fetching transcript:', response.error);
      }
    });
  });
  