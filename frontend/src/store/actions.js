import {httpPut} from "../api-client.js";

export const actions = {
  logout({commit}) {
    commit("setUser", {});
    commit("setCooperative", {});
    commit("setLang", "");
  },
  updateCooperative({commit}, cooperative) {
    httpPut(`/cooperatives/${cooperative.id}/`, cooperative)
      .then((response) => {
        commit("setCooperative", response.data);
      })
  }
};
