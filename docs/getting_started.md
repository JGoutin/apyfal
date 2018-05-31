# Getting Started

This section explains how to use AcceleratorAPI with Python to run accelerators.

All of theses examples requires that you first install the AcceleratorAPI
and get configuration requirements like at least your Accelize credentials (`accelize_client_id` and `accelize_secret_id`
parameters in following examples).

```eval_rst
See :doc:`installation` and :doc:`configuration` for more information.
```

You also needs the name (`accelerator` parameter in following example) of the accelerator you want to use.

See [AccelStore](https://accelstore.accelize.com) for more information.

>Examples below uses configuration as arguments to be more explicit, but you can also set them with configuration file.

>For testing and examples, it is possible to enable acceleratorAPI logger to see more details on running steps:
>
>```python
>import acceleratorAPI
>acceleratorAPI.get_logger(True)
>```

## Running an accelerator on a cloud instance

This tutorial will cover creating a simple accelerator instance and process a file using a Cloud Service 
Provider (*CSP*). 

Parameters required in this case may depends on the CSP used, but it need always at least:

* `provider`: CSP name
* `region`: CSP region name, need a region that support FPGA instance.
* `client_id` and `secret_id`: CSP credentials

See your CSP documentation to know how obtains theses values.

```python
# Import the accelerator module.
import acceleratorAPI

# Choose an accelerator to use and configure it.
with acceleratorAPI.AcceleratorClass(
        # Accelerator parameters
        accelerator='my_accelerator',
        # CSP parameters
        provider='my_provider', region='my_region', 
        client_id='my_client_id', secret_id='my_secret_id',
        # Accelize parameters
        accelize_client_id='my_accelize_client_id',
        accelize_secret_id='my_accelize_secret_id') as myaccel:

    # Start the accelerator:
    # In this case a new CSP instance will be provisioned credential passed to 
    # AcceleratorClass
    # Note: This step can take some minutes depending your CSP
    myaccel.start()

    # Process data:
    # Define witch file you want to process and where they should be stored.
    myaccel.process(file_in='/path/myfile1.dat', file_out='/path/result1.dat')
    myaccel.process(file_in='/path/myfile2.dat', file_out='/path/result2.dat')
    # ... We can run any file as we need.

# The accelerator is automatically closed  on "with" exit.
# In this case, the default stop_mode ('term') is used:
# the previously created instance will be deleted and all its content lost.
```

### Keeping instance running

Starting instance take long time, so it may be a good idea to keeping it running for reusing it later.

This is done with the `stop_mode` parameter.

Depending your CSP, note that you will pay until your instance is alive.

```python
import acceleratorAPI

with acceleratorAPI.AcceleratorClass(
        accelerator='my_accelerator',
        provider='my_provider', region='my_region', 
        client_id='my_client_id', secret_id='my_secret_id',
        accelize_client_id='my_accelize_client_id',
        accelize_secret_id='my_accelize_secret_id') as myaccel:

    # We can start accelerator with "keep" stop mode to keep instance running
    myaccel.start(stop_mode='keep')

    myaccel.process(file_in='/path/myfile.dat', file_out='/path/result.dat')
    
    # We can get and store instance IP and ID for later use
    my_instance_id = myaccel.csp.instance_id
    my_instance_ip = myaccel.csp.public_ip

# This time instance is not deleted and will stay running when accelerator is close.
```

### Reusing existing instance

#### With instance ID and full instance access

With `instance_id`, depending your CSP, your can reuse an already existing instance without providing
`client_id` and `secret_id`.

An accelerator started with `instance_id` keep control on this instance an can stop it.

```python
import acceleratorAPI

# We select the instance to use on AcceleratorClass instantiation
# with its ID stored previously
with acceleratorAPI.AcceleratorClass(
        accelerator='my_accelerator',
        provider='my_provider', region='my_region',
        # Use 'instance_id' and removed 'client_id' and 'secret_id'
        instance_id='my_instance_id',
        accelize_client_id='my_accelize_client_id',
        accelize_secret_id='my_accelize_secret_id') as myaccel:

    myaccel.start()

    myaccel.process(file_in='/path/myfile.dat', file_out='/path/result.dat')
```

#### With instance IP with accelerator only access

With `instance_ip`, your can reuse an already existing instance ID without providing any CSP information.

An accelerator started with `instance_ip` have no control over this instance and can't stop it.

```python
import acceleratorAPI

# We also can select the instance to use on AcceleratorClass instantiation
# with its IP address stored previously
with acceleratorAPI.AcceleratorClass(
        accelerator='my_accelerator', 
        # Use 'instance_ip' and removed 'client_id' and 'secret_id'
        instance_ip='my_instance_ip',
        accelize_client_id='my_accelize_client_id',
        accelize_secret_id='my_accelize_secret_id') as myaccel:

    myaccel.start()

    myaccel.process(file_in='/path/myfile.dat', file_out='/path/result.dat')
```