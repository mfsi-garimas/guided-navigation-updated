function handleClickCommand(targetText, messages) {
  const currentDomain = new URL(location.href).hostname;
  let found = false;
  chrome.storage.local.get([STORAGE_KEY], res => {
    const history = res[STORAGE_KEY] || [];
    for (const msg of history) {
      try { if (new URL(msg.url).hostname !== currentDomain) continue; } catch { continue; }
      if (msg.type == "search_suggestions") {
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = msg.text;
        tempDiv.querySelectorAll('.suggestion-btn').forEach(btn => {
          const btnText = btn.textContent.trim().toLowerCase();
          const target = targetText.trim().toLowerCase();
          if (btnText.includes(target) && !btnText.includes("search") && !btnText.includes("google")) {
            const link = btn.closest('a'); if (link) { link.click(); found = true; return found; }
          }
        });
      }
      if (found) break;
    }
  });
  return found;
}

function awaitUserInput(field, message) {
  return new Promise(resolve => {
    window.waitingForStepInput = true;
    const input = document.querySelector("#input");
    const messagesEl = document.querySelector("#messages");
    messagesEl.innerHTML += `<div class="message bot">🤖 ${message}</div>`;
    messagesEl.scrollTop = messagesEl.scrollHeight;
    saveMessages({ role: "bot", text: message });

    const oldHandler = input.onkeydown;
    input.onkeydown = e => {
      if (e.key === "Enter") {
        const value = input.value.trim(); if (!value) return;
        messagesEl.innerHTML += `<div class="message user">🧑 ${value}</div>`;
        messagesEl.scrollTop = messagesEl.scrollHeight;
        saveMessages({ role: "user", text: value });
        input.value = "";
        input.onkeydown = oldHandler;
        window.waitingForStepInput = false;
        resolve(value);
      }
    };
  });
}

async function executeSteps(steps, inputs, messages) {
  const userValues = {};
  console.log("INPUTS RECEIVED:", inputs);

  for (const step of steps) {

    if (step.action === "ask") {
      console.log("STEP:", step);
      console.log("CHECK:", inputs?.[step.input_name], inputs?.[step.selector?.replace('#','')]);
      step_id = step.selector
      if (step_id.startsWith('#')) { step_id = step_id.slice(1)}
      if (inputs[step.input_name] || inputs[step_id]) {
        userValues[step.field] = inputs[step.input_name] || inputs[step_id];
        console.log(userValues)
        messages.innerHTML += `<div class="message bot">🤖 Using provided ${step.input_name}</div>`;
        saveMessages({ role: "bot", text: `Using provided ${step.input_name}` });
        continue;
      }

      const current_el = document.querySelector(step.selector);
      let currentValue = "";

      const existingValue = current_el?.value?.trim();
      if (existingValue) {
        const newMessage = `Would you like to use this same ${step.field} "${existingValue}"? (Y/N)`;
        const confirmation = await awaitUserInput(step.field, newMessage);

        if (confirmation?.trim().toLowerCase() === "y") {
          userValues[step.field] = existingValue;
        } else {
          currentValue = await awaitUserInput(step.field, step.message);
          userValues[step.field] = currentValue?.trim();
        }
      } else {
        currentValue = await awaitUserInput(step.field, step.message);
        userValues[step.field] = currentValue?.trim();
      }
      messages.innerHTML += `<div class="message bot">🤖 Got input for ${step.field}</div>`;
      saveMessages({ role: "bot", text: `Got input for ${step.field}` });
      console.log(userValues)
      window.waitingForStepInput = false;
    }
    else if (step.action === "type") {
      const el = document.querySelector(step.selector);
      if (el) {
        const value = userValues[step.value_from] || inputs[step.value_from] || "";
        el.value = value;
        el.dispatchEvent(new Event('input', { bubbles: true }));
        messages.innerHTML += `<div class="message bot">🤖 Typed into ${step.selector}</div>`;
      } else {
        messages.innerHTML += `<div class="message bot">⚠️ Element not found: ${step.selector}</div>`;
      }
    }
    else if (step.action === "click") {
      if (step.selector) {
        if (step.selector.includes(":contains")) {
          const text = step.selector.match(/"(.+?)"/)[1];
          const el = Array.from(document.querySelectorAll("button, a, input"))
            .find(e => e.innerText?.trim() === text || e.value === text);
          el?.click();
        } else {
          document.querySelector(step.selector)?.click();
        }
      }
    }
    messages.scrollTop = messages.scrollHeight;
    await new Promise(r => setTimeout(r, 300));
  }
}