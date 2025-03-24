Start the Proxy:
bash
Copy
Edit
python ship_proxy.py
You’ll see an output similar to:
csharp
Copy
Edit
[*] Ship Proxy listening on 0.0.0.0:8080
Send Requests via Proxy:
You can use curl or any HTTP client to send requests through the proxy.

bash
Copy
Edit
curl -v -x http://localhost:8080 -L https://www.google.com
This command connects to the proxy running on localhost:8080 and forwards requests to Google.
