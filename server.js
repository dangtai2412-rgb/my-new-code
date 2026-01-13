const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const customerController = require("./customer_controller");
const debtController = require("./debt_controller");
const paymentController = require("./payment_controller");

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.get("/api/customer", customerController.getCustomers);
app.get("/api/debt/:id", debtController.getDebtsByCustomer);
app.post("/api/payment", paymentController.makePayment);

app.listen(3001, () => {
  console.log("Backend chạy tại http://localhost:3001");
});