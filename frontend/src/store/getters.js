export const getters = {
  userFullName(state) {
    return `${state.user.firstName} ${state.user.lastName}`;
  }
}