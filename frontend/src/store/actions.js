export const actions = {
  logout({commit}) {
    commit("setUser", {});
    commit("setLang", "");
  }
};
