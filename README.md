# 🚢 Ship Proxy with React Frontend


This project consists of:
- A **Ship Proxy** that processes requests and sends responses.
- A **off shore** that interacts with the proxy.

---

## ⚙️ How It Works

###  Start the Proxy
To start the proxy, run the following command:
```bash
### Start the offshoreproxy
python offshore_proxy.py

### Start the shiproxy
python ship_proxy.py

###You can use curl to send requests through the proxy.
```sh
curl -v -x http://localhost:8080 -L https://www.google.com


