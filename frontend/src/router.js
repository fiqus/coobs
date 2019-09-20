import Vue from 'vue';
import VueRouter from 'vue-router';

// route components
import DashboardScreen from './screens/dashboard.vue';
import LoginScreen from './screens/login.vue';
import ActionsListScreen from './screens/actions/list.vue';
import ActionsEditScreen from './screens/actions/edit.vue';
import PrinciplesListScreen from './screens/principles/list.vue';
import PrincipleEditScreen from './screens/principles/edit.vue';

Vue.use(VueRouter);

const routes = [
  {
    name: "actions-list",
    path: "/actions",
    component: ActionsListScreen
  },
  {
    name: "action-edit",
    path: "/action-edit/:actionId",
    component: ActionsEditScreen
  },
  {
    name: "principles-list",
    path: "/principles",
    component: PrinciplesListScreen,
    props: {edited: false}
  },
  {
    name: "principle-edit",
    path: "/principle-edit/:principleId",
    component: PrincipleEditScreen
  },
  {
    name: "dashboard",
    path: "/",
    component: DashboardScreen
  },
  {
    name: "login",
    path: "/login",
    meta: {layout: "empty"},
    component: LoginScreen
  },

  // otherwise redirect to dashboard
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
