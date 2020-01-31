import Vue from "vue";
import VueRouter from "vue-router";

// route components
import DashboardScreen from "./screens/dashboard.vue";
import LoginScreen from "./screens/login.vue";
import ActionsListScreen from "./screens/actions/list.vue";
import ActionsEditScreen from "./screens/actions/edit.vue";
import PrinciplesListScreen from "./screens/principles/list.vue";
import PrincipleEditScreen from "./screens/principles/edit.vue";
import PeriodsListScreen from "./screens/periods/list.vue";
import PeriodEditScreen from "./screens/periods/edit.vue";
import ProfileScreen from "./screens/profile/profile.vue";
import SignupScreen from "./screens/signup.vue";
import BalanceScreen from "./screens/balance.vue";
import ActionsRankingScreen from "./screens/actions-ranking.vue";
import CooperativeScreen from "./screens/cooperative.vue";
import PartnersListScreen from "./screens/partners/list.vue";
import PartnerEditScreen from "./screens/partners/edit.vue";

import store from './store';

Vue.use(VueRouter);

const routes = [
  {
    name: "profile",
    path: "/profile",
    component: ProfileScreen
  },
  {
    name: "periods-list",
    path: "/periods",
    component: PeriodsListScreen
  },
  {
    name: "period-edit",
    path: "/period-edit/:periodId",
    component: PeriodEditScreen
  },
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
    name: "balance",
    path: "/balance",
    component: BalanceScreen
  },  
  {
    name: "actions-ranking",
    path: "/actions-ranking",
    component: ActionsRankingScreen
  },
  {
    name: "cooperative",
    path: "/cooperative",
    component: CooperativeScreen
  },
  {
    name: "partners-list",
    path: "/partners",
    component: PartnersListScreen
  },
  {
    name: "partner-edit",
    path: "/partner-edit/:partnerId",
    component: PartnerEditScreen
  },  
  {
    name: "login",
    path: "/login",
    meta: {layout: "login"},
    component: LoginScreen
  },
  {
    name: "signup",
    path: "/signup",
    meta: {layout: "login"},
    component: SignupScreen,
    props: (route) => ({coopName: route.query.coopName, coopEmail: route.query.coopEmail})
  },

  // otherwise redirect to dashboard
  { path: "*", redirect: "/" }
];

const router = new VueRouter({
  routes
});

const publicScreens = ["login", "signup"];

router.beforeEach((to, from, next) => {
  const navToPrivateScreen = !publicScreens.includes(to.name);
  // const user = getUser();
  const user = store.state.user;
  const loggedIn = user && user.access;

  if (navToPrivateScreen && !loggedIn) {
    return next({name: "login"});
  }

  next();
});

export default router;
