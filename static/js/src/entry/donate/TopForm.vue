<template>
  <form
    ref="form"
    action="/donate"
    method="post"
    class="form"
    @submit="$event.preventDefault()"
  >
    <div v-show="showServerErrorMessage" class="grid_row grid_separator">
      <div class="col">
        <p class="form__error form__error--prominent">
          {{ serverErrorMessage }}
        </p>
      </div>
    </div>

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
          label-text="amount ($)"
          base-classes="form__text form__text--heavy"
          name="amount"
          store-module="baseForm"
        />
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <p class="subtext">
          For three-year commitments of $1,000 or more, join our
          <a href="/circle">Circle Membership program</a>.
        </p>
      </div>
    </div>

    <div class="grid_row grid_separator">
      <div class="col">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          label-text="email address"
          type="email"
          base-classes="form__text form__text--standard"
          name="stripeEmail"
          store-module="baseForm"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          label-text="first name"
          base-classes="form__text form__text--standard"
          name="first_name"
          store-module="baseForm"
        />
      </div>
      <div class="col_6 grid_separator">
        <text-input
          :show-error="showManualErrors || showNativeErrors"
          label-text="last name"
          base-classes="form__text form__text--standard"
          name="last_name"
          store-module="baseForm"
        />
      </div>
    </div>

    <div class="grid_row grid_wrap--s">
      <div class="col_6 grid_separator">
        <text-input
          :required="false"
          :show-error="showManualErrors || showNativeErrors"
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
          label-text="zip code"
          base-classes="form__text form__text--standard"
          name="zipcode"
          store-module="baseForm"
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
              value="Donate"
              @onSubmit="onSubmit"
              @setValue="setValue"
              @setValidationValue="setValidationValue"
            />
          </div>
        </div>
      </div>
    </div>

    <div v-if="showErrorClue" class="grid_separator--l" aria-hidden="true" />

    <div v-if="showErrorClue" class="grid_row" aria-hidden="true">
      <div class="col">
        <p class="form__error form__error--normal form__error--centered">
          Please correct errors above
        </p>
      </div>
    </div>

    <local-hidden :value="stripeToken" name="stripeToken" />
    <hidden name="installments" store-module="baseForm" />
    <hidden name="description" store-module="baseForm" />
    <hidden name="campaign_id" store-module="baseForm" />
    <hidden name="referral_id" store-module="baseForm" />
    <hidden name="openended_status" store-module="baseForm" />
    <hidden name="pay_fees_value" store-module="baseForm" />
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import LocalHidden from '../../elements/LocalHidden.vue';
import Radios from '../../elements/Radios.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import updateValue from '../../elements/mixins/updateValue';
import formStarter from '../../mixins/form/starter';

export default {
  name: 'TopForm',

  components: {
    Hidden,
    LocalHidden,
    TextInput,
    Radios,
    PayFees,
    ManualPay,
    ManualSubmit,
    NativePay,
  },

  mixins: [formStarter, updateValue],

  data() {
    return {
      // eslint-disable-next-line no-underscore-dangle
      serverErrorMessage: window.__TOP_FORM_SERVER_ERROR_MESSAGE__,
      frequencyOptions: [
        { id: 0, text: 'One-time donation', value: 'None' },
        { id: 1, text: 'Monthly donation', value: 'monthly' },
        { id: 2, text: 'Yearly donation', value: 'yearly' },
      ],
    };
  },

  methods: {
    onFrequencyUpdate(newValue) {
      let openEndedVal = '';

      if (newValue === 'yearly' || newValue === 'monthly') {
        openEndedVal = 'Open';
      } else if (newValue === 'None') {
        openEndedVal = 'None';
      }

      this.updateValue({
        storeModule: 'baseForm',
        key: 'openended_status',
        value: openEndedVal,
      });
    },
  },
};
</script>
