<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form"
    @submit="$event.preventDefault()"
  >
    <div class="grid_row grid_wrap--l">
      <div class="col_7">
        <div class="form__group">
          <div class="grid_row grid_separator--xs">
            <div class="col">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.amount"
                has-label
                label-text="amount ($)"
                base-classes="form__text form__text--heavy"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="amount"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
          <div class="grid_row grid_separator">
            <div class="col">
              <radios
                :options="frequencyOptions"
                base-classes="grid_row form__radios"
                name="installment_period"
                store-module="baseForm"
                @updateCallback="onFrequencyUpdate"
              />
            </div>
          </div>
        </div>

        <div class="form__group">
          <div class="grid_row grid_separator">
            <div class="col">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.stripeEmail"
                has-label
                label-text="email address"
                type="email"
                base-classes="form__text form__text--standard"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="stripeEmail"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
          <div class="grid_row grid_wrap--s">
            <div class="col_6 grid_separator">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.first_name"
                has-label
                label-text="first name"
                base-classes="form__text form__text--standard"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="first_name"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
            <div class="col_6 grid_separator">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.last_name"
                has-label
                label-text="last name"
                base-classes="form__text form__text--standard"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="last_name"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>

          <div class="grid_row grid_wrap--s">
            <div class="col_6 grid_separator">
              <text-input
                :required="false"
                has-label
                label-text="encouraged to give by"
                base-classes="form__text form__text--standard"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="reason"
                store-module="baseForm"
              />
            </div>
            <div class="col_6 grid_separator">
              <text-input
                :required="false"
                :show-error="showAllErrors"
                :validation="validation.zipcode"
                has-label
                label-text="zip code"
                maxlength="5"
                base-classes="form__text form__text--standard"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="zipcode"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
        </div>
      </div>

      <div class="col_5 donate-form__payment">
        <div class="donate-form__payment-box">
          <div class="grid_separator--l">
            <pay-fees
              base-classes="form__fees"
              amount-store-module="baseForm"
              pay-fees-value-store-module="baseForm"
            />
          </div>
          <div :class="showManualPay ? 'grid_separator--l' : ''">
            <native-pay
              :form-is-valid="nativeIsValid"
              :supported="nativeIsSupported"
              base-classes="form__native"
              amount-store-module="baseForm"
              token-store-module="baseForm"
              @setValue="setValue"
              @onSubmit="onSubmit"
            />
          </div>
          <div
            :aria-live="nativeIsSupported ? 'polite' : false"
          >
            <div v-if="showManualPay">
              <manual-pay
                :show-error="showManualErrors"
                :validation="validation.card"
                base-classes="form__manual"
                token-store-module="baseForm"
                error-classes="form__error"
                @markErrorValidity="markErrorValidity"
              />
              <div class="grid_row">
                <manual-submit
                  :form-is-valid="manualIsValid"
                  base-classes="col button button--yellow button--l"
                  value="Pay by card"
                  @onSubmit="onSubmit"
                  @setValue="setValue"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

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
        {
          id: 0,
          text: 'Monthly',
          value: 'monthly',
          liClasses: 'col_4',
        },
        {
          id: 1,
          text: 'Yearly',
          value: 'yearly',
          liClasses: 'col_4',
        },
        {
          id: 2,
          text: 'Once',
          value: 'None',
          liClasses: 'col_4',
        },
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
