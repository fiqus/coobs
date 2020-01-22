<template>
  <div>
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">{{$t("dashboard")}}<i class="fas fa-fw fa-tachometer-alt"></i></h1>
      <div class="dropdown no-arrow float-right mx-3">
        <a class="dropdown-toggle my-n2" role="button" aria-haspopup="true" aria-expanded="false">
          <select id="period-select" class="mr-2 d-none d-lg-inline text-gray-600 small form-control form-control-sm" v-on:change="onPeriodChange()" v-model="selectedValue">
            <option v-for="period in allPeriods" :key="period.id" :value="period.id">
              {{period.name}}
            </option>
          </select>
        </a>
      </div>
    </div>

    <!-- Content Row -->
    <div class="row" >

      <smallcard-chart
        :label="$t('actionsDone')"
        icon="calendar"
        color-type="primary">
        <template v-slot:chart-content>
          <div class="h5 mb-0 font-weight-bold text-gray-800">{{doneActions}}</div>
        </template>
      </smallcard-chart>

      <smallcard-chart
        :label="$t('investment')"
        icon="currency"
        color-type="success">
        <template v-slot:chart-content>
          <div class="h5 mb-0 font-weight-bold text-gray-800">$ {{totalInvested}}</div>
        </template>
      </smallcard-chart>

      <smallcard-chart
        :label="$t('promotionFund')"
        icon="coins"
        color-type="info">
        <template v-slot:chart-content>
          <div class="row no-gutters align-items-center">
            <div class="col-auto">
              <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">{{promotionFundPercentage}}%</div>
            </div>
            <div class="col">
              <div class="progress progress-sm mr-2">
                <div class="progress-bar bg-info" role="progressbar" :style=promotionFundStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
              </div>
            </div>
          </div>
        </template>
      </smallcard-chart>

      <smallcard-chart
        :label="$t('pendingActions')"
        icon="clipboard"
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
      </bars-chart>

      <div class="col-xl-6 col-lg-4">
        <div class="card shadow mb-4">
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">{{$t("progress")}}</h6>
          </div>
          <div class="card-body first-col-db" >
            <div class="">
              <!-- Period -->
              <div class="text-xs font-weight-bold text-uppercase mb-1" :class="labelClass">{{$t('periodProgress')}}</div>
              <div class="row no-gutters align-items-center">
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800 align-right">{{progressData.periodProgressData.dateFrom}}</div>
                </div>
                <div class="col center-col">
                  <div class="progress progress-sm mr-2 progress-data center">
                    <div class="progress-bar bg-warning" role="progressbar" :style=periodProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">{{progressData.periodProgressData.dateTo}}</div>
                </div>
              </div>
              <hr>

              <!-- Actions -->
              <div class="text-xs font-weight-bold text-uppercase mb-1" :class="labelClass">{{$t('actionsProgress')}}</div>
              
              <div class="row no-gutters align-items-center">
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800 align-right">0</div>
                </div>
                <div class="col center-col">
                  <div class="progress progress-sm mr-2 progress-data">
                    <div class="progress-bar bg-danger" role="progressbar" :style=actionsProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">{{progressData.actionsProgressData.actionsDone}}</div>
                </div>
              </div>
              <hr>

              <!-- Investment -->
              <div class="text-xs font-weight-bold text-uppercase mb-1" :class="labelClass">{{$t('investmentProgress')}}</div>

              <div class="row no-gutters align-items-center">
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800 align-right">$0,00</div>
                </div>
                <div class="col center-col">
                  <div class="progress progress-sm mr-2 progress-data">
                    <div class="progress-bar bg-success" role="progressbar" :style=investmentProgressStyle aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
                  </div>
                </div>
                <div class="col-3">
                  <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">${{progressData.investmentProgressData.budget}}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <columns-chart
      v-if="showActionsByPartner"
      :title="allActionsByPartnersLabel"
      :columns-data="actionsByPartnerData"
      :xaxis="actionsByPartnerLabels">
    </columns-chart>

    <area-chart
      :title="monthlyInvestmentByPrincipleLabel"
      :columns-data="localizeLabels(monthlyInvestmentByPrincipleData)"
      :xaxis="monthlyInvestmentByPrincipleLabels">
    </area-chart>
    <!-- Content Row -->
    <stacked-columns-chart
      :title="allPrinciplesYearLabel"
      :columns-data="localizeLabels(monthlyActionsByPrincipleData)"
      :xaxis="monthlyActionsByPrincipleLabels">
    </stacked-columns-chart>
  </div>
</template>

<script>
import SmallCardChart from "../components/smallcard-chart.vue";
import StackedColumndsChart from "../components/stacked-columns-chart.vue";
import DonutChart from "../components/donut-chart.vue";
import BarsChart from "../components/bars-chart.vue";
import ColumnsChart from "../components/columns-chart.vue";
import AreaChart from "../components/area-chart.vue";
import * as api from "./../services/api-service";


export default {
  components: {
    "smallcard-chart": SmallCardChart,
    "stacked-columns-chart": StackedColumndsChart,
    "donut-chart": DonutChart,
    "bars-chart": BarsChart,
    "columns-chart": ColumnsChart,
    "area-chart": AreaChart
  },
  computed: {
    allPrinciplesYearLabel() {
      return `${this.$t("allPrinciples")}`;
    },
    allActionsByPartnersLabel() {
      return `${this.$t("allActionsByPartnersLabel")}`;
    },
    monthlyInvestmentByPrincipleLabel() {
      return `${this.$t("monthlyInvestmentByPrincipleLabel")}`;
    }
  },
  methods: {
    showDashboardData(dashboardData){
      this.selectedValue = dashboardData.period.id;
      this.allPeriods = dashboardData.allPeriods;

      this.pendingActions = dashboardData.charts.cardsData.pendingActions;

      this.doneActions = dashboardData.charts.cardsData.doneActions;

      this.totalInvested = dashboardData.charts.cardsData.totalInvested;

      this.promotionFundPercentage = dashboardData.charts.cardsData.promotionFundPercentage;
      this.promotionFundStyle = `width: ${dashboardData.charts.cardsData.promotionFundPercentage}%`;

      this.allPrinciplesData = dashboardData.charts.allPrinciplesData;

      this.actionsByPrincipleData = [{data: this.allPrinciplesData.series}];
      this.actionsByPrincipleLabels = this.allPrinciplesData.labels;
      
      if (dashboardData.charts.actionsByPartner === {}) {
        this.showActionsByPartner = false;
      } else {
        this.actionsByPartnerData = dashboardData.charts.actionsByPartner.result;
        this.actionsByPartnerLabels = {categories: dashboardData.charts.actionsByPartner.labels};
      }

      this.monthlyInvestmentByPrincipleData = dashboardData.charts.monthlyInvestmentByPrinciple.result;
      this.monthlyInvestmentByPrincipleLabels = {type: "datetime", categories: dashboardData.charts.monthlyInvestmentByPrinciple.labels} ;
      
      this.monthlyActionsByPrincipleData = dashboardData.charts.monthlyActionsByPrinciple.result;
      this.monthlyActionsByPrincipleLabels = {categories: dashboardData.charts.monthlyActionsByPrinciple.labels} ;
      
      this.progressData = dashboardData.charts.progressData;
      this.periodProgressStyle = `width: ${this.progressData.periodProgressData.periodProgress}%`;
      this.actionsProgressStyle = `width: ${this.progressData.actionsProgressData.actionsProgress}%`;
      this.investmentProgressStyle = `width: ${this.progressData.investmentProgressData.investmentProgress}%`;      
    },
    localizeDonutChartLabels({labels, series}){
      const localizedLabels = labels.map((label) =>{
        return this.$t(label);
      });  
      return {labels: localizedLabels, series};
    },
    localizeLabels(results) {
      return results.map((result) => {
        result.name = this.$t(result.nameKey);
        return result;
      });
    },
    async onPeriodChange(){
      const params = this.selectedValue ? {periodId: this.selectedValue} : {};
      const dashboardData = await api.getDashboard(params);
      this.showDashboardData(dashboardData);
    }    
  },
  async created() {
    const dashboardData = await api.getDashboard();
    console.log(dashboardData);
    this.showDashboardData(dashboardData);
  },
  data() {
    return {
      periodName: "",
      doneActions: 0,
      pendingActions: 0,
      totalInvested: 0,
      promotionFundPercentage: 0,
      promotionFundStyle: "",
      periodProgressStyle: "",
      actionsProgressStyle: "",
      investmentProgressStyle: "",
      progressData: {periodProgressData: {dateFrom: 0, dateTo: 0}, actionsProgressData: {actionsDone: 0}, investmentProgressData: {budget: 0}},
      allPrinciplesData: {labels: [], series: []},
      actionsByPartnerData: [],
      monthlyActionsByPrincipleData: [],
      monthlyInvestmentByPrincipleData: [],
      xaxis: {categories: []},
      principles: [],
      allPeriods: [],
      selectedValue: [],
      showActionsByPartner: true
    };
  }
};
</script>
