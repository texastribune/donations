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
            :validator="isNumeric"
            base-css-classes="col tt_input donation--amount"
            name="amount"
            store-module="baseForm"
            error-message="Please enter a numeric amount."
            @addError="addError"
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
          error-message="Please enter a valid email address."
          @addError="addError"
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
          error-message="Please enter your first name."
          @addError="addError"
        />
        <text-input
          :validator="isNotEmpty"
          base-css-classes="col_6 tt_input grid_separator--s"
          name="last_name"
          placeholder="Last name"
          store-module="baseForm"
          error-message="Please enter your last name."
          @addError="addError"
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
          error-message="Please enter a 5-digit zip code"
          @addError="addError"
        />
      </div>
      <pay-fees
        div-css-classes="pay_fee grid_row"
        input-css-classes="col_1 pay_fee--checkbox"
        span-css-classes="pay_fee--amount"
        para-css-classes="pay_fee--description col_11"
        amount-store-module="baseForm"
        @updateCallback="onFeeChange"
      />
    </fieldset>

    <fieldset
      class="grid_separator"
    >
      <div
        class="grid_separator"
      >
        <card-pay
          :token="token"
          base-css-classes="donation--card"
          @setToken="setToken"
        />
      </div>
      <div
        class="grid_row"
      >
        <card-submit
          :token="token"
          base-css-classes="col button button--yellow button--l donation--submit"
          value="Donate"
          @onSubmit="onSubmit"
        />
      </div>
    </fieldset>

    <fieldset>
      <p>{{ errorMessage }}</p>
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
import ConnectedHidden from '../../connected-elements/Hidden.vue';
import Radios from '../../connected-elements/Radios.vue';
import Level from '../../connected-elements/Level.vue';
import PayFees from '../../connected-elements/PayFees.vue';
import TextInput from '../../connected-elements/TextInput.vue';
import Email from '../../connected-elements/Email.vue';

import LocalHidden from '../../local-elements/Hidden.vue';
import CardPay from '../../local-elements/CardPay.vue';
import CardSubmit from '../../local-elements/CardSubmit.vue';

import validators from '../../mixins/form/validators';

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
    CardPay,
    CardSubmit,
  },

  mixins: [validators],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
      errors: {
        stripeEmail: '',
        first_name: '',
        last_name: '',
        amount: '',
        zipcode: '',
      },
      token: '',
    };
  },

  computed: {
    errorMessage() {
      let message = '';

      Object.keys(this.errors).forEach((key) => {
        const curr = this.errors[key];
        if (curr) message += ` ${curr}`;
      });

      return message;
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

      this.$store.dispatch(
        'baseForm/updateValue',
        {
          key: 'openended_status',
          value: openEndedVal,
        },
      );
    },

    onFeeChange(checked) {
      this.$store.dispatch(
        'baseForm/updateValue',
        {
          key: 'pay_fees_value',
          value: checked ? 'True' : 'False',
        },
      );
    },

    onSubmit() {
      if (!this.errorMessage) this.$refs.form.submit();
    },

    setToken(newToken) {
      this.token = newToken;
    },

    addError(key, message) {
      this.errors[key] = message;
    },
  },
};
</script>
