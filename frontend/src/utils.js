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

function getMonthlyDataInitialState(principles, months) {
  let result = {};
  principles.map((principle) => {
    return result[principle.nameKey] = new Array(months).fill(0);
  });
  return result;
}

function getCategories(period) {
  //const months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
  //const monthsName = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", , "Oct", "Nov", "Dec"];
  const months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6:"Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"};

  const dateFromMonth = parseInt(getMonthFromDate(period.dateFrom));
  const dateToMonth = parseInt(getMonthFromDate(period.dateTo));
  const currentMonth = (new Date()).getMonth() + 1;

  return {
    categories: currentMonth < dateFromMonth ?  Object.keys(months).slice(dateFromMonth - 1, 12).concat(Object.keys(months).slice(0, dateToMonth))  : Object.keys(months).slice(dateFromMonth - 1, currentMonth),
    categoriesName: currentMonth < dateFromMonth ?  Object.values(months).slice(dateFromMonth - 1, 12).concat(Object.keys(months).slice(0, dateToMonth))  : Object.values(months).slice(dateFromMonth - 1, currentMonth)
  };
}

export function allPrinciplesMonthlyDataParser(doneActions, period, principles) {
  const {categories, categoriesName} = getCategories(period);

  const monthlyData = getMonthlyDataInitialState(principles, categories.length);

  doneActions.map((action) => {
    return  monthlyData[action.principleNameKey][parseInt(getMonthFromDate(action.date))-1] += 1;
  });

  const chartData = Object.keys(monthlyData).map((principle) => {
    return {"name": principle, "data": monthlyData[principle]};
  });
  return {"monthlyData": chartData, "categories": categoriesName};
}


export function getActionsDone(actions) {
  const today = new Date();
  return actions.filter((action) => {
    return new Date(action.date) < today;
  });
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