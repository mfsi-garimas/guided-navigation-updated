const STORAGE_KEY_BASE_URL = "BASE_URL";
const DEFAULT_BASE_URL = "http://127.0.0.1:8001/api";

function setBaseUrl(url) {
  chrome.storage.local.set({ [STORAGE_KEY_BASE_URL]: url });
}

async function getBaseUrl() {
  return new Promise(resolve => {
    chrome.storage.local.get([STORAGE_KEY_BASE_URL], res => {
      const storedUrl = res[STORAGE_KEY_BASE_URL];
      if (storedUrl) {
        resolve(storedUrl);
      } else {
        const userUrl = prompt(
          "Please enter the BASE_URL for the API:",
          DEFAULT_BASE_URL
        );
        const finalUrl = userUrl || DEFAULT_BASE_URL;
        setBaseUrl(finalUrl);
        resolve(finalUrl);
      }
    });
  });
}