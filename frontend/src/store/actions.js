export const actions = {
  logout({commit}) {
    commit("setUser", {});
    commit("setCooperative", {});
    commit("setLang", "");
  }
};
