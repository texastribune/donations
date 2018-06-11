<template>
  <div>
    <div
      v-for="group in groups"
      :key="group.id"
      :selected="selectedGroup === group.bucket"
      :choice="choice"
    >
      <radios
        v-model="value"
        :options="group.options"
        :key="choice.id"
        @updateCallback="onUpdate"
      />
    </div>
  </div>
</template>

<script>
import Radios from './Radios.vue';
import getStoreValue from '../../elements/mixins/connectedElement';

export default {
  name: 'Choices',

  components: { Radios },

  mixins: [getStoreValue],

  props: {
    storeModule: {
      type: String,
      required: true,
    },
  },

  data() {
    return {
      value: null,
      selectedGroup: null,
      allValues: {
        yearlyEditor: {
          bucket: 'editor',
          text: '$1,000 annually',
          installments: '3',
          amount: '1000',
          installmentPeriod: 'yearly',
        },
        monthlyEditor: {
          bucket: 'editor',
          text: '$84 monthly',
          installments: '36',
          amount: '84',
          installmentPeriod: 'monthly',
        },
        yearlyLeadership: {
          bucket: 'leadership',
          text: '$2,500 annually',
          installments: '3',
          amount: '2500',
          installmentPeriod: 'yearly',
        },
        monthlyLeadership: {
          bucket: 'leadership',
          text: '$209 monthly',
          installments: '36',
          amount: '209',
          installmentPeriod: 'monthly',
        },
        yearlyChairman: {
          bucket: 'chairman',
          text: '$5,000 annually',
          installments: '3',
          amount: '5000',
          installmentPeriod: 'yearly',
        },
        monthlyChairman: {
          bucket: 'chairman',
          text: '$417 monthly',
          installments: '36',
          amount: '417',
          installmentPeriod: 'monthly',
        },
      },
      groups: [
        {
          id: 0,
          title: 'Editor\'s Circle',
          bucket: 'editor',
          options: [
            {
              id: 0,
              value: this.buildRadioValue(this.allValues.yearlyEditor),
              text: this.allValues.yearlyEditor.text,
            },
            {
              id: 1,
              value: this.buildRadioValue(this.allValues.monthlyEditor),
              text: this.allValues.monthlyEditor.text,
            },
          ],
        },
        {
          id: 1,
          title: 'Leadership Circle',
          bucket: 'leadership',
          options: [
            {
              id: 0,
              value: this.buildRadioValue(this.allValues.yearlyLeadership),
              text: this.allValues.yearlyLeadership.text,
            },
            {
              id: 1,
              value: this.buildRadioValue(this.allValues.monthlyLeadership),
              text: this.allValues.monthlyLeadership.text,
            },
          ],
        },
        {
          id: 2,
          title: 'Chairman\'s Circle',
          bucket: 'chairman',
          options: [
            {
              id: 0,
              value: this.buildRadioValue(this.allValues.yearlyChairman),
              text: this.allValues.yearlyChairman.text,
            },
            {
              id: 1,
              value: this.buildRadioValue(this.allValues.monthlyChairman),
              text: this.allValues.monthlyChairman.text,
            },
          ],
        },
      ],
    };
  },

  mounted() {
    this.getInitialData();
  },

  methods: {
    buildRadioValue({ installments, installmentPeriod, amount }) {
      return JSON.stringify({
        installments,
        installmentPeriod,
        amount,
      });
    },

    getInitialData() {
      let initialValue = null;
      const { storeModule } = this;

      const installmentPeriod =
        this.getStoreValue({ storeModule, key: 'installment_period' });
      const installments =
        this.getStoreValue({ storeModule, key: 'installments' });
      const amount =
        this.getStoreValue({ storeModule, key: 'amount' });

      Object.keys(this.allValues).forEach((key) => {
        const curr = this.allValues[key];

        if (
          curr.installmentPeriod === installmentPeriod &&
          curr.installments === installments &&
          curr.amount === amount
        ) {
          const { text, ...relevantProperties } = curr;
          initialValue = relevantProperties;
        }
      });

      this.value = initialValue ? JSON.stringify(initialValue) : null;
      this.selectedGroup = initialValue ? initialValue.bucket : null;
    },

    onUpdate(reference) {
      // this.setSelectedGroup(reference);
    },

    setSelectedGroup(reference) {
      this.selected = reference;
    },
  },
};
</script>
