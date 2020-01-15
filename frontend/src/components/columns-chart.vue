<template>
  <div class="row">
    <div class="col-xl-12 col-lg-12">
      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">{{title}}</h6>
        </div>
        <div class="card-body" >
          <apexchart type=bar :options="chartData" :series="columnsData" />
        </div>
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
      columnWidth: "20%",
      barHeight: "20%",
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
    height: 350,
    zoom: {
      enabled: false
    }
  },
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

