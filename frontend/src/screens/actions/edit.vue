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
        v-model="action.name"
        :error="$v.action.name.$error"
        :error-message="$t('required')">
      </input-form>

      <textarea-form
        :label="$t('description')"
        name="description"
        type="text"
        v-model="action.description"
        :error="$v.action.description.$error"
        :error-message="$t('required')">
      </textarea-form>

      <div class="form-row">
        <div class="col-6">
          <select-form
            v-model="action.principle"
            :options="principles"
            :label="$t('principle')"
            :default-value="$t('selectPrinciple')"
            :error="$v.action.principle.$error"
            :error-message="$t('required')">
          </select-form>
        </div>
        <div class="col-6">
          <multi-select-form
            :label="$t('partners')"
            :placeholder="$t('selectPartners')"
            v-model="partnersInvolved"
            :options="partnersList"
            :error="$v.partnersInvolved.$error"
            :error-message="$t('required')"
          />
        </div>
      </div>

      <div class="form-row">
        <div class="col-6">
          <datepicker-form
            :label="$t('date')"
            name="date"
            format="dd/MM/yyyy"
            v-model="action.date"
            :error="$v.action.date.$error"
            :error-message="$t('required')"
            @input="onDateSelected">
          </datepicker-form>
        </div>
        <div class="col-6">
          <input-form
            :label="$t('investedMoney')"
            name="money"
            type="number"
            v-model="action.investedMoney"
            :error="$v.action.investedMoney.$error"
            :error-message="$t('positiveNumber')">
          </input-form>
        </div>
      </div>
      <div class="form-group">
        <bootstrap-toggle class="form-control"
          v-model="action.public"
          data-toggle="toggle"
          :options="{on: $t('public'), off: $t('private'), onstyle: 'success', offstyle: 'danger', size: 'normal'}"
          :disabled="false" />
      </div>
      <div>
				<button type="button" class="btn btn-secondary" @click.stop="$router.go(-1)">
          <i class="fa fa-arrow-left"></i> 
          {{$t("cancel")}}
        </button>
				<button type="submit" class="btn btn-success">
          <i class="fa fa-save"></i>
          {{$t("save")}}
        </button>
			</div>
    </form>
  </div>
</template>

<style>
  @import './../../../node_modules/vue-multiselect/dist/vue-multiselect.min.css';
</style>

<script>
import InputForm from "../../components/input-form.vue";
import TextareaForm from "../../components/textarea-form.vue";
import BootstrapToggle from 'vue-bootstrap-toggle';
import SelectForm from "../../components/select-form.vue";
import DatePickerForm from "../../components/datepicker-form.vue";
import MultiSelectForm from "../../components/multi-select-form.vue";
import swal from "sweetalert";
import {required, minLength, minValue} from "vuelidate/lib/validators";
import {httpPut, httpPost} from "../../api-client.js";
import {partnersParser, capitalizeFirstChar} from "../../utils";
import * as api from "./../../services/api-service";

export default {
  components: {
    "input-form": InputForm,
    "textarea-form": TextareaForm,
    "select-form": SelectForm,
    "datepicker-form": DatePickerForm,
    "bootstrap-toggle": BootstrapToggle,
    "multi-select-form": MultiSelectForm
  },
  watch: {
    // we need to force the translations for principles because the select is not updated automatically
    locale(newLocale) {
      this.principles = this.principles.map((p) => {
        p.name = this.$t(p.nameKey, p.name);
        return p;
      });
    }
  },
  async created() {

    const [principles, partners] = await Promise.all([
      api.getPrinciples(),
      api.getPartners()
    ]);

    this.principles = principles.map((p) => {
      p.name = this.$t(p.nameKey, p.name);
      return p;
    });

    this.partners = partners.reduce(function(acc, partner){
      acc[partner.id] = `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`;
      return acc;
    }, {});
    
    this.partnersList = partnersParser(Object.keys(this.partners), this.partners);
    
    const actionId = this.$route.params.actionId;
    if (!this.isNew) {
      this.action = await api.getAction(actionId);
      this.partnersInvolved = partnersParser(this.action.partnersInvolved, this.partners);
    }
  },
  computed: {
    locale() {
      return this.$i18n.locale();
    }
  },
  data() {
    const isNew = this.$route.params.actionId == "0";
    return {
      action: {
        principle: ""
      },
      principles: [],
      partnersInvolved: [],
      partnersList: [],
      isNew,
      title: isNew ? "createAction" : "editAction"
    };
  },
  methods: {
    onDateSelected(newDate) {
      this.action.date = new Date(newDate).toISOString().slice(0, 10);
    },
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const actionId = this.$route.params.actionId;
        this.action.partnersInvolved = this.partnersInvolved.map((partner) => {
          return partner.id;
        });
        let promise = null;
        if (this.isNew) {
          promise = httpPost("actions/", this.action);
        } else {
          promise = httpPut(`/actions/${actionId}/`, this.action);
        }
        return promise
          .then(() => {
            const actionPerformedMessage = this.isNew ? this.$t("actionCreatedMsg") : this.$t("actionEditedMsg");
            swal(actionPerformedMessage, {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "actions-list"});
          });
      }
    }
  },
  validations: {
    action: {
      date: {required},
      name: {required},
      description: {required},
      principle: {required},
      investedMoney: {minValue: minValue(0)}
    },
    partnersInvolved: {
      required,
      minLength: minLength(1)
    }
  }
};
</script>
