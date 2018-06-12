<template>
  <div>
    <div
      v-for="group in groups"
      :key="group.id"
      :selected="selectedGroup === group.bucket"
    >
      <radios
        :options="group.options"
        base-classes=""
        name="level"
        store-module="circleForm"
        @updateCallback="onUpdate"
      />
    </div>
  </div>
</template>

<script>
import Radios from '../../elements/Radios.vue';
import getStoreValue from '../../elements/mixins/getStoreValue';
import updateStoreValues from '../../elements/mixins/updateStoreValues';
import { CIRCLE_BUCKETS } from './constants';
import addNumberCommas from '../../utils/addNumberCommas';

export default {
  name: 'Choices',

  components: { Radios },

  mixins: [
    getStoreValue,
    updateStoreValues,
  ],

  data() {
    return {
      selectedGroup: this.getInitialSelectedGroup(),
      groups: [
        {
          id: 0,
          bucket: 'editor',
          options: this.buildOptions(['editorMonthly', 'editorYearly']),
        },
        {
          id: 1,
          bucket: 'leadership',
          options: this.buildOptions(['leadershipMonthly', 'leadershipYearly']),
        },
        {
          id: 2,
          bucket: 'chairman',
          options: this.buildOptions(['chairmanMonthly', 'chairmanYearly']),
        },
      ],
    };
  },

  methods: {
    buildText({ installmentPeriod, amount }) {
      return `$${addNumberCommas(amount)} ${installmentPeriod}`;
    },

    buildOptions(bucketNames) {
      const options = [];
      const bucketsToIter = [];

      bucketNames.forEach((name) => {
        bucketsToIter.push({
          ...CIRCLE_BUCKETS[name],
          name,
        });
      });

      bucketsToIter.forEach((bucket, index) => {
        const { installmentPeriod, amount, name } = bucket;

        options.push({
          id: index,
          connector: name,
          value: name,
          text: this.buildText({ installmentPeriod, amount }),
        });
      });

      return options;
    },

    getInitialSelectedGroup() {
      const level =
        this.getStoreValue({ storeModule: 'circleForm', key: 'level' });

      return CIRCLE_BUCKETS[level].bucket;
    },

    onUpdate(level) {
      const {
        amount,
        bucket,
        installments,
        installmentPeriod,
      } = CIRCLE_BUCKETS[level];

      const updates = {
        installment_period: installmentPeriod,
        installments,
        amount,
      };

      this.setSelectedGroup(bucket);
      this.updateStoreValues({ storeModule: 'circleForm', updates });
    },

    setSelectedGroup(bucket) {
      this.selectedGroup = bucket;
    },
  },
};
</script>
