<template>
  <table class="table table-striped">
    <thead>
      <tr>
        <th v-for="header in headers" :key="header.key">
          {{ header.value }}
        </th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="elem in data" :key="elem.id">
        <td class="cursor-pointer" v-for="header in headers" :key="header.key" v-html="parseElem(header, elem)"></td>
        <td>
          <button class="btn btn-primary" @click.stop="onEdit(elem)" title="Edit"><i class="fa fa-edit"></i></button>
          <button class="btn btn-danger" @click.stop="onDelete(elem)" title="Delete"><i class="fa fa-trash"></i></button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
<script>
  export default {
    props: {
      headers: {
        type: Array,
        default: [],
        required: true
      },
      data: {
        type: Array,
        default: [],
        required: true
      },
    },
    methods: {
      parseElem(header, elem) {
        if (header.parser) {
            try {
              return header.parser(elem) || "";
            } catch (err) {
              console.trace(`Can't parse the element for '${header.key}'!`, err);
            }
          }
          return elem[header.key] || "";
      },
      onEdit(elem) {
        this.$emit("onEdit", elem);
      },
      onDelete(elem) {
        this.$emit("onDelete", elem);
      }
    }
  }
</script>
