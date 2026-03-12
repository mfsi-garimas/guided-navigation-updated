function getDirectText(el) {
  return [...el.childNodes]
    .filter(node => node.nodeType === Node.TEXT_NODE)
    .map(node => node.textContent.trim())
    .join(" ");
}

function serializeDOM() {
  return [...document.querySelectorAll('*')]
    .filter(el => {
      if (el.closest('#chatbot')) return false;
      if (['SCRIPT','STYLE','META','LINK'].includes(el.tagName)) return false;
      const text = getDirectText(el).trim();
      const hasIdentity = el.id || el.classList.length > 0;
      const isInteractive = ['INPUT','BUTTON','SELECT','TEXTAREA'].includes(el.tagName);
      const hasRole = el.getAttribute('role');
      return text !== "" || hasIdentity || isInteractive || hasRole;
    })
    .map(el => {
      let text = getDirectText(el).trim();
      const attributes = [...el.attributes].reduce((acc, attr) => {
        acc[attr.name] = attr.value; return acc;
      }, {});
      if ((text === "" || text === "<" || text === ">") && attributes.title) text = attributes.title;
      return {
        tag: el.tagName.toLowerCase(),
        id: el.id || null,
        class: el.classList.length ? [...el.classList].join(" ") : null,
        text: text.slice(0, 500),
        role: el.getAttribute('role'),
        ariaLabel: el.getAttribute('aria-label'),
        attributes: attributes
      };
    });
}