const STORAGE_KEY = "chat_history";

function saveMessages(messagesArray) {
  const msgs = Array.isArray(messagesArray) ? messagesArray : [messagesArray];
  const validMessages = msgs.filter(m => m && m.text);

  chrome.storage.local.get([STORAGE_KEY], res => {
    const history = res[STORAGE_KEY] || [];
    const updated = [...history, ...validMessages.map(m => ({
      ...m,
      id: crypto.randomUUID(),
      time: Date.now(),
      url: location.href
    }))];
    chrome.storage.local.set({ [STORAGE_KEY]: updated }, () => {
      console.log(`Saved ${validMessages.length} messages. Total: ${updated.length}`);
    });
  });
}

function loadMessages(render) {
  const currentDomain = new URL(location.href).hostname;
  chrome.storage.local.get([STORAGE_KEY], res => {
    const history = res[STORAGE_KEY] || [];
    history
      .filter(m => {
        try { return m.url && new URL(m.url).hostname === currentDomain; } 
        catch { return false; }
      })
      .forEach(m => render(m.role, m.text));
  });
}

function isValidJSON(str) {
  try { JSON.parse(str); return true; } 
  catch { return false; }
}