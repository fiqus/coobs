export function formatText(text, limit) {
  return text.length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}