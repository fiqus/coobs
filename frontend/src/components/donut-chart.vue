<template>
  <div class="col-xl-3 col-lg-4">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary">{{label}}</h6>
      </div>
      <div class="card-body">
        <div class="chart-area" style="height:210px;padding-top: 15px;">
          <apexchart width=250 type="donut" :options="donutData" :series="donutData.series"></apexchart>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";

const commonsChartOptions = {
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: "300"
      }
    }
  }],
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false
  },
  colors: ["#ED0017", "#F06704", "#FEFF00", "#53CE00", "#61C9FF", "#1400CD", "#60009A"],
};

export default {
  props: {
    label: {
      type: String
    },
    chartData: {
      type: Array,
      required: true,
      default: {
        label: "Default",
        percentage: 100
      }
    }
  },
  components: {
    "apexchart": VueApexCharts
  },
  computed: {
    donutData() {
      return {
        ...commonsChartOptions,
        series: Object.values(this.chartData),
        labels: Object.keys(this.chartData)
      };
    }
  }
};
</script>

