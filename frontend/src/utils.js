// https://portswigger.net/web-security/cross-site-scripting/cheat-sheet
// https://github.com/cure53/DOMPurify
import DOMPurify from "dompurify";
import marked from "marked";

export function sanitizeMarkdown(text) {
  return sanitizeHtml(marked(text));
}

export function sanitizeHtml(text) {
  return DOMPurify.sanitize(text);
}

export function formatText(text, limit) {
  return text.length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}

export function capitalizeFirstChar(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export function parseNumber(number, locale) {
  return Intl.NumberFormat(locale || "es").format(number);
}

// format YYYY-MM-DD to DD/MM/YYY
export function formatToUIDate(dateString) {
  // TODO should we use assert to check the format?
  if (!dateString) {
    return;
  }
  const dateParts = dateString.split("-");
  if (!dateParts.length) {
    return `Error formatting ${dateString}`;
  }
  const invalidYear = !dateParts[0] || dateParts[0].length !== 4,
    invalidMonth = !dateParts[1] || dateParts[1].length !== 2 || !(dateParts[1] >= 1 && dateParts[1] <= 12),
    invalidDate = !dateParts[2] || dateParts[2].length !== 2 || !(dateParts[1] >= 1 && dateParts[1] <= 31);
  if (invalidYear || invalidMonth || invalidDate) {
    return `Error formatting ${dateString}`;
  }
  return `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
}