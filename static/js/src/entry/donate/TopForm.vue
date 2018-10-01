<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form"
    @submit="$event.preventDefault()"
  >
    <div class="grid_row">
      <div class="col">
        <radios
          :options="frequencyOptions"
          base-classes="form__radios form__radios--stack-at-medium"
          name="installment_period"
          store-module="baseForm"
          @updateCallback="onFrequencyUpdate"
        />
      </div>
    </div>

    <div class="grid_row grid_separator--xs">
      <div class="col">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          :validation="validation.amount"
          label-text="amount ($)"
          base-classes="form__text form__text--heavy"
          name="amount"
          store-module="baseForm"
          @setValidationValue="setValidationValue"
        />
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <p class="subtext">For three-year commitments of $1,000 or more, join our <a href="/circleform">Circle Membership program</a>.</p>
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          :validation="validation.stripeEmail"
          label-text="email address"
          type="email"
          base-classes="form__text form__text--standard"
          name="stripeEmail"
          store-module="baseForm"
          @setValidationValue="setValidationValue"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          :validation="validation.first_name"
          label-text="first name"
          base-classes="form__text form__text--standard"
          name="first_name"
          store-module="baseForm"
          @setValidationValue="setValidationValue"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          :validation="validation.last_name"
          label-text="last name"
          base-classes="form__text form__text--standard"
          name="last_name"
          store-module="baseForm"
          @setValidationValue="setValidationValue"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :required="false"
          label-text="encouraged to give by"
          base-classes="form__text form__text--standard"
          name="reason"
          store-module="baseForm"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :required="false"
          :show-error="showManualErrors || showNativeErrors"
          :validation="validation.zipcode"
          label-text="zip code"
          base-classes="form__text form__text--standard"
          name="zipcode"
          store-module="baseForm"
          @setValidationValue="setValidationValue"
        />
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <pay-fees
          base-classes="form__fees"
          amount-store-module="baseForm"
          pay-fees-value-store-module="baseForm"
          installment-period-store-module="baseForm"
        />
      </div>
    </div>

    <div class="grid_row">
      <div class="col">
        <native-pay
          :form-is-valid="nativeIsValid"
          :supported="nativeIsSupported"
          base-classes="form__native"
          amount-store-module="baseForm"
          email-store-module="baseForm"
          customer-id-store-module="baseForm"
          @setValue="setValue"
          @onSubmit="onSubmit"
        />
      </div>
    </div>

    <div
      v-if="nativeIsSupported && showManualPay"
      class="grid_separator--l"
      aria-hidden="true"
    />

    <div :aria-live="nativeIsSupported ? 'polite' : false">
      <div v-if="showManualPay">
        <div class="grid_row">
          <div class="col">
            <manual-pay
              :show-error="showManualErrors"
              :validation="validation.card"
              base-classes="form__manual"
              @setValidationValue="setValidationValue"
            />
          </div>
        </div>

        <div class="grid_row">
          <div class="col">
            <manual-submit
              :form-is-valid="manualIsValid"
              :is-fetching-token="isFetchingToken"
              base-classes="form__submit button button--yellow button--l"
              email-store-module="baseForm"
              customer-id-store-module="baseForm"
              value="Donate"
              @onSubmit="onSubmit"
              @setValue="setValue"
              @setValidationValue="setValidationValue"
            />
          </div>
        </div>
      </div>
    </div>

    <div
      v-if="showErrorClue"
      class="grid_separator--l"
      aria-hidden="true"
    />

    <div
      v-if="showErrorClue"
      class="grid_row"
      aria-hidden="true"
    >
      <div class="col">
        <p class="form__error form__error--centered">Please correct errors above</p>
      </div>
    </div>

    <hidden
      name="installments"
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
      name="stripeToken"
      store-module="baseForm"
    />
    <hidden
      name="referral_id"
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
        { id: 0, text: 'One-time donation', value: 'None' },
        { id: 1, text: 'Monthly donation', value: 'monthly' },
        { id: 2, text: 'Yearly donation', value: 'yearly' },
      ],
      validation: {
        stripeEmail: {
          manual: true,
          native: true,
          valid: false,
          message: 'Enter a valid email address',
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
