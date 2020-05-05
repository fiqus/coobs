import {httpGet} from "../api-client";

export async function getActions() {
  const response = await httpGet("/actions");
  return response.data ? response.data : [];
}

export async function getAction(actionId) {
  const response = await httpGet(`/actions/${actionId}`);
  return response.data;
}

export async function getPrinciples(){
  const principlesResponse = await httpGet("/principles/");
  return principlesResponse.data;
}

export async function getSustainableDevelopmentGoals(){
  const principlesResponse = await httpGet("/sustainable-development-goals/");
  return principlesResponse.data;
}

export async function getSustainableDevelopmentGoal(goalId) {
  const response = await httpGet(`/sustainable-development-goals/${goalId}`);
  return response.data;
}

export async function getSDGObjective(sdgObjectiveId) {
  const response = await httpGet(`/sdg-objectives/${sdgObjectiveId}`);
  return response.data;
}

export async function getPartners(){
  const partnersResponse = await httpGet("/partners");
  return partnersResponse.data;
}


export async function getPartner(partnerId){
  const partnerResponse = await httpGet(`/partners/${partnerId}`);
  return partnerResponse.data;
}

export async function getDashboard(params) {
  const response = await httpGet("/dashboard", params);
  return response.data ? response.data : [];
}

export async function getMyStats(params) {
  const response = await httpGet("/my-stats", params);
  return response.data ? response.data : [];
}

export async function getPeriods(params) {
  const response = await httpGet("/periods", params);
  return response.data ? response.data : [];
}