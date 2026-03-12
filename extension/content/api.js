async function apiPost(path, payload) {
  const BASE_URL = await getBaseUrl();
  const res = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`${path} failed`);
  return res.json();
}

function showLoader(messages) {
  const loader = document.createElement("div");
  loader.className = "message bot loader";
  loader.textContent = "🤖 Processing...";
  messages.appendChild(loader);
  messages.scrollTop = messages.scrollHeight;
}

function removeLoader(messages) {
  const loaderEl = messages.querySelector(".message.bot.loader");
  if (loaderEl) {
    loaderEl.remove();
  }
}

async function interpretCommandViaAPI(command, messages) {
  showLoader(messages)
  const elements = serializeDOM();
  try {
    const data = await apiPost("/interpret", { command, elements });
    console.log("Interprete Result:", data);
    return data;
  }  finally {
    removeLoader(messages)
  }
}

async function extractCommand(cmd, messages) {
  return await interpretCommandViaAPI(cmd, messages);
}

async function DOMelements(interpretedAction) {
  showLoader(messages)
  const elements = serializeDOM();
  try {
    return await apiPost("/get_required_elements", { interpreted_action: interpretedAction, elements });
  }  finally {
    removeLoader(messages)
  }
}