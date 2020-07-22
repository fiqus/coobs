<template>
  <div>
    <!-- Page Wrapper -->
    <div id="wrapper">

      <!-- Sidebar -->
      <ul class="navbar-nav bg-gradient-info sidebar sidebar-dark accordion" :class="{'toggled': toggled}" data-toggle="collapse" id="accordionSidebar">
        <!-- Sidebar - Brand -->
        <router-link class="sidebar-brand d-flex align-items-center justify-content-center" :to="{name: 'dashboard'}" >
          <div v-if="toggled" class="sidebar-brand-icon">
            <img src="images/bs.png" style="max-height: 45px;">
          </div>
          <div class="sidebar-brand-text mx-3">
            <img src="images/Logo_completo_negativo.png" style="height: 28px;">
          </div>
        </router-link>

        <!-- Divider -->
        <hr class="sidebar-divider my-0">

        <!-- Nav Item - Dashboard -->
        <li class="nav-item">
          <router-link class="nav-link collapsed" class-active="active" :to="{name: 'dashboard'}" >
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>{{$t("dashboard")}}</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'actions-list'}" >
            <i class="fas fa-fw fa-clipboard-list"></i>
            <span>{{$t("actions")}}</span>
          </router-link>
        </li>      
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'balance'}">
            <i class="fas fa-fw fa-balance-scale"></i>
            <span>{{$t("balance")}}</span>
          </router-link>
        </li>        
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'actions-ranking'}">
            <i class="fas fa-fw fa-th-list"></i>
            <span>{{$t("actionsRanking")}}</span>
          </router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link collapsed" class-active="active" :to="{name: 'my-stats'}" >
            <i class="fas fa-fw fa-signal"></i>
            <span>{{$t("myStats")}}</span>
          </router-link>
        </li>
        <li class="nav-item">
          <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapsePages" aria-expanded="false" aria-controls="collapsePages">
            <i class="fas fa-fw fa-cog"></i>
            <span>{{$t("configuration")}}</span>
          </a>
          <div id="collapsePages" class="collapse" aria-labelledby="headingPages" data-parent="#accordionSidebar" style="">
            <div class="bg-white py-2 collapse-inner rounded">
              <router-link class="collapse-item" :to="{name: 'partners-list'}"><i class="fas fa-user-friends"></i> {{$t("partners")}}</router-link>
              <router-link class="collapse-item" :to="{name: 'principles-list'}"><i class="fas fa-fw fa-map-signs"></i> {{$t("principles")}}</router-link>
              <router-link class="collapse-item" :to="{name: 'periods-list'}"><i class="fas fa-fw fa-calendar"></i> {{$t("periods")}}</router-link>
              <router-link class="collapse-item " :to="{name: 'cooperative'}"><i class="fas fa-fw fa-edit"></i> {{$t("yourCoop")}}</router-link>
            </div>
          </div>
        </li>
        <li v-if="$store.state.cooperative.sustainableDevelopmentGoalsActive" class="nav-item">
          <a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapseSDGPages" aria-expanded="false" aria-controls="collapseSDGPages">
            <i class="fas fa-fw fa-globe-americas"></i>
            <span>{{$t("sustainableDevelopmentGoals")}}</span>
          </a>
          <div id="collapseSDGPages" class="collapse" aria-labelledby="headingPages" data-parent="#accordionSidebar" style="">
            <div class="bg-white py-2 collapse-inner rounded">
              <router-link class="collapse-item" :to="{name: 'sdg-balance'}"><i class="fas fa-fw fa-balance-scale"></i> {{$t("socialBalance")}}</router-link>
              <router-link class="collapse-item text-truncate" :to="{name: 'sustainable-development-goals'}"><i class="fas fa-fw fa-table"></i> {{$t("descriptiveTable")}}</router-link>
              <router-link class="collapse-item" :to="{name: 'sdg-objectives-list'}"><i class="fas fa-fw fa-bullseye"></i> {{$t("goals")}}</router-link>
              <router-link class="collapse-item " :to="{name: 'sdg-monitoring'}"><i class="fas fa-fw fa-chart-bar"></i> {{$t("monitoring")}}</router-link> <!-- file-medical-alt -->
            </div>
          </div>
        </li>
        <!-- Sidebar Toggler (Sidebar) -->
        <div class="text-center d-none d-md-inline">
          <button class="rounded-circle border-0" id="sidebarToggle" @click="toggled = !toggled"></button>
        </div>

      </ul>
      <!-- End of Sidebar -->

      <!-- Content Wrapper -->
      <div id="content-wrapper" class="d-flex flex-column">

        <!-- Main Content -->
        <div id="content">

          <!-- Topbar -->
          <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
            <h1 class="display-5">{{$store.state.cooperative.name || $store.state.cooperative.businessName}}</h1>
            <!-- Sidebar Toggle (Topbar) -->
            <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
              <i class="fa fa-bars"></i>
            </button>

            <!-- Topbar Navbar -->
            <ul class="navbar-nav ml-auto">

              <li class="nav-item dropdown no-arrow">
                <a class="nav-link dropdown-toggle" href="#" id="inputGroupSelect01" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <select class="mr-2 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-model="currentLanguage">
                    <option v-for="locale in Object.keys(locales)" :key="locale" :value="locale">
                      {{locales[locale]}}
                    </option>
                  </select>
                </a>
              </li>

              <div class="topbar-divider d-none d-sm-block"></div>

              <!-- Nav Item - User Information -->
              <li class="nav-item dropdown no-arrow">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <span class="mr-2 d-none d-lg-inline text-gray-600 small">{{userFullName}}</span>
                  <i class="fas fa-user-cog fa-sm fa-fw mr-2 text-gray-400"></i>
                </a>
                <!-- Dropdown - User Information -->
                <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">
                  <router-link class="dropdown-item" :to="{name: 'profile'}">
                    <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                    <span>{{$t("profile")}}</span>
                  </router-link>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#" @click="logout()">
                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                    {{$t("logout")}}
                  </a>
                </div>
              </li>

            </ul>

          </nav>
          <!-- End of Topbar -->

          <!-- Begin Page Content -->
          <div class="container-fluid">
            <!-- In this slot will be the screen content of this layout -->
            <slot name="page-content"></slot>
          </div>
          <!-- /.container-fluid -->

        </div>
        <!-- End of Main Content -->

        <!-- Footer -->
        <footer class="sticky-footer bg-white">
          <div class="container my-auto">
            <div class="copyright text-center my-auto">
              <span>{{$t("createdByFiqus")}} | COOBS 2020</span>
            </div>
          </div>
        </footer>
        <!-- End of Footer -->

      </div>
      <!-- End of Content Wrapper -->

    </div>
    <!-- End of Page Wrapper -->

    <!-- Scroll to Top Button-->
    <a class="scroll-to-top rounded" href="#page-top">
      <i class="fas fa-angle-up"></i>
    </a>

  </div>
</template>
<script>
import swal from "sweetalert";
import locales from "../locales/langs";

export default {
  computed: {
    userFullName() {
      return this.$store.getters.userFullName;
    },
    currentLanguage: {
      get() {
        const lang = this.$store.state.lang || this.$i18n.locale();
        this.$i18n.set(lang);
        return lang;
      },
      set(lang) {
        this.$store.commit("setLang", lang);
        this.$i18n.set(lang);
      }
    }
  },
  data() {
    return {
      toggled: true,
      locales
    };
  },
  methods: {
    logout() {
      swal({
        title: this.$t("readyToLeave"),
        text: this.$t("selectLogoutToEnd"),
        icon: "warning",
        buttons: {
          cancel: true,
          confirm: this.$t("logout")
        },
        dangerMode: true,
      })
        .then((willLogout) => {
          if (willLogout) {
            this.$store.dispatch("logout");
            swal(this.$t("sessionEnded"), {
              icon: "success",
              timer: 2000,
              buttons: false
            });
            this.$router.push({name: "login"});
          }
        });
    }
  }
};
</script>

