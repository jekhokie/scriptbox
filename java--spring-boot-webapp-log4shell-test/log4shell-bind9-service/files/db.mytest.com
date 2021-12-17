$TTL    604800
@    IN    SOA    ns1.mytest.com. admin.mytest.com. (
                  3       ; Serial
             604800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
             604800 )   ; Negative Cache TTL
;
; name servers - NS records
     IN      NS      ns1.mytest.com.

; name servers - A records
ns1.mytest.com.          IN      A       10.128.10.11

; others - A records
test1.mytest.com.        IN      A      10.128.8.8
test2.mytest.com.        IN      A      10.128.8.9
