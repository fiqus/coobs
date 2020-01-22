<template>
  <div class="col-xl-3 col-lg-4">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary">{{label}}</h6>
      </div>
      <div class="card-body first-col-db">
        <apexchart height= "230" type=bar :options="barsData" :series="series" />
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

const commonsChartOptions = {
  plotOptions: {
    bar: {
      horizontal: false,
      endingShape: "flat",
      columnWidth: "50%",
      barHeight: "40%",
      distributed: true,
      colors: {
        ranges: [{
          from: 0,
          to: 0,
          color: undefined
        }],
        backgroundBarColors: [],
        backgroundBarOpacity: 1,
      },
      dataLabels: {
        position: "top",
        maxItems: 100,
        hideOverflowingLabels: false,
        orientation: "horizontal"
      }
    }
  },
  colors: ["#ED0017", "#F06704", "#FEFF00", "#53CE00", "#61C9FF", "#1400CD", "#60009A"],

  legend: {
    show: false
  },
  chart: {
    orientation: "horizontal",
    stacked: false,
    height: 240,
    zoom: {
      enabled: false
    }
  },
  stroke: {curve: "straight"},
};

export default {
  props: {
    label: {
      type: String
    },
    chartData: {
      type: Array,
      required: true
    },
    xaxis: {
      type: Object,
      required: true
    }
  },
  components: {
    "apexchart": VueApexCharts
  },
  computed: {
    barsData() {
      return {
        ...commonsChartOptions,
        xaxis: {categories: this.chartData.labels},
        series: [{data: this.chartData.series}],
      };
    }
  } 
};
</script>

