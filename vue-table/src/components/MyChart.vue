<script>
import { Line, mixins } from 'vue-chartjs'
//const { reactiveProp } = mixins;


export default {
  extends: Line,
  mixins: [ mixins.reactiveProp ],
  props:['chartData', 'options'],
  mounted () {
    /*this.renderChart({
      labels: ['11:00', '12:00', '13:00', '14:00', '15:00'],
      datasets: [
        {
          label: 'Cup Detected times',
          //backgroundColor: '#f87979',
          data: this.data,
          borderColor: "#3e95cd",
          fill: false
        },
        {
          label: 'Cellphone Detected times',
          data: [13, 25, 56, 22, 78],
          borderColor: "#e8c3b9",
          fill: false
        }
      ]
    }, this.options)*/
    this.renderLineChart();
  },
  methods: {
    renderLineChart: function() {
      this.renderChart(this.chartData, this.options);
    },
  }, 
  /*watch: {
    chartData: function () {
            this._chart.destroy();
            console.log(this.chartData);
            console.log(this.options);
            this.renderLineChart();
            console.log('render');
    }
  }*/
}
</script>
