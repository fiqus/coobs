<template>
  <div>
    <!-- Page Wrapper -->
    <div id="wrapper">

      <!-- Sidebar -->
      <ul class="navbar-nav bg-gradient-info sidebar sidebar-dark accordion" :class="{'toggled': toggled}" data-toggle="collapse" id="accordionSidebar">

        <!-- Sidebar - Brand -->
        <a class="sidebar-brand d-flex align-items-center justify-content-center" href="index.html">
          <div v-if="toggled" class="sidebar-brand-icon rotate-n-15">
            <img src="/images/bs.png" style="max-height: 45px;">
          </div>
          <div class="sidebar-brand-text mx-3">
            <img src="/images/bscoop.png" style="max-height: 45px;">
          </div>
        </a>

        <!-- Divider -->
        <hr class="sidebar-divider my-0">

        <!-- Nav Item - Dashboard -->
        <li class="nav-item active">
          <a class="nav-link" href="app">
            <i class="fas fa-fw fa-tachometer-alt"></i>
            <span>Dashboard</span></a>
        </li>

        <!-- Nav Item - Pages Collapse Menu -->
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'actions-list'}">
            <i class="fas fa-fw fa-clipboard-list"></i>
            <span>Actions</span>
          </router-link>
        </li>

        <!-- Nav Item - Utilities Collapse Menu -->
        <li class="nav-item">
          <router-link class="nav-link" :to="{name: 'principles-list'}">
            <i class="fas fa-fw fa-map-signs"></i>
            <span>Principles</span>
          </router-link>
        </li>

        <!-- Nav Item - Pages Collapse Menu -->
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'periods-list'}">
            <i class="fas fa-fw fa-calendar"></i>
            <span>Periods</span>
          </router-link>
        </li>
        
        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'balance'}">
            <i class="fas fa-fw fa-balance-scale"></i>
            <span>Balance</span>
          </router-link>
        </li>      

        <li class="nav-item">
          <router-link class="nav-link collapsed" :to="{name: 'cooperative'}">
            <i class="fas fa-fw fa-handshake"></i>
            <span>Your coop</span>
          </router-link>
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

            <!-- Sidebar Toggle (Topbar) -->
            <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
              <i class="fa fa-bars"></i>
            </button>

            <!-- Topbar Navbar -->
            <ul class="navbar-nav ml-auto">
    
              <div class="topbar-divider d-none d-sm-block"></div>

              <!-- Nav Item - User Information -->
              <li class="nav-item dropdown no-arrow">
                <a class="nav-link dropdown-toggle" href="#" id="userDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  <span class="mr-2 d-none d-lg-inline text-gray-600 small">Dear Cooperator</span>
                  <img class="img-profile rounded-circle" src="https://source.unsplash.com/QAB-WJcbgJk/60x60">
                </a>
                <!-- Dropdown - User Information -->
                <div class="dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="userDropdown">
                  <router-link class="dropdown-item" :to="{name: 'profile'}">
                    <i class="fas fa-user fa-sm fa-fw mr-2 text-gray-400"></i>
                    <span>Profile</span>
                  </router-link>
                  <div class="dropdown-divider"></div>
                  <a class="dropdown-item" href="#" @click="logout()">
                    <i class="fas fa-sign-out-alt fa-sm fa-fw mr-2 text-gray-400"></i>
                    Logout
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
              <span>Copyleft &copy; Social Balance Co-op 2019</span>
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
  import swal from 'sweetalert';

  export default {
    data() {
      return {
        toggled: true
      }
    },
    methods: {
      logout() {
        swal({
          title: "Ready to leave?",
          text: "Select 'Logout' if you're ready to end your current session.",
          icon: "warning",
          // buttons: true,
          buttons: {
            cancel: true,
            confirm: "Logout"
          },
          dangerMode: true,
        })
        .then((willLogout) => {
          if (willLogout) {
            localStorage.removeItem("user-token");
            swal("Session ended.", {
              icon: "success",
              timer: 2000,
              buttons: false
            });
            this.$router.push({name: "login"});
          }
        });
      }
    }
  }
</script>

