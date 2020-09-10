<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6">
      <div class="form-row">
        <label>{{$t('name')}}</label>
      </div>
      <input-form
        name="name"
        type="text"
        :value="$t(principle.nameKey, principle.name)"
        :disabled="true">
      </input-form>

      <div class="form-row">
        <label>{{$t('descriptionICA')}}</label>
        <div class="col-9">
          <small class="form-text text-muted font-italic ml-3">{{$t('descriptionICAHelp')}}</small>
        </div>
        <div name="description" v-html="principle.description">
      </div>
      </div><br/>
      <div class="form-row">
        <label class="mr-3">{{$t('custom_description')}}</label>
        <div class="col-9">
          <small class="form-text text-muted font-italic ml-3">{{$t('descriptionPrincipleHelp')}}</small>
        </div>
      </div>
      <textarea-form
        name="custom_description"
        type="text"
        v-model="principle.customDescription">
      </textarea-form>

      <div class="form-row">
        <div class="col-3 py-1">
          <bootstrap-toggle class="form-control"
            v-model="principle.visible"
            data-toggle="toggle"
            :options="{on: $t('visible'), off: $t('hide'), onstyle: 'success', offstyle: 'danger', size: 'normal'}"
            :disabled="false" />
        </div>          
        <div class="col-9">
          <small class="form-text text-muted font-italic ml-3">{{$t('principleVisibilityHelp')}}</small>
        </div>
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
};
</script>
