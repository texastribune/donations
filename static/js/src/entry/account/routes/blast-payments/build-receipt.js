import jsPDF from 'jspdf';
import axios from 'axios';

export default async function buildReceipt({ date, amount, method }) {
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

  doc.save(`blast-receipt-${date}.pdf`);
}
