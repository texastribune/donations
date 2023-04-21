export default function formatTransaction({
  amount,
  date,
  period,
  payment_type: paymentType,
  credit_card: card,
  stripe_customer_id: stripeCustomerId,
}) {
  const transaction = {
    amount,
    date,
    period,
    stripeCustomerId,
  };

  if (paymentType && paymentType.toLowerCase() === 'credit card') {
    transaction.card = { brand: card.brand, last4: card.last4 };
  }

  return transaction;
}
