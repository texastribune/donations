import jsPDF from 'jspdf';
import axios from 'axios';

import formatCurrency from '../../utils/format-currency';

export default async function buildBlastReceipt({ date, amount, contact }) {
  // eslint-disable-next-line new-cap
  const doc = new jsPDF({
    unit: 'px',
    format: 'letter',
    lineHeight: 1.5,
  });
  const leftEdge = 40;
  const topEdge = 30;
  const response = await axios.get('/static/img/receipt-logo.png', {
    responseType: 'blob',
  });
  const ttLogo = await new Promise((resolve, reject) => {
    const reader = new window.FileReader();

    reader.readAsDataURL(response.data);
    reader.onerror = reject;
    reader.onload = () => {
      resolve(reader.result);
    };
  });

  doc.addImage(ttLogo, 'PNG', leftEdge, topEdge, 100, 50);

  doc.setFontSize(10);
  doc.text(
    [
      '919 Congress Avenue, Sixth Floor',
      'Austin, TX 78701',
      'P: 512-716-8600',
      'F: 512-716-8601',
      'www.texastribune.org',
    ],
    425,
    topEdge,
    { align: 'right' }
  );

  doc.setFontSize(12);
  doc.text('Thank you for subscribing to The Blast!', leftEdge, 130);
  doc.text(
    'This constitutes an official digital receipt from the Texas Tribune. For inquiries regarding invoices, please see our contact information below.',
    leftEdge,
    160,
    { maxWidth: '385' }
  );

  doc.setFontStyle('bold');
  doc.text('Date Received', leftEdge, 200);
  doc.setFontStyle('normal');
  doc.text(date, leftEdge, 212);

  doc.setFontStyle('bold');
  doc.text('Name', leftEdge, 242);
  doc.setFontStyle('normal');
  doc.text(contact, leftEdge, 254);

  doc.setFontStyle('bold');
  doc.text('Amount Received', leftEdge, 284);
  doc.setFontStyle('normal');
  doc.text(formatCurrency(amount), leftEdge, 296);

  doc.text('Contact us at any time:', leftEdge, 326);
  doc.text('Email: blast@texastribune.org', leftEdge, 338);
  doc.text('Tel: 512-716-8695 (account questions)', leftEdge, 350);

  doc.text(
    'Please note: Annual subscriptions to The Blast are refundable within the first 30 days after the subscription is paid. To cancel within this period, please email blast@texastribune.org. No other refunds after 30 days will be given on annual subscriptions.',
    leftEdge,
    380,
    { maxWidth: '385' }
  );

  doc.save(`blast-receipt-${date}.pdf`);
}
