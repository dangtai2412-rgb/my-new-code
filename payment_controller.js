const { customers } = require("./data");

exports.makePayment = (req, res) => {
  const { customerId, amount } = req.body;

  // tìm khách hàng theo ID
  const customer = customers.find((c) => c.id === customerId);
  if (!customer) {
    return res.status(404).json({ message: "Không tìm thấy khách hàng" });
  }

  // trừ số tiền thanh toán vào tổng nợ
  customer.total_outstanding_debt -= amount;
  if (customer.total_outstanding_debt < 0) {
    customer.total_outstanding_debt = 0; // không cho âm
  }

  console.log(`Thanh toán ${amount} VND cho khách hàng ${customerId}`);
  res.json({
    message: "Thanh toán thành công!",
    newDebt: customer.total_outstanding_debt,
  });
};