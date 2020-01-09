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
          <div class="h5 mb-0 font-weight-bold text-gray-800">{{actionsDone}}</div>
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
              <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">50%</div>
            </div>
            <div class="col">
              <div class="progress progress-sm mr-2">
                <div class="progress-bar bg-info" role="progressbar" style="width: 50%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
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
          <div class="h5 mb-0 font-weight-bold text-gray-800">18</div>
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
      :columns-data="allPrinciplesYearData">
    </stacked-columns-chart>

  </div>
</template>

<script>
import RadialBarChart from "../components/radialbar-chart.vue";
import SmallCardChart from "../components/smallcard-chart.vue";
import StackedColumndsChart from "../components/stacked-columns-chart.vue";
import DonutChart from "../components/donut-chart.vue";
import * as api from "./../services/api-service";
import {allPrinciplesDataParser, parseMoney} from "./../utils";

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
      return `${this.$t("allPrinciples")} (${this.$t("yearly")})`;
    },
    firstRowPrinciples() {
      return this.principles.slice(0, 3);
    },
    secondRowPrinciples() {
      return this.principles.slice(3);
    }
  },
  async created() {
    //this.period = getCurrentPeriod();
    const actions = await api.getActions();
    this.actionsDone = actions.length;
    this.totalInvested = parseMoney(actions.reduce(function(acc, action){
      return acc += parseInt(action.investedMoney);
    }, 0));
    this.allPrinciplesData = allPrinciplesDataParser(actions);
  },
  data() {
    return {
      actionsDone: 0,
      totalInvested: 0,
      allPrinciplesData: {},
      allPrinciplesYearData: [{
        name: "Principio 1",
        data: [1, 0, 5, 7, 8, 9, 4, 3, 1, 2, 6, 9]
      },
      {
        name: "Principio 2",
        data: [3, 2, 7, 8, 9, 4, 3, 1, 4, 3, 1, 2]
      },
      {
        name: "Principio 3",
        data: [7, 1, 0, 4, 3, 1, 4, 3, 5, 3, 1, 4]
      },
      {
        name: "Principio 4",
        data: [4, 7, 3, 0, 6, 8, 3, 5, 3, 7, 1, 4]
      },
      {
        name: "Principio 5",
        data: [3, 5, 3, 7, 1, 4, 6, 7, 3, 0, 6, 8]
      },
      {
        name: "Principio 6",
        data: [8, 3, 5, 3, 7, 3, 0, 6, 8, 6, 1, 4]
      },
      {
        name: "Principio 7",
        data: [3, 7, 1, 4, 6, 7, 3, 0, 6, 8, 3, 5]
      }
      ],
      principles: [
        {
          label: "Principle 1",
          percentage: 76
        },
        {
          label: "Principle 2",
          percentage: 24
        },
        {
          label: "Principle 3",
          percentage: 30
        },
        {
          label: "Principle 4",
          percentage: 48
        },
        {
          label: "Principle 5",
          percentage: 18
        },
        {
          label: "Principle 6",
          percentage: 52
        },
        {
          label: "Principle 7",
          percentage: 60
        }
      ]
    };
  }
};
</script>
