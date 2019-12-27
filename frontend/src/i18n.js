import Vue from 'vue';
import VueI18n from 'vue-i18n';
import browserLocale from 'browser-locale';

Vue.use(VueI18n);

// browserLocale returns the current browser locale i.e. en-US, we just need the first part 'en'
const locale = localStorage.getItem("lang") || browserLocale().split("-")[0];

function loadLocalMessage(lang) {
  const messages = require(`./locales/${lang}.json`);
  return {[lang]: messages};
}

const currentLang = locale || 'en';
localStorage.setItem("lang", currentLang);
const loadedLanguages = [currentLang];

export const i18n = new VueI18n({
  locale: currentLang,
  fallbackLocale: 'en',
  messages: loadLocalMessage(currentLang)
});

function setI18nLanguage(lang) {
  i18n.locale = lang;
  document.querySelector('html').setAttribute('lang', lang);
  return lang;
}

export function loadLanguageAsync(lang) {
  localStorage.setItem("lang", lang);
  // If the same language and it was already loaded
  if (i18n.locale === lang) {
    return Promise.resolve(setI18nLanguage(lang))
  }

  // If the language was already loaded
  if (loadedLanguages.includes(lang)) {
    return Promise.resolve(setI18nLanguage(lang))
  }

  // If the language hasn't been loaded yet
  return import(`./locales/${lang}.json`).then(
    messages => {
      i18n.setLocaleMessage(lang, messages.default)
      loadedLanguages.push(lang)
      return setI18nLanguage(lang)
    }
  )
}

export function setCurrentBorwserLang() {
  const currentLang = locale || 'en';
  localStorage.setItem("lang", currentLang);
}