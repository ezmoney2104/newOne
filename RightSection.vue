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


-----

<template>
  <v-main class="main">
    <!-- Display LineUtilizationStatus and ChildEquipmentInformation -->
    <template v-if="showFirstSet">
      <line-utilization-status :util-data="extractedDataObject"></line-utilization-status>
      <child-equipment-information :process-data="processData" :ref-cycle-time="refCycleTime">
      </child-equipment-information>
    </template>

    <!-- Display EquipmentFailureInformation -->
    <template v-else>
      <equipment-failure-information></equipment-failure-information>
    </template>

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
      showFirstSet: true, // State to toggle components
    }
  },
  mounted() {
    this.fetchRefCycleTime()
    this.fetchSupplyNotice()

    // Start the alternating timer
    this.startAlternatingComponents()
  },
  computed: {
    extractedDataObject() {
      return {
        plannedUnits: this.plannedUnits ? `${this.plannedUnits} 台` : '',
        goodProducts: this.extractGoodProducts ? `${this.extractGoodProducts} 台` : '',
        rate:
          this.opRate && this.opRate !== 'NaN' ? `${this.opRate}%` : this.opRate === 0 ? '-%' : '',
      }
    },
    extractedId() {
      return this.lastProcess.id
    },
    extractPlannedUnit() {
      return this.lastProcess.plannedUnits
    },
    extractGoodProducts() {
      return this.lastProcess.goodProducts
    },
    computeOpRate() {
      return ((this.extractGoodProducts / this.plannedUnits) * 100).toFixed(2)
    },
  },
  methods: {
    startAlternatingComponents() {
      setInterval(() => {
        this.showFirstSet = !this.showFirstSet
      }, 7000) // Switch every 7 seconds
    },
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
    async fetchSupplyNotice() {
      const fetchApi = new FetchAPI()
      const res = await fetchApi.get('/api/supply_notice')
      if (res.success) {
        this.supplyNoticeData = res.data
      }
    },
    async updatePlannedUnit() {
      const fetchApi = new FetchAPI()
      await fetchApi.put(`/api/update-process/${this.extractedId}`, {
        plannedUnits: this.plannedUnits,
      })
    },
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




----


import { shallowMount } from '@vue/test-utils';
import RightSection from '@/components/RightSection.vue';
import LineUtilizationStatus from '@/components/LineUtilizationStatus.vue';
import ChildEquipmentInformation from '@/components/ChildEquipmentInformation.vue';
import EquipmentFailureInformation from '@/components/EquipmentFailureInformation.vue';
import SupplyNotice from '@/components/SupplyNotice.vue';

jest.useFakeTimers(); // Mock timers for testing setInterval

describe('RightSection.vue', () => {
  let wrapper;

  const mockLastProcess = {
    id: 1,
    plannedUnits: 100,
    goodProducts: 90,
  };

  const mockProcessData = [
    { id: 1, name: 'Process A' },
    { id: 2, name: 'Process B' },
  ];

  beforeEach(() => {
    wrapper = shallowMount(RightSection, {
      props: {
        lastProcess: mockLastProcess,
        processData: mockProcessData,
      },
    });
  });

  afterEach(() => {
    wrapper.unmount();
  });

  it('should render LineUtilizationStatus and ChildEquipmentInformation initially', () => {
    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(true);
    expect(wrapper.findComponent(ChildEquipmentInformation).exists()).toBe(true);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(false);
  });

  it('should switch to EquipmentFailureInformation after 7 seconds', async () => {
    jest.advanceTimersByTime(7000); // Simulate 7 seconds
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(false);
    expect(wrapper.findComponent(ChildEquipmentInformation).exists()).toBe(false);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(true);
  });

  it('should toggle components alternately every 7 seconds', async () => {
    // Initial state
    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(true);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(false);

    // After 7 seconds
    jest.advanceTimersByTime(7000);
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(false);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(true);

    // After another 7 seconds
    jest.advanceTimersByTime(7000);
    await wrapper.vm.$nextTick();

    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(true);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(false);
  });

  it('should render SupplyNotice regardless of toggle state', () => {
    expect(wrapper.findComponent(SupplyNotice).exists()).toBe(true);

    jest.advanceTimersByTime(7000);
    expect(wrapper.findComponent(SupplyNotice).exists()).toBe(true);
  });

  it('should handle abnormal cases gracefully (e.g., missing props)', async () => {
    wrapper = shallowMount(RightSection, {
      props: {
        lastProcess: null,
        processData: null,
      },
    });

    // Verify that no errors are thrown during rendering
    expect(wrapper.exists()).toBe(true);

    // Verify that the components are still alternating
    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(true);
    jest.advanceTimersByTime(7000);
    await wrapper.vm.$nextTick();
    expect(wrapper.findComponent(LineUtilizationStatus).exists()).toBe(false);
    expect(wrapper.findComponent(EquipmentFailureInformation).exists()).toBe(true);
  });

  it('should clear intervals on component unmount', () => {
    const spyClearInterval = jest.spyOn(global, 'clearInterval');
    wrapper.unmount();

    expect(spyClearInterval).toHaveBeenCalled();
    spyClearInterval.mockRestore();
  });
});

