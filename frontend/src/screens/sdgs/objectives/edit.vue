<template>
  <div class="row justify-content-center">
    <div class="col-lg-7">
      <div class="text-left">
        <h1 class="h4 text-gray-900 mb-4">{{$t(title, title)}}</h1>
      </div>
    </div>
    <form v-on:submit.prevent="submit" class="col-lg-6 needs-validation" novalidate>
        <div class="form-row">
          <div class="col-12">
            <select-form
              v-model="sdgObjective.sustainableDevelopmentGoal"
              :options="sustainableDevelopmentGoals"
              :placeholder="$t('sustainableDevelopmentGoal')"
              :label="$t($t('sustainableDevelopmentGoal'))"
              :error="$v.sdgObjective.sustainableDevelopmentGoal.$error"
              :error-message="$t('required')">
            </select-form>
          </div>
        </div>
        <div class="form-row">
          <div class="col-6">
            <select-form
              v-model="sdgObjective.period"
              :options="periods"
              :placeholder="$t('period')"
              :label="$t($t('period'))"
              :error="$v.sdgObjective.period.$error"
              :error-message="$t('required')">
            </select-form>
          </div>
        </div>
        <div class="form-row">
          <div class="col-4">
            <input-form
              :label="$t('hoursToReach')"
              name="hours"
              type="number"
              v-model="sdgObjective.hoursToReach"
              :error="$v.sdgObjective.hoursToReach.$error"
              :error-message="$t('positiveNumber')">
            </input-form>
          </div>
          <div class="col-4">
            <input-form
              :label="$t('moneyToInvest')"
              name="money"
              type="number"
              v-model="sdgObjective.moneyToInvest"
              :error="$v.sdgObjective.moneyToInvest.$error"
              :error-message="$t('positiveNumber')">
            </input-form>
          </div>
          <div class="col-4">
            <input-form
              :label="$t('actionsToPerform')"
              name="actions"
              type="number"
              v-model="sdgObjective.actionsToPerform"
              :error="$v.sdgObjective.actionsToPerform.$error"
              :error-message="$t('positiveNumber')">
            </input-form>
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
import InputForm from "../../../components/input-form.vue";
import {required, minValue} from "vuelidate/lib/validators";
import {httpGet, httpPut, httpPost} from "../../../api-client.js";
import swal from "sweetalert";
import SelectForm from "../../../components/select-form.vue";
import ErrorForm from "../../../components/error-form.vue";
import errorHandlerMixin from "./../../../mixins/error-handler";
import * as api from "./../../../services/api-service";

export default {
  components: {
    "input-form": InputForm,
    "select-form": SelectForm,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
  async created() {
    const [periods, sustainableDevelopmentGoals] = await Promise.all([
      api.getPeriods(),
      api.getSustainableDevelopmentGoals()
    ]);
    this.periods = periods;
    this.sustainableDevelopmentGoals = sustainableDevelopmentGoals;

    if (this.$route.params.sdgObjectiveId && this.$route.params.sdgObjectiveId !== "0") {
      httpGet(`/sdg-objectives/${this.$route.params.sdgObjectiveId}`)
        .then((response) => {
          this.sdgObjective = response.data;
        });
    }
    return httpGet("/sdg-objectives/")
      .then((response) => {
        this.sdgObjectives = response.data;
      });
  },
  data() {
    const isNew = this.$route.params.sdgObjectiveId == "0";
    return {
      sdgObjective: {
        sdgName: "",
        period: "",
        cooperative: "",
        hoursToReach: 0,
        moneyToInvest: 0,
        actionsToPerform: 0
      },
      periods: [],
      sdgObjectives: [],
      isNew,
      title: isNew ? "createSDGObjective" : "editSDGObjective"
    };
  },
  methods: {
    submit() {
      this.$v.$touch();
      if (!this.$v.$invalid) {
        const sdgObjId = this.$route.params.sdgObjectiveId;
        let promise = null;
        if (this.isNew) {
          promise = httpPost("sdg-objectives/", this.sdgObjective);
        } else {
          promise = httpPut(`/sdg-objectives/${sdgObjId}/`, this.sdgObjective);
        }
        return promise
          .then(() => {
            const sdgObjectivePerformed = this.isNew ? "created" : "edited";
            swal(`The objective has been ${sdgObjectivePerformed}!`, {
              icon: "success",
              buttons: false,
              timer: 2000
            });
            this.$router.push({name: "sdg-objectives-list"});
          })
          .catch((err) => {
            this.handleError(err);
          });
      }
    }
  },
  validations: {
    sdgObjective: {
      period: {required},
      sustainableDevelopmentGoal: {required},
      hoursToReach: {minValue: minValue(0)},
      moneyToInvest: {minValue: minValue(0)},
      actionsToPerform: {minValue: minValue(0)}
    }
  }
};
</script>
