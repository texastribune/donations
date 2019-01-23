<template>
  <div class="grid_row grid_wrap--m form-buckets">
    <div
      v-for="group in groups"
      :key="group.id"
      :class="{
        'form-buckets__item--selected': selectedGroup === group.bucket,
      }"
      class="form-buckets__item col_4 grid_separator"
    >
      <p
        :id="getGroupHeadingConnector(group)"
        class="form-buckets__header grid_separator"
      >
        {{ group.heading }}
      </p>
      <radios
        :options="group.options"
        :aria-labelledby="getGroupHeadingConnector(group)"
        aria-describedby="circle-donate-hed circle-donate-intro"
        base-classes="form__radios form__radios--always-stack form__radios--serif"
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
import addNumberCommas from '../../utils/addNumberCommas';
import { CIRCLE_BUCKETS } from './constants';

export default {
  name: 'Choices',

  components: { Radios },

  mixins: [getStoreValue, updateStoreValues],

  data() {
    return {
      selectedGroup: this.getInitialSelectedGroup(),
      groups: [
        {
          id: 0,
          bucket: 'editor',
          heading: "Editor's Circle",
          options: this.buildOptions(['editorMonthly', 'editorYearly']),
        },
        {
          id: 1,
          bucket: 'leadership',
          heading: 'Leadership Circle',
          options: this.buildOptions(['leadershipMonthly', 'leadershipYearly']),
        },
        {
          id: 2,
          bucket: 'chairman',
          heading: "Chairman's Circle",
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

      bucketNames.forEach(name => {
        bucketsToIter.push({
          ...CIRCLE_BUCKETS[name],
          name,
        });
      });

      bucketsToIter.forEach((bucket, index) => {
        const { installmentPeriod, amount, name } = bucket;

        options.push({
          id: index,
          value: name,
          text: this.buildText({ installmentPeriod, amount }),
        });
      });

      return options;
    },

    getInitialSelectedGroup() {
      const level = this.getStoreValue({
        storeModule: 'circleForm',
        key: 'level',
      });

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

    getGroupHeadingConnector({ bucket, id }) {
      return `${bucket}-heading-${id}`;
    },
  },
};
</script>
