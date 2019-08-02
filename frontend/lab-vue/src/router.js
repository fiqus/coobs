import Vue from 'vue';
import VueRouter from 'vue-router';

// route components
import HomeScreen from './screens/home.vue';
import LoginScreen from './screens/login.vue';

Vue.use(VueRouter);

const routes = [
  {
    name: "home",
    path: "/",
    component: HomeScreen
  },
  {
    name: "login",
    path: "/login",
    component: LoginScreen
  },

  // otherwise redirect to home
  { path: '*', redirect: '/' }
];

const router = new VueRouter({
  routes
});

const publicScreens = ["login"];

router.beforeEach((to, from, next) => {
  const navToPrivateScreen = !publicScreens.includes(to.name);
  const loggedIn = true; // can be this an async op?

  if (navToPrivateScreen && !loggedIn) {
    return next({name: "login"});
  }

  next();
});

export default router;
