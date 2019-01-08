<template>
  <div class="ui container">
    <vuetable ref="vuetable"
      api-url="http://10.239.76.23:3000/api/v1/alerts"
      :fields="fields"
      :per-page="5"
      pagination-path=""
      :css="css.table"
      @vuetable:pagination-data="onPaginationData" 
    ></vuetable>
      <!--<vuetable-pagination-info ref="paginationInfo" :css="css.paginationInfo"></vuetable-pagination-info>-->
      <vuetable-pagination ref="pagination"
        class="pull-right"
        @vuetable-pagination:change-page="onChangePage"
        :css="css.pagination">
      </vuetable-pagination>
  </div>
</template>

<script>
import Vuetable from 'vuetable-2/src/components/Vuetable'
import VuetablePagination from 'vuetable-2/src/components/VuetablePagination'
//import VuetablePaginationInfo from 'vuetable-2/src/components/VuetablePaginationInfo'
import CssConfig from './VuetableCssConfig.js'
//import VuetablePaginationBootstrap from './VuetablePaginationBootstrap'


export default {
  components: {
    Vuetable,
    VuetablePagination,
    //VuetablePaginationInfo    
  },
  data() {
    return {
      css: CssConfig,
      fields: [
        {
          name: '__sequence',   // <----
          title: '#',
          titleClass: 'text-center',
          dataClass: 'text-center'
        },
        {
          name: 'timestamp',
          title: 'Timestamp',
          callback: 'timeConverter',
          titleClass: 'text-center',
          dataClass: 'text-center'
        },
        {
          name: 'camera_id',
          title: 'Camera ID',
          titleClass: 'text-center',
          dataClass: 'text-center'
        },
        {
          name: 'class_id',
          title: 'Detected Class',
          callback: 'getClassName',
          titleClass: 'text-center',
          dataClass: 'text-center'
        },
        {
          name: 'timestamp',
          title: 'Details',
          callback: 'getVideo',
          titleClass: 'text-center',
          dataClass: 'text-center'
        }
      ]
    }
  },
  methods: {
    timeConverter (UNIX_timestamp) {
      var a = new Date(UNIX_timestamp);
      var year = a.getFullYear();
      var month = a.getMonth() + 1;
      var date = a.getDate();
      var hour = (a.getHours() < 10? '0' : '') + a.getHours();
      var min = (a.getMinutes() < 10? '0' : '') + a.getMinutes();
      var sec = (a.getSeconds() < 10? '0' : '') + a.getSeconds();
      var time = year + "-" + month + "-" + date + " " + hour + ":" + min + ":" + sec ;
      return time;
    },
    getClassName (class_ids) {
      var className = [];
      var i = 0;
        for(i=0; i<class_ids.length; i++){
            if(class_ids[i] == 77) className.push("cell phone");
            if(class_ids[i] == 47) className.push("cup");
      }
      return className.join();
    },
    getVideo(timestamp) {
      //return "<a ng-click='videoClick($event, http://localhost:3000/video?cam=1&ts=" + timestamp + ".mp4)'>...</a>"
      return "<a href='http://10.239.76.23:3000/video?cam=1&ts=" + timestamp + "' target='_blank'>...</a>"
    },
    onPaginationData (paginationData) {
      this.$refs.pagination.setPaginationData(paginationData);
      //this.$refs.paginationInfo.setPaginationData(paginationData);
    },
    onChangePage (page) {
      this.$refs.vuetable.changePage(page)
    },
    setupStream () {
      var source = new EventSource("http://10.239.76.23:3000/stream");
      var app = this;
      source.addEventListener('notification', function(event) {
        var data = JSON.parse(event.data);
        console.log("The server says " + data.fullDocument.timestamp);
        app.$refs.vuetable.refresh();
      }, false);
      source.addEventListener('error', function(event) {
        console.error("Failed to connect to event stream. Is Redis running?");
      }, false);
    }
  },
  mounted() {
    this.setupStream();
  }
}
</script>
