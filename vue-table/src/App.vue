<template>
  <div id="app">
     <my-vuetable></my-vuetable>
     <div class="ui container">
       <my-chart v-if="loaded" :chartData="dataChart" :options="{responsive: true, maintainAspectRatio: false}"></my-chart>
     </div>
  </div>
</template>

<script>
import MyVuetable from './components/MyVuetable'
import MyChart from './components/MyChart'
import axios from 'axios'


export default {
  name: 'app',
  components: {
    MyVuetable,
    MyChart
  },
  data() { 
    return { 
      showModal: false,
      dataChart: {},
      errors: [], 
      loaded: false
    } 
  },
  mounted() {
    this.getChartData();
    this.streamData();
  },
  methods: {
    streamData() {
        // LIVE PUSH EVENTS
        if (typeof (EventSource) !== "undefined") {
          var app = this;
          var eventSource = new EventSource(
            "http://10.239.76.23:3000/stream");
          eventSource.addEventListener('open', function (e) {
            console.log("Opened connection to event stream!");
          }, false);

          eventSource.addEventListener('error', function (e) {
            console.log("Errored!");
          }, false);

          eventSource.addEventListener('notification', function (e) {
            //var parsedData = JSON.parse(e.data);
            //var cat = parseInt(parsedData.data)
            console.log("chart event.");
            app.getChartData();
          }, false);
        }
    },
    getChartData: function() {
      axios.get("http://10.239.76.23:3000/api/v1/count?tz=Asia%2FShanghai")
        .then(response => {
          if (response.status == 200) {
            console.log(response.data);
            this.dataChart = Object.assign({});
            this.$set(this.dataChart,"labels",[]);  
            this.$set(this.dataChart,"datasets",[]);
            //var newData = {"labels": "", "datasets": []};
            this.dataChart.labels = response.data["labels"];
            for (var key in response.data["data"]) {
              if(key == 47) {
                this.dataChart.datasets.push({
                  label: "Cup Detected times",
                  data: response.data["data"][key],
                  borderColor: "#3e95cd",
                  fill: false
                });
              } else if (key == 77) {
                  this.dataChart.datasets.push({
                    label: "Cell Phone Detected times",
                    data: response.data["data"][key],
                    borderColor: "#e8c3b9",
                    fill: false
                  });
              }
            }
            //this.dataChart = newData;
            print(this.dataChart);
            this.loaded = true;
         }
        })
        .catch(e => {
          this.errors.push(e)
        })
    }
  }, 
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
