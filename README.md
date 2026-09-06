Solis Cloud Control (Personal mod)

Local project folder: /home/pino/Projects

Changes with original mkuthan version: https://github.com/mkuthan/solis-cloud-control

Changes to  entity power_limit:

-input box to slider (line 555 of number.py --> self._attr_mode = NumberMode.BOX )
-step 1 to 5 (File Inverters/inverter.py line 328 -->  step: float = 5)

hacs.json edited to include all files in root (content_in_root": true,)





