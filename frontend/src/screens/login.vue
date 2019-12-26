<template>
  <div class="row justify-content-center">
    <div class="col-xl-8 col-lg-10 col-md-7">
      <div class="card o-hidden border-0 shadow-lg my-5">
        <div class="card-body p-0">
          <div class="row">
            <div class="col-lg-2"></div>
            <div class="col-lg-8">
              <div class="p-5">
                <div class="text-center">
                  <h1 class="h4 text-gray-900 mb-4">Welcome Back!</h1>
                </div>
                <form v-on:submit.prevent="submit" class="user needs-validation" novalidate>
                  <input-form
                    name="email"
                    type="email"
                    v-model="user.email"
                    placeholder="Email..."
                    :error="$v.user.email.$error"
                    error-message="Ingrese un email válido">
                  </input-form>
                  <input-form
                    name="password"
                    type="password"
                    v-model="user.password"
                    placeholder="Password..."
                    :error="$v.user.password.$error"
                    error-message="Ingrese un password válido">
                  </input-form>
                  <button type="summary" class="btn btn-primary btn-user btn-block">Login</button>
                </form>
                <hr>
                <div class="text-center">
                  <a class="small" href="#">Forgot Password?</a>
                </div>
                <div class="text-center">
                  <a class="small" href="landing#signup">Create an Account!</a>
                </div>
              </div>
            </div>
            <div class="col-lg-2"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import InputForm from '../components/input-form.vue'
  import { required, email } from 'vuelidate/lib/validators';
  import {httpPost} from '../api-client';
  import swal from 'sweetalert';
  import {saveUser} from '../services/user-service';

  export default {
    components: {
      InputForm
    },
    data() {
      return {
        user: {
          email: "",
          password: ""
        }
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          const body = {...this.user};
          httpPost("/api-token-auth/", body)
            .then((res) => {
              const {token, user} = res.data;
              saveUser({...user, token});
              this.$router.push({name: "dashboard"});
            })
            .catch((err) => {
              swal("Login has failed", {
                icon: "error"
              });
            })
        }
      }
    },
    validations: {
      user: {
        email: {
          required,
          email
        },
        password: {
          required
        }
      }
    }
  }
</script>

