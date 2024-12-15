import Tx_TCP as T
import Rx_TCP as R


addr = 'Hello world'

data = 10
while(True):
    R.Rx()
    T.Tx(addr, data)
