<template>
  <div>
    <table class="table table-striped">
      <thead>
        <tr v-if="sortEnabled">
          <th class="cursorPointer" v-for="header in headers" :key="header.key" @click="sort(header.key)">
            {{ $t(header.value, header.value) }}<span v-if="header.key == currentSort" class="arrow" :class="currentSortDir"/>
          </th>
          <th></th>
        </tr>
        <tr v-if="!sortEnabled">
          <th v-for="header in headers" :key="header.key">
            {{ $t(header.value, header.value) }}
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="elem in sortedData" :key="elem.id">
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
    currentSort: {
      type: String,
      default: 'name'
    },
    currentSortDir: {
      type: String,
      default: 'asc'
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
    sortEnabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    sortedData(){
      if (!this.sortEnabled){
        return this.data;
      }
      const sortedData = this.data.sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      });
      if (!this.pagination) {
        return sortedData;
      }
      return sortedData.filter((row, index) => {
          let start = (this.pagination.page-1)*this.pagination.pageSize;
          let end = this.pagination.page*this.pagination.pageSize;
          if(index >= start && index < end) return true;
        });
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
    sort(s) {
      //if s == current sort, reverse
      if(s === this.currentSort) {
        this.currentSortDir = this.currentSortDir==='asc'?'desc':'asc';
      }
      this.currentSort = s;
    }    
  }
};
</script>
