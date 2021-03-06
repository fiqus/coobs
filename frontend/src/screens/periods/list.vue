<template>
  <div class="custom-container">
    <div class="row px-3 mb-3">
      <h3 class="col-md-10 col-sm-9 px-0">{{$t("periods")}}</h3>
      <router-link class="col-md-2 col-sm-3 btn btn-primary" :to="{name: 'period-edit', params: {periodId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <loader :loading='isLoading'/>
    <simple-table v-if="periods.length"
      :headers="headers"
      :data="periods"
      :actions="{edit: true, delete: true, showViewButton: false}"
      :empty-state-msg="$t('noPeriodsMessage')" 
      @onEdit="onEdit"
      @onDelete="onDelete">
    </simple-table>
    <missing-data-empty-state v-if="!periods.length"
      :hasPeriod="periods.length"
      :hasActions="true"
    />
  </div>
</template>

<script>
import SimpleTable from "../../components/simple-table.vue";
import {formatText, formatToUIDate} from "../../utils";
import {httpGet, httpDelete} from "../../api-client.js";
import swal from "sweetalert";
import Loader from "../../components/loader-overlay.vue";
import MissingDataEmptyState from "../../components/missing-data-empty-state.vue";


function parseBoolean(value) {
  return `<i class="fas fa-dollar-sign fa-1x"></i> ${value}`;
}

export default {
  components: {
    "simple-table": SimpleTable,
    "loader": Loader,
    "missing-data-empty-state": MissingDataEmptyState,
  },
  created() {
    httpGet("/periods")
      .then((response) => {
        this.periods = response.data;
        this.isLoading = false;
      });
  },
  data() {
    return {
      headers: [
        {key: "name", value: "name", parser: (p) => formatText(p.name)},
        {key: "dateFrom", value: "from", parser: (p) => formatToUIDate(p.dateFrom)},
        {key: "dateTo", value: "to", parser: (p) => formatToUIDate(p.dateTo)},
        {key: "actionsBudget", value: "budget", parser: (p) => parseBoolean(p.actionsBudget)},
      ],
      periods: [],
      isLoading: true,
    };
  },
  methods: {
    onEdit(period) {
      this.$router.push({name: "period-edit", params: {periodId: period.id}});
    },
    onDelete(period) {
      swal({
        title: this.$t('areYouSure'),
        text: this.$t('oncePeriodDeleted'),
        icon: "warning",
        buttons: true,
        dangerMode: true,
      })
      .then((willDelete) => {
        if (willDelete) {
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
      });
    }
  }
};
</script>
