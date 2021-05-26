// https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
// https://github.com/cure53/DOMPurify
import DOMPurify from "dompurify";
import marked from "marked";

export function sanitizeMarkdown(text) {
  return text ? sanitizeHtml(marked(text)) : "";
}

export function sanitizeHtml(text) {
  return text ? DOMPurify.sanitize(text) : "";
}

export function formatText(text, limit) {
  return (text||"").length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}

export function capitalizeFirstChar(s) {
  return s ? s.charAt(0).toUpperCase() + s.slice(1) : "";
}

export function parseNumber(number, locale) {
  return Intl.NumberFormat(locale || "es").format(number);
}

export function formatToUIDate(dateString, locale) {
  if (!dateString) {
    return;
  }

  const opts = {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    //timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
  };
  const dateObj = new Date((new Date(dateString)).getTime() + new Date().getTimezoneOffset()*60000);
  return Intl.DateTimeFormat(locale || "es", opts).format(dateObj);
}