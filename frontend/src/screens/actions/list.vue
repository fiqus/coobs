<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t('actions')}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'action-edit', params: {actionId: 0}}">
        {{$t("addNew")}}   
        <i class="fa fa-plus"></i>
      </router-link>
    </div>

    <spinner :loading='isLoading'/>
    <loader :loading='isLoading'/>

    <form v-on:submit.prevent="submitFilters">
      <div class="row">
        <div class="col-4">
          <select-form
            v-model="filters.principle"
            :options="principlesFilter"
            :label="$t('principle')">
          </select-form>
        </div>
        <div class="col-4">
          <select-form
            v-model="filters.period"
            :options="periodsFilter"
            :label="$t('period')">
          </select-form>
        </div>
        <div class="col-4">
          <select-form
            v-model="filters.partner"
            :options="partnersFilter"
            :label="$t('partner')">
          </select-form>
        </div>
      </div>

      <error-form :error="errorFilter" @clean="cleanError()"/>

      <div class="mb-3">
        <button type="submit" class="btn btn-warning">
          <i class="fa fa-filter"></i>
          {{$t("apply")}}
        </button>
        <button type="button" class="btn btn-secondary" @click.stop="cleanFilters()">
          <i class="fa fa-eraser"></i> 
          {{$t("clean")}}
        </button>
      </div>
    </form>

    <custom-table
        :headers="headers"
        :data="actions"
        :actions="{edit: true, delete: true, showViewButton: true}"
        :empty-state-msg="emptyMsg"
        @onEdit="onEdit"
        @onDelete="onDelete"
        @onQuickView="onQuickView">
      </custom-table>
  </div>
</template>

<script>
import {httpGet, httpDelete} from "../../api-client.js";
import CustomTable from "../../components/custom-table.vue";
import Loader from "../../components/loader-overlay.vue";
import Spinner from "../../components/spinner.vue";
import ActionQuickView from "../../components/action-quick-view.vue";
import {formatText, capitalizeFirstChar} from "../../utils";
import swal from "sweetalert";
import * as api from "./../../services/api-service";
import SelectForm from "../../components/select-form.vue";
import {required} from "vuelidate/lib/validators";
import ErrorForm from "../../components/error-form.vue";
import errorHandlerMixin from "./../../mixins/error-handler";

function parseBoolean(value) {
  const icon = value ? "check" : "times";
  return `<i class="fas fa-${icon}-circle fa-2x"></i>`;
}

function parsePartners(partners) {
  let result = "";
  partners.forEach((partner) => {
    const partnerFullName = `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`;
    result = result.concat(`<span class="multiselect__tag" style="padding: 4px 6px 4px 6px !important;">${partnerFullName}</span>`)
  });
  return result;
}

export default {
  components: {
    "custom-table": CustomTable,
    "loader": Loader,
    "spinner": Spinner,
    "select-form": SelectForm,
    "error-form": ErrorForm
  },
  mixins: [errorHandlerMixin],
  created() {
    return Promise.all([
        httpGet("/actions"),
        httpGet("/principles"),
        httpGet("/periods"),
        httpGet("/partners"),
      ])
      .then(([actions, principles, periods, partners]) => {
        this.actions = actions.data;
        this.principles = principles.data;
        this.periods = periods.data;
        this.partners = partners.data;
        this.isLoading = false;
      })
  },
  watch: {
    'filtersAreInvalid': function _watch$vfilters$error (isInvalid) {
        this.errorFilter.message = "selectAtLeastOneFilter";
        this.errorFilter.exists = isInvalid;
      }
  },
  computed: {
    principlesFilter() {
      return this.principles.map(({id, name, nameKey}) => {
        return {
          id,
          name: this.$t(nameKey, name)
        };
      });
    },
    periodsFilter() {
      return this.periods.map(({id, name, dateFrom, dateTo}) => {
        const label = `${name} | ${dateFrom} - ${dateTo}`
        return {
          id,
          name: label
        }
      });
    },
    partnersFilter() {
      return this.partners.map(({id, firstName, lastName}) => {
        const name = `${capitalizeFirstChar(firstName)} ${capitalizeFirstChar(lastName)}`;
        return {id, name};
      });
    },
    filtersAreInvalid() {
      return this.$v.filters.principle.$error &&
        this.$v.filters.period.$error &&
        this.$v.filters.partner.$error;
    }
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date"},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50)},
        {key: "description", value: "description", parser: (p) => formatText(p.description, 50)},
        //{key: "principle", value: "principle", parser: (p) => formatText(this.$t(p.principleNameKey), 50)},
        {key: "public", value: "public", parser: (p) => parseBoolean(p.public)},
        {key: "partnersInvolved", value: "partners", parser: (p) => parsePartners(p.partnersInvolved)},
      ],
      actions: [],
      principles: [],
      periods: [],
      partners: [],
      filters: {
        principle: null,
        period: null,
        partner: null
      },
      errorFilter: {
        exists: false,
        message: "",
        backgroundClass: "bg-danger"
      },
      isLoading: true,
      emptyMsg: this.$t('emptyActionMsg')
    };
  },
  methods: {
    cleanError() {
      this.$v.filters.$reset();
    },
    cleanFilters() {
      this.filters.principle = null;
      this.filters.period = null;
      this.filters.partner = null;
      this.$v.filters.$reset();
    },
    submitFilters() {
      this.$v.filters.$touch();
      if (!this.filtersAreInvalid) {
        const params = {}
        if (this.filters.principle) {
          params.principle = this.filters.principle;
        }
        if (this.filters.partner) {
          params.partner = this.filters.partner;
        }
        if (this.filters.period) {
          const period = this.periods.find((period) => {
            return period.id === this.filters.period;
          });
          if (period) {
            params.date_from = period.dateFrom;
            params.date_to = period.dateTo;
          }
        }
        return httpGet(`/actions`, params)
          .then((res) => {
            this.actions = res.data;
            if (!this.actions.length) {
              this.emptyMsg = this.$t('noActionsResults');
            }
          })
          .catch((err) => {
            this.handleError(err);
          })
      }
    },
    onEdit(action) {
      this.$router.push({name: "action-edit", params: {actionId: action.id}});
    },
    onDelete(action) {
      swal({
        title: this.$t("areYouSure"),
        text: this.$t("onceActionDeleted"),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      }).then((willDelete) => {
        if (willDelete) {
          httpDelete(`/actions/${action.id}`)
            .then(() => {
              swal( this.$t("deletedActionMsg"), {
                icon: "success",
                buttons: false,
                timer: 2000
              });
              return httpGet("/actions")
                .then((response) => {
                  this.actions = response.data;
                });
            });
        }
      });
    },
    onQuickView(action) {
      Promise.all([
        api.getPrinciples(),
        api.getAction(action.id)
      ]).then(([principles, actionData]) => {
        console.log(principles, actionData);
      });


    }
  },
  validations: {
    filters: {
      principle: {required},
      period: {required},
      partner: {required}
    }
  }
};
</script>