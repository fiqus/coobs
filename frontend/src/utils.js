export function formatText(text, limit) {
  return text.length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}

export function capitalizeFirstChar(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

// TODO not in use. Maybe should?
export function parseMoney(number) {
  return number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,"); 
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