const customers = [
  {
    id: 1,
    name: "Nguyễn Văn A",
    email: "a@example.com",
    total_outstanding_debt: 500000,
  },
  {
    id: 2,
    name: "Trần Thị B",
    email: "b@example.com",
    total_outstanding_debt: 200000,
  },
];

const debts = [
  { id: 1, customerId: 1, description: "Nợ điện", amount: 300000 },
  { id: 2, customerId: 1, description: "Nợ nước", amount: 200000 },
  { id: 3, customerId: 2, description: "Nợ internet", amount: 200000 },
];

module.exports = { customers, debts };