<template>
  <div>
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">{{$t("dashboard")}}</h1>
    </div>

    <!-- Content Row -->
    <div class="row">

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
        :chart-data="allPrinciplesData">

      </donut-chart>

      <radialbar-chart
        v-for="principle in firstRowPrinciples"
        :key="principle.label"
        :label="principle.label"
        :percentage="principle.percentage">
      </radialbar-chart>

    </div>

    <!-- Content Row -->
    <div class="row">

      <radialbar-chart
        v-for="principle in secondRowPrinciples"
        :key="principle.label"
        :label="principle.label"
        :percentage="principle.percentage">
      </radialbar-chart>

    </div>

    <stacked-columns-chart
      :title="allPrinciplesYearLabel"
      :columns-data="monthlyActionsByPrincipleData"
      :xaxis="monthlyActionsByPrincipleLabels">
    </stacked-columns-chart>

  </div>
</template>

<script>
import RadialBarChart from "../components/radialbar-chart.vue";
import SmallCardChart from "../components/smallcard-chart.vue";
import StackedColumndsChart from "../components/stacked-columns-chart.vue";
import DonutChart from "../components/donut-chart.vue";
import * as api from "./../services/api-service";

const coopcolors = ["#ED0017", "#F06704", "#FEFF00", "#53CE00", "#61C9FF", "#1400CD", "#60009A"];

export default {
  components: {
    "radialbar-chart": RadialBarChart,
    "smallcard-chart": SmallCardChart,
    "stacked-columns-chart": StackedColumndsChart,
    "donut-chart": DonutChart
  },
  computed: {
    allPrinciplesYearLabel() {
      return `${this.$t("allPrinciples")}`;
    },
    firstRowPrinciples() {
      return this.principles.slice(0, 3);
    },
    secondRowPrinciples() {
      return this.principles.slice(3);
    }
  },
  async created() {
    const dashboardData = await api.getDashboard();
    console.log(dashboardData);

    this.pendingActions = dashboardData.charts.cardsData.pendingActions;

    this.doneActions = dashboardData.charts.cardsData.doneActions;

    this.totalInvested = dashboardData.charts.cardsData.totalInvested;

    this.promotionFundPercentage = dashboardData.charts.cardsData.promotionFundPercentage;
    this.promotionFundStyle = `width: ${dashboardData.charts.cardsData.promotionFundPercentage}%`;


    this.allPrinciplesData = dashboardData.charts.allPrinciplesData;
    
    this.monthlyActionsByPrincipleData = dashboardData.charts.monthlyActionsByPrinciple.result;
    this.monthlyActionsByPrincipleLabels = {categories: dashboardData.charts.monthlyActionsByPrinciple.labels} ;
    

  },
  data() {
    return {
      periodName: "",
      doneActions: 0,
      pendingActions: 0,
      totalInvested: 0,
      promotionFundPercentage: 0,
      promotionFundStyle: "",
      allPrinciplesData: {},
      monthlyActionsByPrincipleData: [],
      xaxis: {categories: []},
      principles: []
    };
  }
};
</script>
