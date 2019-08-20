<template>
  <div>
    <!-- Page Heading -->
    <div class="d-sm-flex align-items-center justify-content-between mb-4">
      <h1 class="h3 mb-0 text-gray-800">Dashboard</h1>
      <a href="#" class="d-none d-sm-inline-block btn btn-sm btn-primary shadow-sm"> <i class="fas fa-file-download"></i> Generate Balance</a>
    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Cooperative Actions QTY -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-primary shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Actions Done (Year)</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">130</div>
              </div>
              <div class="col-auto">
                <i class="fas fa-calendar fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cooperative Actions Investment -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-success shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Co-op Investment</div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">$215,000</div>
              </div>
              <div class="col-auto">
                <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cooperative promotion fund -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-info shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Co-op Promotion Fund</div>
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
              </div>
              <div class="col-auto">
                <i class="fas fa-coins fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Actions -->
      <div class="col-xl-3 col-md-6 mb-4">
        <div class="card border-left-warning shadow h-100 py-2">
          <div class="card-body">
            <div class="row no-gutters align-items-center">
              <div class="col mr-2">
                <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                  Pending Actions
                </div>
                <div class="h5 mb-0 font-weight-bold text-gray-800">
                  18
                </div>
              </div>
              <div class="col-auto">
                <i class="fas fa-clipboard-list fa-2x text-gray-300"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
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

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 1</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle1" :series="principle1.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 2</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle2" :series="principle2.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 3</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle3" :series="principle3.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Content Row -->
    <div class="row">

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 4</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle4" :series="principle4.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 5</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle5" :series="principle5.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 6</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle6" :series="principle6.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

      <!-- Principle Chart -->
      <div class="col-xl-3 col-lg-4">
        <div class="card shadow mb-4">
          <!-- Card Header -->
          <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
            <h6 class="m-0 font-weight-bold text-primary">Principle 7</h6>
          </div>
          <!-- Card Body -->
          <div class="card-body">
            <div class="chart-area" style="height:210px;">
              <apexchart height=300 type="radialBar" :options="principle7" :series="principle7.series"></apexchart>
            </div>
          </div>
        </div>
      </div>

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
  import VueApexCharts from 'vue-apexcharts'
  const coopcolors = ['#ED0017', '#F06704', '#FEFF00', '#53CE00', '#61C9FF', '#1400CD', '#60009A']
  const principleDataLabels = {
          name: {
            show: false
          },
          value: {
            offsetY: 15,
            fontSize: '22px'
          }
        }

  export default {
    components: {
      "apexchart": VueApexCharts
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
        principle1: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 1'],
          series: [76]
        },
        principle2: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [30]
        },
        principle3: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [30]
        },
        principle4: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [30]
        },
        principle5: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [30]
        },
        principle6: {
          plotOptions: {
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
              dataLabels: {
                name: {
                  show: false
                },
                value: {
                  offsetY: 15,
                  fontSize: '22px'
                }
              }
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [30]
        },
        principle7: {
          plotOptions: {
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
          },
          fill: {
            type: 'gradient',
            gradient: {
              shade: 'light',
              shadeIntensity: 0.4,
              inverseColors: false,
              opacityFrom: 1,
              opacityTo: 1,
              stops: [0, 50, 53, 91]
            },
          },
          labels: ['Principle 2'],
          series: [60]
        },
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
