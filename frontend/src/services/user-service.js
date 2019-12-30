export function saveUser(user, $vm) {
  if ($vm) {
    $vm.localStorage.user = user;
  }
  localStorage.setItem("user", JSON.stringify(user));
}

export function getUser() {
  return JSON.parse(localStorage.getItem("user"));
}

export function removeUser() {
  localStorage.removeItem("user");
}