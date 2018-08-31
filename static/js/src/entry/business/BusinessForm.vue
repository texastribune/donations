<template>
  <form
    ref="form"
    action="/charge"
    method="post"
    class="form business-form"
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
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :required="false"
            label-text="business name"
            base-classes="form__text form__text--standard"
            name="reason"
            store-module="businessForm"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :required="false"
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.zipcode"
            label-text="website"
            maxlength="5"
            base-classes="form__text form__text--standard"
            name="zipcode"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_wrap--s">
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.first_name"
            label-text="contact first name"
            base-classes="form__text form__text--standard"
            name="first_name"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
        <div class="col_6 grid_separator">
          <text-input
            :show-error="showManualErrors || showNativeErrors"
            :validation="validation.last_name"
            label-text="contact last name"
            base-classes="form__text form__text--standard"
            name="last_name"
            store-module="businessForm"
            @setValidationValue="setValidationValue"
          />
        </div>
      </div>

      <div class="grid_row grid_separator">
        <div class="col">
          <pay-fees
            base-classes="form__fees"
            amount-store-module="businessForm"
            pay-fees-value-store-module="businessForm"
            installment-period-store-module="businessForm"
          />
        </div>
      </div>

      <div class="grid_row">
        <div class="col">
          <native-pay
            :form-is-valid="nativeIsValid"
            :supported="nativeIsSupported"
            base-classes="form__native"
            amount-store-module="businessForm"
            email-store-module="businessForm"
            customer-id-store-module="businessForm"
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
                email-store-module="businessForm"
                customer-id-store-module="businessForm"
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
        store-module="businessForm"
      />
      <hidden
        name="installment_period"
        store-module="businessForm"
      />
      <hidden
        name="installments"
        store-module="businessForm"
      />
      <hidden
        name="customerId"
        store-module="businessForm"
      />
      <hidden
        name="description"
        store-module="businessForm"
      />
      <hidden
        name="campaign_id"
        store-module="businessForm"
      />
      <hidden
        name="openended_status"
        store-module="businessForm"
      />
      <hidden
        name="pay_fees_value"
        store-module="businessForm"
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
  name: 'BusinessForm',

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
