(async () => {
  if (document.getElementById("chatbot")) return;

  const BASE_URL = await getBaseUrl();

  const addMessage = ({ role, text, type }) => {
    const messages = document.querySelector("#messages"); 
    if (!messages) return;

    const el = document.createElement("div");
    el.className = `message ${role}`;
    if (type === "search_suggestions") {
      el.innerHTML = text;
    } else {
      el.textContent = `${role === "user" ? "🧑" : "🤖"} ${text}`;
    }
    messages.appendChild(el);
    messages.scrollTop = messages.scrollHeight;

    saveMessages(type ? { role, text, type } : { role, text });
  };

  const createChatbot = () => {
    const chatbot = document.createElement("div");
    chatbot.id = "chatbot";
    chatbot.innerHTML = `
      <div id="header">Guided Navigation</div>
      <div id="messages"></div>
      <div id="input-area"><input id="input" placeholder="Ask or command..." /></div>
    `;
    document.body.appendChild(chatbot);
    return chatbot;
  };

  const injectStyles = () => {
    const style = document.createElement("style");
    style.textContent = `
      #chatbot { position: fixed; bottom:20px; right:20px; width:360px; height:480px; background:#fff; color:#111; z-index:999999; display:flex; flex-direction:column; border-radius:14px; box-shadow:0 8px 20px rgba(0,0,0,0.2); font-family:Arial,sans-serif; overflow:hidden; }
      #header { padding:12px; background:#f5f5f5; cursor:move; font-weight:bold; font-size:15px; color:#333; border-bottom:1px solid #ddd; user-select:none; }
      #messages { flex:1; padding:12px; overflow-y:auto; display:flex; flex-direction:column; gap:8px; background:#fafafa; }
      .message { max-width:75%; padding:0; border-radius:14px; word-break:break-word; font-size:12px; line-height:1.4; }
      .user { align-self:flex-end; background:#007bff; color:#fff; }
      .bot { align-self:flex-start; background:#e5e5e5; color:#111; }
      #input { width:94%; margin:8px; padding:10px 14px; border:1px solid #ccc; border-radius:20px; outline:none; font-size:14px; box-shadow:inset 0 1px 3px rgba(0,0,0,0.1); transition:all 0.2s; }
      #input:focus { border-color:#007bff; box-shadow:0 0 5px rgba(0,123,255,0.4) inset; }
      .message.loader { display:flex; align-items:center; gap:6px; font-style:italic; color:#ff6600; }
      .message.loader::before { content:""; width:12px; height:12px; border:2px solid #ffcc99; border-top:2px solid #ff6600; border-radius:50%; animation:spin 1s linear infinite; }
      @keyframes spin { 0%{transform:rotate(0deg);}100%{transform:rotate(360deg);} }
    `;
    document.head.appendChild(style);
  };

  const enableDrag = (element) => {
    let isDown = false, offsetX = 0, offsetY = 0;
    const header = element.querySelector("#header");
    header.onmousedown = e => {
      isDown = true;
      offsetX = element.offsetLeft - e.clientX;
      offsetY = element.offsetTop - e.clientY;
    };
    document.onmouseup = () => isDown = false;
    document.onmousemove = e => {
      if (!isDown) return;
      element.style.left = e.clientX + offsetX + "px";
      element.style.top = e.clientY + offsetY + "px";
      element.style.bottom = "auto";
      element.style.right = "auto";
    };
  };

  // --- Initialize ---
  const chatbot = createChatbot();
  injectStyles();
  enableDrag(chatbot);

  const input = chatbot.querySelector("#input");
  const messages = chatbot.querySelector("#messages");

  loadMessages((role, text) => {
    messages.innerHTML += `<div class="message ${role}">${role === "user" ? "🧑" : "🤖"} ${text}</div>`;
    messages.scrollTop = messages.scrollHeight;
  });
  window.waitingForStepInput = false;

  input.onkeydown = async e => {
    if (e.key !== "Enter") return;
    const cmd = input.value.trim();
    if (!cmd) return;
    addMessage({ role: "user", text: cmd });
    input.value = "";

    if (window.waitingForStepInput) return;

    const response = await extractCommand(cmd, messages);
    if (!response || !response.action || !response.key) {
      addMessage( { role: "bot", text: "⚠️ Invalid command or format" });
      return;
    }
    addMessage({ role: "bot", text: `${JSON.stringify(response)}` });

    try {
      if (response.action === "form") {
          const forms = Array.from(document.querySelectorAll("form, input, textarea, select, button"))
                            .map(el => ({
                                tag: el.tagName.toLowerCase(),
                                id: el.id || null,
                                class: el.className || null,
                                name: el.name || null,
                                type: el.type || null,
                                text: el.innerText || el.value || el.placeholder || "",
                                selector: el.id ? `#${el.id}` : null
                            }));

          fetch(`${BASE_URL}/multi_step`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              command: cmd,
              elements: forms
            })
          })
            .then(res => res.json())
            .then(plan => {
                console.log("MultiStep Plan:", plan);
              messages.innerHTML += `<div class="message bot">🤖 Executing ${plan.steps.length} steps...</div>`;
              executeSteps(plan.steps, response.inputs, messages).then(() => {
                messages.innerHTML += `<div class="message bot">✅ Done executing form steps</div>`;
                addMessage({ role: "bot", text: `Executed ${plan.steps.length} steps for form` });
              });
            })
            .catch(err => {
              console.error(err);
              messages.innerHTML += `<div class="message bot">⚠️ Failed to process form</div>`;
              addMessage({ role: "bot", text: '⚠️ Failed to process form' });
            });

        } else {
          // -------------------- EXISTING CLICK/SEARCH/CHECK --------------------
          const clickresult = handleClickCommand(response.key,messages);
          if (!clickresult) {
            DOMelements(response)
            .then(scriptStr => {
              console.log("Full scriptStr response:", scriptStr);
              const script = scriptStr.selected_element;
              console.log("Script received:", script);
              // --- existing logic for click/search/check/uncheck remains unchanged ---
              if (script.action === 'click') {
                console.log("Trying selector:", script.selector);
                const selectedElements = document.querySelectorAll(script.selector);
                console.log("Found elements:", selectedElements.length);
                let found = false;
                for (const el of selectedElements) {
                  const text = (el.textContent || "").trim();
                  const title = el.getAttribute("title") || "";
                  const aria = el.getAttribute("aria-label") || "";
                  if (text.includes(script.text) || title.includes(script.text) || aria.includes(script.text)) {
                    const href = el.getAttribute("href") || "";
                    if (href.startsWith("javascript:")) {
                      const jsCode = href.replace(/^javascript:/, "");

                      const scriptTag = document.createElement("script");
                      scriptTag.textContent = jsCode;
                      document.documentElement.appendChild(scriptTag);
                      scriptTag.remove();
                    } else {
                      el.click(); 
                    }
                    addMessage({ role: "bot", text: `Clicked ${response.key}` })
                    found = true;
                    break;
                  }
                }
                if (!found) {
                  addMessage({ role: "bot", text: "⚠️ Element Not Found" })
                }
              }
              else if (script.action === 'check' || script.action === 'uncheck' || script.action === 'radio') {

                const elements = document.querySelectorAll(script.selector);

                if (!elements || elements.length === 0) {
                  addMessage({ role: "bot", text: "⚠️ Element Not Found" });
                  return;
                }

                const index = script.index ?? 0;
                const el = elements[index];

                if (!el) {
                  addMessage({ role: "bot", text: "⚠️ Invalid element index" });
                  return;
                }

                const shouldCheck = script.action === "check";

                if (el.type === "checkbox" || el.type === "radio") {
                  if (el.checked !== shouldCheck) el.click();
                } else {
                  el.click();
                }
                addMessage({
                  role: "bot",
                  text: `${script.action === 'check' ? 'Checked' : 'Unchecked'} ${script.text}`
                });
              }

                
              else if (script.action === 'search') {
                // --- search logic remains unchanged ---
                const inputElements = document.querySelectorAll(script.searchInput?.selector || '');
                for (const input of inputElements) {
                  const tag = input.tagName.toLowerCase();
                  if (tag === 'input' || tag === 'textarea') {
                    input.value='';
                    input.value = script.searchInput.key || '';
                    input.click();
                    input.focus();
                    input.dispatchEvent(new Event('input', { bubbles: true }));
                    input.dispatchEvent(new Event('change', { bubbles: true }));
                    input.dispatchEvent(new KeyboardEvent('keyup', { bubbles: true }));
                  }
                }
                const buttonElements = document.querySelectorAll(script.searchButton?.selector || '');
                for (const button of buttonElements) {
                  const tag = button.tagName.toLowerCase();
                  button.click();
                }

                if (script.resultsContainer && script.resultsContainer.selector) {
                  const resultsElements = document.querySelectorAll(script.resultsContainer?.selector || '');
                  for (const container of resultsElements) {
                    const items = [];
                    const elementsMap = new Map();
                    container.querySelectorAll('a, button, div[data-click], span[data-click]').forEach(child => {
                      const text = child.textContent?.trim();
                      const href = child.getAttribute('href');
                      if (text) {
                        items.push({ text, href });
                        elementsMap.set(text, child);
                      }
                    });

                    if (items.length === 0) {
                      addMessage({ role: "bot", text: "No suggestions found" });
                      break;
                    }

                    let suggestionsHTML = `<div class="message bot">Choose an option:</div><div class="bot-suggestions">`;
                    items.forEach(item => {
                      suggestionsHTML += `<a href="${item.href}"><button class="suggestion-btn">${item.text}</button></a>`;
                    });
                    suggestionsHTML += `</div>`;
                    addMessage({ role: "bot", text: suggestionsHTML, type: "search_suggestions" });
                  }
                } else {
                  addMessage({ role: "bot", text: 'Search results updated' });
                }
              }
              else {
                addMessage({ role: "bot", text: `⚠️ Unknown action: ${script.action}` });
              }
            })
            .catch(err => {
              console.error('Error fetching script:', err);
              addMessage({ role: "bot", text: '⚠️ Failed to process the action' });
            });
          }
        }
    } catch (err) {
      console.error(err);
      addMessage({ role: "bot", text: '⚠️ Failed to process the action' });
    }
  };
})();