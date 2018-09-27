<template>
  <div
    class="grid_row grid_wrap--m"
  >
    <div
      v-for="group in groups"
      :key="group.id"
      :class="{ selected: selectedGroup === group.bucket }"
      class="business-form__bucket col_4 grid_separator"
    >
      <p
        :id="getGroupHeadingConnector(group)"
        class="business-form__bucket-header grid_separator"
      >
        {{ group.heading }}
      </p>
      <radios
        :options="group.options"
        :aria-labelledby="getGroupHeadingConnector(group)"
        aria-describedby="business-donate-hed business-donate-intro"
        base-classes="form__radios form__radios--always-stack form__radios--serif"
        name="level"
        store-module="businessForm"
        @updateCallback="onUpdate"
      />
    </div>
  </div>
</template>

<script>
import Radios from '../../elements/Radios.vue';
import getStoreValue from '../../elements/mixins/getStoreValue';
import updateStoreValues from '../../elements/mixins/updateStoreValues';
import addNumberCommas from '../../utils/addNumberCommas';
import {
  BUSINESS_BUCKETS,
  MEMBERSHIP_LEVELS,
  POSITION_0,
  POSITION_1,
  POSITION_2
} from './constants';

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
          bucket: 'levelA',
          heading: MEMBERSHIP_LEVELS[POSITION_0].header,
          options: this.buildOptions(['levelAMonthly', 'levelAYearly', 'levelAOneTime']),
        },
        {
          id: 1,
          bucket: 'levelB',
          heading: MEMBERSHIP_LEVELS[POSITION_1].header,
          options: this.buildOptions(['levelBMonthly', 'levelBYearly', 'levelBOneTime']),
        },
        {
          id: 2,
          bucket: 'levelC',
          heading: MEMBERSHIP_LEVELS[POSITION_2].header,
          options: this.buildOptions(['levelCMonthly', 'levelCYearly', 'levelCOneTime']),
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
          ...BUSINESS_BUCKETS[name],
          name,
        });
      });

      bucketsToIter.forEach((bucket, index) => {
        const { installmentPeriod, amount, name, header } = bucket;
        options.push({
          id: index,
          header: header,
          value: name,
          text: this.buildText({ installmentPeriod, amount }),
        });
      });
      console.log(options);
      return options;
    },

    getInitialSelectedGroup() {
      const level =
        this.getStoreValue({ storeModule: 'businessForm', key: 'level' });
      console.log("Setting initial selection state: level");
      console.log(level);
      console.log("Setting initial selection state: bucket");
      console.log(BUSINESS_BUCKETS[level].bucket);
      return BUSINESS_BUCKETS[level].bucket;
    },

    onUpdate(level) {
      const {
        amount,
        bucket,
        installments,
        installmentPeriod,
      } = BUSINESS_BUCKETS[level];

      const updates = {
        installment_period: installmentPeriod,
        installments,
        amount,
      };

      this.setSelectedGroup(bucket);
      this.updateStoreValues({ storeModule: 'businessForm', updates });
    },

    setSelectedGroup(bucket) {
      this.selectedGroup = bucket;
    },

    getGroupHeadingConnector({ bucket, id }) {
      return `${bucket}-heading-${id}`;
    },
  },
};
</script>
