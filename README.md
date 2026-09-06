Solis Cloud Control (Personal mod)

Local project folder: /home/pino/Projects

Changes with original mkuthan version: https://github.com/mkuthan/solis-cloud-control

Changes to  entity power_limit:

-input box to slider (number.py --> self._attr_mode = NumberMode.BOX --> .SLIDER)
-step 1 to 5 (File Inverters/inverter.py --> step: float = 5)

hacs.json edited to include all files in root (content_in_root": true,)

Removed all battery functionality from integration.

Tested only on my Solis S6-GR1P3.6K-M

USE AT YOUR OWN RISK.

Credit go to @mkuthan

test123

