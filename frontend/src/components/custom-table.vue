<template>
  <div>
    <table class="table table-striped">
      <thead>
        <tr>
          <th v-for="header in headers" :key="header.key" @click="sort(header.key)">
            {{ $t(header.value, header.value) }}<span v-if="header.key == currentSort" class="arrow" :class="currentSortDir"/>
          </th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="elem in sortedData" :key="elem.id">
          <td class="cursor-pointer" v-for="header in headers" :key="header.key" v-html="parseElem(header, elem)"></td>
          <td>
            <button v-if="actions.edit && !elem.noActions" class="btn btn-primary" @click.stop="onEdit(elem)" :title="$t('edit')"><i class="fa fa-edit"></i></button>
            <button v-if="actions.delete && !elem.noActions && actions.showViewButton" class="btn btn-success" @click.stop="onQuickView(elem)" :title="$t('quickView')"><i class="fa fa-eye"></i></button>
            <button v-if="actions.delete && !elem.noActions" class="btn btn-danger" @click.stop="onDelete(elem)" :title="$t('delete')"><i class="fa fa-trash"></i></button>
          </td>
        </tr>
        <tr v-if="!data.length">
          <td :colspan="headers.length + 1">{{emptyStateMsg}}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="data.length" class="row">
      <div class="col-sm-12 col-md-5">
        <div class="" role="status" aria-live="polite">
          {{paginationMessage}}
        </div>
      </div>
      <div class="col-sm-12 col-md-7">
        <div class=" paging_simple_numbers">
          <ul class="justify-content-end pagination">
            <li class="paginate_button page-item previous" :class="{'disabled': !pagination.previous}">
              <button class="page-link" @click="goPrevious()">{{$t('previous')}}</button>
            </li>
            <li v-for="pageNumber in pagination.numPages" :key="pageNumber" class="paginate_button page-item " :class="{'active': pageNumber === pagination.page}">
              <button class="page-link" @click="goToPage(pageNumber)">{{pageNumber}}</button>
            </li>
            <li class="paginate_button page-item next" :class="{'disabled': !pagination.next}">
              <button class="page-link" @click="goNext()">{{$t('next')}}</button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
// import '../css/custom.css'

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
    pagination: {
      type: Object,
      default: null
    }
  },
  computed: {
    paginationMessage() {
      const start = (this.pagination.pageSize * (this.pagination.page-1)) + 1;
      const end = this.data.length < this.pagination.pageSize ? ((this.pagination.pageSize * (this.pagination.page-1)) + this.data.length) : this.pagination.pageSize * this.pagination.page;
      return this.$t('paginationMessage', {start, end, count: this.pagination.count});
    },
    sortedData(){
      return this.data.sort((a,b) => {
        let modifier = 1;
        if(this.currentSortDir === 'desc') modifier = -1;
        if(a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
        if(a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        return 0;
      }).filter((row, index) => {
          let start = (this.pagination.page-1)*this.pagination.pageSize;
          let end = this.pagination.page*this.pagination.pageSize;
          if(index >= start && index < end) return true;
        });
    }
  },
  methods: {
    goToPage(page) {
      this.$emit("goToPage", page);
    },
    goNext() {
      this.$emit("goNext");
    },
    goPrevious() {
      this.$emit("goPrevious");
    },
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
