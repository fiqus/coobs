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

export function translateLabels(obj, translateFunction) {
  const labels = Object.keys(obj);
  return labels.map((label) => {
    return translateFunction(label);
  });
}

export function allPrinciplesDataParser(actions, principles, translateFunction) {
  let principlesData = actions.reduce(function(acc, action){
    acc[action.principleNameKey] += 1;
    return acc;
  }, principles);
  return {"labels": translateLabels(principlesData, translateFunction), "series": Object.values(principlesData)};
}

function getMonthFromDate(date) {
  return date.slice(5, 7);
}

export function allPrinciplesMonthlyDataParser(doneActions, period) {
  const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const dateFromMonth = parseInt(getMonthFromDate(period.dateFrom));
  const currentMonth = (new Date()).getMonth() + 1;

  const categories = months.slice(dateFromMonth - 1, currentMonth);

  categories.map((categorie, index) => {
    doneActions.filter((action) => {
      return getMonthFromDate(action.date) == index
    });
  });
}

export function getActionsDone(actions) {
  const today = new Date();
  return actions.filter((action) => {
    return new Date(action.date) < today;
  });
}

export function principlesParser(allPrinciplesData, totalActions) {
  return allPrinciplesData.labels.map((principle, index) => {
    return {"label": principle, "percentage": parseInt(allPrinciplesData.series[index])/totalActions*100};
  });
}

export function parseMoney(number) {
  return number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,"); 
}