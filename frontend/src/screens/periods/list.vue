<template>
  <div class="container">
    <div class="row">
      <h3 class="col-10">{{$t("periods")}}<i class="fas fa-fw fa-calendar"></i></h3>
      <router-link class="col-2 btn btn-primary mb-3" :to="{name: 'period-edit', params: {periodId: 0}}">
        {{$t("addNew")}}
        <i class="fa fa-plus"></i>
      </router-link>
    </div>
    <spinner :loading='isLoading'/>
    <loader :loading='isLoading'/>
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
import Loader from "../../components/loader-overlay.vue";
import Spinner from "../../components/spinner.vue";


function parseBoolean(value) {
  return `<i class="fas fa-dollar-sign fa-1x"></i> ${value}`;
}

export default {
  components: {
    "custom-table": CustomTable,
    "loader": Loader,
    "spinner": Spinner
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
        {key: "dateFrom", value: "from", parser: (p) => formatText(p.dateFrom, 50)},
        {key: "dateTo", value: "to", parser: (p) => formatText(p.dateTo, 50)},
        {key: "actionsBudget", value: "budget", parser: (p) => parseBoolean(p.actionsBudget)},
      ],
      periods: [],
      isLoading: true
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

