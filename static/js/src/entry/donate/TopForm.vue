<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form_membership splash_box col_5"
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
          <text-input
            :show-error="showAllErrors"
            :validation="validation.amount"
            base-classes="col tt_input donation--amount"
            name="amount"
            store-module="baseForm"
            @markErrorValidity="markErrorValidity"
          />
        </div>
      </div>
      <radios
        :options="frequencyOptions"
        ul-classes="radio_toggle grid_row grid_separator--s"
        name="installment_period"
        store-module="baseForm"
        @updateCallback="onFrequencyUpdate"
      />
    </fieldset>

    <fieldset
      class="details grid_separator"
    >
      <div
        class="grid_row grid_separator--s"
      >
        <text-input
          :show-error="showAllErrors"
          :validation="validation.stripeEmail"
          type="email"
          base-classes="col_12 tt_input"
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
          :show-error="showAllErrors"
          :validation="validation.first_name"
          base-classes="col_6 tt_input grid_separator--s"
          name="first_name"
          placeholder="First name"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
        <text-input
          :show-error="showAllErrors"
          :validation="validation.last_name"
          base-classes="col_6 tt_input grid_separator--s"
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
          base-classes="col_7 tt_input grid_separator--s"
          name="reason"
          placeholder="Encouraged to give by ..."
          store-module="baseForm"
        />
        <text-input
          :show-error="showAllErrors"
          :validation="validation.zipcode"
          maxlength="5"
          base-classes="col_5 tt_input grid_separator--s"
          name="zipcode"
          placeholder="Zip code"
          store-module="baseForm"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <pay-fees
        div-classes="pay_fee grid_row"
        input-classes="col_1 pay_fee--checkbox"
        span-classes="pay_fee--amount"
        para-classes="pay_fee--description col_11"
        amount-store-module="baseForm"
        pay-fees-value-store-module="baseForm"
      />
    </fieldset>

    <fieldset
      class="grid_separator"
    >
      <native-pay
        :form-is-valid="nativeIsValid"
        amount-store-module="baseForm"
        token-store-module="baseForm"
        @setValue="setValue"
        @onSubmit="onSubmit"
      />
      <div
        class="grid_separator"
      >
        <manual-pay
          :show-error="showManualErrors"
          :validation="validation.card"
          token-store-module="baseForm"
          base-classes="donation--card"
          @markErrorValidity="markErrorValidity"
        />
      </div>
      <div
        class="grid_row"
      >
        <manual-submit
          :form-is-valid="manualIsValid"
          base-classes="col button button--yellow button--l donation--submit"
          value="Pay by card"
          @onSubmit="onSubmit"
          @setValue="setValue"
        />
      </div>
    </fieldset>

    <hidden
      name="installments"
      store-module="baseForm"
    />
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
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import updateStoreValue from '../../elements/mixins/updateStoreValue';
import formStarter from '../../mixins/form/starter';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    TextInput,
    Radios,
    PayFees,
    Level,
    ManualPay,
    ManualSubmit,
    NativePay,
  },

  mixins: [
    formStarter,
    updateStoreValue,
  ],

  data() {
    return {
      frequencyOptions: [
        { id: 0, text: 'monthly', value: 'monthly' },
        { id: 1, text: 'yearly', value: 'yearly' },
        { id: 2, text: 'one time', value: 'None' },
      ],
      validation: {
        stripeEmail: {
          manual: true,
          native: true,
          valid: false,
          message: 'Invalid email address',
          validator: this.isEmail,
        },
        first_name: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter your first name',
          validator: this.isNotEmpty,
        },
        last_name: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter your last name',
          validator: this.isNotEmpty,
        },
        amount: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter numeric amount above $1',
          validator: this.isValidDonationAmount,
        },
        zipcode: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a 5-digit zip code',
          validator: this.isEmptyOrZip,
        },
      },
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

      this.updateStoreValue({
        storeModule: 'baseForm',
        key: 'openended_status',
        value: openEndedVal,
      });
    },
  },
};
</script>
