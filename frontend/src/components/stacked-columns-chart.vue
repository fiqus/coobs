<template>
  <div class="row">
    <div class="col-xl-12 col-lg-12">
      <div class="card shadow mb-4">
        <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
          <h6 class="m-0 font-weight-bold text-primary">{{title}}</h6>
        </div>
        <div class="card-body" >
          <apexchart height= "350" type=bar :options="chartData" :series="columnsData" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueApexCharts from "vue-apexcharts";

const formatterTooltipValue = (val, obj) => {
  // show the percentage instead of value
  const sum = obj.w.globals.series.reduce((acc, col) => {
    return acc + col[obj.dataPointIndex];
  }, 0);
  return `${((val/sum)*100).toFixed(1)}%`;
}

const commonsChartOptions = {
  colors: ["#e55763", "#f2aa76", "#ffffa8", "#9bcc78", "#b7e1f7", "#5348ce", "#7d3ba5"],
  chart: {
    stacked: true,
    stackType: '100%',
    height: 350,
    zoom: {
      enabled: false
    }
  },
  stroke: {curve: "straight"},
  legend: {
    position: 'bottom',
    offsetX: 50
  },
  tooltip: {
    x: {
      show: false
    },
    y: {
      formatter: (val, index) => formatterTooltipValue(val, index)
    }
  },
  dataLabels: {
    enabled: true,
    formatter: (val) => `${val.toFixed(1)}%`
  },
  responsive: [{
    breakpoint: 480,
    options: {
      legend: {
        position: 'bottom',
        offsetX: -10,
        offsetY: 0
      }
    }
  }]
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

