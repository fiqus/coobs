import {httpGet} from "../api-client";
  
export async function getAction(actionId) {
  const response = await httpGet(`/actions/${actionId}`);
  return response.data;
}

export async function getPrinciples(){
  const principlesResponse = await httpGet("/principles/");
  return principlesResponse.data;
}

export async function getPartners(cooperativeId){
  const partnersResponse = await httpGet(`/cooperatives/${cooperativeId}/partners`);
  return partnersResponse.data;
}

