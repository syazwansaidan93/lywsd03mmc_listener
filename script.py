import asyncio,sys,time,json
from bleak import BleakClient,BleakScanner
from bleak.exc import BleakError
CF="config.json"
try:
 with open(CF,'r') as f:c_d=json.load(f)
except FileNotFoundError:sys.exit(f"Error: {CF} not found.")
except json.JSONDecodeError:sys.exit(f"Error: Could not parse {CF}.")
MACS=c_d.get("mac_addresses",[])
if not MACS:sys.exit("Error: No MAC addresses found in config.json.")
PI=c_d.get("poll_interval_minutes",1)*60
RT=20
MDR=3
DRD=5
D_C_U="ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"
B_C_U="00002a19-0000-1000-8000-00805f9b34fb"
l_s_d={}
a_c={}
def n_h(m,s,d):
 if len(d)>=3:
  t=int.from_bytes(d[0:2],'little',signed=True)/100.0
  h=d[2]
  if m not in l_s_d:l_s_d[m]={}
  l_s_d[m].update({"temperature":t,"humidity":h})
  b_p=l_s_d[m].get("battery_percentage","N/A")
  print(f'{{"mac":"{m}","temperature":{t:.2f},"humidity":{h},"battery_percentage":{b_p}}}')
async def c_a_l(m):
 while True:
  c=None
  try:
   await asyncio.sleep(2)
   d=None
   for a in range(MDR):
    d=await BleakScanner.find_device_by_address(m,timeout=10.0)
    if d:break
    await asyncio.sleep(DRD)
   if not d:
    await asyncio.sleep(PI)
    continue
   c=BleakClient(m,timeout=RT)
   await c.connect()
   a_c[m]=c
   if not c.is_connected:
    await asyncio.sleep(PI)
    continue
   if m not in l_s_d:l_s_d[m]={}
   try:
    b_v=await c.read_gatt_char(B_C_U)
    b_p=int.from_bytes(b_v,'little',signed=False)
    l_s_d[m]["battery_percentage"]=b_p
   except Exception:
    l_s_d[m]["battery_percentage"]="Error"
   await c.start_notify(D_C_U,lambda s,d:n_h(m,s,d))
   while c.is_connected:
    await asyncio.sleep(PI)
  except asyncio.TimeoutError:pass
  except BleakError:pass
  except Exception:pass
  finally:
   if c and c.is_connected:
    try:await c.stop_notify(D_C_U)
    except Exception:pass
    await c.disconnect()
   if m in a_c:del a_c[m]
   await asyncio.sleep(5)
async def main():
 await asyncio.gather(*[c_a_l(m) for m in MACS])
if __name__=="__main__":
 try:asyncio.run(main())
 except KeyboardInterrupt:pass
 finally:
  async def cl_c():
   for m,c in list(a_c.items()):
    if c.is_connected:
     try:
      await c.stop_notify(D_C_U)
      await c.disconnect()
     except Exception:pass
   a_c.clear()
  asyncio.run(cl_c())
