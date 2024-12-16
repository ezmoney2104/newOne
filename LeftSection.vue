<template>
  <v-main>
    <indicator :last-process="lastProcess"></indicator>
    <canvas-display :process-array="processData"></canvas-display>
  </v-main>
</template>

<script>
import Indicator from './Indicator.vue'
import CanvasDisplay from './CanvasDisplay.vue'
import { FetchAPI } from '@/utils/apiRequest'

export default {
  name: 'LeftSection',
  components: { Indicator, CanvasDisplay },

  data() {
    return {
      processData: [],
      lastProcess: null,
    }
  },
  mounted() {
    this.fetchData()
  },
  methods: {
    /**
     * Fetch the process data from the database
     */
    async fetchData() {
      const fetchApi = new FetchAPI()
      const res = await fetchApi.get('/api/process')
      if (res.success) {
        for (const data of res.data) {
          const obj = {
            processName: data.process_name,
            id: data.id,
            x: data.x_coord,
            y: data.y_coord,
            width: data.width,
            height: data.height,
            productNum: data.product_num,
            opStatus: this.validateStatus(data.operation_status),
          }
          this.processData.push(obj)
        }
        this.getLastProcessData()
      }
    },

    /**
     * This function get the last data from the canvas.
     */
    getLastProcessData() {
      if (this.processData) {
        const lastIndex = this.processData.length - 1
        this.lastProcess = this.processData[lastIndex]
      }
    },

    /**
     * Validates the status of the process if within the range of 1 to 3
     * @param {Number} status - status of the operation
     * @returns {Number} - returns the status number if within the range else it will return to 3.
     */
    validateStatus(status) {
      return status >= 1 && status <= 3 ? status : 3
    },
  },
}
</script>
