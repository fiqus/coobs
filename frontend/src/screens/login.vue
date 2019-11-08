<template>
  <div class="row justify-content-center">
    <div class="col-lg-10">
      <div class="text-center">
        <h1 class="h4 text-gray-900 mb-4">Bienvenido!</h1>
      </div>
      <form v-on:submit.prevent="submit" class="needs-validation" novalidate>
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
        <div class="form-group">
          <div class="custom-control custom-checkbox small">
            <input type="checkbox" class="custom-control-input" id="customCheck">
            <label class="custom-control-label text-gray-900" for="customCheck">Remember Me</label>
          </div>
        </div>
        <button type="submit" class="btn btn-primary btn-user btn-block">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
  import InputForm from '../components/input-form.vue'
  import { required, email } from 'vuelidate/lib/validators';
  import {httpPost} from '../api-client';
  import swal from 'sweetalert';

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
          const body = {
            username: this.user.email,
            password: this.user.password
          }
          httpPost("/token/", body)
            .then((res) => {
              const token = res.data.access;
              const refresh = res.data.refresh;
              localStorage.setItem("user-token", token);
              localStorage.setItem("user-token-refresh", refresh);
              this.$router.push({name: "dashboard"});
            })
            .catch((err) => {
              swal("login breaks", {
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

