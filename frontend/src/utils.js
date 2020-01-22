export function formatText(text, limit) {
  return text.length > limit ? `${text.substring(0, (limit - 3))}..` : text;
}

export function partnersSelectedParser(selectedPartnersIdList, partnersObject) {
  let parsedPartners = selectedPartnersIdList.map(function(partnerId){
    return {id: partnerId.toString(), name: partnersObject[partnerId]};
  });
  return parsedPartners;
}

export function principlesSelectedParser(selectedPrinciplesIdList, principles) {
  const principlesObject = principles.reduce((acc, principle) => {
    acc[principle.id] = [principle.name, principle.nameKey];
    return acc;
  }, {});
  let parsedPrinciples = selectedPrinciplesIdList.map(function(principleId){
    return {id: principleId.toString(), name: principlesObject[principleId][0], nameKey: principlesObject[principleId][1]} ;
  });
  return parsedPrinciples;
}

export function capitalizeFirstChar(s) {
  return s.charAt(0).toUpperCase() + s.slice(1);
}

export function principlesParser(allPrinciplesData, totalActions) {
  const fullPercentage = totalActions / allPrinciplesData.labels.length / totalActions;

  return allPrinciplesData.labels.map((principle, index) => {
    return {"label": principle, "percentage": (parseInt(allPrinciplesData.series[index]) / totalActions * 100 / fullPercentage).toFixed(0)};
  });
}

export function parseMoney(number) {
  return number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,"); 
}

export function translatePrinciples(results, translateFunction) {
  return results.map((result) => {
    result.name = translateFunction(result.name);
    return result;
  });
}