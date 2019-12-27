<template>
  <div class="col-xl-3 col-md-6 mb-4">
    <div class="card shadow h-100 py-2" :class="borderLeftClass">
      <div class="card-body">
        <div class="row no-gutters align-items-center">
          <div class="col mr-2">
            <div class="text-xs font-weight-bold text-uppercase mb-1" :class="labelClass">{{label}}</div>
            <slot name="chart-content"/>
          </div>
          <div class="col-auto">
            <i class="fas fa-2x text-gray-300" :class="iconClass"></i>
          </div>
        </div>
      </div>
    </div>
  </div>  
</template>
<script>
const typesMap = {
  calendar: "fa-calendar",
  currency: "fa-dollar-sign",
  coins: "fa-coins",
  clipboard: "fa-clipboard-list"
};

export default {
  props: {
    label: {
      type: String
    },
    icon: {
      type: String
    },
    colorType: {
      type: String,
      default: "primary"
    }
  },
  data() {
    return {
      iconClass: typesMap[this.icon] || "",
      labelClass: `text-${this.colorType}`,
      borderLeftClass: `border-left-${this.colorType}`
    };
  }
};
</script>

