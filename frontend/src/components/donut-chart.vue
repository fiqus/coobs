<template>
  <div class="col-xl-6 col-lg-4">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary">{{label}}</h6>
      </div>
      <div class="first-col-db" >
        <apexchart id="donut-chart" height="250" type="donut" :options="donutData" :series="donutData.series"></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";

const formatterTooltipValue = (val, index) => {
  // show the percentage instead of value
  const sum = index.globals.series.reduce((acc, num) => {
    return acc + num;
  }, 0);
  return `${((val/sum)*100).toFixed(1)}%`;
}

const commonsChartOptions = {
  chart: {
    type: 'donut'
  },
  dataLabels: {
    enabled: true,
    style: {
      fontSize: '13px'
    }
  },
  colors: ["#e55763", "#f2aa76", "#ffffa8", "#9bcc78", "#b7e1f7", "#5348ce", "#7d3ba5"],
  states: {
    hover: {
      filter: {
        type: 'darken', // or lighten
        value: 0.8,
      }
    }
  },
  tooltip: {
    enabled: true,
    y: {
      formatter: (val, index) => formatterTooltipValue(val, index)
    }
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        height: 300
      },
      legend: {
        position: "bottom"
      },
      dataLabels: {
        style: {
          fontSize: '10px'
        }
      },
    }
  }],
};

export default {
  props: {
    label: {
      type: String
    },
    chartData: {
      type: Array,
      required: true,
    }
  },
  components: {
    "apexchart": VueApexCharts
  },
  computed: {
    donutData() {
      return {
        ...commonsChartOptions,
        series: this.chartData.series,
        labels: this.chartData.labels
      };
    }
  }
};
</script>
