<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form_membership"
    @submit="$event.preventDefault()"
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
            :validator="isValidDonationAmount"
            base-css-classes="col tt_input donation--amount"
            name="amount"
            store-module="baseForm"
            @markErrorValidity="markErrorValidity"
          />
        </div>
      </div>
      <radios
        :options="frequencyOptions"
        ul-css-classes="radio_toggle grid_row grid_separator--s"
        name="installment_period"
        store-module="baseForm"
        @updateCallback="onFrequencyUpdate"
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
          :validator="isEmail"
          base-css-classes="col_12 tt_input"
          name="stripeEmail"
          placeholder="Email address"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <div
        class="grid_row grid_wrap--s"
      >
        <text-input
          :validator="isNotEmpty"
          base-css-classes="col_6 tt_input grid_separator--s"
          name="first_name"
          placeholder="First name"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
        <text-input
          :validator="isNotEmpty"
          base-css-classes="col_6 tt_input grid_separator--s"
          name="last_name"
          placeholder="Last name"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <div
        class="grid_row grid_wrap--s"
      >
        <text-input
          base-css-classes="col_7 tt_input grid_separator--s"
          name="reason"
          placeholder="Encouraged to give by ..."
          store-module="baseForm"
        />
        <text-input
          :validator="isEmptyOrZip"
          base-css-classes="col_5 tt_input grid_separator--s"
          name="zipcode"
          placeholder="5-digit zip code"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <pay-fees
        div-css-classes="pay_fee grid_row"
        input-css-classes="col_1 pay_fee--checkbox"
        span-css-classes="pay_fee--amount"
        para-css-classes="pay_fee--description col_11"
        amount-store-module="baseForm"
        pay-fees-value-store-module="baseForm"
      />
    </fieldset>

    <fieldset
      class="grid_separator"
    >
      <div
        class="grid_separator"
      >
        <native-pay
          amount-store-module="baseForm"
          token-store-module="baseForm"
          @toggleError="toggleError"
          @setValue="setValue"
          @onSubmit="onSubmit"
        />
      </div>
      <div
        class="grid_separator"
      >
        <card-pay
          token-store-module="baseForm"
          base-css-classes="donation--card"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <div
        class="grid_row"
      >
        <card-submit
          :valid="valid"
          base-css-classes="col button button--yellow button--l donation--submit"
          value="Donate"
          @onSubmit="onSubmit"
          @setValue="setValue"
          @toggleError="toggleError"
        />
      </div>
    </fieldset>

    <fieldset
      v-if="showErrors"
      class="form-error"
    >
      <p
        class="error-form-message"
      >
        {{ errorMessage }}
      </p>
    </fieldset>

    <hidden
      name="stripeToken"
      store-module="baseForm"
    />
    <hidden
      name="description"
      store-module="baseForm"
    />
    <hidden
      name="campaign_id"
      store-module="baseForm"
    />
    <hidden
      name="openended_status"
      store-module="baseForm"
    />
    <hidden
      name="pay_fees_value"
      store-module="baseForm"
    />
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import Radios from '../../elements/Radios.vue';
import Level from '../../elements/Level.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import Email from '../../elements/Email.vue';
import CardPay from '../../elements/CardPay.vue';
import CardSubmit from '../../elements/CardSubmit.vue';
import NativePay from '../../elements/NativePay.vue';

import updateStoreValue from '../../elements/mixins/updateStoreValue';

import validators from '../../mixins/form/validators';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    TextInput,
    Radios,
    PayFees,
    Level,
    Email,
    CardPay,
    CardSubmit,
    NativePay,
  },

  mixins: [
    validators,
    updateStoreValue,
  ],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
      errors: {
        stripeEmail: {
          message: 'Please enter valid email address.',
          valid: false,
          include: true,
        },
        first_name: {
          message: 'Please enter your first name.',
          valid: false,
          include: true,
        },
        last_name: {
          message: 'Please enter your last name.',
          valid: false,
          include: true,
        },
        amount: {
          message: 'Please enter an amount above $1.',
          valid: false,
          include: true,
        },
        zipcode: {
          message: 'Please enter a 5-digit zip code.',
          valid: false,
          include: true,
        },
        stripeToken: {
          message: 'Please enter your card information.',
          valid: false,
          include: true,
        },
      },
      showErrors: false,
    };
  },

  computed: {
    errorMessage() {
      let message = '';

      Object.keys(this.errors).forEach((key) => {
        const curr = this.errors[key];
        if (!curr.valid) {
          message += ` ${curr.message}`;
        }
      });

      return message;
    },

    valid() {
      let valid = true;

      Object.keys(this.errors).forEach((key) => {
        const curr = this.errors[key];
        if (curr.include && !curr.valid) valid = false;
      });

      return valid;
    },
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

      this.updateStoreValue({
        storeModule: 'baseForm',
        key: 'openended_status',
        value: openEndedVal,
      });
    },

    onSubmit() {
      this.$refs.form.submit();
    },

    setValue(key, value) {
      this[key] = value;
    },

    markErrorValidity(key, bool) {
      this.errors[key].valid = bool;
    },

    toggleError(key, bool) {
      this.errors[key].include = bool;
    },
  },
};
</script>
