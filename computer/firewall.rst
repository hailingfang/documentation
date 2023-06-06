firewalld forward
==================


within host and between host

within host
--------------

Forward package from 5423 to 80

.. code-block:: bash

    firewall-cmd --permanent --add-forward-port=port=5423:proto=tcp:toport=80




between host
-----------------

Need add masquerade firstly.
Forward data from 8080 to 8080 of host 192.168.37.2

.. code-block:: bash

    firewall-cmd --zone=trusted --add-masquerade --permanent
    firewall-cmd --permanent --add-forward-port=port=8080:proto=tcp:toport=8080:toaddr=192.168.37.2
   


