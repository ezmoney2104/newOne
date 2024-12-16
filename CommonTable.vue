<template>
  <v-table>
    <thead>
      <tr>
        <th
          v-for="columnItem in tableProperties.TABLE_HEADER"
          :key="columnItem.id"
          v-bind="columnItem.directives"
        >
          <common-label :item="columnItem"></common-label>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td
          v-for="columnItem in tableProperties.TABLE_BODY"
          :key="columnItem.id"
          v-bind="columnItem.directives"
        >
          <common-label :item="columnItem"></common-label>
        </td>
      </tr>
    </tbody>
  </v-table>
</template>

<script>
import CommonLabel from './CommonLabel.vue'
import { TABLE_PROPERTIES } from '@/common/recipe/rCommonTable'
export default {
  name: 'CommonTable',
  props: { item: { type: Array, required: true } },
  components: { CommonLabel },
  data() {
    return {
      tableProperties: { ...TABLE_PROPERTIES },
    }
  },
  mounted() {
    console.log('tableProperties: ', this.tableProperties)
  },
}
</script>
