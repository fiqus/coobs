<template>
  <table class="table table-hover">
    <thead>
      <tr class="thead-light">
        <th scope="col" colspan="4">{{$t(periodSummary.principleNameKey, periodSummary.principleNameKey)}}</th>
      </tr>
      <tr>
        <th scope="col">Accion</th>
        <th scope="col">Descripcion</th>
        <th scope="col">Fecha</th>
        <th scope="col">Invertido</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="action in periodSummary.actions" :key="action.name">
        <td>{{action.name}}</td>
        <td>{{action.description}}</td>
        <td>{{action.date}}</td>
        <td>{{action.investedMoney}}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    periodSummary: {
      type: Object,
      required: true
    }
  }
}
</script>

