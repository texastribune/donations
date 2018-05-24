<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form splash_box"
    @submit="$event.preventDefault()"
  >
    <div class="grid_row grid_separator">
      <p class="col form__prompt">
        I'm ready to give
      </p>
    </div>

    <div class="grid_row grid_wrap--l">
      <div class="col_7">
        <fieldset class="form__fieldset grid_separator">
          <div class="grid_row">
            <div class="col grid_separator--xs">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.amount"
                has-label
                label-text="amount ($)"
                input-classes="form__text form__amount"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="amount"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
          <div class="grid_row">
            <div class="col">
              <radios
                :options="frequencyOptions"
                list-classes="grid_row form__frequency"
                name="installment_period"
                store-module="baseForm"
                @updateCallback="onFrequencyUpdate"
              />
            </div>
          </div>
        </fieldset>

        <fieldset class="form__fieldset">
          <div class="grid_row grid_separator">
            <div class="col">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.stripeEmail"
                has-label
                label-text="email address"
                type="email"
                input-classes="form__text"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="stripeEmail"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
          <div class="grid_row grid_wrap--s grid_separator">
            <div class="col_6">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.first_name"
                has-label
                label-text="first name"
                input-classes="form__text"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="first_name"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
            <div class="col_6">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.last_name"
                has-label
                label-text="last name"
                input-classes="form__text"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="last_name"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>

          <div class="grid_row grid_wrap--s">
            <div class="col_6">
              <text-input
                has-label
                label-text="encouraged to give by"
                input-classes="form__text"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="reason"
                store-module="baseForm"
              />
            </div>
            <div class="col_6">
              <text-input
                :show-error="showAllErrors"
                :validation="validation.zipcode"
                has-label
                label-text="zip code"
                maxlength="5"
                input-classes="form__text"
                error-classes="form__error"
                label-classes="form__label grid_separator--xs"
                name="zipcode"
                store-module="baseForm"
                @markErrorValidity="markErrorValidity"
              />
            </div>
          </div>
        </fieldset>
      </div>

      <div class="col_5 form__payment">
        <fieldset class="form__payment-box">
          <div class="grid_separator">
            <pay-fees
              container-classes="form__fees grid_row"
              checkbox-classes="col_1"
              fee-classes="pay_fee--amount"
              text-classes="form__fees-graf col_11"
              amount-store-module="baseForm"
              pay-fees-value-store-module="baseForm"
            />
          </div>
          <div class="grid_separator--l">
            <native-pay
              :form-is-valid="nativeIsValid"
              amount-store-module="baseForm"
              token-store-module="baseForm"
              @setValue="setValue"
              @onSubmit="onSubmit"
            />
          </div>
          <div class="grid_separator--s">
            <manual-pay
              :show-error="showManualErrors"
              :validation="validation.card"
              token-store-module="baseForm"
              card-classes="form__card"
              error-classes="form__error"
              @markErrorValidity="markErrorValidity"
            />
          </div>
          <div class="grid_row">
            <manual-submit
              :form-is-valid="manualIsValid"
              base-classes="col button button--yellow button--l"
              value="Pay by card"
              @onSubmit="onSubmit"
              @setValue="setValue"
            />
          </div>
        </fieldset>
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
          liClasses: 'col_4 form__frequency-item',
          inputClasses: 'form__frequency-radio',
        },
        {
          id: 1,
          text: 'Yearly',
          value: 'yearly',
          liClasses: 'col_4 form__frequency-item',
          inputClasses: 'form__frequency-radio',
        },
        {
          id: 2,
          text: 'One time',
          value: 'None',
          liClasses: 'col_4 form__frequency-item',
          inputClasses: 'form__frequency-radio',
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
