<template>
  <div class="row">
    <div class="col-xl-12 col-lg-12">
      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">{{title}}</h6>
        </div>
        <div class="card-body" style="padding-bottom: 40px;">
          <div class="chart-area">
            <apexchart type=bar height=300 :options="chartData" :series="columnsData" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

const commonsChartOptions = {
  colors: ["#ED0017", "#F06704", "#FEFF00", "#53CE00", "#61C9FF", "#1400CD", "#60009A"],
  
  chart: {
    stacked: true,
    height: 350,
    zoom: {
      enabled: false
    }
  },
  dataLabels: {enabled: false},
  stroke: {curve: "straight"},

};

export default {
  props: {
    title: {
      type: String
    },
    columnsData: {
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
    chartData() {
      return {
        ...commonsChartOptions,
        xaxis: this.xaxis,
        series: this.columnsData,
      };
    }
  } 
};
</script>

