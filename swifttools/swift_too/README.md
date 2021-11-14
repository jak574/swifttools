# The `swift_too` Python module

## Swift TOO API Client Python implementation

### API Version 1.2

This implements a client for the Swift TOO API in Python. This allows, amongst other things, for the construction and submission of Target of Opportunity (TOO) requests to NASA's Neil Gehrels *Swift* Observatory. TOO requests are created utilizing the `Swift_TOO` class. In addition to TOO requests, the `swift_too` module allows also allows the user to query past *Swift* observations using the `Swift_ObsQuery` class, and calculation of visibility of an fixed celestial object with `Swift_VisQuery`. 

The `Swift_TOO` class mainly acts as a way to input parameters required for TOO requests, such as coordinates, exposure time requests and instrument nodes. These input are used to create a JSON structure which is used to submit the TOO request to the TOO API server. The JSON format is agnostic of how it was created, so this Python implementation should be considered a reference implementation. Compliant TOOs could be constructed using any method, even by hand, as long as the format and required parameters are in the JSON and the JSON is in the required format.

Submission is performed utilizing a signed format known as JSON Web Token ([JWT](http://jwt.io)). Signing is done with a "shared secret", i.e. both TOO submitter and the Swift MOC have a copy of the text secret, and use it primarily to confirm that the TOO was from in fact from the user specified.

Submitted TOOs are generated by importing the `Swift_TOO` class and then assigning required attibutes for the TOO submission. What follows is a brief example of how to submit a *Swift* TOO request, using the `Swift_TOO` class.

```python
from swifttools.swift_too import Swift_TOO

# Initiate the Swift_TOO class
too = Swift_TOO()

# The relevant details of the object to observe
too.source_name = "SMC X-3" # Typical name of source, if it resolves in Simbad, all the better
too.ra = 13.023439          # Right ascension in decimal degrees
too.dec = -72.434508        # Declination in decimal degrees
too.source_type = "Be/XRB"  # Short description of source class

# Estimate of how bright it is
too.xrt_countrate = 0.1         # XRT counts/s
too.obs_type = too.obs_types[1] # This is "Light Curve" - the options are:["Spectroscopy","Light Curve","Position","Timing"]

# Science Justification - one to three paragraphs to explain why this TOO request should be accepted
too.science_just = ("SMC X-3 has gone into outburst again! We wish to track the flux, "
                    "spectral and temporal (pulsar timing) evolution of this outburst. "
                    "This is only the third outburst of SMC X-3 detected since 1980. ")

# Exposure description
too.exp_time_per_visit = 3000  # Must be in seconds
too.monitoring_freq = "2 days" # Options for units are seconds, minutes, hours, days, weeks, orbit
too.num_of_visits = 14         # So this would monitor the source for 28 days.

# Exposure time justification - Explain why 3ks is needed per observation.
too.exp_time_just = ("3ks per observation will allow us to not only monitor " 
                     "this exciting new outburst of this well known Be/XRB. "
                     "We request 14 observations in order to cover the first "
                     "month of the outburst.")


# Username and secret key
too.username = "example_too_user"
too.shared_secret = 'this_is_my_shared_secret_key_that_I_and_Swift_MOC_have'

# Urgency
too.urgency = 2  # Observations needed within 24 hours
```

The TOO is now set to submit. You can do a quick internal validation of the TOO, which checks that you have not missed any of the required steps:

```python
if too.validate():
    print("TOO is good to go!")
else:
    print("Uh-oh!")
```

If everything looks good, go ahead and submit the TOO to Swift. Note: submit() will also run validate() before attempting to submit to the TOO server. 

```python
if too.submit():
    print("TOO submitted succesfully")
else:
    print("Sorry there was a problem with the submission")
```

To see the validity of the request, the TOO API returns a JSON based on the Swift_TOO_Status class, which is read in upon submission and can be accessed with the following code, which displays its contents as a JSON:

```python
print(too.status.json)
```

which displays the following:

```json
{"api_name": "Swift_TOO_Status", "api_version": "1.2", "api_data": {"status": "Accepted", "too_id": 13332, "errors": [], "warnings": []}}
```

Notice for a sucessful TOO submission, `status` is set to `Accepted` and `too_id` is set to a number, which uniquely identifies your TOO request. Any errors or warnings are given in `errors` and `warnings`. For a rejected TOO, `status` is `Rejected` and `errors` will enumerate the reason why the request failed.