const { customers } = require("./data");

exports.getCustomers = (req, res) => {
  res.json(customers);
};