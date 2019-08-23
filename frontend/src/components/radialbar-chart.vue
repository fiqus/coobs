<template>
  <div class="col-xl-3 col-lg-4">
    <div class="card shadow mb-4">
      <!-- Card Header -->
      <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
        <h6 class="m-0 font-weight-bold text-primary">{{label}}</h6>
      </div>
      <!-- Card Body -->
      <div class="card-body">
        <div class="chart-area" style="height:210px;">
          <apexchart height=300 type="radialBar" :options="chartOptions" :series="chartOptions.series"></apexchart>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import VueApexCharts from 'vue-apexcharts';

  export default {
    props: {
      label: {
        type: String,
      },
      percentage: {
        type: Number,
        required: true
      }
    },
    components: {
      "apexchart": VueApexCharts
    },
    data() {
      const principleDataLabels = {
        name: {
          show: false
        },
        value: {
          offsetY: 15,
          fontSize: '22px'
        }
      };
      const plotOptions = {
        radialBar: {
          startAngle: -90,
          endAngle: 90,
          track: {
            background: "#e7e7e7",
            strokeWidth: '97%',
            margin: 5, // margin is in pixels
            shadow: {
              enabled: true,
              top: 2,
              left: 0,
              color: '#999',
              opacity: 1,
              blur: 2
            }
          },
          dataLabels: principleDataLabels
        }
      };
      const fill = {
        type: 'gradient',
        gradient: {
          shade: 'light',
          shadeIntensity: 0.4,
          inverseColors: false,
          opacityFrom: 1,
          opacityTo: 1,
          stops: [0, 50, 53, 91]
        },
      };

      return {
        chartOptions: {
          plotOptions,
          fill,
          labels: [this.label],
          series: [this.percentage]
        }
      }
    }
  }
</script>

