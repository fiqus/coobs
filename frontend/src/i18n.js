export function loadLocalMessage(lang) {
  const messages = require(`./locales/${lang}.json`);
  return messages;
}
