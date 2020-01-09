export function formatText(text, limit) {
  return text.length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}

export function partnersParser(selectedPartnersIdList, partnersObject) {
  let parsedPartners = selectedPartnersIdList.map(function(partnerId){
    return {id: partnerId.toString(), name: partnersObject[partnerId]};
  });
  return parsedPartners;
}

export function capitalizeFirstChar(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export function allPrinciplesDataParser(actions) {
  let accumulator = {
    "Open and voluntary membership": 0,
    "Democratic control of the members": 0,
    "Economic participation of members": 0,
    "Autonomy and independence": 0,
    "Education, training and information": 0,
    "Cooperation between cooperatives": 0,
    "Commitment to the community": 0
  };
  return actions.reduce(function(acc, action){
    acc[action.principleName] += 1;
    return acc;
  }, accumulator);
}

export function parseMoney(number) {
  return number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,"); 
}