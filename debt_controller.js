const { debts } = require("./data");

exports.getDebtsByCustomer = (req, res) => {
  const customerId = parseInt(req.params.id);
  const result = debts.filter((d) => d.customerId === customerId);
  res.json(result);
};