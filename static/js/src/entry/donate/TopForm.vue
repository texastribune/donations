<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form_membership"
    @submit="onSubmit"
  >
    <fieldset
      class="donation grid_separator"
    >
      <div class="grid_separator--s">
        <legend
          class="donation--prompt grid_separator--s"
        >
          I'm ready to give ...
        </legend>
        <div
          class="grid_row donation--input"
        >
          <span
            class="donation--dollar"
          >
            $
          </span>
          <text-input
            base-css-classes="col tt_input donation--amount"
            name="amount"
            store-module="baseForm"
          />
        </div>
      </div>
      <radios
        :update-callback="onFrequencyUpdate"
        :options="frequencyOptions"
        ul-css-classes="radio_toggle grid_row grid_separator--s"
        name="installment_period"
        store-module="baseForm"
      />
      <level
        amount-store-module="baseForm"
        installment-period-store-module="baseForm"
        para-css-classes="donation--level"
        span-css-classes="donation--level_name"
      />
    </fieldset>

    <fieldset
      class="details grid_separator"
    >
      <div
        class="grid_row grid_separator--s"
      >
        <email
          base-css-classes="col_12 tt_input"
          name="stripeEmail"
          placeholder="Email address"
          store-module="baseForm"
        />
      </div>
      <div
        class="grid_row grid_wrap--s"
      >
        <text-input
          base-css-classes="col_6 tt_input grid_separator--s"
          name="first_name"
          placeholder="First name"
          store-module="baseForm"
        />
        <text-input
          base-css-classes="col_6 tt_input grid_separator--s"
          name="last_name"
          placeholder="Last name"
          store-module="baseForm"
        />
      </div>
      <div
        class="grid_row grid_wrap--s"
      >
        <text-input
          :required="false"
          base-css-classes="col_8 tt_input grid_separator--s"
          name="reason"
          placeholder="Encouraged to give by ..."
          store-module="baseForm"
        />
        <text-input
          :required="false"
          base-css-classes="col_4 tt_input grid_separator--s"
          pattern="[0-9]{5}"
          name="zipcode"
          placeholder="Zip code"
          store-module="baseForm"
        />
      </div>
      <pay-fees
        :update-callback="onFeeChange"
        div-css-classes="pay_fee grid_row"
        input-css-classes="col_1 pay_fee--checkbox"
        span-css-classes="pay_fee--amount"
        para-css-classes="pay_fee--description col_11"
        amount-store-module="baseForm"
      />
    </fieldset>

    <fieldset>
      <basic-pay
        :token="token"
        @setToken="setToken"
      />
    </fieldset>

    <local-hidden
      :value="token"
      name="stripeToken"
    />
    <connected-hidden
      name="description"
      store-module="baseForm"
    />
    <connected-hidden
      name="campaign_id"
      store-module="baseForm"
    />
    <connected-hidden
      name="openended_status"
      store-module="baseForm"
    />
    <connected-hidden
      name="pay_fees_value"
      store-module="baseForm"
    />
  </form>
</template>

<script>
import ConnectedHidden from '../../connected/Hidden.vue';
import Radios from '../../connected/Radios.vue';
import Level from '../../connected/Level.vue';
import PayFees from '../../connected/PayFees.vue';
import TextInput from '../../connected/TextInput.vue';
import Email from '../../connected/Email.vue';

import LocalHidden from '../../local/Hidden.vue';
import BasicPay from '../../local/BasicPay.vue';

import replaceSingleValue from '../../mixins/replaceSingleValue';

export default {
  name: 'TopForm',

  components: {
    ConnectedHidden,
    LocalHidden,
    TextInput,
    Radios,
    PayFees,
    Level,
    Email,
    BasicPay,
  },

  mixins: [replaceSingleValue],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],

      token: '',
    };
  },

  methods: {
    onFrequencyUpdate(newValue) {
      let openEndedVal = '';

      if (newValue === 'yearly' ||
          newValue === 'monthly'
      ) {
        openEndedVal = 'Open';
      } else if (newValue === 'None') {
        openEndedVal = 'None';
      }

      this.replaceSingleValue({
        storeModule: 'baseForm',
        name: 'openended_status',
        newValue: openEndedVal,
      });
    },

    onFeeChange(checked) {
      this.replaceSingleValue({
        storeModule: 'baseForm',
        name: 'pay_fees_value',
        newValue: checked ? 'True' : 'False',
      });
    },

    onSubmit(event) {
      event.preventDefault();
    },

    setToken(newToken, cb) {
      this.token = newToken;
      cb();
    },
  },
};
</script>
