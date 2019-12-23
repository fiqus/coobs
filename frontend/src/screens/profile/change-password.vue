<template>
<div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">Change your password</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <div class="form-row">
        <div class="col-12">
          <input-form
            label="Current password"
            name="current password"
            type="text"
            v-model="partner.password"
            :error="$v.partner.password.$error"
            error-message="Required">
          </input-form>
        </div>
      </div>
      <div class="form-row">
        <div class="col-12">
          <input-form
            label="New password"
            name="new password"
            type="text"
            v-model="partner.new_password"
            :error="$v.partner.new_password.$error"
            error-message="Required">
          </input-form>
        </div>
      </div>
      <div class="form-row">
        <div class="col-12">
          <input-form
            label="Confirm password"
            name="confirm password"
            type="text"
            v-model="partner.confirm_password"
            :error="$v.partner.confirm_password.$error"
            error-message="Required">
          </input-form>
        </div>
      </div>
      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> Cancel</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> Save</button>
			</div>
    </form>
  </div>
</template>

<script>
  import InputForm from "../../components/input-form.vue";
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut} from "../../api-client.js";
  import swal from 'sweetalert';

  export default {
    components: {
      "input-form": InputForm
    },
    created() {
      // TODO deberíamos usar el partner id del usuario logueado
      httpGet(`/partners/1`)
        .then((response) => {
          this.partner = response.data;
        });
    },
    data() {
      return {
        partner: {},
        title: "Edit Password"
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          // TODO deberíamos usar el partner id del usuario logueado
          httpPut(`/partners/1/`, this.partner)
            .then(() => {
              swal("The partner password has been edited!", {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              this.$router.push({name: "partner"});
            })
        }
      }
    },
    validations: {
      partner: {
        password: {required},
        new_password: {required},
        confirm_password: {required},
      }
    }
  }
</script>
