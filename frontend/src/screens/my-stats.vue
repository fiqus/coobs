<template>
    <div v-if="error.exists" :class="error.backgroundClass" class="d-sm-flex align-items-center p-3">
      <div class="col-sm-9">
        <h5 class="mb-0 text-gray-100">
          <i class="fas fa-exclamation-circle"></i>
          {{$t(error.message, error.message)}}
        </h5>
      </div>
      <div v-if="allPeriods.length" class="col-sm-2 float-right ">
        <div class="dropdown no-arrow float-right mx-3">
          <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
            <label class="text-gray-100">{{$t('periods')}}</label>
            <select id="period-select" class="ml-2 mr-5 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
              <option v-for="period in allPeriods" :key="period.id" :value="period.id">
                {{period.name}}
              </option>
            </select>
          </a>
        </div>
      </div>
    </div>
    <div v-else>
      <loader :loading='isLoading'/>
      <div>
        <!-- Page Heading -->
        <div class="d-sm-flex align-items-center justify-content-between mb-4">
          <div class="dropdown no-arrow float-right">
            <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
              <label>{{$t('periods')}}</label>
              <select id="period-select" class="ml-2 mr-5 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
                <option v-for="period in allPeriods" :key="period.id" :value="period.id">
                  {{period.name}}
                </option>
              </select>
            </a>
          </div>
          <div class="col-9">
            <small class="form-text text-muted font-italic ml-3">{{$t('myStatsHelp')}}</small>
          </div>
        </div>

        <!-- Content Row -->
        <div class="row" >

          <smallcard-chart
            :label="$t('actionsDone')"
            icon="calendar"
            columns="col-xl-4"
            color-type="primary">
            <template v-slot:chart-content>
              <div class="h5 mb-0 font-weight-bold text-gray-800">{{doneActions}}</div>
            </template>
          </smallcard-chart>

          <smallcard-chart
            :label="$t('investedHours')"
            icon="time"
            columns="col-xl-4"
            color-type="success">
            <template v-slot:chart-content>
              <div class="h5 mb-0 font-weight-bold text-gray-800">{{totalHoursInvested}}</div>
            </template>
          </smallcard-chart>

          <smallcard-chart
            :label="$t('pendingActions')"
            icon="clipboard"
            columns="col-xl-4"
            color-type="warning">
            <template v-slot:chart-content>
              <div class="h5 mb-0 font-weight-bold text-gray-800">{{pendingActions}}</div>
            </template>
          </smallcard-chart>

        </div>

        <!-- Content Row -->
        <div class="row">
          <!-- Principle Chart -->
          <donut-chart
            :label="$t('allPrinciples')"
            :chart-data="localizeDonutChartLabels(allPrinciplesData)">
          </donut-chart>

          <bars-chart
            :label="$t('allPrinciples')"
            :chart-data="localizeDonutChartLabels(allPrinciplesData)">
            <template v-slot:tooltip>
              <span class="d-inline-block" tabindex="0" data-toggle="tooltip" :title="localizeTooltip()">
                <icon id="allPrinciplesTooltip" class="fa fa-question-circle"></icon>
              </span>
            </template>
          </bars-chart>

          <div class="col-xl-4 col-lg-4">
            <div class="card shadow mb-4">
              <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
                <h6 class="m-0 font-weight-bold text-primary">{{$t("progress")}}</h6>
              </div>
              <div class="card-body first-col-db" >
                <div class="">
                  <!-- Period -->
                  <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('periodProgress')}}</div>
                  <div class="row no-gutters align-items-center">
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">{{progressData.periodProgressData.dateFrom}}</div>
                    </div>
                    <div class="col center-col">
                      <div class="progress progress-sm mr-2 progress-data center">
                        <div class="progress-bar custom-orange" role="progressbar" :style=periodProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{progressData.periodProgressData.dateTo}}</div>
                    </div>
                  </div>
                  <hr>

                  <!-- Actions -->
                  <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('actionsProgress')}}</div>
                  
                  <div class="row no-gutters align-items-center">
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">0</div>
                    </div>
                    <div class="col center-col">
                      <div class="progress progress-sm mr-2 progress-data">
                        <div class="progress-bar custom-red" role="progressbar" :style=actionsProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{progressData.actionsProgressData.actionsDone + pendingActions}}</div>
                    </div>
                  </div>
                  <hr>

                  <!-- Investment -->
                  <div class="text-xs font-weight-bold text-uppercase mb-2" :class="labelClass">{{$t('investedHours')}}</div>

                  <div class="row no-gutters align-items-center">
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800 align-right">0</div>
                    </div>
                    <div class="col center-col">
                      <div class="progress progress-sm mr-2 progress-data">
                        <div class="progress-bar custom-green" role="progressbar" :style=investmentProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                      </div>
                    </div>
                    <div class="col-3">
                      <div class="small mb-0 mr-2 font-weight-bold text-gray-800">{{progressData.investmentProgressData.partnerHoursGoal}}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      <line-chart
        :title="monthlyHoursByDateLabel"
        :columns-data="monthlyHoursByDateData"
        :xaxis="monthlyHoursByDateLabels">
      </line-chart>

      <!-- Content Row -->
      <stacked-columns-chart
        :title="allPrinciplesYearLabel"
        :columns-data="localizeLabels(monthlyActionsByPrincipleData)"
        :xaxis="monthlyActionsByPrincipleLabels">
      </stacked-columns-chart>
    </div>
  </div>
</template>

<script>
import SmallCardChart from "../components/smallcard-chart.vue";
import StackedColumndsChart from "../components/stacked-columns-chart.vue";
import DonutChart from "../components/donut-chart.vue";
import BarsChart from "../components/bars-chart.vue";
import ColumnsChart from "../components/columns-chart.vue";
import LineChart from "../components/line-chart.vue";
import * as api from "./../services/api-service";
import Loader from "../components/loader-overlay.vue";
import parseMoney from "./../utils";
import moment from "moment";
import _ from "lodash";


function dateToUserTimeZone (date){
  return moment(date).format("YYYY-MM-DDTHH:mm:ssZ");
}

export default {
  components: {
    "smallcard-chart": SmallCardChart,
    "stacked-columns-chart": StackedColumndsChart,
    "donut-chart": DonutChart,
    "bars-chart": BarsChart,
    "columns-chart": ColumnsChart,
    "line-chart": LineChart,
    "loader": Loader
  },
  computed: {
    allPrinciplesYearLabel() {
      return `${this.$t("allPrinciples")}`;
    },
    monthlyHoursByDateLabel() {
      return `${this.$t("monthlyHoursByDateLabel")}`;
    },
    monthlyHoursByDateLabels(){
      const labels = _.get(this.dashboardData, "charts.monthlyHoursByDate.labels", []);
      const newLabels = labels.map(dateToUserTimeZone);
      
      return {type: "datetime", categories: newLabels};
    }
  },
  methods: {
    showDashboardData(dashboardData){
      this.dashboardData = dashboardData;
      this.selectedValue = dashboardData.period.id;
      this.allPeriods = dashboardData.allPeriods;

      this.pendingActions = dashboardData.charts.cardsData.pendingActions;

      this.doneActions = dashboardData.charts.cardsData.doneActions;
      this.totalHoursInvested = dashboardData.charts.cardsData.totalHoursInvested ? (dashboardData.charts.cardsData.totalHoursInvested).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,") : 0;

      this.allPrinciplesData = dashboardData.charts.allPrinciplesData;

      this.actionsByPrincipleData = [{data: this.allPrinciplesData.series}];
      this.actionsByPrincipleLabels = this.allPrinciplesData.labels;

      this.monthlyHoursByDateData = dashboardData.charts.monthlyHoursByDate.result;
      
      this.monthlyActionsByPrincipleData = dashboardData.charts.monthlyActionsByPrinciple.result;
      this.monthlyActionsByPrincipleLabels = {categories: dashboardData.charts.monthlyActionsByPrinciple.labels} ;
      
      this.progressData = dashboardData.charts.progressData;
      // FIXME #137 we could show hours invested against hours expected to use in cooperativistic activities
      this.progressData.investmentProgressData.budget = this.progressData.periodProgressData !== undefined ? parseInt(dashboardData.charts.progressData.investmentProgressData.budget).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, "$&,") : 0;
      this.periodProgressStyle = `width: ${this.progressData.periodProgressData.periodProgress}%`;
      this.actionsProgressStyle = `width: ${this.progressData.actionsProgressData.actionsProgress}%`;
      this.investmentProgressStyle = `width: ${this.progressData.investmentProgressData.investmentProgress}%`;      
      this.isLoading = false;
    },
    localizeDonutChartLabels({labels, series}){
      if (!labels) {
        return {labels: []};
      }
      const localizedLabels = labels.map((label) =>{
        return this.$t(label);
      });  
      return {labels: localizedLabels, series};
    },
    localizeLabels(results) {
      return results ? results.map((result) => {
        result.name = this.$t(result.nameKey);
        return result;
      }) : [];
    },
    localizeTooltip(){
      return this.$t('allPrinciplesTooltip');
    },
    async onPeriodChange(){
      this.error.exists = false;
      const params = this.selectedValue ? {periodId: this.selectedValue} : {};
      const dashboardData = await api.getMyStats(params);
      if (!dashboardData.actions.length) {
        this.error = {
          exists: true,
          backgroundClass: " bg-danger",
          message: "notEnoughInfoForDashboard"
        };
      } else {
        this.showDashboardData(dashboardData);
      }
    }    
  },
  async created() {
    const dashboardData = await api.getMyStats();
    if (!dashboardData.actions.length) {
      this.error = {
        exists: true,
        backgroundClass: " bg-danger",
        message: "notEnoughInfoForDashboard"
      };
    } else {
      this.showDashboardData(dashboardData);
    }
  },
  toggleTooltip(){
    this.$refs.tooltip.$emit('toggle');
  },
  data() {
    return {
      periodName: "",
      doneActions: 0,
      pendingActions: 0,
      totalHoursInvested: 0,
      actionsProgressStyle: "",
      investmentProgressStyle: "",
      progressData: {periodProgressData: {dateFrom: 0, dateTo: 0}, actionsProgressData: {actionsDone: 0}, investmentProgressData: {budget: 0}},
      allPrinciplesData: {labels: [], series: []},
      actionsByPartnerData: [],
      monthlyActionsByPrincipleData: [],
      monthlyHoursByDateData: [],
      principles: [],
      allPeriods: [],
      selectedValue: [],
      error: {
        exists: false,
        backgroundClass: " bg-danger",
        message: ""
      },
      isLoading: true,
      dashboardData: {}
    };
  }
};
</script>
