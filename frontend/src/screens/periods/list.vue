<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("periods")}}</h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'period-edit', params: {periodId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <custom-table
      :headers="headers"
      :data="periods"
      :actions="{edit: true, delete: true}"
      :empty-state-msg="$t('noPeriodsMessage')" 
      @onEdit="onEdit"
      @onDelete="onDelete">
    </custom-table>
  </div>
</template>

<script>
import CustomTable from "../../components/custom-table.vue";
import {formatText} from "../../utils";
import {httpGet, httpDelete} from "../../api-client.js";
import swal from "sweetalert";

function parseBoolean(value) {
  return `<i class="fas fa-dollar-sign fa-1x"></i> ${value}`;
}

export default {
  components: {
    "custom-table": CustomTable
  },
  created() {
    httpGet("/periods")
      .then((response) => {
        this.periods = response.data;
      });
  },
  data() {
    return {
      headers: [
        {key: "name", value: this.$t("name"), parser: (p) => formatText(p.name)},
        {key: "dateFrom", value: this.$t("from"), parser: (p) => formatText(p.date_from, 50)},
        {key: "dateTo", value: this.$t("to"), parser: (p) => formatText(p.date_to, 50)},
        {key: "actionsBudget", value: this.$t("budget"), parser: (p) => parseBoolean(p.actions_budget)},
      ],
      periods: []
    };
  },
  methods: {
    onEdit(period) {
      this.$router.push({name: "period-edit", params: {periodId: period.id}});
    },
    onDelete(period) {
      httpDelete(`/periods/${period.id}`)
        .then(() => {
          swal(this.$t("deletedPeriodMsg"), {
            icon: "success",
            buttons: false,
            timer: 2000
          });
          return httpGet("/periods")
            .then((response) => {
              this.periods = response.data;
            });
        });
    }
  }
};
</script>

