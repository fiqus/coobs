<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
      <input-form
        :label="$t('name')"
        name="name"
        type="text"
        :value="$t(principle.nameKey, principle.name)"
        :disabled="true"
        :error="$v.principle.name.$error"
        error-message="Required">
      </input-form>

      <textarea-form
        :label="$t('description')"
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

      <error-form :error="error" />

      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)"><i class="fa fa-arrow-left"></i> {{$t("cancel")}}</button>
				<button type="submit" class="btn btn-success"><i class="fa fa-save"></i> {{$t("save")}}</button>
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
import ErrorForm from "../../components/error-form.vue";
import errorHandlerMixin from "./../../mixins/error-handler";

export default {
  components: {
    "input-form": InputForm,
    "textarea-form": TextareaForm,
    "bootstrap-toggle": BootstrapToggle,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
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
      title: this.isNew ? "createPrinciple" : "editPrinciple"
    };
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
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations: {
    principle: {
      name: {required},
      description: {required}
    }
  }
};
</script>
