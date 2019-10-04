<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{title}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        label="Name"
        name="name"
        type="text"
        v-model="principle.name"
        :disabled="true"
        :error="$v.principle.name.$error"
        error-message="Required">
      </input-form>

      <textarea-form
        label="Description"
        name="description"
        type="text"
        v-model="principle.description"
        :error="$v.principle.description.$error"
        error-message="Required">
      </textarea-form>

      <div class="form-group">
        <bootstrap-toggle class="form-control"
          v-model="principle.visible"
          data-toggle="toggle"
          :options="{on: 'Visible', off: 'Hide', onstyle: 'success', offstyle: 'danger', size: 'normal'}"
          :disabled="false" />
      </div>

      <div class="action-bar-buttons">
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> Cancel</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> Save</button>
			</div>
    </form>
  </div>
</template>

<script>
  import InputForm from "../../components/input-form.vue";
  import TextareaForm from "../../components/textarea-form.vue";
  import BootstrapToggle from 'vue-bootstrap-toggle'
  import {required} from "vuelidate/lib/validators";
  import {httpGet, httpPut} from "../../api-client.js";
  import swal from 'sweetalert';

  export default {
    components: {
      "input-form": InputForm,
      "textarea-form": TextareaForm,
      "bootstrap-toggle": BootstrapToggle
    },
    created() {
      if (this.$route.params.principleId) {
        httpGet(`/principles/${this.$route.params.principleId}`)
          .then((response) => {
            this.principle = response.data;
          });
      }
    },
    data() {
      return {
        principle: {},
        isNew: !Boolean(this.$route.params.principleId),
        title: this.isNew ? "Create a principle" : "Edit principle"
      }
    },
    methods: {
      submit() {
        this.$v.$touch();
        if (!this.$v.$invalid) {
          httpPut(`/principles/${this.$route.params.principleId}/`, this.principle)
            .then(() => {
              swal("The principle has been edited!", {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              this.$router.push({name: "principles-list"});
            })
        }
      }
    },
    validations: {
      principle: {
        name: {required},
        description: {required}
      }
    }
  }
</script>
