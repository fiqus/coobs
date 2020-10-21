<template>
  <div class="container">
    <div class="row justify-content-center p-sm-5">
      <div class="col-lg-8">
        <div class="text-left">
          <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
        </div>
      </div>

      <form v-on:submit.prevent="submit" class="col-lg-8 needs-validation" novalidate>
        <input-form
          :label="$t('name')"
          name="name"
          type="text"
          v-model="action.name"
          :error="$v.action.name.$error"
          :error-message="$t('required')">
        </input-form>

        <div class="form-group">
          <ckeditor
            :editor="editor"
            v-model="action.description"
            :config="editorConfig">
          </ckeditor>
        </div>

        <multi-select-form
          v-model="action.principles"
          :options="principles"
          :placeholder="$t('selectPrinciple')"
          :label="$t('principle')"
          :default-value="$t('selectPrinciple')"
          :error="$v.action.principles.$error"
          :error-message="$store.state.cooperative.sustainableDevelopmentGoalsActive ? $t('selectPrincipleOrODS'):$t('selectPrinciple')">
        </multi-select-form>

        <multi-select-form
          v-if="$store.state.cooperative.sustainableDevelopmentGoalsActive"
          v-model="action.sustainableDevelopmentGoals"
          :options="sustainableDevelopmentGoals"
          :placeholder="$t('selectSustainableDevelopmentGoals')"
          :label="$t('sustainableDevelopmentGoals')"
          :default-value="sustainableDevelopmentGoals"
          :error="$v.action.sustainableDevelopmentGoals.$error"
          :error-message="$t('selectPrincipleOrODS')">
        </multi-select-form>

        <div class="row">
          <div class="col-12 col-sm-6">
            <multi-select-form
              :label="$t('partners')"
              :placeholder="$t('selectPartners')"
              v-model="partnersInvolved"
              :options="partnersList"/>
          </div>
          <div class="col-12 col-sm-6">
            <datepicker-form
              :label="$t('startingDate')"
              name="date"
              format="dd/MM/yyyy"
              v-model="action.date"
              :error="$v.action.date.$error"
              :error-message="$t('required')"
              @input="onDateSelected">
            </datepicker-form>
          </div>
        </div>

        <div class="row">
          <div class="col-12 col-sm-6">
            <input-form
              :label="$t('investedHours')"
              name="hours"
              type="number"
              v-model="action.investedHours"
              :error="$v.action.investedHours.$error"
              :error-message="$t('positiveNumber')">
            </input-form>
          </div>
          <div class="col-12 col-sm-6">
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

        <div class="form-group row">
          <div class="col-12 col-sm-3 py-1">
            <bootstrap-toggle class="form-control"
              v-model="action.public"
              data-toggle="toggle"
              :options="{on: $t('public'), off: $t('private'), onstyle: 'success', offstyle: 'danger', size: 'normal'}"
              :disabled="false" />
          </div>
          <div class="col-12 col-sm-9 col-md-9">
            <small class="form-text text-muted font-italic">{{$t('actionVisibilityHelp')}}</small>
          </div>
        </div>

        <error-form :error="error" />

        <div class="d-flex flex-column flex-sm-row mb-3">
          <button type="button" class="btn btn-secondary mb-3 mb-sm-0" @click.stop="$router.go(-1)">
            <i class="fa fa-arrow-left"></i>
            {{$t("cancel")}}
          </button>
          <button type="submit" class="btn btn-success ml-0 ml-sm-3">
            <i class="fa fa-save"></i>
            {{$t("save")}}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
  @import './../../../node_modules/vue-multiselect/dist/vue-multiselect.min.css';
</style>

<script>
import InputForm from "../../components/input-form.vue";
import TextareaForm from "../../components/textarea-form.vue";
import BootstrapToggle from "vue-bootstrap-toggle";
import DatePickerForm from "../../components/datepicker-form.vue";
import MultiSelectForm from "../../components/multi-select-form.vue";
import swal from "sweetalert";
import {required, minLength, minValue, requiredIf} from "vuelidate/lib/validators";
import {httpPut, httpPost} from "../../api-client.js";
import {sanitizeMarkdown, capitalizeFirstChar} from "../../utils";
import * as api from "./../../services/api-service";
import ErrorForm from "../../components/error-form.vue";
import errorHandlerMixin from "./../../mixins/error-handler";
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import CKEditor from '@ckeditor/ckeditor5-vue';
import TurndownService from 'turndown';
const turndownService = new TurndownService()

function parserPartners(partners) {
  return partners.map(({id, firstName, lastName}) => {
    const name = `${capitalizeFirstChar(firstName)} ${capitalizeFirstChar(lastName)}`;
    return {id, name, firstName, lastName};
  });
}

export default {
  components: {
    "input-form": InputForm,
    "textarea-form": TextareaForm,
    "datepicker-form": DatePickerForm,
    "bootstrap-toggle": BootstrapToggle,
    "multi-select-form": MultiSelectForm,
    "error-form": ErrorForm,
    "ckeditor": CKEditor.component
  },
  mixins: [errorHandlerMixin],
  watch: {
    // we need to force the translations for principles because the select is not updated automatically
    locale(newLocale) {
      this.principles = this.principles.map((p) => {
        p.name = this.$t(p.nameKey, p.name);
        return p;
      });
      this.action.principles = this.action.principles.map((p) => {
        p.name = this.$t(p.nameKey, p.name);
        return p;
      });
      if (this.$store.state.cooperative.sustainableDevelopmentGoalsActive) {
        return api.getSustainableDevelopmentGoals()
          .then((sustainableDevelopmentGoals) => {
            this.sustainableDevelopmentGoals = sustainableDevelopmentGoals;
            this.action.sustainableDevelopmentGoals = this.action.sustainableDevelopmentGoals.map((actionGoal) => {
              const goal = sustainableDevelopmentGoals.find(({id}) => {
                return id === actionGoal.id;
              });
              return goal;
            });
          })
      }
    }
  },
  async created() {

    const [principles, partners, sustainableDevelopmentGoals] = await Promise.all([
      api.getPrinciples(),
      api.getPartners(),
      api.getSustainableDevelopmentGoals()
    ]);

    this.principles = principles.map((p) => {
      p.name = this.$t(p.nameKey, p.name);
      return p;
    });

    this.partners = partners.reduce(function(acc, partner){
      acc[partner.id] = `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`;
      return acc;
    }, {});
    
    this.partnersList = parserPartners(partners);
    if (this.$store.state.cooperative.sustainableDevelopmentGoalsActive) {
      this.sustainableDevelopmentGoals = sustainableDevelopmentGoals;
    }

    const actionId = this.$route.params.actionId;
    if (!this.isNew) {
      this.action = await api.getAction(actionId);
      this.action.principles = this.action.principles.map((p) => {
        p.name = this.$t(p.nameKey, p.name);
        return p;
      });
      this.partnersInvolved = parserPartners(this.action.partnersInvolved);
      this.action.description = sanitizeMarkdown(this.action.description);
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
        principles: [],
        sustainableDevelopmentGoals: [],
        public: true
      },
      principles: [],
      sustainableDevelopmentGoals: [],
      partnersInvolved: [],
      partnersList: [],
      isNew,
      title: isNew ? "createAction" : "editAction",
      editor: ClassicEditor,
      editorData: '<p>Content of the editor.</p>',
      editorConfig: {
          // The configuration of the editor.
          removePlugins: [ 'MediaEmbed', 'Image', 'ImageUpload']
      }      
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
        this.action.partnersInvolved = this.partnersInvolved;
        // @FIXME [DMC] I think it makes no sense to sanitize here, let the server do it and just sanitize with JS at display/parse time
        this.action.description = this.action.description ? turndownService.turndown(this.action.description) : "";
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
          })
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations: {
    action: {
      date: {required},
      name: {required},
      principles: {
        requiredIf: requiredIf((v) => {
          return !required(v.sustainableDevelopmentGoals);
        }),
        minLength: minLength(1)
      },
      sustainableDevelopmentGoals: {
        requiredIf: requiredIf((v) => {
          return !required(v.principles);
        }),
        minLength: minLength(1)
      },
      investedMoney: {minValue: minValue(0)},
      investedHours: {minValue: minValue(0)}
    }
  }
};
</script>
