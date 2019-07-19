<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-4 offset-sm-4">
        <form v-on:submit.prevent="submit" class="needs-validation" novalidate>
          <input-form
            name="email"
            type="email"
            v-model="user.email"
            label="Email: "
            :error="$v.user.email.$error"
            error-message="Ingrese un email válido">
          </input-form>
          <input-form
            name="password"
            type="password"
            v-model="user.password"
            label="Password: "
            :error="$v.user.password.$error"
            error-message="Ingrese un password válido">
          </input-form>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
  import InputForm from '../components/input-form.vue'
  import { required, email } from 'vuelidate/lib/validators';

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
      submit(aa) {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          // TODO perform login action
          console.log(`Email: ${this.user.email}`);
          console.log(`Password: ${this.user.password}`);
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

