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
      <p class="form-buckets__header grid_separator">
        {{ group.heading }} <br />
      </p>
      <radios
        :options="group.options"
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
import getValue from '../../elements/mixins/getValue';
import updateValues from '../../elements/mixins/updateValues';
import addNumberCommas from '../../utils/addNumberCommas';
import {
  BUSINESS_BUCKETS,
  MEMBERSHIP_LEVELS,
  POSITION_ON_FORM_0,
  POSITION_ON_FORM_1,
  POSITION_ON_FORM_2,
} from './constants';

export default {
  name: 'FormBuckets',

  components: { Radios },

  mixins: [getValue, updateValues],

  data() {
    return {
      selectedGroup: this.getInitialSelectedGroup(),
      groups: [
        {
          id: 0,
          bucket: 'levelA',
          heading: MEMBERSHIP_LEVELS[POSITION_ON_FORM_0].header,
          options: this.buildOptions(['levelAYearly', 'levelAMonthly']),
        },
        {
          id: 1,
          bucket: 'levelB',
          heading: MEMBERSHIP_LEVELS[POSITION_ON_FORM_1].header,
          options: this.buildOptions(['levelBYearly', 'levelBMonthly']),
        },
        {
          id: 2,
          bucket: 'levelC',
          heading: MEMBERSHIP_LEVELS[POSITION_ON_FORM_2].header,
          options: this.buildOptions(['levelCYearly', 'levelCMonthly']),
        },
      ],
    };
  },

  methods: {
    buildText({ uiInstallmentPeriod, amount }) {
      return `$${addNumberCommas(amount)} ${uiInstallmentPeriod}`;
    },

    buildOptions(bucketNames) {
      const options = [];
      const bucketsToIter = [];

      bucketNames.forEach(name => {
        bucketsToIter.push({
          ...BUSINESS_BUCKETS[name],
          name,
        });
      });

      bucketsToIter.forEach((bucket, index) => {
        const { amount, name } = bucket;
        const { uiInstallmentPeriod } = bucket.paymentDetails;
        options.push({
          id: index,
          value: name,
          text: this.buildText({ uiInstallmentPeriod, amount }),
        });
      });
      return options;
    },

    getInitialSelectedGroup() {
      const level = this.getValue({
        storeModule: 'businessForm',
        key: 'level',
      });
      return BUSINESS_BUCKETS[level].bucket;
    },

    onUpdate(level) {
      const { amount, bucket, paymentDetails } = BUSINESS_BUCKETS[level];

      const updates = {
        installment_period: paymentDetails.installmentPeriod,
        installments: paymentDetails.installments,
        openended_status: paymentDetails.openEndedStatus,
        amount,
      };

      this.setSelectedGroup(bucket);
      this.updateValues({ storeModule: 'businessForm', updates });
    },

    setSelectedGroup(bucket) {
      this.selectedGroup = bucket;
    },
  },
};
</script>
