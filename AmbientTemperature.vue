<template>
  <v-container fluid><div ref="plotElement"></div></v-container>
</template>

<script>
import Plotly from 'plotly.js-dist'

export default {
  name: 'AmbientTemperature',

  data() {
    return {
      config: { responsive: true, displayModeBar: false },
      cnt: 0,
      chartData: [
        {
          y: [this.randomTemp()],
          mode: 'lines+markers',
          marker: { color: 'red', size: 4 },
          line: { width: 1 },
        },
      ],
      layout: {
        xaxis: { range: [0, 50] },
        title: 'Process Temperature Monitoring Screen',
      },
      polling: null,
    }
  },
  mounted() {
    this.renderChart()
    this.newTrace()
  },

  methods: {
    /**
     * Function to initialize and display Ambient Temperature Graph
     */

    renderChart() {
      Plotly.newPlot(this.$refs.plotElement, this.chartData, this.layout, this.config)
    },

    /**
     * Function to extends movement of the Ambient Temperature Graph when counter reacher greater 50
     */

    newTrace() {
      this.pooling = setInterval(() => {
        Plotly.extendTraces(this.$refs.plotElement, { y: [[this.randomTemp()]] }, [0])
        this.cnt++
        if (this.cnt > 50) {
          Plotly.relayout(this.$refs.plotElement, {
            xaxis: {
              range: [this.cnt - 50, this.cnt],
            },
          })
        }
      }, 100)
    },

    /**
     * Returns a random integer from 0 to 100
     * @returns {interger} returns randon integer
     */
    randomTemp() {
      return Math.floor(Math.random() * 101)
    },
  },
}
</script>
