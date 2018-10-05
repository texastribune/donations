<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form circle-form"
    @submit="$event.preventDefault()"
  >
    <div class="grid_container--l grid_separator">
      <div class="grid_row">
        <div class="col">
          <choices />
        </div>
      </div>
    </div>

    <div class="grid_container--m">
      <div class="grid_row grid_separator">
        <div class="col">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.stripeEmail"
            label-text="email address"
            type="email"
            base-classes="form__text form__text--standard"
            name="stripeEmail"
            store-module="circleForm"
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
            store-module="circleForm"
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
            store-module="circleForm"
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
            store-module="circleForm"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :required="false"
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.zipcode"
            label-text="zip code"
            maxlength="5"
            base-classes="form__text form__text--standard"
            name="zipcode"
            store-module="circleForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <pay-fees
            base-classes="form__fees"
            amount-store-module="circleForm"
            pay-fees-value-store-module="circleForm"
            installment-period-store-module="circleForm"
          />
        </div>
      </div>

      <div class="grid_row">
        <div class="col">
          <native-pay
            :form-is-valid="nativeIsValid"
            :supported="nativeIsSupported"
            base-classes="form__native"
            amount-store-module="circleForm"
            email-store-module="circleForm"
            customer-id-store-module="circleForm"
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
                email-store-module="circleForm"
                customer-id-store-module="circleForm"
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
        name="amount"
        store-module="circleForm"
      />
      <hidden
        name="installment_period"
        store-module="circleForm"
      />
      <hidden
        name="installments"
        store-module="circleForm"
      />
      <hidden
        name="customerId"
        store-module="circleForm"
      />
      <hidden
        name="description"
        store-module="circleForm"
      />
      <hidden
        name="campaign_id"
        store-module="circleForm"
      />
      <hidden
        name="referral_id"
        store-module="circleForm"
      />
      <hidden
        name="openended_status"
        store-module="circleForm"
      />
      <hidden
        name="pay_fees_value"
        store-module="circleForm"
      />
    </div>
  </form>
</template>

<script>
import Hidden from '../../elements/Hidden.vue';
import Level from '../../elements/Level.vue';
import PayFees from '../../elements/PayFees.vue';
import TextInput from '../../elements/TextInput.vue';
import ManualPay from '../../elements/ManualPay.vue';
import ManualSubmit from '../../elements/ManualSubmit.vue';
import NativePay from '../../elements/NativePay.vue';
import Choices from './Choices.vue';
import updateStoreValue from '../../elements/mixins/updateStoreValue';
import formStarter from '../../mixins/form/starter';

export default {
  name: 'CircleForm',

  components: {
    Hidden,
    TextInput,
    PayFees,
    Level,
    ManualPay,
    ManualSubmit,
    NativePay,
    Choices,
  },

  mixins: [
    formStarter,
    updateStoreValue,
  ],

  data() {
    return {
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
};
</script>
