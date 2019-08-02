<template>
  <div>
    <h1>Ahora si!</h1>
    <apexchart height=350 type="radialBar" :options="chartOptions" :series="series"></apexchart>
  </div>
</template>

<script>
  import VueApexCharts from 'vue-apexcharts'

  export default {
    components: {
      "apexchart": VueApexCharts
    },
    data() {
      return {
        chartOptions: {
          plotOptions: {
            radialBar: {
              hollow: {
                size: '70%',
              }
            },
          },
          labels: ['Cooperación entre cooperativas']
        },
        series: [70]
      }
    }
  }
</script>
