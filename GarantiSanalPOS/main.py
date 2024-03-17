from PaymentProcess import GarantiPaymentProcess

# Create an instance of GarantiPaymentProcess
payment_process = GarantiPaymentProcess()

# Prepare the payment by calling the prepare_payment method
xml_payment_data = payment_process.prepare_payment()
# json_response = payment_process.pay(xml_payment_data)


print(xml_payment_data)
print("Done!")