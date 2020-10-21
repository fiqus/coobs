<template>
  <div class="custom-container">
    <div class="row px-3 mb-3">
      <h3 class="col-md-10 col-sm-9 px-0">{{$t('actions')}}</h3>
      <router-link class="col-md-2 col-sm-3 btn btn-primary" :to="{name: 'action-edit', params: {actionId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>

    <loader :loading='isLoading'/>
    
    <detail-modal 
      :title="$t('actionDetail')">
      <template v-slot:modal-body>
        <label class="bold">{{$t('name')}}:</label>
        <span name="name"
          type="text">{{modalAction.actionData.name}}
        </span><br/>
        <label class="bold">{{$t('description')}}:</label>
        <div name="description" v-html="modalAction.actionData.description">
        </div><br/>        
        <!-- <span name="description"
          type="text">
          {{modalAction.actionData.description}}
        </span><br/> -->
        <label class="bold">{{$t('principles')}}:</label><br/>
        <span class="multiselect__tag" v-for="principle in modalAction.actionData.principles" v-bind:key="principle" 
          name="principles" type="text">
          {{$t(principle.nameKey)}}
        </span><br/>
        <div v-if="$store.state.cooperative.sustainableDevelopmentGoalsActive">
          <label class="bold">{{$t('sustainableDevelopmentGoals')}}:</label><br/>
          <span class="multiselect__tag" v-for="goal in modalAction.actionData.sustainableDevelopmentGoals" v-bind:key="goal" 
            name="sustainableDevelopmentGoals" type="text">
            {{$t(goal.name)}}
          </span><br/>
        </div>
        <label class="bold">{{$t('partners')}}:</label><br/>
        <span class="multiselect__tag" v-for="partner in modalAction.actionData.partnersSelected" v-bind:key="partner" 
          name="partners" type="text">
          {{partner}}
        </span><br/>
        <label class="bold">{{$t('startingDate')}}:</label>
        <span name="startingDate"
          type="text">{{modalAction.actionData.date | formatToUIDate}}
        </span><br/>
        <label class="bold">{{$t('investedHours')}}:</label>
        <span name="investedHours"
          type="text">{{formatNumber(modalAction.actionData.investedHours)}}
        </span><br/>
        <label class="bold">{{$t('investedMoney')}}:</label>
        <span name="investedMoney"
          type="text">$ {{formatNumber(modalAction.actionData.investedMoney)}}
        </span><br/>
      </template>
    </detail-modal>

    <filters-table-component
      :filters="filters"
      @applyFilters="applyFilters">
    </filters-table-component>

    <error-form :error="error"></error-form>

    <simple-table
        :headers="headers"
        :data="actions"
        :actions="{edit: true, delete: true, showViewButton: true}"
        :empty-state-msg="emptyMsg"
        :pagination="pagination"
        :ordering="ordering"
        @onEdit="onEdit"
        @onDelete="onDelete"
        @onQuickView="onQuickView"
        @onSort=onSort>
      </simple-table>
      <pagination-table-component
        :dataLength="actions.length"
        :pagination="pagination"
        @goNext="goNext"
        @goPrevious="goPrevious"
        @goToPage="goToPage">
      </pagination-table-component>
  </div>
</template>

<script>
import {httpGet, httpDelete} from "../../api-client.js";
import SimpleTable from "../../components/simple-table.vue";
import DetailModal from "../../components/detail-modal.vue";
import FiltersTable from "../../components/filters-table-component.vue";
import PaginationTable from "../../components/pagination-table-component.vue";
import Loader from "../../components/loader-overlay.vue";
import {sanitizeMarkdown, formatText, capitalizeFirstChar, formatToUIDate, parseNumber} from "../../utils";
import swal from "sweetalert";
import * as api from "./../../services/api-service";
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

const parsePrinciples = (translator, principles) => {
  let result = "";
  principles.forEach((principle) => {
    const princripleName = translator(principle.nameKey);
    result = result.concat(`<span class="multiselect__tag" style="padding: 4px 6px 4px 6px !important;">${princripleName}</span>`)
  });
  return result;
}

export default {
  components: {
    "simple-table": SimpleTable,
    "loader": Loader,
    "error-form": ErrorForm,
    "filters-table-component": FiltersTable,
    "pagination-table-component": PaginationTable,
    "detail-modal": DetailModal
  },
  mixins: [errorHandlerMixin],
  created() {
    return Promise.all([
        httpGet("/actions"),
        httpGet("/principles"),
        httpGet("/periods"),
        httpGet("/partners"),
        httpGet("/sustainable-development-goals"),
      ])
      .then(([actions, principles, periods, partners, sustainableDevelopmentGoals]) => {
        this.actions = actions.data.results;
        const {next, previous, count, page, numPages, pageSize} = actions.data;
        this.pagination = {next, previous, count, page, numPages, pageSize};
        this.periods = periods.data;
        this.filters.forEach((filter) => {
          if (filter.key === "principle") {
            filter.options = this.principlesFilter(principles.data);
          }
          if (filter.key === "sustainable_development_goal") {
            filter.options = this.sustainableDevelopmentGoalsFilter(sustainableDevelopmentGoals.data);
          }
          if (filter.key === "partner") {
            filter.options = this.partnersFilter(partners.data);
          }
          if (filter.key === "period") {
            filter.options = this.periodsFilter(periods.data);
          }
        });
        this.isLoading = false;
      })
  },
  data() {
    return {
      headers: [
        {key: "date", value: "date", parser: (p) => formatToUIDate(p.date), sortEnabled: true},
        {key: "name", value: "name", parser: (p) => formatText(p.name, 50), sortEnabled: true},
        // {key: "description", value: "description", parser: (p) => formatText(p.description, 50)},
        {key: "public", value: "public", parser: (p) => parseBoolean(p.public)},
        {key: "principles", value: "principles", parser: (p) => parsePrinciples(this.$t, p.principles)},
        // {key: "partnersInvolved", value: "partners", parser: (p) => parsePartners(p.partnersInvolved)},
      ],
      actions: [],
      pagination: {},
      periods: [],
      filters: this.loadFilters(),
      ordering: {
        enabled: true,
        by: "date",
        dir: "-"
      },
      filterParams: {},
      orderingParams: {},
      isLoading: true,
      emptyMsg: this.$t('emptyActionMsg'),
      modalAction: {actionData:{}, principles: {}, sustainableDevelopmentGoals:{}}
    };
  },
  methods: {
    loadFilters() {
      const filters = [
        {
          key: "principle",
          value: null,
          options: []
        },
        {
          key: "period",
          value: null,
          options: []
        },
        {
          key: "partner",
          value: null,
          options: []
        },
        
      ];
      if (this.$store.state.cooperative.sustainableDevelopmentGoalsActive) {
        filters.push({
          key: "sustainable_development_goal", // query params are not supported by DRF camel case lib
          value: null,
          options: []
        });
      }
      return filters;
    },
    formatNumber(number){
      return parseNumber(number, this.$i18n.locale());
    },
    principlesFilter(principles) {
      return principles.map(({id, name, nameKey}) => {
        return {
          id,
          name: this.$t(nameKey, name)
        };
      });
    },
    periodsFilter(periods) {
      return periods.map(({id, name, dateFrom, dateTo}) => {
        const label = `${name} | ${formatToUIDate(dateFrom)} - ${formatToUIDate(dateTo)}`
        return {
          id,
          name: label
        }
      });
    },
    partnersFilter(partners) {
      return partners.map(({id, firstName, lastName}) => {
        const name = `${capitalizeFirstChar(firstName)} ${capitalizeFirstChar(lastName)}`;
        return {id, name};
      });
    },
    sustainableDevelopmentGoalsFilter(sustainableDevelopmentGoals){
      return sustainableDevelopmentGoals.map(({id, name, nameKey}) => {
        return {
          id,
          name: this.$t(nameKey, name)
        };
      });
    },
    goToPage(page) {
      const params = this.filters.reduce((acc, filter) => {
        if (filter.value) {
          acc[filter.key] = filter.value;
        }
        return acc;
      }, {});
      const fetchParams = Object.assign({}, params, this.orderingParams);
      return this.getActions(`/actions/?page=${page}`, fetchParams);
    },
    goNext() {
      const urlParts = this.pagination.next.split("/api");
      const relativeUrl = urlParts[1];
      return this.getActions(relativeUrl)
    },
    goPrevious() {
      const urlParts = this.pagination.previous.split("/api");
      const relativeUrl = urlParts[1];
      return this.getActions(relativeUrl);
    },
    applyFilters(params) {
      if (params && params.period) {
        const period = this.periods.find((period) => {
          return period.id === params.period;
        });
        if (period) {
          params.date_from = period.dateFrom;
          params.date_to = period.dateTo;
        }
      }
      this.filterParams = params;
      const fetchParams = Object.assign({}, params, this.orderingParams);
      return this.getActions(`/actions`, fetchParams);
    },
    getActions(url, params=null) {
      this.isLoading = true;
      return httpGet(url, params)
          .then((res) => {
            this.actions = res.data.results;
            const {next, previous, count, page, numPages, pageSize} = res.data;
            this.pagination = {next, previous, count, page, numPages, pageSize};
            if (!this.actions.length) {
              this.emptyMsg = this.$t('noActionsResults');
            }
            this.isLoading = false;
          })
          .catch((err) => {
            this.isLoading = false;
            this.handleError(err);
          })
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
              return this.getActions("/actions");
            });
        }
      });
    },
    onSort(sort) {
      if (this.ordering.by === sort) {
        this.ordering.dir = !this.ordering.dir ? "-" : "";
      }
      this.ordering.by = sort;
      const params = {
        ordering: `${this.ordering.dir}${this.ordering.by}`
      };
      this.orderingParams = params;
      const fetchParams = Object.assign({}, params, this.filterParams);
      return this.getActions("/actions", fetchParams);
    },
    onQuickView(action) {
      Promise.all([
        api.getPrinciples(),
        api.getAction(action.id),
        api.getSustainableDevelopmentGoals()
      ]).then(([principles, actionData, sustainableDevelopmentGoals]) => {
        actionData.partnersSelected = actionData.partnersInvolved.map((partner) => {
          return `${capitalizeFirstChar(partner.firstName)} ${capitalizeFirstChar(partner.lastName)}`
        });
        actionData.description = sanitizeMarkdown(actionData.description);
        this.modalAction = {actionData};
        $('#detailModal').modal()
      });
    }
  }
};
</script>