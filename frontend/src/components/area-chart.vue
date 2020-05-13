<template>
  <div class="row">
    <div class="col-xl-12 col-lg-12">
      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">{{title}}</h6>
        </div>
        <div class="card-body" >
          <apexchart height= "350" type=area :options="chartData" :series="columnsData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";
import {parseMoney} from "../utils"

const commonsChartOptions = {
  colors: ["#e55763", "#f2aa76", "#ffffa8", "#9bcc78", "#b7e1f7", "#5348ce", "#7d3ba5"],
  chart: {
    height: 350,
    stacked: true
  },
  dataLabels: {
    enabled: true,
    formatter: (val) => `$ ${parseMoney(val)}`
  },
  stroke: {
    curve: "smooth"
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.6,
      opacityTo: 0.8,
    }
  },
  xaxis: {
    type: "datetime",
  },
  tooltip: {
    x: {
      show: false
    },
    y: {
      formatter: (val) => `$ ${parseMoney(val)}`
    }
  }
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

