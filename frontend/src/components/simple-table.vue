<template>
  <div>
    <table class="table table-striped">
      <thead>
        <tr v-if="ordering.enabled">
          <th :class="{'cursorPointer': header.sortEnabled}" v-for="header in headers" :key="header.key" @click="onSort(header.sortEnabled, header.key)">
            {{ $t(header.value, header.value) }}<span v-if="header.key == ordering.by" :class="{'arrow': header.sortEnabled, [sortDirClass]: header.sortEnabled}"/>
          </th>
          <th></th>
        </tr>
        <tr v-if="!ordering.enabled">
          <th v-for="header in headers" :key="header.key">
            {{ $t(header.value, header.value) }}
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="elem in data" :key="elem.id">
          <td class="cursor-pointer" v-for="header in headers" :key="header.key" v-html="parseElem(header, elem)"></td>
          <td>
            <button v-if="actions.edit && !elem.noActions" class="btn btn-primary" @click.stop="onEdit(elem)" :title="$t('edit')"><i class="fa fa-edit"></i></button>
            <!-- <button v-if="actions.delete && !elem.noActions && actions.showViewButton" class="btn btn-success" @click.stop="onQuickView(elem)" :title="$t('quickView')"><i class="fa fa-eye"></i></button> FIXME no idea why it depends on delete-->
            <button v-if="!elem.noActions && actions.showViewButton" class="btn btn-success" @click.stop="onQuickView(elem)" :title="$t('quickView')"><i class="fa fa-eye"></i></button>
            <button v-if="actions.delete && !elem.noActions" class="btn btn-danger" @click.stop="onDelete(elem)" :title="$t('delete')"><i class="fa fa-trash"></i></button>
          </td>
        </tr>
        <tr v-if="!data.length">
          <td :colspan="headers.length + 1">{{emptyStateMsg}}</td>
        </tr>
      </tbody>
    </table>
  </div>
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
    actions: {
      type: Object,
      default: {
        delete: false,
        edit: false
      }
    },
    emptyStateMsg: {
      type: String
    },
    ordering: {
      type: Object,
      default: {
        enabled: false
      }
    }
  },
  computed: {
    sortDirClass() {
      return !this.ordering.dir ? "asc" : "desc";
    }
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
    },
    onQuickView(elem) {
      this.$emit("onQuickView", elem);
    },
    onSort(enabled, sort) {
      if (enabled) {
        this.$emit("onSort", sort);
      }
    }
  }
};
</script>
