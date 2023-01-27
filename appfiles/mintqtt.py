import appfiles
from cherrystrap import logger, formatter
import mintapi
from appfiles.mqtt import establish_sensor, update_values, update_attributes
import time

def mintqtt_vars():

    mintqtt_args = [appfiles.MINT_USERNAME, formatter.decode(appfiles.MINT_PASSWORD)]
    mintqtt_kwargs = {}
    if appfiles.INTUIT_ACCOUNT:
        mintqtt_kwargs['intuit_account'] = appfiles.INTUIT_ACCOUNT
    if appfiles.MFA_METHOD:
        mintqtt_kwargs['mfa_method'] = appfiles.MFA_METHOD
    else:
        pass
    if appfiles.MFA_TOKEN:
        mintqtt_kwargs['mfa_token'] = formatter.decode(appfiles.MFA_TOKEN)
    if appfiles.MFA_INPUT_CALLBACK:
        mintqtt_kwargs['mfa_input_callback'] = appfiles.MFA_INPUT_CALLBACK
    if appfiles.IMAP_ACCOUNT:
        mintqtt_kwargs['imap_account'] = appfiles.IMAP_ACCOUNT
    if appfiles.IMAP_PASSWORD:
        mintqtt_kwargs['imap_password'] = formatter.decode(appfiles.IMAP_PASSWORD)
    if appfiles.IMAP_SERVER:
        mintqtt_kwargs['imap_server'] = appfiles.IMAP_SERVER
    if appfiles.IMAP_FOLDER != "INBOX":
        mintqtt_kwargs['imap_folder'] = appfiles.IMAP_FOLDER
    if appfiles.SESSION_PATH:
        mintqtt_kwargs['session_path'] = appfiles.SESSION_PATH
    if appfiles.WAIT_FOR_SYNC_TIMEOUT:
        mintqtt_kwargs['wait_for_sync_timeout'] = appfiles.WAIT_FOR_SYNC_TIMEOUT
    if appfiles.DRIVER:
        mintqtt_kwargs['driver'] = appfiles.DRIVER
    
    # must include all booleans
    mintqtt_kwargs['headless'] = appfiles.HEADLESS
    mintqtt_kwargs['wait_for_sync'] = appfiles.WAIT_FOR_SYNC
    mintqtt_kwargs['fail_if_stale'] = appfiles.FAIL_IF_STALE
    mintqtt_kwargs['use_chromedriver_on_path'] = appfiles.USE_CHROMEDRIVER_ON_PATH
    mintqtt_kwargs['quit_driver_on_fail'] = appfiles.QUIT_DRIVER_ON_FAIL

    # also want to pass mqtt info
    mintqtt_kwargs['mqtt_client_id'] = appfiles.MQTT_CLIENT_ID
    mintqtt_kwargs['mqtt_broker_addr'] = appfiles.MQTT_BROKER_ADDR
    mintqtt_kwargs['mqtt_broker_port'] = int(appfiles.MQTT_BROKER_PORT)
    mintqtt_kwargs['mqtt_username'] = appfiles.MQTT_USERNAME
    mintqtt_kwargs['mqtt_password'] = formatter.decode(appfiles.MQTT_PASSWORD)
    mintqtt_kwargs['mqtt_prefix'] = appfiles.MQTT_PREFIX

    return mintqtt_args, mintqtt_kwargs

def run_mint(*args, **kwargs):

	logger.info("Opening connection with Mint and gathering data")

	mqtt_kwargs = {}
	mqtt_kwargs['mqtt_broker_addr'] = kwargs['mqtt_broker_addr']
	mqtt_kwargs['mqtt_broker_port'] = kwargs['mqtt_broker_port']
	mqtt_kwargs['mqtt_username'] = kwargs['mqtt_username']
	mqtt_kwargs['mqtt_password'] = kwargs['mqtt_password']
	mqtt_kwargs['mqtt_client_id'] = kwargs['mqtt_client_id']
	mqtt_kwargs['mqtt_prefix'] = kwargs['mqtt_prefix']

	del kwargs['mqtt_broker_addr']
	del kwargs['mqtt_broker_port']
	del kwargs['mqtt_username']
	del kwargs['mqtt_password']
	del kwargs['mqtt_client_id']
	del kwargs['mqtt_prefix']

	mint = mintapi.Mint(args[0], args[1], **kwargs)

	try:
		net_worth = mint.get_net_worth_data()
	except Exception as e:
		logger.error("Could not connect to Mint for Net Worth data:" % e)
	try:
		net_worth_sensor_kwargs = mqtt_kwargs
		net_worth_sensor_kwargs['attributes'] = False
		net_worth_sensor_kwargs['units'] = 'USD'
		net_worth_sensor_kwargs['icon'] = 'mdi:currency-usd'
		establish_sensor('Net Worth', **net_worth_sensor_kwargs)
		update_values('Net Worth', str(round(float(net_worth))), **mqtt_kwargs)
	except Exception as e:
		logger.error("Could not publish Net Worth to MQTT:" % e)

	try:
		credit_score = mint.get_credit_score_data()
	except Exception as e:
		logger.error("Could not connect to Mint for Credit Score data:" % e)
	try:
		credit_score_sensor_kwargs = mqtt_kwargs
		credit_score_sensor_kwargs['attributes'] = False
		credit_score_sensor_kwargs['units'] = False
		credit_score_sensor_kwargs['icon'] = 'mdi:clipboard-account-outline'
		establish_sensor('Credit Score', **credit_score_sensor_kwargs)
		update_values('Credit Score', str(int(credit_score)), **mqtt_kwargs)
	except Exception as e:
		logger.error("Could not publish Credit Score to MQTT:" % e)


	# bills_data = mint.get_bills()
	# print(bills_data)

	# account_data = mint.get_account_data()
	# print(account_data)

	# budget_data = mint.get_budget_data()
	# print(budget_data)

	# investment_data = mint.get_investment_data()
	# print(investment_data)

	# transaction_data = mint.get_transaction_data() # as pandas dataframe
	# print(transaction_data)

	# accounts = mint.get_account_data()
	# for account in accounts:
	# 	mint.get_transaction_data(id=account["id"])

	logger.info("Closing connection with Mint")
	mint.close()

	return

def schedule_mint():
	[mintqtt_args, mintqtt_kwargs] = mintqtt_vars()
	scheduled_job = run_mint(*mintqtt_args, **mintqtt_kwargs)

	return scheduled_job

def delete_sensors():
	update_values('Net Worth', '')
	update_values('Credit Score', '')

if __name__ == '__main__':
	run_mint()
	