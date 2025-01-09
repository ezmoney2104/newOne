<template>
  <v-main class="main">
    <line-utilization-status :util-data="extractedDataObject"></line-utilization-status>
    <child-equipment-information :process-data="processData" :ref-cycle-time="refCycleTime">
    </child-equipment-information>
    <equipment-failure-information></equipment-failure-information>
    <supply-notice class="supply" :supply-notice-data="supplyNoticeData"></supply-notice>
  </v-main>
</template>

<script>
import { FetchAPI } from '@/utils/apiRequest'
import LineUtilizationStatus from './LineUtilizationStatus.vue'
import ChildEquipmentInformation from './ChildEquipmentInformation.vue'
import SupplyNotice from './SupplyNotice.vue'
import EquipmentFailureInformation from './EquipmentFailureInformation.vue'
export default {
  name: 'RightSection',
  components: {
    LineUtilizationStatus,
    ChildEquipmentInformation,
    SupplyNotice,
    EquipmentFailureInformation,
  },
  props: {
    lastProcess: {
      type: [Object],
      required: true,
    },
    processData: {
      type: Array,
      required: true,
    },
  },

  data() {
    return {
      refCycleTime: 0,
      plannedUnits: null,
      opRate: null,
      supplyNoticeData: null,
    }
  },
  mounted() {
    this.fetchRefCycleTime()
    this.fetchSupplyNotice()
  },

  computed: {
    /**
     * Objects of extracted data to be passed to props
     * @returns {Object} data of planned units, product quantity, and rate
     */
    extractedDataObject() {
      return {
        plannedUnits: this.plannedUnits ? `${this.plannedUnits} 台` : '',
        goodProducts: this.extractGoodProducts ? `${this.extractGoodProducts} 台` : '',
        rate:
          this.opRate && this.opRate !== 'NaN' ? `${this.opRate}%` : this.opRate === 0 ? '-%' : '',
      }
    },

    /**
     * Extracts the last process ID from props
     * @returns {Number} extracted ID
     */
    extractedId() {
      return this.lastProcess.id
    },

    /**
     * Extract the data of planned number of units from last process
     * @returns {Number} planned number of units
     */
    extractPlannedUnit() {
      return this.lastProcess.plannedUnits
    },

    /**
     * Extract number of good products from last process
     * @returns {Number} number of good products
     */
    extractGoodProducts() {
      return this.lastProcess.goodProducts
    },

    /**
     * Computes the operation rate
     * @returns {Number} Operation rate value
     */
    computeOpRate() {
      return ((this.extractGoodProducts / this.plannedUnits) * 100).toFixed(2)
    },
  },
  methods: {
    /**
     * Fetching the reference cycle time in database
     */
    async fetchRefCycleTime() {
      const fetchApi = new FetchAPI()
      const res = await fetchApi.get('/api/reference_cycle_time')
      if (res.success) {
        this.plannedUnits = this.extractPlannedUnit
        const [obj] = res.data
        this.refCycleTime = obj.cycle_time
        this.opRate = 0
        setInterval(() => {
          this.plannedUnits += 1
          this.updatePlannedUnit()
          this.calculateOpRate()
        }, this.refCycleTime)
      }
    },

    /**
     * Fetch the supply notice data from database.
     */
    async fetchSupplyNotice() {
      const fetchApi = new FetchAPI()
      const res = await fetchApi.get('/api/supply_notice')
      if (res.success) {
        this.supplyNoticeData = res.data
      }
    },

    /**
     * Updates the planned number of units in the database
     */
    async updatePlannedUnit() {
      const fetchApi = new FetchAPI()
      await fetchApi.put(`/api/update-process/${this.extractedId}`, {
        plannedUnits: this.plannedUnits,
      })
    },

    /**
     * Reassing the value from computed operation rate to opRate global variable
     */
    calculateOpRate() {
      this.opRate = this.computeOpRate
    },
  },
}
</script>

<style scoped>
.main {
  position: relative;
  padding-top: 80px;
  margin: 8px;
}

.supply {
  margin: 0;
  padding: 0px;
  position: absolute;
  bottom: 20px;
}

@media screen and (max-width: 1402px) {
  .main {
    flex-direction: column;
    padding-top: 0;
    margin-left: 24px;
  }

  .supply {
    position: relative;
    bottom: 0px;
    margin-left: 0px;
  }
}
</style>
