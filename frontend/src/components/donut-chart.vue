<template>
  <div class="col-xl-3 col-lg-4">
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary">{{label}}</h6>
      </div>
      <div class="first-col-db" >
        <apexchart height= "355" type= "donut" :options="donutData" :series="donutData.series"></apexchart>
      </div>
    </div>
  </div>
</template>
<script>
import VueApexCharts from "vue-apexcharts";

const commonsChartOptions = {
  
  plotOptions: {
    pie: {
      customScale: 0.74
    },
  },  
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: "auto"
      }
    }
  }],
  dataLabels: {
    enabled: true,
  },
  legend: {
    show: false,
    
  },
  chart: {
    height: 300
  },
  
  colors: ["#e55763", "#f2aa76", "#ffffa8", "#9bcc78", "#b7e1f7", "#5348ce", "#7d3ba5"],
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

