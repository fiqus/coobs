<template>
  <div>
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Dashboard</h1>
      <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"> <i class="fas fa-file-download"></i> Generate Balance</a>
    </div>

    <!-- Content Row -->
    <div class="row">

      <smallcard-chart
        label="Actions Done (Year)"
        icon="calendar"
        color-type="primary">
        <div class="h5 mb-0 font-weight-bold text-gray-800">130</div>
      </smallcard-chart>

      <smallcard-chart
        label="Co-op Investment"
        icon="currency"
        color-type="success">
        <div class="h5 mb-0 font-weight-bold text-gray-800">$215,000</div>
      </smallcard-chart>

      <smallcard-chart
        label="Co-op Promotion Fund"
        icon="coins"
        color-type="info">
        <div class="row no-gutters align-items-center">
          <div class="col-auto">
            <div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">50%</div>
          </div>
          <div class="col">
            <div class="progress progress-sm mr-2">
              <div class="progress-bar bg-info" role="progressbar" style="width: 50%" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100"></div>
            </div>
          </div>
        </div>
      </smallcard-chart>

      <smallcard-chart
        label="Pending Actions"
        icon="clipboard"
        color-type="warning">
        <div class="h5 mb-0 font-weight-bold text-gray-800">18</div>
      </smallcard-chart>

    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">All Principles</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;padding-top: 15px;">
              <apexchart width=250 type="donut" :options="allPrinciplesPie" :series="allPrinciplesPie.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <radialbar-chart
        v-for="principle in firstRowPrinciples"
        :key="principle.label"
        :label="principle.label"
        :percentage="principle.percentage">
      </radialbar-chart>

    </div>

    <!-- Content Row -->
    <div class="row">

      <radialbar-chart
        v-for="principle in secondRowPrinciples"
        :key="principle.label"
        :label="principle.label"
        :percentage="principle.percentage">
      </radialbar-chart>

    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Principle Chart -->
      <div class="col-xl-12 col-lg-12">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">All Principles (Year)</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body" style="padding-bottom: 40px;">
            <div class="chart-area">
              <apexchart type=bar height=300 :options="allPrinciplesYear" :series="allPrinciplesYear.series" />
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script>
  import VueApexCharts from 'vue-apexcharts';
  import RadialBarChart from "../components/radialbar-chart.vue";
  import SmallCardChat from "../components/smallcard-chart.vue"

  const coopcolors = ['#ED0017', '#F06704', '#FEFF00', '#53CE00', '#61C9FF', '#1400CD', '#60009A']

  export default {
    components: {
      "apexchart": VueApexCharts,
      "radialbar-chart": RadialBarChart,
      "smallcard-chart": SmallCardChat
    },
    computed: {
      firstRowPrinciples() {
        return this.principles.slice(0, 3);
      },
      secondRowPrinciples() {
        return this.principles.slice(3);
      }
    },
    data() {
      return {
        allPrinciplesYear: {
          chart: {
            stacked: true,
            height: 350,
            zoom: {
              enabled: false
            }
          },
          dataLabels: {
            enabled: false
          },
          stroke: {
            curve: 'straight'
          },
          xaxis: {
            categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
          },
          series: [{
              name: "Principio 1",
              data: [1, 0, 5, 7, 8, 9, 4, 3, 1, 2, 6, 9]
            },
            {
              name: "Principio 2",
              data: [3, 2, 7, 8, 9, 4, 3, 1, 4, 3, 1, 2]
            },
            {
              name: "Principio 3",
              data: [7, 1, 0, 4, 3, 1, 4, 3, 5, 3, 1, 4]
            },
            {
              name: "Principio 4",
              data: [4, 7, 3, 0, 6, 8, 3, 5, 3, 7, 1, 4]
            },
            {
              name: "Principio 5",
              data: [3, 5, 3, 7, 1, 4, 6, 7, 3, 0, 6, 8]
            },
            {
              name: "Principio 6",
              data: [8, 3, 5, 3, 7, 3, 0, 6, 8, 6, 1, 4]
            },
            {
              name: "Principio 7",
              data: [3, 7, 1, 4, 6, 7, 3, 0, 6, 8, 3, 5]
            }
          ],
          colors:coopcolors
        },
        principles: [
          {
            label: "Principle 1",
            percentage: 76
          },
          {
            label: "Principle 2",
            percentage: 24
          },
          {
            label: "Principle 3",
            percentage: 30
          },
          {
            label: "Principle 4",
            percentage: 48
          },
          {
            label: "Principle 5",
            percentage: 18
          },
          {
            label: "Principle 6",
            percentage: 52
          },
          {
            label: "Principle 7",
            percentage: 60
          }
        ],
        allPrinciplesPie: {
          responsive: [{
            breakpoint: 480,
            options: {
              chart: {
                width: '300'
              }
            }
          }],
          dataLabels: {
            enabled: false,
          },
          legend: {
            show: false
          },
          series: [44, 55, 41, 17, 15, 10, 20],
          labels: ["Principio 1", "Principio 2", "Principio 3", "Principio 4", "Principio 5", "Principio 6", "Principio 7"],
          colors:coopcolors
        }
      }
    }
  }
</script>
