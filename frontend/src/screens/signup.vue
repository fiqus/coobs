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
                  <h1 class="h4 text-gray-900 mb-2">Create user for</h1>
                  <h1 class="h3 text-gray-900 mb-4">{{coopName}}</h1>
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
                  <input-form
                    name="password"
                    type="password"
                    v-model="user.repeatPassword"
                    placeholder="Repeat..."
                    :error="$v.user.repeatPassword.$error"
                    error-message="Las passwords no coinciden">
                  </input-form>
                  <button type="summary" class="btn btn-primary btn-user btn-block">Create</button>
                </form>
                <hr>
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
  import { required, email, sameAs } from 'vuelidate/lib/validators';
  import {httpPost} from '../api-client';
  import swal from 'sweetalert';

  export default {
    components: {
      InputForm
    },
    props: {
      coopEmail: {
        type: String,
        required: true
      },
      coopName: {
        type: String,
        required: true
      }
    },
    data() {
      return {
        user: {
          email: "",
          password: "",
          repeatPassword: ""
        }
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          const {email, password} = this.user;
          // TODO post to create user/account endpoint
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
        },
        repeatPassword: {
          sameAsPassword: sameAs('password')
        }
      }
    }
  }
</script>

